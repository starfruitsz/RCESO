# -*- coding: utf-8 -*-
"""空载段差异的多噪声种子复核：纯 ESO vs 无自适应 RCESO（同一负载噪声实现，成对比较）"""
from multiprocessing import Pool

import numpy as np
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
from tl_profile import disc_unbalance_profile

DT, TEND, TL0 = 2e-6, 8.0, 2.0
N_REF = 600.0
AMP = 0.1
SEEDS = [20261017, 20261019, 20261023, 20261027]


def one(job):
    key, beta3, seedT = job
    t = np.arange(0.0, TEND, DT)
    TL = (0.50 * (t >= TL0)).astype(float) * 0.637
    cfg = dict(n_ref=N_REF, T=0.1, fci=500.0, beta3=beta3,
               Q0=0.98, tau0=20e-3,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               seed_i=20261018, seed_T=seedT, seed_n=20261018,
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP, tl_ang_start=TL0,
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
    m0 = (tt >= 1.0) & (tt < 2.0)
    m1 = (tt >= 5.0) & (tt < 6.0)
    return (key, seedT,
            float(np.sqrt(np.mean(e[m0]**2))),      # 空载 RMS
            float(np.sqrt(np.mean(e[m1]**2))))      # 故障段 RMS


if __name__ == "__main__":
    jobs = [(k, b, s) for s in SEEDS for (k, b) in (("eso", 0.0), ("rceso", 4000.0))]
    with Pool(8) as p:
        rows = p.map(one, jobs)
    by = {}
    for k, s, n0, n1 in rows:
        by.setdefault(s, {})[k] = (n0, n1)
    print("seed_T     空载ESO  空载RCESO  降幅    故障ESO  故障RCESO  降幅")
    for s in SEEDS:
        a = by[s]["eso"]; b = by[s]["rceso"]
        print("%d  %8.2f %9.2f %6.1f%%  %8.1f %9.1f %6.1f%%" % (
            s, a[0], b[0], 100*(1-b[0]/a[0]), a[1], b[1], 100*(1-b[1]/a[1])))
