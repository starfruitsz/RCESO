# -*- coding: utf-8 -*-
"""_run_s6.py —— 重建 _ppt_fig1.npz（纯 ESO vs 无自适应 RCESO，三合一故障）。"""
import numpy as np
from multiprocessing import Pool
import noise_cfg as NC
from pmsm_inv_sim import sim_inv

TEND = 8.0
FAULT = dict(start=2.0,
             unbalance=dict(M=0.1, e=1e-4, kappa=580.0),
             misalign=dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0),
             parallel=dict(e=1e-4, dk=1.0e5, kappa=100.0))

def one(case):
    t = np.arange(0.0, TEND, 2e-6)
    TL = (0.5 * (t >= 2.0)).astype(float) * 0.637
    cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0, tl_fault=FAULT)
    if case == "eso":
        cfg.update(beta3=0.0, b3_min=0.0, b3_max=0.0)
    Y = sim_inv(t, TL, cfg)
    return case, np.asarray(Y["t"]), np.asarray(Y["y"]), np.asarray(Y["iq"]), np.asarray(Y["tl"])

if __name__ == "__main__":
    with Pool(2) as p:
        res = p.map(one, ["eso", "rceso"])
    out = {"t": res[0][1], "TL": res[0][4]}
    for case, tt, y, iq, tl in res:
        out["y_" + case] = y
        out["iq_" + case] = iq
    np.savez("_ppt_fig1.npz", **out)
    print("saved _ppt_fig1.npz", [r[0] for r in res], flush=True)
