# -*- coding: utf-8 -*-
"""run_tau_fft.py —— tau=20ms 与 10ms 的稳态频谱（找极限环主频）"""
import math
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from run_laws_compare import build_loads, N_REF, AMP, ANG_START, TW
from tl_profile import disc_unbalance_profile

CASES = [(0.020, -0.143), (0.010, -0.089)]


def one(job):
    from pmsm_inv_sim import sim_inv
    tau, d0 = job
    t, TL = build_loads()
    cfg = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=tau, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
               tl_ang_start=ANG_START, tl_ang_rev=TW,
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               T_es=True, es_d0=d0, es_step=0.0, es_dith=0.0)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"])
    np.savez("_tau_fft_%04d.npz" % int(tau * 1e5), t=tt, y=y)
    return tau


if __name__ == "__main__":
    with Pool(2) as p:
        p.map(one, CASES)
    print("done")
