# -*- coding: utf-8 -*-
"""run_lpf_cmp.py —— 无自适应 RCESO：有低通（tau=20 ms）vs 无低通（tau=dt）

三个工况（各自独立 8 s 仿真，600 rpm、实验室噪声、fci=500 Hz、beta3=4000、Q=0.98、种子 20261018）：
  A 负载突变：2 s 加载 0.50 额定 + 圆盘型线 V2 + 5.9 Hz 振动
  B 参考转速突变：同 A，并在 5 s 把参考 600 -> 900 rpm
  C 回声重影：同 A，并在 5.98361 s 把型线整体反相（零交越）
输出：_wave_lpf_<case>_<cfg>.npz（t, y, iq）
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

CFG = [("lpf", 20e-3), ("nolpf", 2e-6)]
CASES = ["load", "speed", "echo"]


def build():
    t = np.arange(0.0, TEND, DT)
    vib = np.zeros_like(t)
    for n, a in enumerate(VIB_H, start=1):
        vib += a * np.sin(2.0 * math.pi * F_VIB * n * (t - TL0) * (t >= TL0))
    TL = (0.50 * (t >= TL0)).astype(float) * 0.637 + VIB1 * vib
    return t, TL


def one(job):
    from pmsm_inv_sim import sim_inv
    case, (ck, tau) = job
    t, TL = build()
    cfg = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=tau, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
               tl_ang_start=2.01868, tl_ang_rev=(T_REV if case == "echo" else 1e9),
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
    if case == "speed":
        cfg.update(n_ref2=900.0, t_nref=5.0)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    np.savez("_wave_lpf_%s_%s.npz" % (case, ck), t=tt, y=y, iq=iq)
    e = (y - 1.0) * N_REF
    if case == "load":
        m = (tt >= 1.9) & (tt <= 2.5)
        print("%-5s %-5s dip %9.1f stepRMS %8.1f" % (case, ck, float(np.min(e[m])),
                                                     float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2)))), flush=True)
    elif case == "speed":
        spd = y * N_REF
        m = tt >= 5.0
        print("%-5s %-5s over %9.1f settle %8.1f ms iq %8.1f" % (
            case, ck, float(np.max(spd[m] - 900.0)),
            float((tt[np.where((np.abs(spd - 900.0) <= 20.0) & m)[0][0]] - 5.0) * 1e3),
            float(np.max(np.abs(iq)))), flush=True)
    else:
        m = (tt >= 6.0) & (tt <= 6.2)
        print("%-5s %-5s echo |e|max %9.1f echoRMS %9.1f iq %8.1f" % (
            case, ck, float(np.max(np.abs(e[m]))), float(np.sqrt(np.mean(e[m] ** 2))),
            float(np.max(np.abs(iq)))), flush=True)
    return case + "_" + ck


if __name__ == "__main__":
    jobs = [(c, cfg) for c in CASES for cfg in CFG]
    with Pool(6) as p:
        p.map(one, jobs)
    print("done")
