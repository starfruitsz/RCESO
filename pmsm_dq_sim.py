# -*- coding: utf-8 -*-
"""PMSM dq 轴模型（含 id、交叉耦合）+ 双 PI 电流环 + 简化逆变器（电压圆限幅）
   三档时序（铁律）：对象 10 us / 电流环 50 us / 转速环 1 ms，均零阶保持。
   速度环：灰箱 ESO + 低通重复通道 + 律 D + 律 F-B（与 adrc_sim 同口径）。
   id* = 0；PI 含 dq 解耦前馈；逆变器按理想电压源 + 幅值限幅（允许的简化）。
"""
import math
import numpy as np

R_S   = 0.175
L_D   = 0.57e-3
L_Q   = 0.57e-3
PSI_F = 0.101/(1.5*4)
P_POL = 4
J_M   = 1.89e-5
V_DC  = 60.0
V_MAX = V_DC/math.sqrt(3.0)
N_REF = 600.0
W_REF = N_REF*math.pi/30.0
I_BASE = 0.637/0.101

def band_noise(n, sigma, fc, dt, seed):
    rng = np.random.default_rng(seed); x = rng.standard_normal(n)
    a = 1.0 - math.exp(-2*math.pi*fc*dt)
    nk = max(1, int(math.ceil(6.0/(2*math.pi*fc*dt))))
    y = np.convolve(x, a*np.power(1.0-a, np.arange(nk)))[:n]
    return y/y.std()*sigma

