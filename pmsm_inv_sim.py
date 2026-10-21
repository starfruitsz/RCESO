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

R_S = 0.175
L_S = 0.57e-3
PSI_F = 0.101 / (1.5 * 4.0)      # 0.016833 Wb
P_POL = 4
J_M = 1.89e-5
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
    B_GAIN = 0.101 * I_BASE / (J_M * w_ref); B0 = 1.2 * B_GAIN
    BETA3 = cfg.get("beta3", 2000.0); TAU0 = cfg.get("tau0", 20e-3)
    Q0 = cfg.get("Q0", 0.98); ZETA = 0.2
    kp_boost = cfg.get("kp_boost", 0.0); det_eps = cfg.get("det_eps", 0.01)
    ff_flush = cfg.get("ff_flush", 0.0); tauf = cfg.get("ff_tau_f", 4e-3)
    taus = cfg.get("ff_tau_s", 0.5); ff_cool = cfg.get("ff_cool", 0.3)
    ff_src = str(cfg.get("ff_src", "e1"))
    ff_amin = cfg.get("ff_amin", 0.0); ff_gmax = cfg.get("ff_gmax", -1.0)
    ff_vmax = cfg.get("ff_vmax", -1.0)
    ff_mism = cfg.get("ff_mism", 0.0)          # 记忆失配阈值（0=关）；>0 时与包络比值 OR
    ff_mism_eps = cfg.get("ff_mism_eps", 1e-6)
    ff_wait = cfg.get("ff_wait", 0.0)          # 检测后再等待的相位延迟（s），0=立即复位
    ff_confirm = cfg.get("ff_confirm", 0.0)    # 连续确认窗（ms），0=首拍触发
    ff_imin = cfg.get("ff_imin", 0.0)          # 带载门控：|iq| 低于该值不复位（A）
    ff_vphase = cfg.get("ff_vphase", None)     # 相位条件：v 低于该阈值时复位（None=关）
    ff_vwait_max = cfg.get("ff_vwait_max", 0.03)  # 相位等待的上限（s）
    ff_phase = cfg.get("ff_phase", None)       # 10 Hz 相位目标（rad，None=关）
    ff_phase_tol = cfg.get("ff_phase_tol", 0.35)
    ff_phase_max = cfg.get("ff_phase_max", 0.04)
    ff_phi = cfg.get("ff_phi", 0.0)
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
    vd_buf = np.zeros(nd); ip = 0; vd_delay = 0.0
    vm_buf = np.zeros(nd); vm_old = np.zeros(nd)
    vm_now = 0.0; vm_prev = 0.0; mip = 0

    # F-B 检测状态
    efs = efl = 0.0; fft = 0.0; fft2 = 0.0
    e1g_acc = 0.0; e1g_buf = np.zeros(nd); e1g_p = 0
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
        w += dt * (Te - (TL[k] + TLn[min(k // nTstep, nT - 1)])) / J_M

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
            kpe = KP * (1.0 + kp_boost * g)
            z1n = z1 + 1e-3 * (z2 + B0 * u + v + 2.0 * WO * e1)
            z2n = z2 + 1e-3 * (WO * WO * e1)
            e1p = (e1 - ff_phi * math.tanh(e1 / ff_phi)) if ff_phi > 0.0 else e1
            vd_delay = vd_buf[ip]
            chi = Q0 * vd_delay + BETA3 * math.tanh(e1p / ZETA)
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
            # F-A oracle：事件时刻直接复位（0=清空，-1=反相）
            if (flush_t is not None) and (not oracle_done) and (k * dt >= float(flush_t)):
                oracle_log.append((float(k * dt), float(v), float(vn)))
                if flush_alpha == 0.0:
                    vn = 0.0; vd_buf[:] = 0.0
                else:
                    vn = flush_alpha * vn; vd_buf[:] = flush_alpha * vd_buf
                oracle_done = True
            u = (kpe * (1.0 - y_m) - z2n - vn) / B0
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
                    Dm = abs(vm_now - vm_prev) / (vm_prev + ff_mism_eps)
                    dm_o[k // dec] = Dm
                raw = raw_env or ((ff_mism > 0.0) and (Dm > ff_mism) and okg and okv and oki)
                if raw and (fft <= 0.0) and (k * dt > 0.05):
                    raw_cnt += 1
                else:
                    raw_cnt = 0
                _need = max(1, int(round(ff_confirm)))
                if (raw_cnt >= _need) and (fft <= 0.0) and (k * dt > 0.05) and (pending_t is None) and (not phase_pending):
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
                        vn = 0.0; vd_buf[:] = 0.0; fft = ff_cool
                        fl_o[k // dec] = 1.0
                        trig_log.append((k * dt, v, efs, Dm))
                if phase_pending:
                    _dphi = (v10_ph - ff_phase + math.pi) % TWO_PI - math.pi
                    if (abs(_dphi) < ff_phase_tol) or (k * dt >= phase_deadline):
                        vn = 0.0; vd_buf[:] = 0.0; fft = ff_cool
                        phase_pending = False
                        fl_o[k // dec] = 1.0
                        trig_log.append((k * dt, v, efs, Dm))
                if pending_t is not None:
                    _go = ((pending_phase is not None and v < pending_phase)
                           or (k * dt >= pending_t))
                    if _go:
                        vn = 0.0; vd_buf[:] = 0.0; fft = ff_cool
                        pending_t = None; pending_phase = None
                        fl_o[k // dec] = 1.0
                        trig_log.append((k * dt, v, efs, Dm))
            z1, z2, v = z1n, z2n, vn
            vd_buf[ip] = v; ip = (ip + 1) % nd

        if k % dec == 0:
            j = k // dec
            y_o[j] = w / w_ref; id_o[j] = idq[0]; iq_o[j] = idq[1]
            ia_o[j] = ia; vd_o[j] = vd; vq_o[j] = vq
            u_o[j] = u; vqc_o[j] = vq_cmd; iqr_o[j] = u * I_BASE
    tt = t[::dec]
    m = min(len(tt), no)
    return dict(t=tt[:m], y=y_o[:m], id=id_o[:m], iq=iq_o[:m], ia=ia_o[:m],
                vd=vd_o[:m], vq=vq_o[:m], u=u_o[:m], vqc=vqc_o[:m],
                iqr=iqr_o[:m], fl=fl_o[:m], dm=dm_o[:m],
                trig=trig_log, oracle=oracle_log)

