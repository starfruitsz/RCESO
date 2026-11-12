# -*- coding: utf-8 -*-
"""run_uz1_cmp.py —— 控制律比例项：r-y（现用） vs r-z1（新式）

三工况（负载突变 / 参考转速突变 / 回声）各 8 s，600 rpm、实验室噪声、fci=500 Hz、
beta3=4000、Q=0.98、tau=20 ms、类 fal ESO、种子 20261018、无律D/ESC。
"""
import math
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from tl_profile import disc_unbalance_profile

DT, TEND, TL0 = 2e-6, 8.0, 2.0
N_REF, AMP = 600.0, 0.095
F_VIB, VIB1 = 5.9, 0.03
VIB_H = (1.0, 0.2654, 0.0408, 0.2245, 0.0612, 0.1837)
T_REV = 5.98361


def build():
    t = np.arange(0.0, TEND, DT)
    vib = np.zeros_like(t)
    for n, a in enumerate(VIB_H, start=1):
        vib += a * np.sin(2.0 * math.pi * F_VIB * n * (t - TL0) * (t >= TL0))
    TL = (0.50 * (t >= TL0)).astype(float) * 0.637 + VIB1 * vib
    return t, TL


def one(job):
    from pmsm_inv_sim import sim_inv
    case, tag, uz = job
    t, TL = build()
    cfg = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
               tl_ang_start=2.01868, tl_ang_rev=(T_REV if case == "echo" else 1e9),
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               u_z1=uz)
    if case == "speed":
        cfg.update(n_ref2=900.0, t_nref=5.0)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * N_REF
    spd = y * N_REF
    if case == "load":
        m = (tt >= 1.9) & (tt <= 2.5)
        msg = "dip %8.1f stepRMS %7.1f" % (float(np.min(e[m])),
                                           float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))))
    elif case == "speed":
        m = tt >= 5.0
        e2 = spd - 900.0
        idx = np.where((np.abs(e2) <= 20.0) & m)[0]
        msg = "over %8.1f settle %6.1f ms" % (float(np.max(e2[m])),
                                              float((tt[idx[0]] - 5.0) * 1e3))
    else:
        m = (tt >= 6.0) & (tt <= 6.2)
        msg = "echoPeak %8.1f echoRMS %8.1f" % (float(np.max(np.abs(e[m]))),
                                                float(np.sqrt(np.mean(e[m] ** 2))))
    print("%-5s %-3s %s  iq %6.2f  max|spd| %7.1f" % (case, tag, msg,
          float(np.max(np.abs(iq))), float(np.max(np.abs(spd)))), flush=True)
    np.savez("_wave_uz1_%s_%s.npz" % (case, tag), t=tt, y=y, iq=iq)
    return case + tag


if __name__ == "__main__":
    jobs = [(c, t, u) for c in ("load", "speed", "echo") for t, u in (("y", False), ("z1", True))]
    with Pool(6) as p:
        p.map(one, jobs)
    print("done")
