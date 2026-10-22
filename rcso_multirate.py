# -*- coding: utf-8 -*-
"""rcso_multirate.py —— 多速率（控制器分频）仿真器
对象按 dt 积分；控制器按 t_ctrl 迭代（零阶保持）。t_ctrl=dt 时退化为单速率。
实现与 adrc_eso_closed.adrc_sim 同口径的关键部件：灰箱 ESO、低通重复通道 v=Q*v(t-T)+b3*tanh(e1/zeta)、
零均值 phi 压缩驱动 + 带通 D、Q 律、律 B（wo 调度）、律 D（kp 调度）。
"""
import math
import numpy as np

from eso_gain import make_gains


def sim_mr(t, r, d, b, b0, wo, kp, Tper, zeta, beta3, tau0, mu, s2, dt_ci, NI=None, DN=None,
           law="none", kp_boost=0.0, wo_sched=0.0, det_eps=0.01, t_ctrl=0.0, Q0=0.98,
           e0_win=None, phi_c=0.1,
           eso_law="fal", eso_a=0.75, eso_a1=1.0, eso_delta=0.10, eso_lam=10.0):
    """law: 'none'(ESO) | 'rc'(RCESO) | 'adapt'（RC + Q/B/D 三调度）
    t_ctrl: 控制器周期（0=与对象同步）"""
    n = len(t); dt = float(t[1] - t[0])
    nsp = max(1, int(round(t_ctrl / dt))) if t_ctrl > 0 else 1
    dtc = dt * nsp
    win = int(round((e0_win if e0_win else Tper) / dtc))          # E0 窗（控制器步数）
    nt = int(round(Tper / dtc))                                    # 重复周期（控制器步数）
    phi = lambda x, c: x - c * math.tanh(x / c) if c > 0 else x
    # 状态
    y = 0.0; ia = 0.0; z1 = 0.0; z2 = 0.0; v = 0.0; Q = Q0; u = 0.0; ef_prev = 0.0
    vbuf = np.zeros(nt + 1); e2buf = np.zeros(win + 1); e2acc = 0.0
    e1buf = np.zeros(win + 1); e1acc = 0.0; e1p = 0
    wf = 0.0; ws = 0.0; qf = 0.0; qs = 0.0; ip = 0; e2p = 0
    af = 1.0 - math.exp(-2 * math.pi * (1.0 / (5.0 * Tper)) * dtc)   # 快支 5T（2 Hz）
    as_ = 1.0 - math.exp(-2 * math.pi * (1.0 / (50.0 * Tper)) * dtc) # 慢支 50T（0.2 Hz）
    ys = np.zeros(n); ias = np.zeros(n); Qs = np.zeros(n)
    b3 = 0.0 if law == "none" else beta3
    bs1, bs2 = 2.0 * wo, wo * wo
    ESO_G1, ESO_G2 = make_gains(dict(eso_law=eso_law, eso_a=eso_a, eso_a1=eso_a1,
                                     eso_delta=eso_delta, eso_lam=eso_lam))
    for k in range(1, n):
        rk = r[k]; dk = d[k]
        # ---- 对象：每步积分（用保持的 u）----
        if dt_ci > 0:
            ia += (1.0 - math.exp(-dt / dt_ci)) * ((u - (NI[k] if NI is not None else 0.0)) - ia)
        else:
            ia = u - (NI[k] if NI is not None else 0.0)
        y += dt * (b * ia + dk + (DN[k] if DN is not None else 0.0))   # 与主程序同量纲：d_noise 已是 y 单位
        ys[k] = y; ias[k] = ia
        # ---- 控制器：仅在控制步执行 ----
        if nsp > 1 and (k % nsp) != 0:
            Qs[k] = Q; continue
        eo = y - z1
        e1 = eo
        # 驱动（零均值实参 + phi 压缩 + 带通）
        vd = vbuf[ip]
        e2old = e2buf[e2p]
        e2new = ef_prev * ef_prev * dtc        # meansq 口径（与主程序 eo_def='meansq' 一致）
        e2acc += e2new - e2old; e2buf[e2p] = e2new
        E0 = e2acc / (win * dtc)
        w = phi((ef_prev * ef_prev - E0) / (E0 + 6.5), phi_c)   # norm_floor=6.5（与主程序一致）
        wf += af * (w - wf); ws += as_ * (w - ws)
        D = wf - ws
        Dq = max(0.0, D)
        # 检测器（律 D）
        ef_det = e1 - phi_c * math.tanh(e1 / phi_c) if phi_c > 0 else e1
        g = 0.0
        # 检测器：g = e1m^2/(e1m^2+eps^2)，e1m = (1/T)∫e1（周期信号在 T 上均值为 0）
        e1acc += e1 * dtc - e1buf[e1p]; e1buf[e1p] = e1 * dtc
        e1m = e1acc / (win * dtc) if win > 0 else 0.0
        g = 0.0
        if kp_boost > 0.0 or wo_sched > 0.0:
            g = e1m * e1m / (e1m * e1m + det_eps ** 2)
        kpe = kp * (1.0 + kp_boost * g)
        b1e = bs1 * (1.0 + wo_sched * g); b2e = bs2 * (1.0 + wo_sched * g)
        # ESO（控制器步长 dtc）
        _g1 = ESO_G1(eo); _g2 = ESO_G2(eo)
        z1n = z1 + dtc * (z2 + b0 * u + v + b1e * _g1)
        z2n = z2 + dtc * (b2e * _g2)
        # 重复通道：tau*v_dot + v = chi，chi = Q*v(t-T) + b3*tanh(e1/zeta)
        chi = (Q * vd + b3 * math.tanh(e1 / zeta)) if b3 > 0.0 else 0.0
        vn = chi + (v - chi) * math.exp(-dtc / tau0)
        ef = chi - vn                                   # 滤波误差 = tau*v_dot（与主程序同式）
        # Q 律
        if law == "adapt":
            Qn = Q + dtc * (-mu / (2.0 * tau0) * (1.0 - (1.0 - Q) ** 2) * Dq
                            + s2 * math.atanh(max(-0.999, min(0.999, 1.0 - Q))))
            Qn = min(1.8, max(0.2, Qn))
        else:
            Qn = Q
        un = (kpe * (rk - y) - z2n - vn) / b0
        # 推进
        z1, z2, v, Q, u = z1n, z2n, vn, Qn, un; ef_prev = ef
        vbuf[ip] = v; ip = (ip + 1) % (nt + 1)
        e2p = (e2p + 1) % (win + 1); e1p = (e1p + 1) % (win + 1)
        Qs[k] = Q
    return dict(y=ys, ia=ias, Q=Qs)


