# -*- coding: utf-8 -*-
"""run_t_cmp_600.py —— 600 rpm 实验室工况：T 自适应 vs 无自适应

场景与 run_t_es3/4 完全一致：圆盘型线 V2、2 s 加载 0.5 额定 + 5.9 Hz 振动、
实验室噪声（3 rpm / 0.1 A / 0.01 N·m）、fci=500 Hz、类 fal ESO、30 s。
对比：base（δ≡0，T=2π/ω） 与 esc（δ0=-14.3%，Δ=0.5%，σ=1%，Pd=1.5 s，N=3，t0=3 s）
输出：_wave_t_cmp_600.npz（t, y_base, y_esc, amp_base, amp_esc, es_esc）
"""
import math

import numpy as np

import noise_cfg as NC
from tl_profile import disc_unbalance_profile

DT, TEND, TL0 = 2e-6, 30.0, 2.0
N_REF, AMP = 600.0, 0.095
F_VIB, VIB1 = 5.9, 0.03
VIB_H = (1.0, 0.2654, 0.0408, 0.2245, 0.0612, 0.1837)


def build():
    t = np.arange(0.0, TEND, DT)
    vib = np.zeros_like(t)
    for n, a in enumerate(VIB_H, start=1):
        vib += a * np.sin(2.0 * math.pi * F_VIB * n * (t - TL0) * (t >= TL0))
    TL = (0.50 * (t >= TL0)).astype(float) * 0.637 + VIB1 * vib
    return t, TL


def base_cfg():
    return dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
                fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
                i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
                sig_n=NC.NOISE_LAB["sig_n_rpm"],
                sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
                tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
                tl_ang_start=2.01868, tl_ang_rev=29.9,
                eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
                rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
                es_Pd=1.5, es_N=3, es_dead=1e-5, es_dmax=0.20, es_t0=3.0)


def metrics(tt, y, es):
    e = (np.asarray(y) - 1.0) * N_REF
    m = tt >= 25.0
    rms = float(np.sqrt(np.mean(e[m] ** 2)))
    tc = tt[m]
    a = 2.0 * np.mean(e[m] * np.sin(2 * np.pi * 10.0 * tc))
    b = 2.0 * np.mean(e[m] * np.cos(2 * np.pi * 10.0 * tc))
    amp10 = float(np.hypot(a, b))
    return rms, amp10


if __name__ == "__main__":
    from pmsm_inv_sim import sim_inv
    t, TL = build()
    out = {}
    for key, kw in [("base", dict(T_es=True, es_d0=0.0, es_step=0.0, es_dith=0.0)),
                    ("esc", dict(T_es=True, es_d0=-0.143, es_step=0.01, es_dith=0.005))]:
        cfg = base_cfg(); cfg.update(kw)
        Y = sim_inv(t, TL, cfg)
        tt = np.asarray(Y["t"]); y = np.asarray(Y["y"])
        A = np.asarray(Y["amp"]); dl = np.asarray(Y["es"])
        rms, amp10 = metrics(tt, y, dl)
        mA = tt >= 20.0
        print("%-4s 稳态RMS %6.2f rpm  10Hz %6.2f rpm  A %0.5f  δ均 %+.4f  δp2p %0.3f%%"
              % (key, rms, amp10, float(np.mean(A[mA])), float(np.mean(dl[tt >= 20.0])),
                 100 * float(np.ptp(dl[tt >= 20.0]))), flush=True)
        out["y_" + key] = y; out["amp_" + key] = A; out["es_" + key] = dl
    np.savez("_wave_t_cmp_600.npz", t=tt, **out)
    print("saved _wave_t_cmp_600.npz")
