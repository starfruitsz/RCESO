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
from fault_torque import unbalance_torque, misalign_torque, parallel_torque

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
    _J_STEP_T = float(cfg.get("j_step_t", 1e9))
    _J_STEP_V = float(cfg.get("j_step_val", J_TRUE))
    _Jt = J_TRUE
    # ---- J 辨识/自适应（2026-11-13）----
    _jid = bool(cfg.get("j_id", False))
    _jid_f = float(cfg.get("j_id_f", 100.0))
    _jid_w = 2.0 * math.pi * _jid_f
    _jid_amp = float(cfg.get("j_id_amp_u", 0.0785))      # 归一化电流 dither 幅值（×I_BASE）
    _jid_n = max(int(round(float(cfg.get("j_id_win", 0.2)) / 1e-3)), 10)
    _jid_lp = float(cfg.get("j_id_lp", 0.5))
    _jid_tend = float(cfg.get("j_id_tend", 1e9))   # 调试期结束：冻结估计、关闭 dither
    _jid_t0 = float(cfg.get("j_id_t0", 0.5))       # 辨识起始（避开启动瞬态）
    _jid_snr_min = float(cfg.get("j_id_snr_min", 2.0))   # 转速 dither 幅值下限 / rpm
    _jid_nmin = int(cfg.get("j_id_nmin", 3))
    _jid_std_max = float(cfg.get("j_id_std_max", 0.15))
    _jlist = []
    _jstate = 0 if not _jid else 1
    jstate_o = []
    _j_adapt_b0 = bool(cfg.get("j_adapt_b0", True))
    _j_adapt_kp = bool(cfg.get("j_adapt_kp", False))
    _oracle = bool(cfg.get("j_oracle", False))
    # 辨识是否一开始就打开（用于 j_val 的默认值：只有 j_id 开时才可能进入校验）
    _jid_on0 = _jid
    _jhat = J_M
    # ---- ESO/DO 观测器在线惯量辨识（实验，2026-11-14；默认关闭）----
    _jdo_on = bool(cfg.get("j_do", False))
    _jdo_gamma = float(cfg.get("j_do_gamma", 2.0e-4))
    _jdo_lpf = float(cfg.get("j_do_lpf", 0.02))
    _jdo_tau = float(cfg.get("j_do_tau", 0.5))
    _jdo_J = J_M
    _jdo_TL = 0.0
    _jdo_wprev = 0.0
    _jdo_wdotf = 0.0
    # ---- Yang 2018 AKO-RLS 在线惯量辨识（实验，2026-11-14；默认关闭）----
    _ako_on = bool(cfg.get("j_ako", False))
    _ako_J = J_M
    _ako_X = None
    _ako_P = np.eye(3)
    _ako_Q = np.diag([1e-3, 1e-2, 1e-1])
    _ako_R = float(cfg.get("j_ako_R", 1e-3))
    _ako_ethr = float(cfg.get("j_ako_ethr", 1e-4))
    _ako_rho = float(cfg.get("j_ako_rho", 0.1))
    _ako_lam = float(cfg.get("j_ako_lam", 0.99))
    _ako_sigma = np.zeros(2)
    _ako_psi = np.eye(2)
    _ako_th_prev = None
    _ako_th_unw = 0.0
    _ako_w_prev = 0.0
    _ako_TL_prev = 0.0
    _ako_Te_prev = 0.0
    _ako_first = True
    # ---- 周期 dither 复检（实验，2026-11-14；默认关闭）----
    _jrec = bool(cfg.get("j_recheck", False))
    _jrec_period = float(cfg.get("j_recheck_period", 5.0))
    _jrec_len = float(cfg.get("j_recheck_len", 0.6))
    _jrec_f = float(cfg.get("j_recheck_f", 100.0))
    _jrec_f_auto = bool(cfg.get("j_recheck_f_auto", False))
    _jrec_f_ci = float(cfg.get("fci", 500.0))
    _jrec_f_q = float(cfg.get("j_recheck_f_q", _jrec_f_ci / 100.0 + 1.0))
    _jrec_f_alpha = float(cfg.get("j_recheck_f_alpha", 0.35))
    _jrec_f_min = float(cfg.get("j_recheck_f_min", 50.0))
    _jrec_f_max = float(cfg.get("j_recheck_f_max", _jrec_f_ci / 5.0 + 10.0))
    _jrec_f_grid = float(cfg.get("j_recheck_f_grid", 5.0))
    _jrec_fd = _jrec_f
    _jrec_w = 2.0 * math.pi * _jrec_fd
    _jrec_amp = float(cfg.get("j_recheck_amp", 0.157))
    _jrec_amp_auto = bool(cfg.get("j_recheck_amp_auto", False))
    _jrec_amp_use = _jrec_amp
    _jrec_apply = bool(cfg.get("j_recheck_apply", True))
    _jrec_alpha = float(cfg.get("j_recheck_alpha", 0.8))
    # ---- 逐 burst 异常剔除（2026-11-19）：按与滑动中位数的偏离度调 alpha ----
    #   偏离越小 alpha 越接近 _jrec_alpha；偏离越大越趋近 _jrec_amin
    #   只有被采信的估计才进入中位数历史，保证中位数本身干净
    # 平台 + 陡降 + 硬截 的自适应权重（2026-11-19 v2）
    #   基线改为指数滑动均值（每次采信即跟随），彻底避免"历史冻结→永久拒绝"的自锁
    _amed = bool(cfg.get("j_amed", False))
    _amed_d1 = float(cfg.get("j_amed_d1", 0.10))      # 平台半宽
    _amed_d2 = float(cfg.get("j_amed_d2", 0.08))      # 陡降宽度
    _amed_dmax = float(cfg.get("j_amed_dmax", 0.30))  # 硬截阈值
    _amed_abase = float(cfg.get("j_amed_abase", 0.30))  # 平滑基增益
    _amed_mu = float(cfg.get("j_amed_mu", 0.35))      # 基线滑动速率
    _amed_warm = int(cfg.get("j_amed_warm", 3))       # 预热 burst 数
    _amed_hist = []
    _amed_base = [None]
    def _amed_alpha(est):
        if not _amed:
            return _jrec_alpha
        if _amed_base[0] is None:
            _amed_base[0] = est
            return _jrec_alpha
        if len(_amed_hist) < _amed_warm:            # 预热：全速收敛
            _amed_hist.append(est)
            _amed_base[0] = est
            return _jrec_alpha
        _m = _amed_base[0]
        _d = abs(est - _m) / max(abs(_m), 1e-9)
        _s = max(_amed_d2, 1e-9)
        if _d <= _amed_d1:
            _w = 1.0
        elif _d <= _amed_dmax:
            _w = math.exp(-(_d - _amed_d1) / _s)
        else:                                   # 软底：不再归零，留恒定逃生通道
            _w = math.exp(-(_amed_dmax - _amed_d1) / _s)
        if _w > 0.0:                                # 采信：基线与历史都跟随
            _amed_base[0] = _m + _amed_mu * (est - _m)
            _amed_hist.append(est)
            if len(_amed_hist) > 15:
                _amed_hist.pop(0)
        return _amed_abase * _w
    _jrec_btau = float(cfg.get("j_recheck_btau", 0.0))   # b0 更新低通时间常数 / s，0=瞬时更新（原行为）
    _jrec_b0d = bool(cfg.get("j_b0_direct", False))      # True：直接测 b0（不经 J 中间量）
    _jrec_bgoal = None
    _jrec_win = float(cfg.get("j_recheck_win", 0.2))
    _jrec_n = max(int(round(_jrec_win / 1e-3)), 10)
    _jrec_nmin = int(cfg.get("j_recheck_nmin", 2))
    _jrec_t0 = float(cfg.get("j_recheck_t0", 1.0))
    _jrec_next = _jrec_t0
    # 周期调度：t < j_period_switch_t 用 j_recheck_period，之后改用 j_period_after
    _jpsw = float(cfg.get("j_period_switch_t", 1.0e9))
    _jpaft = float(cfg.get("j_period_after", 0.0))
    if _jpaft <= 0.0:
        _jpaft = float(cfg.get("j_recheck_period", 5.0))
    def _jnext(tk):
        return tk + (float(cfg.get("j_recheck_period", 5.0)) if tk < _jpsw else _jpaft)
    _jrec_active = False
    _jrec_end = 0.0
    _jrec_list = []
    _jrec_nid = 0
    _jrec_te_c = _jrec_te_s = _jrec_w_c = _jrec_w_s = 0.0; _jrec_iq_c = _jrec_iq_s = 0.0
    _jrec_jhat = J_M
    # 跟踪门控与冻结/回滚（实验）：gate=False 时保持旧的“每窗立即更新”行为
    _jrec_gate = bool(cfg.get("j_recheck_gate", False))
    _jrec_gate_ac = float(cfg.get("j_recheck_gate_ac", 4.0))       # rpm，预窗 LP 波动
    _jrec_gate_step = float(cfg.get("j_recheck_gate_step", 8.0))   # rpm，burst 内 LP 偏移
    _jrec_gate_pre = float(cfg.get("j_recheck_gate_pre", 0.3))     # s
    _jrec_gate_bad = max(int(cfg.get("j_recheck_gate_bad_ms", 20)), 1)
    _jrec_lp_alpha = 1.0 - math.exp(-1e-3 / 0.25)   # 0.25 s 低通，压 10 Hz 纹波
    _jrec_er_lp = 0.0
    _jrec_lp_hist = []
    _jrec_pre_mean = 0.0
    _jrec_bad_cnt = 0
    _jrec_abort = False
    _jrec_B0_pre = 0.0
    _jrec_fd_o = []
    _jrec_abort_o = []
    # 每 burst 状态4校验：0.6 s 环形窗（基线与后窗），2 s 周期内完成
    _es_nofreeze = bool(cfg.get("es_nofreeze", False))   # True：换速时不冻结 ESC（用于验证无冻结行为）
    _es_cont = bool(cfg.get("es_cont", False))          # True：连续滑动窗解调（窗内 δ̂ 每 1 ms 更新，不 hold）
    _jrec_val_on = bool(cfg.get("j_validate", False))  # 默认关闭状态4 的 burst 后校验（不回退）；b0 慢变，周期自检无需频繁
    _jrec_val_log = []      # 状态4 校验日志：(t, iq比, 幅值比, bad_iq, bad_a)
    _jrec_ring_n = 600
    _jrec_iq_ring = np.zeros(_jrec_ring_n)
    _jrec_e_ring = np.zeros(_jrec_ring_n)
    _jrec_t_ring = np.zeros(_jrec_ring_n)
    _jrec_ring_i = 0
    _jrec_ring_fill = 0
    _jrec_base_iq = float("nan")
    _jrec_base_a = float("nan")
    _jrec_val_t = 1e9
    _jrec_val_pending = False
    _jrec_val_iq0 = float("nan")
    _jrec_val_a0 = float("nan")
    _jrec_fv = n_ref / 60.0
    _jrec_jband = float(cfg.get("j_recheck_jband", 0.0))
    _jrec_jref = 0.0
    _jrec_reject = 0
    _B0e = B0 * float(cfg.get("b0_scale", 1.0))     # 纯 b0 失配实验：直接缩放控制器/ESO 的 b0
    # ---- 诊断日志（2026-11-18）：1 kHz 记录 ESO 内部量，用于内模传递函数核验 ----
    _log_eso = bool(cfg.get("log_eso", False))
    _lg = []
    # ---- 内模反演自标定 b0 辨识（2026-11-18）------------------------------------
    #   d^ = V + P(jw)E1/(jw)，  P/(jw) = b1 + j(w^2-b2)/w，  delta_b = Re(d^/U)
    #   依据：1/G = Delta/(sD) = P/s + beta3/D 且 beta3/D = V/E1（见附录 D 的 H(s)）
    _jnew = bool(cfg.get("j_b0_new", False))
    _jalt = bool(cfg.get("j_b0_alt", False))          # 双幅值差分（抗撞频）
    _jalt_r = float(cfg.get("j_b0_alt_ratio", 0.5))   # 第二档幅值比
    _tcorr = bool(cfg.get("j_b0_tcorr", False))       # 差分结果再除以 T(jw_h)
    _onoff = bool(cfg.get("j_b0_onoff", False))       # 前段不注入 + 后段注入，两段 SDFT 后差分
    _dsq = bool(cfg.get("j_dith_sq", False))          # 方波注入（基波与正弦同峰值）
    _dtri = bool(cfg.get("j_dith_tri", False))         # 三角波注入（峰值 1，基波 8/pi^2）
    # ---- 批量辨识：连续 N 个 burst 后一次性定 b0，随后长时间冻结 ----
    _jbatch = bool(cfg.get("j_b0_batch", False))
    _jbn = int(cfg.get("j_batch_n", 12))               # burst 个数
    _jbmad = float(cfg.get("j_batch_mad", 0.15))       # 相对 MAD 拒收门限
    _jbwarm = int(cfg.get("j_batch_warm", 3))          # 预热 burst 数（直接采用，不进批）
    _batch_list = []
    _batch_cnt = 0
    _blast = []                    # 最近若干 burst 的估计（冻结时取均值用）
    _bwin = int(cfg.get("j_freeze_avg_n", 4))   # 取最近几个 burst 平均（4×5s=20s）
    _jalg = bool(cfg.get("j_b0_alg", False))   # 代数法：b=(b0+d^/u)/T，T 在线测量
    _jnew_ec = _jnew_es = _jnew_vc = _jnew_vs = 0.0
    _jnew_uc = _jnew_us = _jnew_woe = 0.0
    _jnew_qc = _jnew_qs = 0.0
    _jnew_yc = _jnew_ys = 0.0
    # 精确反演：类 fal 两路增益的 SDFT（Ĝ1、Ĝ2）；线性观测器时自动退化为 E1
    _jnew_g1c = _jnew_g1s = _jnew_g2c = _jnew_g2s = 0.0
    _jnew_n = 0
    _jnew_log = []
    _jnew_bpv_log = []        # 逐窗原始估计 (t, bpv)，供与 MATLAB 的 bq 对照
    _jnew_list = []
    _jnew_pending = False
    # ---- 定稿更新律（与 b0_ident_m/C 一致）：预热·门控·中值·冻结 ----
    _jrec_b0final = bool(cfg.get("j_b0_final", False))
    # 转速门限（与 b0_ident_m 一致）：低于 on 不启动；burst 中低于 off 丢弃本次
    _jomega_on = float(cfg.get("j_omega_on", 180.0))
    _jomega_off = float(cfg.get("j_omega_off", 150.0))
    _jf_valid = False; _jf_nest = 0; _jf_base = 0.0; _jf_blast = []
    _jprev = None
    _jnew_win = 0
    _jnew_g0 = 0.0
    _jb1g = float(getattr(ESO_G1, "slope0", 1.0))   # fal 小信号斜率（z1 通道，a1=1 -> 1）
    _jb2g = float(getattr(ESO_G2, "slope0", 1.0))   # fal 小信号斜率（z2 通道，a=0.75 -> 1.778）

    if _oracle:
        _B0e *= (J_M / J_TRUE)
    _KPe = KP
    # ---- J 应用后校验 / 回退（状态 4）与死区（状态 5）（2026-11-13）----
    # 上电状态机扩展：0 空闲 / 1 辨识 / 2 已应用 / 3 超时回退 / 4 校验回退 / 5 死区保持标称。
    # 辨识完成（提前置信或 _jid_tend 超时）后：
    #   * 死区：|Jhat/J_M-1| <= j_apply_thr ⇒ 不更新 b0、冻结估计、dither 关、状态 5；
    #   * j_val=True：先采"公平基线"（dither 已关、b0 仍标称）：
    #       静默 j_val_settle（默认 0.2 s）→ 基线窗 j_base_win（0.5 s）
    #       → 施加 B0e=B0*J_M/Jhat → 等 j_val_delay（0.5 s）→ 后窗 j_val_win（0.5 s）
    #       → 比较 iq 纹波 AC-RMS 与 10 Hz 转速误差幅值，任一恶化 > j_val_tol（20%）
    #         则 B0e=B0、状态 4（回退）；否则状态 2（已应用）。
    #   * j_val=False：与旧版一致，辨识完成立即应用（状态 2，向后兼容）。
    # iq 纹波口径：1 ms 控制拍上的 iq 采样，先减窗均值再取 RMS（AC-RMS）；
    #   10 Hz 幅值：同一窗内对 (y-1)*600 rpm 做正交解调。
    _j_val_on = bool(cfg.get("j_val", _j_adapt_b0)) and _jid_on0
    _j_apply_thr = float(cfg.get("j_apply_thr", 0.20))     # 死区：|Jhat/J_M-1| 阈值
    _j_val_settle = float(cfg.get("j_val_settle", 0.2))    # 辨识结束→基线窗的静默期（s）
    _j_base_win = float(cfg.get("j_base_win", 0.5))        # 基线窗长（s）
    _j_val_delay = float(cfg.get("j_val_delay", 0.5))      # 施加→后窗的等待（s）
    _j_val_win = float(cfg.get("j_val_win", 0.5))          # 后窗长（s）
    _j_val_tol = float(cfg.get("j_val_tol", 0.20))         # 恶化容限（0.20 = 20%）
    # 10 Hz 比值只在基线幅值足够大时才有判别力（否则 0.3 rpm 级的噪声会让比值乱跳）；
    # 低于该下限时只用 iq 纹波判据。这是测量口径，不是放宽判据。
    _j_val_a10_floor = float(cfg.get("j_val_a10_floor", 2.0))
    _jv_w10 = TWO_PI * 10.0
    _jv_phase = 0          # 0 未启动 / 1 基线静默 / 2 基线窗 / 3 应用后等待 / 4 后窗 / 5 完成
    _jv_iq1 = _jv_iq2 = _jv_c = _jv_s = 0.0
    _jv_n = 0; _jv_pk = 0.0
    _jv_s1 = _jv_s2 = _jv_sc = _jv_ss = 0.0; _jv_sn = 0; _jv_pks = 0.0
    _jv_tdec = None; _jv_tfinal = None
    _jv_tbase0 = _jv_tbase1 = _jv_tapply = 0.0
    _jv_rho = float("nan"); _jv_B0e = _B0e
    _jv_base = _jv_settle = _jv_post = _jv_merged = _jv_ratios = None
    _jv_applied = False; _jv_rollback = False; _jv_decision = None
    _jv_guard_pk = 0.0
    _jfin_evt = False
    _te_c = _te_s = _w_c = _w_s = 0.0
    _nid = 0
    jhat_o = []
    b0e_o = []

    def _jv_stats(s1, s2, sc, ss, n, pk, t0, t1):
        """窗统计：iq 均值/AC-RMS/峰值 + 10 Hz 转速误差幅值（rpm）。"""
        if n <= 0:
            return dict(n=0, iq_mean=0.0, iq_rms=0.0, a10=0.0, iq_pk=float(pk),
                        t0=float(t0), t1=float(t1))
        mu = s1 / n
        rms = math.sqrt(max(s2 / n - mu * mu, 0.0))
        a10 = 2.0 / n * math.hypot(sc, ss)
        return dict(n=int(n), iq_mean=float(mu), iq_rms=float(rms), a10=float(a10),
                    iq_pk=float(pk), t0=float(t0), t1=float(t1))

    BETA3 = cfg.get("beta3", 2000.0); TAU0 = cfg.get("tau0", 20e-3)
    Q0 = cfg.get("Q0", 0.98); ZETA = float(cfg.get("zeta_inj", 0.2))   # 注入 tanh 的线性区宽度
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
    _T_dft = float(cfg.get("T_dft", 0.0))        # >0：改用整数机械周期 DFT 取基波幅值（单位 = 周期数），带通仍在跑但 A 被覆盖
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
    _tflt_rev = float(_tflt["rev"]) if (_tflt and "rev" in _tflt) else None
    _tflt_rev_done = False
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
    _inj_now = 0.0
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
    # es_cont：连续滑动窗（窗长 N·P_d），δ̂ 每 1 ms 按 (σ/T_win)·sgn(I) 更新
    _es_win_s = max(es_N * es_Pd, 1e-3)
    _es_ring_n = max(int(round(_es_win_s / 1e-3)), 10)
    _es_ring = np.zeros(_es_ring_n); _es_ring_p = 0; _es_ring_fill = 0; _es_acc = 0.0
    _es_tfreeze = 0.0; _es_n = 0; _Tgnow = T; _Tgprev = None; _Tglp = T
    bp_acc = 0.0; bp_buf = np.zeros(nd); bp_p = 0; _A_now = 0.0; _b3_now = BETA3
    _dft_q = []                                   # T_dft：最近 N 个 (x·cosθ, x·sinθ)
    _dft_N = 0
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
    inj_o = np.zeros(no)                      # 注入分量（含波形），供三波对比""
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
            _p = _tflt.get("parallel")
            if _p:
                _tlf += parallel_torque(_phimf, w, **_p)
            if _tflt_rev is not None and (not _tflt_rev_done) and (k * dt >= _tflt_rev):
                _tflt_rev_done = True
            if _tflt_rev_done:
                _tlf = -_tlf
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
        if k * dt >= _J_STEP_T:
            _Jt = _J_STEP_V
        w += dt * (Te - _tl_tot) / _Jt  # 主循环用真实 J；B0 仍由 J_M 标称

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
            if (_jrec_btau > 0.0) and (_jrec_bgoal is not None):   # b0 无扰切换：一阶低通逼近目标
                _ba = 1.0 - math.exp(-1e-3 / max(_jrec_btau, 1e-6))
                _B0e += _ba * (_jrec_bgoal - _B0e)
                if abs(_jrec_bgoal - _B0e) <= 1e-4 * max(abs(_jrec_bgoal), 1.0):
                    _B0e = _jrec_bgoal
                    _jrec_bgoal = None
            e1 = y_m - z1
            # g 门控：e1 的 T 窗均值
            e1g_acc += e1 * 1e-3 - e1g_buf[e1g_p]; e1g_buf[e1g_p] = e1 * 1e-3
            e1g_p = (e1g_p + 1) % nd
            e1m = e1g_acc / T
            eps_g = det_eps if det_eps > 0.0 else 0.01
            g = (e1m * e1m) / (e1m * e1m + eps_g * eps_g)
            if _jnew and _jrec_active:   # 辨识窗内冻结律D 门控：保证窗内 LTI（否则 woe 变化使 1/G 无定义）
                g = _jnew_g0
            _gp = g ** kp_gpow if kp_gpow != 1.0 else g   # 律D 门控形状（2026-11-11）
            kpe = _KPe * (1.0 + kp_boost * _gp)
            _g1 = ESO_G1(e1); _g2 = ESO_G2(e1)       # 线性档 G(e)=e（逐位不变）
            _woe = WO * (1.0 + kb_eso * g) if kb_eso > 0.0 else WO
            z1n = z1 + 1e-3 * (z2 + _B0e * u + v + 2.0 * _woe * _g1)
            z2n = z2 + 1e-3 * (_woe * _woe * _g2)
            if _log_eso:   # tk, e1, v, z2, u(本步所用,含上一拍 dither), B0e, woe
                _lg.append((k * dt, e1, v, z2, u, _B0e, _woe))
            if _jnew and _jrec_active:   # 内模反演：在本步所用 (e1,v,u) 上同步解调
                _jph = _jrec_w * (k * dt)
                _jc = math.cos(_jph); _js = math.sin(_jph)
                _jnew_ec += e1 * _jc; _jnew_es += e1 * _js
                _jnew_vc += v * _jc;  _jnew_vs += v * _js
                _jnew_uc += u * _jc;  _jnew_us += u * _js
                _jnew_qc += idq[1] * _jc; _jnew_qs += idq[1] * _js
                _jnew_yc += y_m * _jc;    _jnew_ys += y_m * _js
                _g1v = ESO_G1(e1); _g2v = ESO_G2(e1)     # 类 fal 增益输出（精确反演用）
                _jnew_g1c += _g1v * _jc; _jnew_g1s += _g1v * _js
                _jnew_g2c += _g2v * _jc; _jnew_g2s += _g2v * _js
                _jnew_woe += _woe; _jnew_n += 1
                if _jnew_n >= _jrec_n:
                    _nn = float(_jnew_n)
                    _E = complex(2.0 * _jnew_ec / _nn, -2.0 * _jnew_es / _nn)
                    _V = complex(2.0 * _jnew_vc / _nn, -2.0 * _jnew_vs / _nn)
                    _U = complex(2.0 * _jnew_uc / _nn, -2.0 * _jnew_us / _nn)
                    _QC = complex(2.0 * _jnew_qc / _nn, -2.0 * _jnew_qs / _nn)
                    _Yc = complex(2.0 * _jnew_yc / _nn, -2.0 * _jnew_ys / _nn)
                    _wm = _jnew_woe / _nn
                    _b1n = 2.0 * _wm * _jb1g
                    _b2n = _wm * _wm * _jb2g
                    # 观测器按 1 ms 显式欧拉离散（beta1*dt≈1），必须用离散算子
                    #   s_d = (e^{j w dt} - 1)/dt，否则 65 Hz 处实部差 ~82 rad/s
                    _sd = complex(math.cos(_jrec_w * 1e-3) - 1.0,
                                  math.sin(_jrec_w * 1e-3)) / 1e-3
                    _pq = (_sd * _sd + _b1n * _sd + _b2n) / _sd   # 线性化口径（保留：对照用）
                    # 精确口径：β1·Ĝ1 + β2/Sd·Ĝ2，线性观测器时 Ĝ=E1，与 _pq 完全相同
                    _G1 = complex(2.0 * _jnew_g1c / _nn, -2.0 * _jnew_g1s / _nn)
                    _G2 = complex(2.0 * _jnew_g2c / _nn, -2.0 * _jnew_g2s / _nn)
                    if abs(_U) > 1e-6:
                        _Tc = (_QC / I_BASE) / _U    # 电流环在 w_h 的复传函（标幺 iq/u）
                        # d^ = V + Sd·E1 + β1·Ĝ1 + (β2/Sd)·Ĝ2（精确恒等式）
                        _dd = _V + _sd * _E + (2.0 * _wm) * _G1 + ((_wm * _wm) / _sd) * _G2
                        if _jalg and abs(_Tc) > 1e-3:
                            # 单窗代数解：b0 + d^/u = b*T  =>  b = (b0 + d^/u)/T
                            _bhat = ((_B0e + _dd / _U) / _Tc).real
                            _btn = min(max(_bhat, 0.02 * B0), 2.4 * B0)
                        else:
                            _btn = min(max(_B0e + (_dd / _U).real, 0.02 * B0), 2.4 * B0)
                        # 实测电流差分（无 T）： d = f + b*It - b0*u
                        #   => d2 - d1 = b*(It2-It1) - b0*(u2-u1)
                        #   => b = [ (d2-d1) + b0*(u2-u1) ] / (It2-It1)
                        _QCp = _QC / I_BASE
                        _bpv = 0.0
                        if _onoff:
                            # 前后两段各自 SDFT，段末取均值后做差
                            if _jnew_win == 0:
                                _jprev = (_dd, _U, _Tc, _B0e, _QCp)
                            elif _jprev is not None:
                                _d1, _U1, _T1, _b1, _Q1 = _jprev
                                if abs(_QCp - _Q1) > 1e-6:
                                    # 定稿口径：取模长（不是实部），免相位折扣；T 修正默认关
                                    _bpv = abs(((_dd - _d1) + _b1 * (_U - _U1))
                                               / (_QCp - _Q1))
                                    _bpv = min(max(_bpv, 0.02 * B0), 2.4 * B0)
                                    _jnew_bpv_log.append((k * dt, _bpv))
                        elif _jalt and (_jprev is not None):
                            _d1, _U1, _T1, _b1, _Q1 = _jprev
                            if abs(_QCp - _Q1) > 1e-6:
                                _bpv = abs(((_dd - _d1) + _b1 * (_U - _U1))
                                           / (_QCp - _Q1))
                                if _tcorr:
                                    _Tp = 0.5 * (_T1 + _Tc)   # 两窗电流环传函均值
                                    if abs(_Tp) > 1e-6:
                                        _bpv = (_bpv / _Tp).real
                                _bpv = min(max(_bpv, 0.02 * B0), 2.4 * B0)
                        if not _onoff:
                            _jprev = (_dd, _U, _Tc, _B0e, _QCp)
                        if _onoff:
                            if abs(_bpv) > 1e-9:      # 仅注入段末尾的差分有效
                                _jnew_list.append(_bpv)
                        else:
                            _jnew_list.append(_bpv if abs(_bpv) > 1e-9 else _btn)
                        _jnew_log.append((k * dt, _B0e, _btn, abs(_U), abs(_Tc), _bpv, abs(_Yc)))
                        _jnew_win += 1
                    _jnew_ec = _jnew_es = _jnew_vc = _jnew_vs = 0.0
                    _jnew_uc = _jnew_us = _jnew_qc = _jnew_qs = 0.0
                    _jnew_yc = _jnew_ys = 0.0
                    _jnew_g1c = _jnew_g1s = _jnew_g2c = _jnew_g2s = 0.0
                    _jnew_woe = 0.0; _jnew_n = 0
            if _jnew and _jnew_pending and (not _jrec_active):
                # burst 结束：用窗均值一次性更新（窗内不动 b0，避免更新本身污染测量）
                _jnew_pending = False
                _nmin_eff = 1 if _onoff else _jrec_nmin
                if _jrec_apply and (not _jrec_abort) and len(_jnew_list) >= _nmin_eff:
                    if _jbatch:
                        _bt0 = sum(_jnew_list) / len(_jnew_list)
                        _jnew_list = []
                        _batch_cnt += 1
                        if _batch_cnt <= _jbwarm:        # 预热段：立即采用
                            if _jrec_btau > 0.0:
                                _jrec_bgoal = _bt0
                            else:
                                _B0e = _bt0
                            _jnew_log.append((k * dt, _B0e, _bt0, -3.0, 0.0, 0.0, 0.0))
                            continue
                        _batch_list.append(_bt0)         # 批量段：只收集
                        if _batch_cnt >= _jbn:
                            _bs = sorted(_batch_list)
                            _n = len(_bs)
                            _mdn = float(_bs[_n // 2])
                            _nk = int(_n * 0.2)              # 双边各去 20%
                            _core = _bs[_nk:_n - _nk] if (_n - 2 * _nk) >= 3 else _bs
                            _mean = sum(_bs) / _n
                            _bm = sum(_core) / len(_core)    # 截尾平均
                            _mad = float(sorted(abs(x - _bm) for x in _bs)[_n // 2])
                            _rel = _mad / max(abs(_bm), 1e-9)
                            _jnew_log.append((k * dt, _B0e, _bm, -2.0, _rel,
                                              _mean, _mdn))
                            if _rel <= _jbmad:          # 通过一致性检验才采用
                                if _jrec_btau > 0.0:
                                    _jrec_bgoal = _bm
                                else:
                                    _B0e = _bm
                            _jrec_next = 1.0e9           # 之后不再辨识
                        continue
                    _btm = sum(_jnew_list) / len(_jnew_list)
                    _blast.append(_btm)
                    if len(_blast) > _bwin:
                        _blast.pop(0)
                    _jnew_log.append((k * dt, _B0e, _btm, -1.0, 0.0, 0.0, 0.0))
                    # 本 burst 若是辨识窗口内最后一个，冻结为最近若干 burst 的均值
                    if _tk >= _jpsw - float(cfg.get("j_recheck_period", 5.0)):
                        _B0e = sum(_blast) / len(_blast)
                        _jrec_bgoal = None
                    if _jrec_b0final:
                        # ===== 定稿更新律（b0_ident_m 的等价实现）=====
                        _bq = min(max(_btm, float(cfg.get("j_b0_lo", 0.5 * B0))),
                                  float(cfg.get("j_b0_hi", 2.0 * B0)))  # 限幅（可配）
                        if not _jf_valid:                             # 首次：经低通
                            _jf_base = _bq; _jf_valid = True
                            _jrec_bgoal = _bq; _jf_nest = 1
                        elif _jf_nest < 3:                            # 预热：经低通
                            _jf_base = _bq; _jrec_bgoal = _bq; _jf_nest += 1
                        else:                                         # 平台 + 软底门控
                            _dd = abs(_bq - _jf_base) / max(abs(_jf_base), 1e-9)
                            if _dd <= 0.10:
                                _wg = 1.0
                            elif _dd <= 0.50:
                                _wg = math.exp(-(_dd - 0.10) / 0.20)
                            else:
                                _wg = math.exp(-(0.50 - 0.10) / 0.20)
                            _al = 0.30 * _wg
                            _jrec_bgoal = _B0e + _al * (_bq - _B0e)
                            _jf_base += 0.35 * (_bq - _jf_base)       # 基线滑动
                            _jf_nest += 1
                        _jf_blast.append(_bq)
                        if len(_jf_blast) > 4:
                            _jf_blast.pop(0)
                        if _jf_nest >= 24:                            # 冻结：末 4 次均值
                            _B0e = sum(_jf_blast) / len(_jf_blast)
                            _jrec_bgoal = None
                            _jrec_next = 1.0e9
                    elif _jrec_btau > 0.0:
                        _jrec_bgoal = _B0e + _amed_alpha(_btm) * (_btm - _B0e)
                    else:
                        _B0e += _amed_alpha(_btm) * (_btm - _B0e)
                _jnew_list = []
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
                if _T_dft > 0.0:
                    # 整数机械周期 DFT（机械角为相位基准，等价 1× 锁相）：
                    #   A = sqrt(2)/N * |sum x[k-i] exp(-j*theta_m[k-i])|，N = m*T/1ms
                    _Nnew = int(round(_T_dft * (TWO_PI / max(abs(_wT), 1e-6)) / 1e-3))
                    _Nnew = max(8, min(2000, _Nnew))
                    if (_dft_N == 0) or (abs(_Nnew - _dft_N) > max(2, int(0.05 * _dft_N))):
                        _dft_N = _Nnew; _dft_q = []
                    _thm = th / P_POL
                    _xv = e1 if rc_src == "e1" else (1.0 - y_m)
                    _dft_q.append((_xv * math.cos(_thm), _xv * math.sin(_thm)))
                    if len(_dft_q) > _dft_N:
                        _dft_q.pop(0)
                    if len(_dft_q) >= _dft_N:
                        _dft_c = 0.0; _dft_s = 0.0
                        for _pq in _dft_q:
                            _dft_c += _pq[0]; _dft_s += _pq[1]
                        _A_now = math.sqrt(2.0) * math.hypot(_dft_c, _dft_s) / len(_dft_q)
                if T_es:
                    # 换速冻结：标称周期相对 20 ms 低通偏离 >5% 时暂停搜索并清空累加器
                    _al = 1.0 - math.exp(-1e-3 / 0.02)
                    if (not _es_nofreeze) and abs(_Tgnow - _Tglp) > 0.05 * _Tglp:
                        _es_tfreeze = k * dt + es_freeze
                        _es_I = 0.0
                        _es_tnext = k * dt + es_freeze + es_N * es_Pd
                        _es_ring[:] = 0.0; _es_ring_p = 0; _es_ring_fill = 0; _es_acc = 0.0
                    _Tglp += _al * (_Tgnow - _Tglp)
                    _Tgprev = _Tgnow
                    if es_ff and (k * dt < _es_tfreeze):
                        # 冻结期间用理论值 δ*=-arctan(ωτ)/2π 跟踪新转速
                        _dff = -math.atan(max(_wT, 1e-6) * TAU0) / (2.0 * math.pi)
                        _es_dh = max(-es_dmax, min(es_dmax, _dff))
                    if (k * dt >= es_t0) and (k * dt >= _es_tfreeze):
                        if _es_cont:
                            # 连续滑动窗（§15 连续版本）：δ̂ 每 1 ms 更新，窗内不 hold
                            #   I = 2/T_win ∫_{t-T_win}^{t} A sin(ω_d τ) dτ（不满窗不动）
                            _ev = _A_now * math.sin(_es_ph) * 1e-3
                            _old = _es_ring[_es_ring_p]
                            _es_ring[_es_ring_p] = _ev
                            _es_ring_p = (_es_ring_p + 1) % _es_ring_n
                            _es_acc += _ev - _old
                            if _es_ring_fill < _es_ring_n:
                                _es_ring_fill += 1
                            if _es_ring_fill >= _es_ring_n:
                                _Ibar = 2.0 * _es_acc / _es_win_s
                                if abs(_Ibar) > es_dead:
                                    _es_dh = max(-es_dmax, min(es_dmax,
                                               _es_dh - (es_step / _es_win_s) * 1e-3 *
                                               (1.0 if _Ibar > 0 else -1.0)))
                                _es_n += 1
                        else:
                            # 锁相解调：I = 2/(N·P_d) ∫ A·sin(ω_d t) dt，窗边界更新（hold）
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
            _tk = k * dt
            _inj_now = 0.0
            _fb = (_yref - z1n) if u_z1 else (_yref - y_m)
            u = (kpe * _fb - z2n - vn) / _B0e
            # ---- ESO/DO 在线 J 辨识（实验）：DO 估 T_L，梯度更新 J，慢更新 b0 ----
            if _jdo_on and _tk > 0.2:
                _wdot = (w_enc - _jdo_wprev) / 1e-3
                _a = 1.0 - math.exp(-1e-3 / _jdo_lpf)
                _jdo_wdotf += _a * (_wdot - _jdo_wdotf)
                _jdo_TL += _a * (Te - _jdo_J * _jdo_wdotf - _jdo_TL)
                _eJ = Te - _jdo_TL - _jdo_J * _jdo_wdotf
                _jdo_J += _jdo_gamma * 1e-3 * _jdo_wdotf * _eJ
                _jdo_J = min(max(_jdo_J, 0.5 * J_M), 50.0 * J_M)
                _jhat = _jdo_J
                _B0e += (1e-3 / _jdo_tau) * (B0 * (J_M / _jdo_J) - _B0e)
            _jdo_wprev = w_enc
            # ---- Yang 2018 AKO-RLS：3 状态 KF（theta,w,TL）+ RLS（a1,b1）----
            if _ako_on and _tk > 0.1:
                _theta_m = (cnt % ENC_CPR) / ENC_CPR * TWO_PI
                if _ako_first:
                    _ako_th_unw = _theta_m; _ako_th_prev = _theta_m
                    _ako_X = np.array([_theta_m, 0.0, 0.0]); _ako_first = False
                _dth = _theta_m - _ako_th_prev
                if _dth > math.pi: _dth -= TWO_PI
                elif _dth < -math.pi: _dth += TWO_PI
                _ako_th_unw += _dth; _ako_th_prev = _theta_m
                _Jk = _ako_J
                _A = np.array([[1.0, 1e-3, 0.0], [0.0, 1.0, -1e-3 / _Jk], [0.0, 0.0, 1.0]])
                _Bv = np.array([0.0, 1e-3 / _Jk, 0.0])
                _Xp = _A @ _ako_X + _Bv * Te
                _Pp = _A @ _ako_P @ _A.T + _ako_Q
                _S = _Pp[0, 0] + _ako_R
                _K = _Pp[:, 0] / _S
                _V = _ako_th_unw - _Xp[0]
                _ako_X = _Xp + _K * _V
                _ako_P = _Pp - np.outer(_K, _Pp[0, :])
                if _V * _V >= _ako_ethr:
                    _ako_Q = _ako_Q * (1.0 + _ako_rho)
                else:
                    _ako_Q = _ako_Q * (1.0 - _ako_rho)
                _ako_Q = np.diag(np.clip(np.diag(_ako_Q), 1e-9, 1e2))
                _tau_r = np.array([-_ako_w_prev, _ako_Te_prev - _ako_TL_prev])
                _psi_tau = _ako_psi @ _tau_r
                _eta = _psi_tau / (_ako_lam + _tau_r @ _psi_tau)
                _er = _ako_X[1] - _ako_sigma @ _tau_r
                _ako_sigma = _ako_sigma + _eta * _er
                _ako_psi = (_ako_psi - np.outer(_eta, _psi_tau)) / _ako_lam
                _a1, _b1 = _ako_sigma
                _Jnew = J_M
                if _b1 > 1e-12 and _a1 < 0.0:
                    _Bh = (1.0 + _a1) / _b1
                    if abs(_Bh) > 1e-9:
                        _Jnew = -_Bh * 1e-3 / math.log(-_a1)
                    else:
                        _Jnew = 1e-3 / _b1
                _Jnew = min(max(_Jnew, 0.5 * J_M), 50.0 * J_M)
                if _V * _V <= _ako_ethr:
                    _ako_J = 0.999 * _ako_J + 0.001 * _Jnew
                    _ako_w_prev = _ako_X[1]
                    _ako_TL_prev = _ako_X[2]
                    _ako_Te_prev = Te
                    _jhat = _ako_J
                    _B0e += (1e-3 / 0.5) * (B0 * (J_M / _ako_J) - _B0e)
            # ---- 周期 dither 复检：每 period 开 len 秒 dither，DFT 更新 b0 ----
            if _jrec:
                _jrec_iq_ring[_jrec_ring_i] = idq[1]
                _jrec_e_ring[_jrec_ring_i] = (y_m - 1.0) * n_ref
                _jrec_t_ring[_jrec_ring_i] = _tk
                _jrec_ring_i = (_jrec_ring_i + 1) % _jrec_ring_n
                if _jrec_ring_fill < _jrec_ring_n:
                    _jrec_ring_fill += 1
                if _jrec_gate:
                    _er = _fb * n_ref
                    _jrec_er_lp += _jrec_lp_alpha * (_er - _jrec_er_lp)
                    _jrec_lp_hist.append(_jrec_er_lp)
                    _pre_need = int(round(_jrec_gate_pre / 1e-3))
                    if len(_jrec_lp_hist) > _pre_need:
                        _jrec_lp_hist.pop(0)
                _jwrpm_now = abs(w_enc) * 30.0 / math.pi
                _jspd_ok = (_jomega_on <= 0.0) or (_jwrpm_now >= _jomega_on)
                if (not _jrec_active) and _tk >= _jrec_next and _jspd_ok:
                    _pre_need = int(round(_jrec_gate_pre / 1e-3))
                    _pre_ok = (not _jrec_gate) or (len(_jrec_lp_hist) >= _pre_need and
                                                   (max(_jrec_lp_hist) - min(_jrec_lp_hist)) <= _jrec_gate_ac)
                    if not _pre_ok:
                        _jrec_next = _jnext(_tk)
                        _jstate = 6
                        _jrec_abort_o.append((_tk, 1.0))
                    else:
                        _jrec_active = True
                        _jrec_end = _tk + _jrec_len
                        _jrec_next = _jnext(_tk)
                        _jrec_list = []; _jrec_nid = 0
                        _jnew_list = []; _jnew_pending = True; _jnew_g0 = g
                        _jprev = None; _jnew_win = 0
                        _jrec_te_c = _jrec_te_s = _jrec_w_c = _jrec_w_s = 0.0; _jrec_iq_c = _jrec_iq_s = 0.0
                        _jrec_B0_pre = _B0e
                        _jrec_abort = False
                        _jrec_bad_cnt = 0
                        _jrec_val_pending = False
                        _jrec_pre_mean = (sum(_jrec_lp_hist) / len(_jrec_lp_hist)) if _jrec_gate else 0.0
                        if _jrec_ring_fill >= _jrec_ring_n:
                            _mi = float(np.mean(_jrec_iq_ring))
                            _jrec_base_iq = float(np.sqrt(np.mean((_jrec_iq_ring - _mi) ** 2)))
                            _phb = 2.0 * math.pi * _jrec_fv * _jrec_t_ring
                            _jrec_base_a = float(2.0 / _jrec_ring_n * np.hypot(
                                np.sum(_jrec_e_ring * np.cos(_phb)), np.sum(_jrec_e_ring * np.sin(_phb))))
                        else:
                            _jrec_base_iq = float("nan"); _jrec_base_a = float("nan")
                        if _jrec_f_auto:
                            # ---- 三约束选频（2026-11-19）----
                            #   下界: 速度环衰减 3kp/2pi、谐波余量 2.5*f_rot、配置下限
                            #   上界: ESO 带宽 wo/2pi、电流环 0.2*fci、配置上限
                            #   栅格: 5 Hz（= 1/窗长），保证严格相干；避开整数倍谐波，优先半整数
                            _fv = max(n_ref / 60.0, 1e-3)
                            _lo = max(3.0 * KP / TWO_PI, 2.5 * _fv, _jrec_f_min)
                            _hi = min(WO / TWO_PI, 0.2 * float(cfg.get("fci", 500.0)),
                                      _jrec_f_max)
                            _tg = (_jrec_f_q + _jrec_f_alpha) * _fv
                            _best = None
                            _nk = int(math.floor(_lo / _jrec_f_grid))
                            while _nk * _jrec_f_grid <= _hi + 1e-9:
                                _c = _nk * _jrec_f_grid
                                if _c >= _lo - 1e-9:
                                    _rt = _c / _fv
                                    if abs(_rt - round(_rt)) > 0.10:
                                        _pen = abs(_c - _tg)
                                        if abs(_rt - round(_rt) - 0.5) > 0.12:
                                            _pen += _jrec_f_grid
                                        if (_best is None) or (_pen < _best[0]):
                                            _best = (_pen, _c)
                                _nk += 1
                            _jrec_fd = _best[1] if (_best is not None) else min(max(_tg, _lo), _hi)
                        else:
                            _jrec_fd = _jrec_f
                        _jrec_w = 2.0 * math.pi * _jrec_fd
                        _jrec_amp_use = _jrec_amp * (max(1.0, _jrec_fd / 100.0) if _jrec_amp_auto else 1.0)
                        # 纹波预算（可选）：u_d <= R*w/(600*b_nom)，需给出名义物理增益
                        _bnom = float(cfg.get("j_recheck_b_nom", 0.0))
                        _rbud = float(cfg.get("j_recheck_rpm_budget", 0.0))
                        if (_bnom > 0.0) and (_rbud > 0.0):
                            _jrec_amp_use = min(_jrec_amp_use, _rbud * _jrec_w / (600.0 * _bnom))
                        _jrec_fd_o.append((_tk, _jrec_fd))
                        _jstate = 1
                if _jrec_active:
                    # burst 中掉速到 off 以下：丢弃本次（窗口已被污染）
                    if (_jomega_off > 0.0) and (abs(w_enc) * 30.0 / math.pi < _jomega_off):
                        _jrec_active = False; _jrec_abort = True
                        _jrec_list = []; _jnew_list = []
                        _jstate = 3
                    if _jrec_active and _jrec_gate:
                        if abs(_jrec_er_lp - _jrec_pre_mean) > _jrec_gate_step:
                            _jrec_bad_cnt += 1
                        else:
                            _jrec_bad_cnt = 0
                        if _jrec_bad_cnt >= _jrec_gate_bad:
                            _jrec_abort = True
                            _jrec_active = False
                            _B0e = _jrec_B0_pre; _jrec_bgoal = None
                            _jstate = 6
                            _jrec_list = []
                            _jrec_abort_o.append((_tk, 1.0))
                    if _jrec_active and _tk < _jrec_end:
                        _ph = _jrec_w * _tk
                        if _onoff:
                            _jampf = 0.0 if (_jnew_win == 0) else 1.0   # 前段不注入
                        else:
                            _jampf = _jalt_r if (_jalt and (_jnew_win % 2 == 1)) else 1.0
                        if _dsq:
                            _dsv = 1.0 if math.sin(_ph) >= 0.0 else -1.0
                        elif _dtri:
                            _dsv = (2.0 / math.pi) * math.asin(math.sin(_ph))
                        else:
                            _dsv = math.sin(_ph)
                        _inj_now = _jrec_amp_use * _jampf * _dsv
                        u += _inj_now
                        _jrec_te_c += Te * math.cos(_ph); _jrec_te_s += Te * math.sin(_ph)
                        _jrec_w_c += w_enc * math.cos(_ph); _jrec_w_s += w_enc * math.sin(_ph)
                        _jrec_iq_c += idq[1] * math.cos(_ph); _jrec_iq_s += idq[1] * math.sin(_ph)
                        _jrec_nid += 1
                        if _jrec_nid >= _jrec_n:
                            _ate = 2.0 / _jrec_nid * math.hypot(_jrec_te_c, _jrec_te_s)
                            _aw = 2.0 / _jrec_nid * math.hypot(_jrec_w_c, _jrec_w_s)
                            _snr = _aw * 60.0 / (2.0 * math.pi)
                            if _aw > 1e-9 and _snr >= 2.0:
                                if _jrec_b0d:
                                    # 直接测 b0：b0 = 1.2·ω_d·A_ω·I_base/(A_iq·ω_ref)
                                    # A_iq 取实测 q 轴电流的 dither 幅值（含电流环/速度环反作用），不经 J、k_t
                                    _aiq = 2.0 / _jrec_nid * math.hypot(_jrec_iq_c, _jrec_iq_s)
                                    _jn = 1.2 * (_jrec_w * _aw * I_BASE) / max(_aiq * w_ref, 1e-12)
                                    _jn = min(max(_jn, 0.02 * B0), 2.4 * B0)
                                else:
                                    _jn = _ate / (_jrec_w * _aw)
                                    _jn = min(max(_jn, 0.5 * J_M), 50.0 * J_M)
                                _jrec_list.append(_jn)
                                if (not _jrec_gate) and len(_jrec_list) >= _jrec_nmin:
                                    _jrec_jhat = sum(_jrec_list) / len(_jrec_list)
                                    _jhat = (J_M * B0 / _jrec_jhat) if _jrec_b0d else _jrec_jhat
                                    if _jrec_apply and (not _jnew):
                                        _bt = _jrec_jhat if _jrec_b0d else B0 * (J_M / _jrec_jhat)
                                        if _jrec_btau > 0.0:
                                            _jrec_bgoal = _B0e + _amed_alpha(_bt) * (_bt - _B0e)
                                        else:
                                            _B0e += _amed_alpha(_bt) * (_bt - _B0e)
                            _jrec_te_c = _jrec_te_s = _jrec_w_c = _jrec_w_s = 0.0; _jrec_iq_c = _jrec_iq_s = 0.0
                            _jrec_nid = 0
                    elif _jrec_active and _tk >= _jrec_end:
                        _jrec_active = False
                        if _jrec_gate:
                            if (not _jrec_abort) and len(_jrec_list) >= _jrec_nmin:
                                _jn = sum(_jrec_list) / len(_jrec_list)
                                if (_jrec_jband > 0.0) and (_jrec_jref > 0.0) and (abs(_jn / _jrec_jref - 1.0) > _jrec_jband):
                                    _B0e = _jrec_B0_pre; _jrec_bgoal = None
                                    _jstate = 3
                                    _jrec_reject += 1
                                else:
                                    if _jrec_jref <= 0.0:
                                        _jrec_jref = _jn
                                    _jrec_jhat = _jn
                                    _jhat = (J_M * B0 / _jrec_jhat) if _jrec_b0d else _jrec_jhat
                                    if _jrec_apply and (not _jnew):
                                        _bt = _jrec_jhat if _jrec_b0d else B0 * (J_M / _jrec_jhat)
                                        if _jrec_btau > 0.0:
                                            _jrec_bgoal = _B0e + _amed_alpha(_bt) * (_bt - _B0e)
                                        else:
                                            _B0e += _amed_alpha(_bt) * (_bt - _B0e)
                                    _jstate = 2
                                    _jrec_val_pending = True
                                    _jrec_val_t = _tk + 0.7
                                    _jrec_val_iq0 = _jrec_base_iq
                                    _jrec_val_a0 = _jrec_base_a
                            else:
                                _B0e = _jrec_B0_pre; _jrec_bgoal = None
                                _jstate = 3 if not _jrec_abort else 6
                            _jrec_abort_o.append((_tk, 0.0 if not _jrec_abort else 1.0))
                        else:
                            _jstate = 2 if len(_jrec_list) >= _jrec_nmin else 3
            # ---- 每 burst 状态4校验：burst 后 0.7 s 比较 iq AC-RMS 与故障频率幅值 ----
            if _jrec and _jrec_val_pending and (not _jrec_active) and _tk >= _jrec_val_t:
                _jrec_val_pending = False
                if not _jrec_val_on:
                    _jstate = 2                      # 校验关闭：直接接受，不回退
                elif _jrec_ring_fill >= _jrec_ring_n:
                    _mi = float(np.mean(_jrec_iq_ring))
                    _piq = float(np.sqrt(np.mean((_jrec_iq_ring - _mi) ** 2)))
                    _php = 2.0 * math.pi * _jrec_fv * _jrec_t_ring
                    _pa = float(2.0 / _jrec_ring_n * np.hypot(
                        np.sum(_jrec_e_ring * np.cos(_php)), np.sum(_jrec_e_ring * np.sin(_php))))
                    _bad_iq = (_jrec_val_iq0 == _jrec_val_iq0) and (_jrec_val_iq0 > 0.0) and (_piq / _jrec_val_iq0 > 1.20)
                    _bad_a = (_jrec_val_a0 == _jrec_val_a0) and (_jrec_val_a0 >= 2.0) and (_pa / _jrec_val_a0 > 1.20)
                    _jrec_val_log.append((float(_tk),
                                          float(_piq / _jrec_val_iq0) if _jrec_val_iq0 > 0 else -1.0,
                                          float(_pa / _jrec_val_a0) if _jrec_val_a0 >= 2.0 else -1.0,
                                          int(_bad_iq), int(_bad_a)))
                    if _bad_iq or _bad_a:
                        _B0e = _jrec_B0_pre; _jrec_bgoal = None
                        _jstate = 4
                    else:
                        _jstate = 2
            if _jid:
                if _tk >= _jid_tend:                 # 超时：有有效窗则进入应用/校验，否则回退
                    _jid = False
                    if _jlist:
                        _jhat = sum(_jlist) / len(_jlist)
                        _jfin_evt = True
                    else:
                        _jstate = 3                  # 超时无有效窗：保持标称 b0
                elif _tk >= _jid_t0:
                    _ph = _jid_w * _tk
                    u += _jid_amp * math.sin(_ph)
                    _te_c += Te * math.cos(_ph); _te_s += Te * math.sin(_ph)
                    _w_c += w_enc * math.cos(_ph); _w_s += w_enc * math.sin(_ph)
                    _nid += 1
                    if _nid >= _jid_n:
                        _ate = 2.0 / _nid * math.hypot(_te_c, _te_s)
                        _aw = 2.0 / _nid * math.hypot(_w_c, _w_s)
                        _snr_rpm = _aw * 60.0 / (2.0 * math.pi)
                        if _aw > 1e-9 and _snr_rpm >= _jid_snr_min:
                            _jnew = _ate / (_jid_w * _aw)
                            _jnew = min(max(_jnew, 0.5 * J_M), 50.0 * J_M)
                            _jlist.append(_jnew)
                            _jhat = sum(_jlist) / len(_jlist)
                            if len(_jlist) >= _jid_nmin:
                                _sd = math.sqrt(sum((x - _jhat) ** 2 for x in _jlist) / len(_jlist))
                                if _sd <= _jid_std_max * _jhat:   # 置信：进入应用/校验
                                    _jid = False
                                    _jfin_evt = True
                        _te_c = _te_s = _w_c = _w_s = 0.0
                        _nid = 0
            if _jfin_evt:                             # 辨识完成：死区 / 立即应用 / 进入校验
                _jfin_evt = False
                _jv_rho = _jhat / J_M
                _jv_tdec = _tk
                if abs(_jv_rho - 1.0) <= _j_apply_thr:       # 死区：状态 5，保持标称 b0
                    _jstate = 5
                    _jv_decision = "deadband"
                elif _j_val_on:                              # 状态 4 前置：先采基线，再应用、复测
                    _jv_B0e = B0 * (J_M / _jhat)
                    _jv_tbase0 = _tk + _j_val_settle
                    _jv_tbase1 = _jv_tbase0 + _j_base_win
                    _jv_phase = 1
                else:                                        # 向后兼容：立即应用（旧行为）
                    _B0e = B0 * (J_M / _jhat)
                    _jstate = 2
                    _jv_applied = True
                    _jv_decision = "applied"
            # ---- 状态 4：应用后校验（基线 → 应用 → 后窗 → 判定）----
            if _jv_phase == 1:
                if _tk >= _jv_tbase0:
                    _jv_iq1 = _jv_iq2 = _jv_c = _jv_s = 0.0
                    _jv_n = 0; _jv_pk = 0.0
                    _jv_phase = 2
            elif _jv_phase == 2:
                _iqv = idq[1]
                _jv_iq1 += _iqv; _jv_iq2 += _iqv * _iqv
                if abs(_iqv) > _jv_pk: _jv_pk = abs(_iqv)
                _jv_e = (y_m - 1.0) * 600.0
                _jv_c += _jv_e * math.cos(_jv_w10 * _tk)
                _jv_s += _jv_e * math.sin(_jv_w10 * _tk)
                _jv_n += 1
                if _tk >= _jv_tbase1:
                    _jv_base = _jv_stats(_jv_iq1, _jv_iq2, _jv_c, _jv_s, _jv_n, _jv_pk, _jv_tbase0, _tk)
                    _B0e = _jv_B0e
                    _jv_applied = True
                    _jv_tapply = _tk
                    _jv_s1 = _jv_s2 = _jv_sc = _jv_ss = 0.0; _jv_sn = 0; _jv_pks = 0.0
                    _jv_phase = 3
            elif _jv_phase == 3:
                _iqv = idq[1]
                _jv_s1 += _iqv; _jv_s2 += _iqv * _iqv
                if abs(_iqv) > _jv_pks: _jv_pks = abs(_iqv)
                _jv_e = (y_m - 1.0) * 600.0
                _jv_sc += _jv_e * math.cos(_jv_w10 * _tk)
                _jv_ss += _jv_e * math.sin(_jv_w10 * _tk)
                _jv_sn += 1
                if _tk >= _jv_tapply + _j_val_delay:
                    _jv_settle = _jv_stats(_jv_s1, _jv_s2, _jv_sc, _jv_ss, _jv_sn, _jv_pks, _jv_tapply, _tk)
                    _jv_iq1 = _jv_iq2 = _jv_c = _jv_s = 0.0
                    _jv_n = 0; _jv_pk = 0.0
                    _jv_phase = 4
            elif _jv_phase == 4:
                _iqv = idq[1]
                _jv_iq1 += _iqv; _jv_iq2 += _iqv * _iqv
                if abs(_iqv) > _jv_pk: _jv_pk = abs(_iqv)
                _jv_e = (y_m - 1.0) * 600.0
                _jv_c += _jv_e * math.cos(_jv_w10 * _tk)
                _jv_s += _jv_e * math.sin(_jv_w10 * _tk)
                _jv_n += 1
                if _tk >= _jv_tapply + _j_val_delay + _j_val_win:
                    _jv_post = _jv_stats(_jv_iq1, _jv_iq2, _jv_c, _jv_s, _jv_n, _jv_pk,
                                         _jv_tapply + _j_val_delay, _tk)
                    # 并窗（含施加瞬态）：settle + post 的样本和直接相加
                    _jv_merged = _jv_stats(_jv_s1 + _jv_iq1, _jv_s2 + _jv_iq2,
                                           _jv_sc + _jv_c, _jv_ss + _jv_s,
                                           _jv_sn + _jv_n, max(_jv_pks, _jv_pk),
                                           _jv_tapply, _tk)
                    _riq = _jv_post["iq_rms"] / max(_jv_base["iq_rms"], 1e-12)
                    _ra10 = _jv_post["a10"] / max(_jv_base["a10"], 1e-12)
                    _bad_iq = _riq > 1.0 + _j_val_tol
                    _bad_a10 = ((_jv_base["a10"] >= _j_val_a10_floor)
                                and (_ra10 > 1.0 + _j_val_tol))
                    _jv_ratios = dict(iq=_riq, a10=_ra10)
                    _jv_tfinal = _tk
                    _jv_guard_pk = _jv_pks
                    if _bad_iq or _bad_a10:
                        _B0e = B0
                        _jstate = 4
                        _jv_rollback = True
                        _jv_decision = ("rollback" + ("_iq" if _bad_iq else "")
                                        + ("_a10" if _bad_a10 else ""))
                    else:
                        _jstate = 2
                        _jv_decision = "applied"
                    _jv_phase = 5
            jhat_o.append(_jhat)
            jstate_o.append(_jstate)
            b0e_o.append(_B0e)
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
            inj_o[j] = _inj_now
            tl_o[j] = _tl_tot                                 # 出图用：含负载噪声的总负载
            sg_o[j] = sg_now
            b3_o[j] = _b3_now; a_o[j] = _A_now; es_o[j] = _es_delta
    tt = t[::dec]
    m = min(len(tt), no)
    return dict(t=tt[:m], y=y_o[:m], id=id_o[:m], iq=iq_o[:m], ia=ia_o[:m], inj=inj_o[:m],
                vd=vd_o[:m], vq=vq_o[:m], u=u_o[:m], vqc=vqc_o[:m],
                iqr=iqr_o[:m], fl=fl_o[:m], dm=dm_o[:m], tl=tl_o[:m], sg=sg_o[:m],
                b3=b3_o[:m], amp=a_o[:m], es=es_o[:m],
                dftN=_dft_N, dftn=len(_dft_q), wT=float(_wT),
                trig=trig_log, oracle=oracle_log,
                jhat=np.asarray(jhat_o), t_j=np.arange(len(jhat_o)) * 1e-3,
                jstate=np.asarray(jstate_o),
                b0e=np.asarray(b0e_o), lg=_lg, jnew=np.asarray(_jnew_log),
                bpv=np.asarray(_jnew_bpv_log),
                fd=np.asarray(_jrec_fd_o), abort=np.asarray(_jrec_abort_o), jval_log=_jrec_val_log,
                # ---- J 应用后校验（状态 4）记录 ----
                jval=dict(enable=bool(_j_val_on), rho=float(_jv_rho),
                          t_decision=_jv_tdec, t_final=_jv_tfinal,
                          decision=_jv_decision,
                          applied=bool(_jv_applied), rollback=bool(_jv_rollback),
                          state=int(_jstate),
                          jhat=float(_jhat),
                          thr=float(_j_apply_thr), tol=float(_j_val_tol),
                          settle=float(_j_val_settle), base_win=float(_j_base_win),
                          delay=float(_j_val_delay), win=float(_j_val_win),
                          a10_floor=float(_j_val_a10_floor),
                          iq_rated=float(I_BASE),
                          base=_jv_base, settle_win=_jv_settle, post=_jv_post,
                          merged=_jv_merged, ratios=_jv_ratios,
                          guard_pk=float(_jv_guard_pk)))