def sim_dq(t, TL, cfg=None):
    cfg = cfg or {}
    dt = float(t[1]-t[0]); n = len(t)
    T  = cfg.get("T", 0.1)
    KP = cfg.get("kp", 75.36); WO = cfg.get("wo", 500.0)
    B_GAIN = 0.101*I_BASE/(J_M*W_REF); B0 = 1.2*B_GAIN
    BETA3 = cfg.get("beta3", 2000.0); TAU0 = cfg.get("tau0", 5e-3)
    Q0 = cfg.get("Q0", 0.98); ZETA = 0.2
    kp_boost = cfg.get("kp_boost", 0.0); det_eps = cfg.get("det_eps", 0.01)
    ff_flush = cfg.get("ff_flush", 0.0); tauf = cfg.get("ff_tau_f", 4e-3); taus = cfg.get("ff_tau_s", 0.5)
    ff_cool = cfg.get("ff_cool", 0.3)
    ff_phi = cfg.get("ff_phi", 0.0)          # 检测器前置软死区宽度（标幺），0=关闭
    ff_src = str(cfg.get("ff_src", "e1"))    # [新增] 检测器输入：'e1'=ESO 残差（旧）；'et'=跟踪误差 1-y
    ff_amin = cfg.get("ff_amin", 0.0)        # [新增] 快包络绝对下限（标幺），0=关
    ff_vmax = cfg.get("ff_vmax", -1.0)       # [新增] 复位前 |v| 上限：补偿已塌陷才允许复位，<0=关
    ff_gmax = cfg.get("ff_gmax", -1.0)       # [新增] 非周期能量门控：要求 g<ff_gmax，<0=关
    ff_deb = int(cfg.get("ff_deb", 1))       # [新增] 去抖：R>阈值需连续保持的转速环拍数
    ff_a10 = cfg.get("ff_a10", 0.0)          # [新增] 10 Hz 幅值塌陷判据：A10<ff_a10*A10s 触发（0=关）
    ff_a10max = cfg.get("ff_a10max", 0.0)    # [新增] A10/A10s 上限（塌陷门控）：只在幅值塌陷时放行，0=关
    ff_a10_win = cfg.get("ff_a10_win", 0.02) # 正交解调窗长（s）
    ff_a10_tau = cfg.get("ff_a10_tau", 0.3)  # 慢幅值 A10s 的时间常数（s）
    ff_a10_amin = cfg.get("ff_a10_amin", 0.0)  # A10s 绝对下限（标幺），低于它不判事件
    ff_cool_d = cfg.get("ff_cool_drop", 0.1)   # 塌陷通道独立冷却（s），可越过 R 通道冷却
    ff_tmin = cfg.get("ff_tmin", 0.0)          # [新增] 事件检测最早允许时刻（s），避开启动/爬坡
    trace_det = bool(cfg.get("trace_det", False))  # [新增] 记录检测器逐拍量，供归因
    f_fb = cfg.get("f_ci_fb", 0.0)           # 电流反馈一阶低通截止频率 (Hz)，0=不滤
    f_yfb = cfg.get("f_y_fb", 0.0)           # 转速反馈一阶低通截止频率 (Hz)，0=不滤
    rc_phi = cfg.get("rc_phi", 0.0)          # 重复通道泵浦口的软死区宽度（标幺），0=关闭
    wci = 2*math.pi*cfg.get("fci", 1000.0); kpi, kii = L_D*wci, R_S*wci
    T_CI = cfg.get("T_ci", 50e-6); T_SP = cfg.get("T_ctrl", 1e-3)
    nci = max(1, int(round(T_CI/dt))); nsp = max(1, int(round(T_SP/dt)))
    sig_i = cfg.get("sig_i", 0.5); sig_n = cfg.get("sig_n", 15.0)
    NI = band_noise(n, sig_i, 2000.0, dt, cfg.get("seed_i", 20261016))
    NQ = band_noise(n, sig_i, 2000.0, dt, cfg.get("seed_q", 20261017))
    NW = band_noise(n, sig_n, 200.0, dt, cfg.get("seed_w", 20261018))

    idq = np.zeros(2); w = 0.0
    idf = iqf = 0.0                          # 电流反馈滤波状态
    afb = (1.0 - math.exp(-2*math.pi*f_fb*T_CI)) if f_fb > 0.0 else 1.0
    yf = 0.0                                  # 转速反馈滤波状态
    ayf = (1.0 - math.exp(-2*math.pi*f_yfb*T_SP)) if f_yfb > 0.0 else 1.0
    z1 = z2 = v = 0.0; u = 0.0
    nd = int(round(T/T_SP)); vbuf = np.zeros(nd+1); ip = 0
    nw = nd; e1buf = np.zeros(nw+1); e1acc = 0.0; e1p = 0
    efs = efl = 0.0; fft = 0.0
    dc = 0; trig_log = []
    DET = {"t": [], "R": [], "ef": [], "es": [], "g": [], "v": [],
           "raw": [], "fire": [], "blk": [], "a10": [], "rawd": [], "fired": []}
    w10 = max(2, int(round(ff_a10_win/T_SP)))
    a10c = np.zeros(w10); a10s_ = np.zeros(w10)
    a10acc_c = a10acc_s = 0.0; a10p = 0; a10slow = 0.0; a10 = 0.0
    fft2 = 0.0; dc2 = 0
    acoef = 1.0 - math.exp(-T_SP/ff_a10_tau) if ff_a10_tau > 0.0 else 1.0
    int_d = int_q = 0.0
    vd_cmd = vq_cmd = 0.0
    y_out = np.zeros(n); id_out = np.zeros(n); iq_out = np.zeros(n)
    vd_out = np.zeros(n); vq_out = np.zeros(n); v_out = np.zeros(n)
    fl_out = np.zeros(n)
    af = 1.0-math.exp(-T_SP/tauf); as_ = 1.0-math.exp(-T_SP/taus)

    for k in range(1, n):
        # ---- 电气/机械方程：每 dt 一步（电压、电流指令零阶保持）----
        we = P_POL*w
        did = (vd_cmd - R_S*idq[0] + we*L_Q*idq[1])/L_D
        diq = (vq_cmd - R_S*idq[1] - we*L_D*idq[0] - we*PSI_F)/L_Q
        idq[0] += dt*did; idq[1] += dt*diq
        Te = 1.5*P_POL*PSI_F*idq[1]
        w += dt*(Te - TL[k])/J_M

        # ---- 电流环：每 T_CI = 50 us ----
        if k % nci == 0:
            idf += afb*((idq[0] + NI[k]) - idf); iqf += afb*((idq[1] + NQ[k]) - iqf)
            id_m, iq_m = (idf, iqf) if f_fb > 0.0 else (idq[0] + NI[k], idq[1] + NQ[k])
            ed = 0.0 - id_m; eq = u*I_BASE - iq_m
            vd_ff = -we*L_Q*iq_m; vq_ff = we*(L_D*id_m + PSI_F)
            vd_n = kpi*ed + kii*int_d + vd_ff
            vq_n = kpi*eq + kii*int_q + vq_ff
            vmag = math.hypot(vd_n, vq_n)
            if vmag > V_MAX:
                sc = V_MAX/vmag; vd_n *= sc; vq_n *= sc
            else:
                sc = 1.0
                int_d += ed*T_CI; int_q += eq*T_CI
            vd_cmd, vq_cmd = vd_n, vq_n

        # ---- 转速环：每 T_SP = 1 ms ----
        if k % nsp == 0:
            y_true = w/W_REF
            yf += ayf*((y_true + NW[k]/N_REF) - yf)
            y_m = yf if f_yfb > 0.0 else (y_true + NW[k]/N_REF)
            e1 = y_m - z1
            vd_delay = vbuf[ip]
            if det_eps > 0.0:
                e1acc += e1*T_SP - e1buf[e1p]; e1buf[e1p] = e1*T_SP
                e1m = e1acc/T
                g = (e1m*e1m)/(e1m*e1m + det_eps*det_eps)
            else:
                g = 0.0
            kpe = KP*(1.0 + kp_boost*g)
            z1n = z1 + T_SP*(z2 + B0*u + v + 2*WO*e1)
            z2n = z2 + T_SP*(WO*WO*e1)
            e1p_ = (e1 - rc_phi*math.tanh(e1/rc_phi)) if rc_phi > 0.0 else e1
            chi = Q0*vd_delay + BETA3*math.tanh(e1p_/ZETA)
            vn = chi + (v - chi)*math.exp(-T_SP/TAU0)
            u = (kpe*(1.0 - y_m) - z2n - vn)/B0
            # 【软死区】phi(x,c)=x-c*tanh(x/c)：小噪声被三次方压低、大事件几乎原样通过
            e_src = (1.0 - y_m) if ff_src == "et" else e1
            e1d = (e_src - ff_phi*math.tanh(e_src/ff_phi)) if ff_phi > 0.0 else e_src
            a_abs = abs(e1d)
            efs += af*(a_abs - efs); efl += as_*(a_abs - efl)
            if fft > 0: fft -= T_SP
            if fft2 > 0: fft2 -= T_SP
            # 10 Hz 幅值（短窗正交解调）+ 慢幅值：检测"周期分量塌陷"（撤除/反相）
            if ff_a10 > 0.0 or ff_a10max > 0.0:
                cc = e_src*math.cos(2*math.pi*t[k]/T); ss = e_src*math.sin(2*math.pi*t[k]/T)
                a10acc_c += cc - a10c[a10p]; a10c[a10p] = cc
                a10acc_s += ss - a10s_[a10p]; a10s_[a10p] = ss
                a10p = (a10p+1) % w10
                a10 = 2.0*math.hypot(a10acc_c, a10acc_s)/w10
                a10slow += acoef*(a10 - a10slow)
            Rr = efs/max(efl, 1e-12)
            okg = (ff_gmax < 0.0) or (g < ff_gmax)
            okv = (ff_vmax < 0.0) or (abs(v) < ff_vmax)
            oka = (ff_a10max <= 0.0) or (a10 < ff_a10max*a10slow)
            raw_r = ((ff_flush > 0.0) and (efs > ff_flush*max(efl, 1e-9))
                     and (efs > ff_amin) and okg and okv and oka)
            raw_d = ((ff_a10 > 0.0) and (a10slow > ff_a10_amin)
                     and (a10 < ff_a10*a10slow))
            dc = dc + 1 if raw_r else 0
            dc2 = dc2 + 1 if raw_d else 0
            fire_r = raw_r and (dc >= ff_deb) and (fft <= 0.0) and (k*T_SP >= ff_tmin)
            fire_d = raw_d and (dc2 >= ff_deb) and (fft2 <= 0.0) and (k*T_SP >= ff_tmin)
            fire = fire_r or fire_d
            if trace_det:
                DET["t"].append(float(t[k])); DET["R"].append(float(Rr))
                DET["ef"].append(float(efs)); DET["es"].append(float(efl))
                DET["g"].append(float(g)); DET["v"].append(float(v))
                DET["raw"].append(1 if raw_r else 0)
                DET["fire"].append(1 if fire else 0)
                DET["blk"].append(1 if (raw_r and fft > 0.0 and k > 50) else 0)
                DET["a10"].append(float(a10)); DET["rawd"].append(1 if raw_d else 0)
                DET["fired"].append(1 if fire_d else 0)
            if fire:
                vn = 0.0; vbuf[:] = 0.0; fft = ff_cool; fft2 = ff_cool_d; fl_out[k] = 1.0
                trig_log.append((float(t[k]), float(v), float(Rr), float(g),
                                 float(efs), 1 if fire_r else 2))
            z1, z2, v = z1n, z2n, vn
            vbuf[ip] = v; ip = (ip+1) % (nd+1); e1p = (e1p+1) % (nw+1)

        y_out[k] = w/W_REF; id_out[k] = idq[0]; iq_out[k] = idq[1]
        vd_out[k] = vd_cmd; vq_out[k] = vq_cmd; v_out[k] = v
    return dict(y=y_out, id=id_out, iq=iq_out, vd=vd_out, vq=vq_out, v=v_out,
                fl=fl_out, trig=trig_log, det=DET)