if __name__ == "__main__":
    import sys
    KT, J_M, T_RATED = 0.101, 1.89e-5, 0.637
    N = 600.0; W_REF = N * math.pi / 30.0; I_BASE = T_RATED / KT
    B = KT * I_BASE / (J_M * W_REF); B0 = 1.2 * B
    T, DT, TEND, TL0 = 0.1, 2e-5, 12.0, 2.0
    KP, WO, FCI, B3, tau0 = 75.36, 188.4, 1000.0, 1000.0, 10e-3
    t = np.arange(0.0, TEND, DT); n = len(t)
    def bn(sig, fc, sd):
        rng = np.random.default_rng(sd); x = rng.standard_normal(n)
        a = 1.0 - math.exp(-2 * math.pi * fc * DT); nk = max(1, int(math.ceil(6.0 / (2 * math.pi * fc * DT))))
        y = np.convolve(x, a * np.power(1 - a, np.arange(nk)))[:n]; return y / y.std() * sig
    NI = bn(0.01, 2000.0, 20261016); NT = bn(0.05, 200.0, 20261017)
    tau = np.maximum(t - TL0, 0.0); on = (t >= TL0).astype(float)
    step = 0.60 * on; npc = 0.15 * np.sin(2 * math.pi * 0.7 * tau) * on
    amp = np.full_like(t, 0.05)
    amp = np.where((tau >= 0.5) & (tau < 0.6), 0.30, amp); amp = np.where((tau >= 1.0) & (tau < 1.5), 0.30, amp)
    amp = np.where(tau >= 2.0, 0.40, amp); ph = 2 * math.pi * tau / T
    TL = (step + npc + amp * (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))) * on
    d = -B * TL; r = np.full_like(t, 1.0); DN = -B * NT * on
    W = [(0.5, 2.0), (2.0, 2.5), (2.5, 2.6), (3.0, 3.5), (3.5, 4.0), (4.0, 6.0), (7.0, 12.0)]
    def rep(Y):
        e = Y["y"] * N - N
        return [float(np.sqrt(np.mean(e[(t >= a) & (t < b)] ** 2))) for a, b in W]
    for lbl, kw in [("ESO (t_ctrl=dt)", dict(law="none")), ("RCESO (t_ctrl=dt)", dict(law="rc")),
                    ("自适应 (t_ctrl=dt)", dict(law="adapt", kp_boost=4.0, wo_sched=3.0)),
                    ("RCESO (t_ctrl=1ms)", dict(law="rc", t_ctrl=1e-3)),
                    ("自适应 (t_ctrl=1ms)", dict(law="adapt", kp_boost=4.0, wo_sched=3.0, t_ctrl=1e-3))]:
        Y = sim_mr(t, r, d, B, B0, WO, KP, T, 0.2, B3, tau0, 0.06, 5.0, 1.0 / (2 * math.pi * FCI),
                   NI=NI, DN=DN, det_eps=0.01, **kw)
        print("%-22s %s" % (lbl, " ".join("%8.2f" % x for x in rep(Y))))



