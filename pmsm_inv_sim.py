# -*- coding: utf-8 -*-
"""PMSM + 三相电压源逆变器（PWM / 死区 / 器件压降 / 母线纹波）时域模型

与 pmsm_dq_sim.py 的区别（“更逼真的 dq 电流”来源）：
  1. 三相 PWM 逆变器：10 kHz 载波、占空比比较、死区平均电压误差、IGBT/二极管压降与导通电阻；
  2. 电机侧电感 Ld=Lq=0.57 mH 与反电动势 e=ω_e ψ_f 显式进入 ODE（不是一阶电流环等效）；
  3. 相电流由 dq 反变换得到，逆变器输出电压再 Park 回 dq —— 电流里能看到开关纹波与死区畸变；
  4. dq 电流采样噪声：均匀分布 ±0.3 A（峰值），10 kHz 采样；
  5. 编码器 2500 PPR（4 倍频 10000 计数/转），角度量化，速度由 1 ms 计数差得到。

控制器沿用 pmsm_dq_sim 的速度环（灰箱 ESO + 低通重复通道 + 律 B/D/F），
电流环为 dq PI + 解耦前馈 + SVPWM（最小-最大注入）。

用法：
    from pmsm_inv_sim import sim_inv
    Y = sim_inv(t, TL, dict(i_noise_peak=0.3))
"""
import math
import numpy as np

from eso_gain import make_gains
from fault_torque import unbalance_torque, misalign_torque

R_S = 0.175
L_S = 0.57e-3
PSI_F = 0.101 / (1.5 * 4.0)      # 0.016833 Wb
P_POL = 4
J_M = 1.89e-5          # 电机转子惯量（=ESO 标称 J_nom 的来源）
V_DC = 60.0
N_REF = 600.0
W_REF = N_REF * math.pi / 30.0
I_BASE = 0.637 / 0.101
ENC_CPR = 10000.0                # 2500 PPR × 4
TWO_PI = 2.0 * math.pi


def band_noise(n, sigma, fc, dt, seed):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    a = 1.0 - math.exp(-2 * math.pi * fc * dt)
    nk = max(1, int(math.ceil(6.0 / (2 * math.pi * fc * dt))))
    y = np.convolve(x, a * np.power(1.0 - a, np.arange(nk)))[:n]
    return y / y.std() * sigma


