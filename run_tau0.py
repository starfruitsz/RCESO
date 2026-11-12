# -*- coding: utf-8 -*-
"""run_tau0.py —— 把低通时间常数直接设为 tau=0，并与 tau=2us 对照"""
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
CASES = ["load", "speed", "echo"]


def build():
    t = np.arange(0.0, TEND, DT)
    vib = np.zeros_like(t)
    for n, a in enumerate(VIB_H, start=1):
        vib += a * np.sin(2.0 * math.pi * F_VIB * n * (t - TL0) * (t >= TL0))
    TL = (0.50 * (t >= TL0)).astype(float) * 0.637 + VIB1 * vib
    return t, TL


def one(case):
    from pmsm_inv_sim import sim_inv
    t, TL = build()
    cfg = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=0.0, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
               tl_ang_start=2.01868, tl_ang_rev=(T_REV if case == "echo" else 1e9),
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
    if case == "speed":
        cfg.update(n_ref2=900.0, t_nref=5.0)
    Y = sim_inv(t, TL, cfg)
    y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    np.savez("_wave_lpf_%s_tau0.npz" % case, t=np.asarray(Y["t"]), y=y, iq=iq)
    d2 = np.load("_wave_lpf_%s_nolpf.npz" % case)
    dy = float(np.max(np.abs(y - d2["y"])))
    di = float(np.max(np.abs(iq - d2["iq"])))
    print("%-5s tau=0: iq_max %7.2f  A；与 tau=2us 的 max|dy| %.3e, max|diq| %.3e"
          % (case, float(np.max(np.abs(iq))), dy, di), flush=True)
    return case


if __name__ == "__main__":
    with Pool(3) as p:
        p.map(one, CASES)
    print("done")