# =====================================================================
#  铁律（2026-10-18 定稿）多速率口径：
#    被控对象数值积分 dt   = 10 us
#    电流环离散采样 t_ci   = 50 us   (20 kHz)
#    转速环离散采样 t_ctrl = 1  ms   (1 kHz)
#  三者不可混用；任何新仿真一律调用 sim_mr3（或显式给出这三个周期）。
# =====================================================================
def sim_mr3(t, r, d, b, b0, wo, kp, Tper, zeta, beta3, tau0,
            law="rc", kp_boost=0.0, wo_sched=0.0, det_eps=0.01,
            dt_ci=50e-6, t_ctrl=1e-3, Q0=0.98, tau_ci=None,
            NI=None, DN=None, phi_c=0.1,
            eso_law="fal", eso_a=0.75, eso_a1=1.0, eso_delta=0.10, eso_lam=10.0):
    """三速率仿真：对象 dt、电流环 dt_ci、转速环 t_ctrl（零阶保持）。

    law: 'none'(ESO) | 'rc'(RCESO) | 'adapt'(RC + 律D/律B)
    tau_ci: 电流环闭环一阶时间常数（默认取 1/(2*pi*1kHz) 之外由调用方给定）
    """
    n = len(t)
    dt = float(t[1] - t[0])
    nci = max(1, int(round(dt_ci / dt)))
    nsp = max(1, int(round(t_ctrl / dt)))
    dtc = dt * nsp
    win = max(1, int(round(Tper / dtc)))
    nt = max(1, int(round(Tper / dtc)))
    phi = lambda x, c: x - c * math.tanh(x / c) if c > 0 else x
    y = 0.0; ia = 0.0; z1 = 0.0; z2 = 0.0; v = 0.0; Q = Q0; u = 0.0; ef_prev = 0.0
    vbuf = np.zeros(nt + 1); e2buf = np.zeros(win + 1); e2acc = 0.0
    e1buf = np.zeros(win + 1); e1acc = 0.0; e1p = 0; e2p = 0; ip = 0
    wf = 0.0; ws = 0.0
    af = 1.0 - math.exp(-2 * math.pi * (1.0 / (5.0 * Tper)) * dtc)
    as_ = 1.0 - math.exp(-2 * math.pi * (1.0 / (50.0 * Tper)) * dtc)
    aci = 1.0 - math.exp(-dt_ci / tau_ci) if tau_ci else 1.0
    ys = np.zeros(n); ias = np.zeros(n); Qs = np.zeros(n)
    b3 = 0.0 if law == "none" else beta3
    bs1, bs2 = 2.0 * wo, wo * wo
    ESO_G1, ESO_G2 = make_gains(dict(eso_law=eso_law, eso_a=eso_a, eso_a1=eso_a1,
                                     eso_delta=eso_delta, eso_lam=eso_lam))
    for k in range(1, n):
        # 1) 对象：机械方程按 dt 积分（ia 为电流环保持值）
        y += dt * (b * ia + d[k] + (DN[k] if DN is not None else 0.0))
        # 2) 电流环：按 dt_ci 更新（零阶保持）
        if k % nci == 0:
            i_ref = u - (NI[k] if NI is not None else 0.0)
            ia += aci * (i_ref - ia)
        ys[k] = y; ias[k] = ia
        # 3) 转速环：按 t_ctrl 更新
        if k % nsp != 0:
            Qs[k] = Q
            continue
        eo = y - z1
        e1 = eo
        vd = vbuf[ip]
        e2old = e2buf[e2p]
        e2new = ef_prev * ef_prev * dtc
        e2acc += e2new - e2old; e2buf[e2p] = e2new
        E0 = e2acc / (win * dtc)
        w = phi((ef_prev * ef_prev - E0) / (E0 + 6.5), phi_c)
        wf += af * (w - wf); ws += as_ * (w - ws)
        Dq = max(0.0, wf - ws)
        e1acc += e1 * dtc - e1buf[e1p]; e1buf[e1p] = e1 * dtc
        e1m = e1acc / (win * dtc) if win > 0 else 0.0
        g = 0.0
        if kp_boost > 0.0 or wo_sched > 0.0:
            g = e1m * e1m / (e1m * e1m + det_eps ** 2)
        kpe = kp * (1.0 + kp_boost * g)
        b1e = bs1 * (1.0 + wo_sched * g); b2e = bs2 * (1.0 + wo_sched * g)
        _g1 = ESO_G1(eo); _g2 = ESO_G2(eo)
        z1n = z1 + dtc * (z2 + b0 * u + v + b1e * _g1)
        z2n = z2 + dtc * (b2e * _g2)
        chi = (Q * vd + b3 * math.tanh(e1 / zeta)) if b3 > 0.0 else 0.0
        vn = chi + (v - chi) * math.exp(-dtc / tau0)
        ef = chi - vn
        if law == "adapt":
            Qn = Q + dtc * (-0.06 / (2.0 * tau0) * (1.0 - (1.0 - Q) ** 2) * Dq
                            + 5.0 * math.atanh(max(-0.999, min(0.999, 1.0 - Q))))
            Qn = min(1.8, max(0.2, Qn))
        else:
            Qn = Q
        u = (kpe * (r[k] - y) - z2n - vn) / b0
        z1, z2, v, Q = z1n, z2n, vn, Qn; ef_prev = ef
        vbuf[ip] = v; ip = (ip + 1) % (nt + 1)
        e2p = (e2p + 1) % (win + 1); e1p = (e1p + 1) % (win + 1)
        Qs[k] = Q
    return dict(y=ys, ia=ias, Q=Qs)