def sim_inv(t, TL, cfg=None):
    """t: 时间数组（s）；TL: 确定性负载转矩（N·m，不含噪声）；cfg: 参数"""
    cfg = cfg or {}
    dt = float(t[1] - t[0])
    n = len(t)
    T = cfg.get("T", 0.1)
    n_ref = float(cfg.get("n_ref", N_REF))
    w_ref = n_ref * math.pi / 30.0
    Tpwm = cfg.get("Tpwm", 1e-4)
    Td = cfg.get("Td", 2e-6)
    Vdc = cfg.get("Vdc", V_DC)
    Vdrop = cfg.get("Vdrop", 0.9)
    Ron = cfg.get("Ron", 0.01)
    Vlim = 0.95 * Vdc / math.sqrt(3.0)

    # ---- 速度环（与 pmsm_dq_sim 同口径）----
    KP = cfg.get("kp", 75.36); WO = cfg.get("wo", 500.0)
    # ---- ESO 校正通道增益（2026-10-22）----
    # 默认 fal（2026-10-22 定）：类 fal 增益（见 eso_gain.py / eso_fal.md）；
    # cfg["eso_law"]="linear" 逐位回到 v4.0 的线性 ESO（_inv_*.json 可复现）：
    #   z1: beta1*G(e; a1, delta, lam)，z2: beta2*G(e; a, delta, lam)
    ESO_G1, ESO_G2 = make_gains(cfg)
    B_GAIN = 0.101 * I_BASE / (J_M * w_ref); B0 = 1.2 * B_GAIN
    # 真实机械惯量（仿真主循环用；默认等于 J_M，向后兼容）
    # 物理折算：J_true = J_motor + J_coupling + J_disc/gear^2 + n_bearings*J_bearing
    J_TRUE = float(cfg.get("J_true", J_M))
    # ---- J 辨识/自适应（2026-11-13）----
    _jid = bool(cfg.get("j_id", False))
    _jid_f = float(cfg.get("j_id_f", 100.0))
    _jid_w = 2.0 * math.pi * _jid_f
    _jid_amp = float(cfg.get("j_id_amp_u", 0.0785))      # 归一化电流 dither 幅值（×I_BASE）
    _jid_n = max(int(round(float(cfg.get("j_id_win", 0.2)) / 1e-3)), 10)
    _jid_lp = float(cfg.get("j_id_lp", 0.5))
    _jid_tend = float(cfg.get("j_id_tend", 1e9))   # 调试期结束：冻结估计、关闭 dither
    _j_adapt_b0 = bool(cfg.get("j_adapt_b0", True))
    _j_adapt_kp = bool(cfg.get("j_adapt_kp", False))
    _oracle = bool(cfg.get("j_oracle", False))
    _jhat = J_M
    _B0e = B0 * (J_M / J_TRUE) if _oracle else B0
    _KPe = KP
    _te_c = _te_s = _w_c = _w_s = 0.0
    _nid = 0
    jhat_o = []
    BETA3 = cfg.get("beta3", 2000.0); TAU0 = cfg.get("tau0", 20e-3)
    Q0 = cfg.get("Q0", 0.98); ZETA = 0.2
    rc_inj = str(cfg.get("rc_inj", "tanh"))   # 重复通道注入非线性：tanh（默认）或 fal
    u_z1 = bool(cfg.get("u_z1", True))      # 控制律比例项：默认用 z1（2026-11-12 统一）；False 可复现旧法规 r-y
    kp_boost = cfg.get("kp_boost", 0.0); det_eps = cfg.get("det_eps", 0.01)
    kp_gpow = float(cfg.get("kp_gpow", 1.0))      # 门控形状：g^p，p>1 更只在冲击瞬间发力
    # 律D 增益自适应（2026-11-11）：瞬态时同时抬高 ESO 带宽与重复通道注入增益
    #   ESO: β1' = 2ω_o(1+a g)、(β2' = [ω_o(1+a g)]²)  —— 保持二阶带宽一致的配套缩放
    #   重复: β3' = β3 (1+b g)
    kb_eso = float(cfg.get("kb_eso", 0.0))       # ESO 带宽相对提升（×g）
    kb_b3 = float(cfg.get("kb_b3", 0.0))         # 重复通道注入增益相对提升（×g）
    # β₃ 幅值自适应（2026-11-11 用户思路）：
    #   e1 经"自适应中心频率的带通（巴斯沃夫/SVF）"取出周期基波 → 一个周期 RMS 估幅值 A
    #   β₃_eff = β₃min + (β₃max-β₃min)·min(1,(A/A_ref)²)
    rc_bp = float(cfg.get("rc_bp", 0.0))         # >0 启用；值即带通 Q（±10% 带宽 ⇒ Q=5）
    b3_min = float(cfg.get("b3_min", 1000.0))
    b3_max = float(cfg.get("b3_max", 4000.0))
    a_ref = float(cfg.get("a_ref", 0.02))        # 目标基波幅值（归一化转速误差）
    rc_src = str(cfg.get("rc_src", "e1"))        # 带通输入：e1（ESO 新息）或 et（跟踪误差 1-y）
    # A 作"振荡幅值监督器"：A 超限时把 β₃ 回落到安全值（默认关）
    a_lim = float(cfg.get("a_lim", 0.0))
    b3_safe = float(cfg.get("b3_safe", 4000.0))
    # 周期自整定（ESC，2026-11-11）：T = T_gross*(1+delta)，目标 min A
    T_es = bool(cfg.get("T_es", False))
    es_d0 = float(cfg.get("es_d0", -0.143))      # 初始 δ（默认取理论值 -arctan(ωτ)/2π）
    es_step = float(cfg.get("es_step", 0.01))    # 每次更新的步长 σ
    es_dith = float(cfg.get("es_dith", 0.01))    # 抖动幅度 Δ（正弦）
    es_Pd = float(cfg.get("es_Pd", 1.5))         # 抖动周期 P_d（s）
    es_N = int(cfg.get("es_N", 3))               # 每 N 个抖动周期更新一次
    es_dead = float(cfg.get("es_dead", 0.0))     # 调制量死区
    es_dmax = float(cfg.get("es_dmax", 0.20))
    es_t0 = float(cfg.get("es_t0", 3.0))         # 开始搜索的时刻
    es_freeze = float(cfg.get("es_freeze", 2.0))
    es_ff = bool(cfg.get("es_ff", False))        # 解冻时用理论值前馈重置 δ
    ff_flush = cfg.get("ff_flush", 0.0); tauf = cfg.get("ff_tau_f", 4e-3)
    taus = cfg.get("ff_tau_s", 0.5); ff_cool = cfg.get("ff_cool", 0.3)
    ff_src = str(cfg.get("ff_src", "e1"))
    ff_amin = cfg.get("ff_amin", 0.0); ff_gmax = cfg.get("ff_gmax", -1.0)
    ff_vmax = cfg.get("ff_vmax", -1.0)
    ff_mism = cfg.get("ff_mism", 0.0)          # 记忆失配阈值（0=关）；>0 时与包络比值 OR
    ff_mism_eps = cfg.get("ff_mism_eps", 1e-6)
    # 2026-10-22：记忆失配的方向限定。0=对称 |E_v(t)-E_v(t-T)|（v4.0）；
    #   1=只认"旧记忆比当前强"的方向 max(0, E_v(t-T)-E_v(t))——撤除事件该量为正，
    #   而稳态周期波动时正负对称、事件前误报显著减少。
    ff_mism_dir = int(cfg.get("ff_mism_dir", 0))
    # 2026-10-22：检测器触发的复位算子 R_alpha。0=清空（默认，v4.0 行为）；
    #   -1 = 反相复位（v->-v，缓冲同时取反），用于"反相突变"事件——此时清空是错的动作。
    ff_alpha = float(cfg.get("ff_alpha", 0.0))
    # 角度锁相失效事件（2026-11-11）：在 tl_ang_phase_t 时刻把型线相位整体跳 tl_ang_phase（rad）
    _phj_t = float(cfg.get("tl_ang_phase_t", -1.0))
    _phj_d = float(cfg.get("tl_ang_phase", 0.0))
    _phj_i = int(round(_phj_t / dt)) if _phj_t >= 0.0 else None
    # 符号一致性检测（2026-11-11）：e1 与记忆 v 的瞬时投影 C=<e1·v>/<v²>。
    # 记忆正确时 C≈0；反相后记忆符号反了，e1≈-2v ⇒ C 迅速变负，可在 ~10 ms 内报警。
    ff_sgn = float(cfg.get("ff_sgn", 0.0))          # 阈值（>0 启用，触发条件 C<-ff_sgn）
    ff_sgn_win = float(cfg.get("ff_sgn_win", 0.010))  # 滑窗长度（s）
    ff_sgn_v2 = float(cfg.get("ff_sgn_v2", 1e-9))     # 记忆能量下限
    ff_sgn_src = str(cfg.get("ff_sgn_src", "et"))       # 检测量：et=跟踪误差 1-y，e1=ESO 新息
    ff_max_trig = int(cfg.get("ff_max_trig", 0))        # F 通道单次运行最多动作次数（0=不限）
    # 2026-10-22：角度锁相周期负载 T(φ)=T(φ+2π)，dφ/dt=ω（φ 为机械角）。
    #   推荐型线：tl_profile.disc_unbalance_profile()，即「圆盘质量不对中模式」
    #   （1–6 次谐波，基波为主，THD=77.46%；旧 30% 约束不再满足）。
    #   tl_ang       : 单位幅值的周期表（长度 N，均匀铺满 0..2π），None=关闭
    #   tl_ang_amp   : 该分量的幅值（N·m）
    #   tl_ang_start : 该分量开始作用的时刻（s）
    _tla = cfg.get("tl_ang", None)
    _TLA = np.asarray(_tla, dtype=float) if _tla is not None else None
    _TLAA = float(cfg.get("tl_ang_amp", 0.0))
    _TLAK = (len(_TLA) / TWO_PI) if _TLA is not None else 0.0
    _nang0 = int(round(float(cfg.get("tl_ang_start", 0.0)) / dt))
    _tlae = cfg.get("tl_ang_end", None)       # 角度锁相分量的撤除时刻（None=不撤除）
    _nang1 = int(round(float(_tlae) / dt)) if _tlae is not None else None
    _tlar = cfg.get("tl_ang_rev", None)       # 角度锁相分量的反相时刻（None=不反相）
    # 故障负载模型（2026-11-13，附录 A/B）：tl_fault=None 时关闭，逐位不变
    #   cfg["tl_fault"] = {"start": 0.0,
    #                      "unbalance": {"M":0.1,"e":1e-4,"kappa":1.0},
    #                      "misalign":  {"M":0.1,"beta":0.01745,"l":0.05,"kappa":1.0}}
    _tflt = cfg.get("tl_fault", None)
    _tflt_n0 = int(round(float((_tflt or {}).get("start", 0.0)) / dt))
    _nangr = int(round(float(_tlar) / dt)) if _tlar is not None else None
    ff_wait = cfg.get("ff_wait", 0.0)          # 检测后再等待的相位延迟（s），0=立即复位
    ff_confirm = cfg.get("ff_confirm", 0.0)    # 连续确认窗（ms），0=首拍触发
    ff_imin = cfg.get("ff_imin", 0.0)          # 带载门控：|iq| 低于该值不复位（A）
    ff_vphase = cfg.get("ff_vphase", None)     # 相位条件：v 低于该阈值时复位（None=关）
    ff_vwait_max = cfg.get("ff_vwait_max", 0.03)  # 相位等待的上限（s）
    ff_phase = cfg.get("ff_phase", None)       # 10 Hz 相位目标（rad，None=关）
    ff_phase_tol = cfg.get("ff_phase_tol", 0.35)
    ff_phase_max = cfg.get("ff_phase_max", 0.04)
    ff_phi = cfg.get("ff_phi", 0.0)
    # F 通道解耦（2026-11-11）：用 F 档单独标定出的触发时刻回放复位，
    # 这样律D 开/关都不会改变 F 的动作时刻。
    _rep = cfg.get("replay_trig", None)
    _rep = sorted(float(x) for x in _rep) if _rep else None
    _rep_i = 0
    # 参考转速突变 + 自适应重复周期（2026-11-11）
    #   n_ref2 / t_nref：t_nref 之后参考转速从 n_ref 切到 n_ref2（归一化后 y_ref = n_ref2/n_ref）
    #   T_adapt=True：重复控制延迟 = 2π/ω，ω 取实测转速 ⇒ T 随转速变化
    _nref2 = cfg.get("n_ref2", None)
    _tnref = float(cfg.get("t_nref", 1e9))
    _yref2 = (float(_nref2) / n_ref) if _nref2 is not None else 1.0
    _nref3 = cfg.get("n_ref3", None)          # 第二次参考跳变（往返换速用）
    _tnref2 = float(cfg.get("t_nref2", 1e9))
    _yref3 = (float(_nref3) / n_ref) if _nref3 is not None else _yref2
    _Tadapt = bool(cfg.get("T_adapt", False))
    _Tfilt = float(cfg.get("T_filt", 0.0))       # 对用于算 T 的转速滤波（s），0=不滤
    flush_t = cfg.get("flush_t", None)         # F-A oracle：在该时刻直接复位
    flush_alpha = cfg.get("flush_alpha", 0.0)  # 0=清空；-1=反相

    # ---- 电流环 ----
    fci = cfg.get("fci", 500.0); wci = TWO_PI * fci
    kpi = L_S * wci; kii = R_S * wci

    # ---- 采样与噪声 ----
    i_peak = cfg.get("i_noise_peak", 0.2)   # dq 采样噪声峰值（A），均匀分布
    sig_n = cfg.get("sig_n", 6.0)           # 转速采样噪声（rpm）：1% × 600
    sig_Tp = cfg.get("sig_T_pct", 2.5)      # 负载噪声（% 额定，旧口径）
    sig_T_nm = cfg.get("sig_T_nm", 0.025)   # 负载噪声（N·m，真实对象默认口径）
    sig_T_sigma = float(sig_T_nm) if sig_T_nm is not None else sig_Tp / 100.0 * 0.637
    seed_i = cfg.get("seed_i", 20261016)
    seed_n = cfg.get("seed_n", 20261018)
    seed_T = cfg.get("seed_T", 20261017)

    nsp = max(1, int(round(1e-3 / dt)))
    npwm = max(1, int(round(Tpwm / dt)))
    nTstep = max(1, int(round(1e-4 / dt)))
    nS = int(round(t[-1] / 1e-3)) + 2
    nT = int(round(t[-1] / 1e-4)) + 2
    TLn = band_noise(nT, sig_T_sigma, 200.0, 1e-4, seed_T)
    NW = band_noise(nS, sig_n, 200.0, 1e-3, seed_n)
    nCI = int(n // npwm) + 2
    rng = np.random.default_rng(seed_i)
    NID = rng.uniform(-i_peak, i_peak, nCI)
    NIQ = rng.uniform(-i_peak, i_peak, nCI)

    # 状态
    idq = np.zeros(2)
    w = 0.0
    th = 0.0
    z1 = z2 = v = 0.0
    u = 0.0
    int_d = int_q = 0.0
    vd_cmd = vq_cmd = 0.0
    duty = np.array([0.5, 0.5, 0.5])
    cnt_prev = 0

    # 重复通道延迟（T/1ms 拍）
    nd = max(1, int(round(T / 1e-3)))
    NMAX = 640                                   # 自适应延迟线最大长度（640 ms）
    vd_buf = np.zeros(NMAX); ip = 0; vd_delay = 0.0; nd_now = nd
    vm_buf = np.zeros(nd); vm_old = np.zeros(nd)
    vm_now = 0.0; vm_prev = 0.0; mip = 0

    # F-B 检测状态
    efs = efl = 0.0; fft = 0.0; fft2 = 0.0
    e1g_acc = 0.0; e1g_buf = np.zeros(nd); e1g_p = 0
    nsg = max(2, int(round(ff_sgn_win / 1e-3))) if ff_sgn > 0.0 else 2
    sg_ev_buf = np.zeros(nsg); sg_vv_buf = np.zeros(nsg)
    sg_p = 0; sg_ev = 0.0; sg_vv = 0.0; sg_ready = 0; sg_now = 0.0
    _wT = w_ref
    _bp_low = 0.0; _bp_band = 0.0
    _es_dh = es_d0; _es_delta = es_d0; _es_I = 0.0
    _es_tnext = es_t0 + es_N * es_Pd; _es_ph = 0.0
    _es_tfreeze = 0.0; _es_n = 0; _Tgnow = T; _Tgprev = None; _Tglp = T
    bp_acc = 0.0; bp_buf = np.zeros(nd); bp_p = 0; _A_now = 0.0; _b3_now = BETA3
    trig_log = []
    oracle_log = []
    oracle_done = False
    pending_t = None
    pending_phase = None
    raw_cnt = 0
    phase_pending = False
    phase_deadline = 0.0
    n10 = max(4, int(round(0.02 / 1e-3)))   # 20 ms 正交解调窗
    vc10 = np.zeros(n10); vs10 = np.zeros(n10); v10p = 0
    v10c = 0.0; v10s = 0.0; v10_ph = 0.0; v10_amp = 0.0

    # 输出（按 10 us 抽取）
    dec = max(1, int(round(1e-5 / dt)))
    no = n // dec + 1
    y_o = np.zeros(no); id_o = np.zeros(no); iq_o = np.zeros(no)
    ia_o = np.zeros(no); vd_o = np.zeros(no); vq_o = np.zeros(no)
    u_o = np.zeros(no); vqc_o = np.zeros(no); iqr_o = np.zeros(no)
    fl_o = np.zeros(no)
    dm_o = np.zeros(no)
    sg_o = np.zeros(no)
    b3_o = np.zeros(no); a_o = np.zeros(no); es_o = np.zeros(no)
    tl_o = np.zeros(no)          # 实际施加的负载转矩（含角度锁相分量），供出图/核对

    def leg(g, cur):
        s = 1.0 if cur > 0.0 else (-1.0 if cur < 0.0 else 0.0)
        return Vdc * (g - 0.5) - s * Vdc * Td / Tpwm - s * Vdrop - Ron * cur

    c3 = math.cos(2.0943951023931953)
    s3 = math.sin(2.0943951023931953)
    for k in range(1, n):
        we = P_POL * w
        th += we * dt
        ca, sa = math.cos(th), math.sin(th)
        cb, sb = math.cos(th - 2.0943951023931953), math.sin(th - 2.0943951023931953)
        cc, sc = math.cos(th + 2.0943951023931953), math.sin(th + 2.0943951023931953)
        ia = idq[0] * ca - idq[1] * sa
        ib = idq[0] * cb - idq[1] * sb
        ic = -(ia + ib)
        # PWM：中心对齐三角载波
        ph = (k * dt) % Tpwm / Tpwm
        tri = 2.0 * ph if ph < 0.5 else 2.0 * (1.0 - ph)
        va = leg(1.0 if duty[0] > tri else 0.0, ia)
        vb = leg(1.0 if duty[1] > tri else 0.0, ib)
        vc = leg(1.0 if duty[2] > tri else 0.0, ic)
        vcm = (va + vb + vc) / 3.0
        va -= vcm; vb -= vcm; vc -= vcm
        vd = (2.0 / 3.0) * (va * ca + vb * cb + vc * cc)
        vq = (2.0 / 3.0) * (-va * sa - vb * sb - vc * sc)
        did = (vd - R_S * idq[0] + we * L_S * idq[1]) / L_S
        diq = (vq - R_S * idq[1] - we * L_S * idq[0] - we * PSI_F) / L_S
        idq[0] += dt * did; idq[1] += dt * diq
        Te = 1.5 * P_POL * PSI_F * idq[1]
        _tl = TL[k]
        if _tflt is not None and k >= _tflt_n0:
            _phimf = (th / P_POL) % TWO_PI
            _tlf = 0.0
            _u = _tflt.get("unbalance")
            if _u:
                _tlf += unbalance_torque(_phimf, w, **_u)
            _m = _tflt.get("misalign")
            if _m:
                _tlf += misalign_torque(_phimf, w, **_m)
            _tl += _tlf
        if _TLA is not None and k >= _nang0 and (_nang1 is None or k < _nang1):  # 角度锁相分量：按当前机械角查表
            _phim = (th / P_POL) % TWO_PI
            if (_phj_i is not None) and (k >= _phj_i):
                _phim = (_phim + _phj_d) % TWO_PI
            _tlv = _TLAA * _TLA[int(_phim * _TLAK) % len(_TLA)]
            if _nangr is not None and k >= _nangr:   # 反相：值连续、符号翻转
                _tlv = -_tlv
            _tl += _tlv
        _tl_tot = _tl + TLn[min(k // nTstep, nT - 1)]      # 实际施加的总负载（含负载噪声）
        w += dt * (Te - _tl_tot) / J_TRUE  # 主循环用真实 J；B0 仍由 J_M 标称

        # ---- 电流环：每个 PWM 周期一次 ----
        if k % npwm == 0:
            ci = k // npwm
            idm = idq[0] + NID[ci]
            iqm = idq[1] + NIQ[ci]
            ed = 0.0 - idm; eq = u * I_BASE - iqm
            int_d += ed * Tpwm; int_q += eq * Tpwm
            vd_cmd = kpi * ed + kii * int_d - we * L_S * iqm
            vq_cmd = kpi * eq + kii * int_q + we * (L_S * idm + PSI_F)
            vm = math.hypot(vd_cmd, vq_cmd)
            if vm > Vlim:
                sc_ = Vlim / vm
                vd_cmd *= sc_; vq_cmd *= sc_
                int_d *= 0.999; int_q *= 0.999
            v_a = vd_cmd * ca - vq_cmd * sa
            v_b = vd_cmd * cb - vq_cmd * sb
            v_c = -(v_a + v_b)
            vmx = max(v_a, v_b, v_c); vmn = min(v_a, v_b, v_c)
            v0 = -(vmx + vmn) / 2.0
            duty = np.clip(np.array([0.5 + (v_a + v0) / Vdc,
                                     0.5 + (v_b + v0) / Vdc,
                                     0.5 + (v_c + v0) / Vdc]), 0.0, 1.0)

        # ---- 速度环：每 1 ms 一次 ----
        if k % nsp == 0:
            cnt = int(math.floor((th / P_POL) / TWO_PI * ENC_CPR))
            dcnt = cnt - cnt_prev
            if dcnt > ENC_CPR / 2:
                dcnt -= ENC_CPR
            elif dcnt < -ENC_CPR / 2:
                dcnt += ENC_CPR
            w_enc = dcnt / ENC_CPR * TWO_PI / 1e-3
            cnt_prev = cnt
            y_m = (w_enc / w_ref) + NW[min(k // nsp, nS - 1)] / n_ref
            e1 = y_m - z1
            # g 门控：e1 的 T 窗均值
            e1g_acc += e1 * 1e-3 - e1g_buf[e1g_p]; e1g_buf[e1g_p] = e1 * 1e-3
            e1g_p = (e1g_p + 1) % nd
            e1m = e1g_acc / T
            eps_g = det_eps if det_eps > 0.0 else 0.01
            g = (e1m * e1m) / (e1m * e1m + eps_g * eps_g)
            _gp = g ** kp_gpow if kp_gpow != 1.0 else g   # 律D 门控形状（2026-11-11）
            kpe = _KPe * (1.0 + kp_boost * _gp)
            _g1 = ESO_G1(e1); _g2 = ESO_G2(e1)       # 线性档 G(e)=e（逐位不变）
            _woe = WO * (1.0 + kb_eso * g) if kb_eso > 0.0 else WO
            z1n = z1 + 1e-3 * (z2 + _B0e * u + v + 2.0 * _woe * _g1)
            z2n = z2 + 1e-3 * (_woe * _woe * _g2)
            e1p = (e1 - ff_phi * math.tanh(e1 / ff_phi)) if ff_phi > 0.0 else e1
            if _Tadapt:
                if _Tfilt > 0.0:
                    _a = 1.0 - math.exp(-1e-3 / _Tfilt)
                    _wT += _a * (abs(w_enc) - _wT)
                else:
                    _wT = abs(w_enc)
                _Tnow = TWO_PI / max(_wT, 1e-6)
            else:
                _Tnow = T
            _Tgnow = _Tnow
            if T_es:
                if k * dt >= es_t0:
                    _es_ph = TWO_PI * (k * dt - es_t0) / es_Pd
                    _es_delta = _es_dh + es_dith * math.sin(_es_ph)
                else:
                    _es_delta = _es_dh
                _Tnow = _Tnow * (1.0 + _es_delta)
            _ndf = max(4.0, min(float(NMAX - 2), _Tnow / 1e-3))
            nd_now = int(_ndf)
            _ndfrac = _ndf - nd_now
            vd_delay = ((1.0 - _ndfrac) * vd_buf[(ip - nd_now) % NMAX]
                        + _ndfrac * vd_buf[(ip - nd_now - 1) % NMAX])
            if rc_bp > 0.0:
                # 巴斯沃夫带通（SVF 实现）：中心 f0=ω/2π，Q=rc_bp（±10% ⇒ Q=5）
                #   A = sqrt( (1/T) ∫_{t-T}^{t} y_bp² )：带通输出的一个周期均方根
                _f0 = max(abs(_wT), 1.0) / TWO_PI
                _f0 = min(_f0, 400.0)
                _ffc = 2.0 * math.sin(math.pi * _f0 / 1000.0)
                _bp_low += _ffc * _bp_band
                _xin = e1 if rc_src == "e1" else (1.0 - y_m)
                _bp_high = _xin - _bp_low - (1.0 / rc_bp) * _bp_band
                _bp_band += _ffc * _bp_high
                _v2 = _bp_band * _bp_band
                bp_acc += _v2 - bp_buf[bp_p]; bp_buf[bp_p] = _v2
                bp_p = (bp_p + 1) % nd
                _A_now = math.sqrt(max(bp_acc, 0.0) / nd)
                if T_es:
                    # 换速冻结：标称周期相对 20 ms 低通偏离 >5% 时暂停搜索并清空累加器
                    _al = 1.0 - math.exp(-1e-3 / 0.02)
                    if abs(_Tgnow - _Tglp) > 0.05 * _Tglp:
                        _es_tfreeze = k * dt + es_freeze
                        _es_I = 0.0
                        _es_tnext = k * dt + es_freeze + es_N * es_Pd
                    _Tglp += _al * (_Tgnow - _Tglp)
                    _Tgprev = _Tgnow
                    if es_ff and (k * dt < _es_tfreeze):
                        # 冻结期间用理论值 δ*=-arctan(ωτ)/2π 跟踪新转速
                        _dff = -math.atan(max(_wT, 1e-6) * TAU0) / (2.0 * math.pi)
                        _es_dh = max(-es_dmax, min(es_dmax, _dff))
                    if (k * dt >= es_t0) and (k * dt >= _es_tfreeze):
                        # 锁相解调：I = 2/(N·P_d) ∫ A·sin(ω_d t) dt
                        _es_I += _A_now * math.sin(_es_ph) * 1e-3
                        if k * dt >= _es_tnext:
                            _Nw = max(1.0, _es_tnext - (k * dt - es_N * es_Pd))
                            _Ibar = 2.0 * _es_I / max(es_N * es_Pd, 1e-9)
                            if abs(_Ibar) > es_dead:
                                _es_dh = max(-es_dmax, min(es_dmax,
                                           _es_dh - es_step * (1.0 if _Ibar > 0 else -1.0)))
                            _es_I = 0.0
                            _es_n += 1
                            _es_tnext = k * dt + es_N * es_Pd
                _r = _A_now / max(a_ref, 1e-9)
                _b3_now = b3_min + (b3_max - b3_min) * min(1.0, _r * _r)
                if (a_lim > 0.0) and (_A_now > a_lim):
                    _b3_now = b3_safe
                _b3e = _b3_now
            else:
                _b3e = BETA3 * (1.0 + kb_b3 * g) if kb_b3 > 0.0 else BETA3
            if rc_inj == "fal":
                _inj = ESO_G2(e1p)            # 类 fal：次线性、无界
            else:
                _inj = math.tanh(e1p / ZETA)  # 饱和、有界
            chi = Q0 * vd_delay + _b3e * _inj
            if TAU0 <= 1e-9:
                vn = chi          # tau=0：无低通（一阶低通极限）
            else:
                vn = chi + (v - chi) * math.exp(-1e-3 / TAU0)
            # 10 Hz 正交解调：v 的相位/幅值（20 ms 窗）
            if ff_phase is not None:
                _c = math.cos(2 * math.pi * k * dt / T)
                _s = math.sin(2 * math.pi * k * dt / T)
                _cc = vn * _c; _ss = vn * _s
                v10c += _cc - vc10[v10p]; v10s += _ss - vs10[v10p]
                vc10[v10p] = _cc; vs10[v10p] = _ss
                v10p = (v10p + 1) % n10
                v10_amp = 2.0 * math.hypot(v10c, v10s) / n10
                _phi = math.atan2(v10s, v10c)
                v10_ph = (2 * math.pi * k * dt / T - _phi) % TWO_PI
            # 回放 F 档的触发时刻（与 D 无关）
            if (_rep is not None) and (_rep_i < len(_rep)) and (k * dt >= _rep[_rep_i]):
                vn = ff_alpha * vn; vd_buf[:] = ff_alpha * vd_buf
                trig_log.append((k * dt, v, 0.0, -99.0))
                _rep_i += 1
            # F-A oracle：事件时刻直接复位（0=清空，-1=反相）
            if (flush_t is not None) and (not oracle_done) and (k * dt >= float(flush_t)):
                oracle_log.append((float(k * dt), float(v), float(vn)))
                if flush_alpha == 0.0:
                    vn = 0.0; vd_buf[:] = 0.0
                else:
                    vn = flush_alpha * vn; vd_buf[:] = flush_alpha * vd_buf
                oracle_done = True
            if k * dt >= _tnref2:
                _yref = _yref3
            elif k * dt >= _tnref:
                _yref = _yref2
            else:
                _yref = 1.0
            _fb = (_yref - z1n) if u_z1 else (_yref - y_m)
            u = (kpe * _fb - z2n - vn) / _B0e
            if _jid and k * dt >= _jid_tend:
                _jid = False
                _B0e = B0 * (J_M / _jhat)       # 冻结估计，应用一次
                _KPe = KP
            if _jid:
                _ph = _jid_w * k * dt
                u += _jid_amp * math.sin(_ph)          # 转矩 dither（叠加在电流指令上）
                _te_c += Te * math.cos(_ph); _te_s += Te * math.sin(_ph)
                _w_c += w_enc * math.cos(_ph); _w_s += w_enc * math.sin(_ph)
                _nid += 1
                if _nid >= _jid_n:
                    _ate = 2.0 / _nid * math.hypot(_te_c, _te_s)
                    _aw = 2.0 / _nid * math.hypot(_w_c, _w_s)
                    if _aw > 1e-9:
                        _jnew = _ate / (_jid_w * _aw)
                        _jnew = min(max(_jnew, 0.5 * J_M), 50.0 * J_M)
                        _jhat = (1.0 - _jid_lp) * _jhat + _jid_lp * _jnew
                        if _j_adapt_b0:
                            _B0e = B0 * (J_M / _jhat)
                        if _j_adapt_kp:
                            _KPe = KP * (_jhat / J_M)
                    _te_c = _te_s = _w_c = _w_s = 0.0
                    _nid = 0
            jhat_o.append(_jhat)
            # F-B 检测：包络比值（ff_flush）和/或记忆失配（ff_mism），默认关
            if ff_flush > 0.0 or ff_mism > 0.0:
                fft = max(0.0, fft - 1e-3); fft2 = max(0.0, fft2 - 1e-3)
                esrc = (1.0 - y_m) if ff_src == "et" else e1
                raw_env = False
                okg = (ff_gmax < 0.0) or (g < ff_gmax)
                oki = (ff_imin <= 0.0) or (abs(idq[1]) > ff_imin)
                okv = (ff_vmax < 0.0) or (abs(v) < ff_vmax)
                if ff_flush > 0.0:
                    efs += (1.0 - math.exp(-1e-3 / max(tauf, 1e-9))) * (abs(esrc) - efs)
                    efl += (1.0 - math.exp(-1e-3 / max(taus, 1e-9))) * (abs(esrc) - efl)
                    raw_env = ((efs > ff_flush * max(efl, 1e-9)) and (efs > ff_amin)
                               and okg and okv)
                Dm = 0.0
                if ff_mism > 0.0:
                    v2d = vn * vn * 1e-3
                    leave = vm_buf[mip]; drop = vm_old[mip]
                    vm_now += v2d - leave
                    vm_prev += leave - drop
                    vm_buf[mip] = v2d; vm_old[mip] = leave
                    mip = (mip + 1) % nd
                    if ff_mism_dir:
                        Dm = max(0.0, vm_prev - vm_now) / (vm_prev + ff_mism_eps)
                    else:
                        Dm = abs(vm_now - vm_prev) / (vm_prev + ff_mism_eps)
                    dm_o[k // dec] = Dm
                raw = raw_env or ((ff_mism > 0.0) and (Dm > ff_mism) and okg and okv and oki)
                if raw and (fft <= 0.0) and (k * dt > 0.05):
                    raw_cnt += 1
                else:
                    raw_cnt = 0
                _need = max(1, int(round(ff_confirm)))
                _armed = (ff_max_trig <= 0) or (len(trig_log) < ff_max_trig)
                if (raw_cnt >= _need) and _armed and (fft <= 0.0) and (k * dt > 0.05) and (pending_t is None) and (not phase_pending):
                    raw_cnt = 0
                    if ff_phase is not None:
                        phase_pending = True
                        phase_deadline = k * dt + ff_phase_max
                    elif ff_vphase is not None:
                        pending_t = k * dt + ff_vwait_max
                        pending_phase = ff_vphase
                    elif ff_wait > 0.0:
                        pending_t = k * dt + ff_wait
                        pending_phase = None
                    else:
                        vn = ff_alpha * vn; vd_buf[:] = ff_alpha * vd_buf; fft = ff_cool
                        fl_o[k // dec] = 1.0
                        trig_log.append((k * dt, v, efs, Dm))
                if phase_pending and _armed:
                    _dphi = (v10_ph - ff_phase + math.pi) % TWO_PI - math.pi
                    if (abs(_dphi) < ff_phase_tol) or (k * dt >= phase_deadline):
                        vn = ff_alpha * vn; vd_buf[:] = ff_alpha * vd_buf; fft = ff_cool
                        phase_pending = False
                        fl_o[k // dec] = 1.0
                        trig_log.append((k * dt, v, efs, Dm))
                if (pending_t is not None) and _armed:
                    _go = ((pending_phase is not None and v < pending_phase)
                           or (k * dt >= pending_t))
                    if _go:
                        vn = ff_alpha * vn; vd_buf[:] = ff_alpha * vd_buf; fft = ff_cool
                        pending_t = None; pending_phase = None
                        fl_o[k // dec] = 1.0
                        trig_log.append((k * dt, v, efs, Dm))
            # 符号一致性检测
            if ff_sgn > 0.0:
                fft = max(0.0, fft - 1e-3)
                _err = (1.0 - y_m) if ff_sgn_src == "et" else e1
                _ev = _err * vn
                _vv = vn * vn
                sg_ev += _ev - sg_ev_buf[sg_p]; sg_ev_buf[sg_p] = _ev
                sg_vv += _vv - sg_vv_buf[sg_p]; sg_vv_buf[sg_p] = _vv
                sg_p = (sg_p + 1) % nsg
                if sg_ready < nsg:
                    sg_ready += 1
                if sg_vv > ff_sgn_v2:
                    sg_now = sg_ev / (sg_vv + 1e-15)
                if (sg_ready >= nsg) and (sg_vv > ff_sgn_v2) and (fft <= 0.0) and (k * dt > 0.1):
                    if sg_now < -ff_sgn:
                        vn = ff_alpha * vn; vd_buf[:] = ff_alpha * vd_buf; fft = ff_cool
                        fl_o[k // dec] = 1.0
                        trig_log.append((k * dt, v, efs, sg_now))
            z1, z2, v = z1n, z2n, vn
            vd_buf[ip] = v; ip = (ip + 1) % NMAX

        if k % dec == 0:
            j = k // dec
            y_o[j] = w / w_ref; id_o[j] = idq[0]; iq_o[j] = idq[1]
            ia_o[j] = ia; vd_o[j] = vd; vq_o[j] = vq
            u_o[j] = u; vqc_o[j] = vq_cmd; iqr_o[j] = u * I_BASE
            tl_o[j] = _tl_tot                                 # 出图用：含负载噪声的总负载
            sg_o[j] = sg_now
            b3_o[j] = _b3_now; a_o[j] = _A_now; es_o[j] = _es_delta
    tt = t[::dec]
    m = min(len(tt), no)
    return dict(t=tt[:m], y=y_o[:m], id=id_o[:m], iq=iq_o[:m], ia=ia_o[:m],
                vd=vd_o[:m], vq=vq_o[:m], u=u_o[:m], vqc=vqc_o[:m],
                iqr=iqr_o[:m], fl=fl_o[:m], dm=dm_o[:m], tl=tl_o[:m], sg=sg_o[:m],
                b3=b3_o[:m], amp=a_o[:m], es=es_o[:m],
                trig=trig_log, oracle=oracle_log,
                jhat=np.asarray(jhat_o), t_j=np.arange(len(jhat_o)) * 1e-3)

