# -*- coding: utf-8 -*-
"""run_j_fig.py —— 自适应对比图数据：big_fault / big_oracle / big_comm"""
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC

JM, JB = 1.89e-5, 9.95e-5
CASES = [("big_fault", dict(j_oracle=False, comm=False)),
         ("big_oracle", dict(j_oracle=True, comm=False)),
         ("big_comm", dict(j_oracle=False, comm=True))]

def one(job):
    from pmsm_inv_sim import sim_inv
    key, o = job
    t = np.arange(0.0, 10.0, 2e-6); TL = np.zeros_like(t)
    cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0, J_true=JB,
               tl_fault={"start": 0.0, "unbalance": dict(M=0.1, e=1e-4, kappa=580.0)})
    if o["j_oracle"]: cfg.update(j_oracle=True)
    if o["comm"]:
        cfg.update(j_id=True, j_id_f=100.0, j_id_amp_u=0.157, j_id_win=0.2,
                   j_id_lp=0.4, j_id_tend=2.0, j_adapt_b0=True)
    Y = sim_inv(t, TL, cfg)
    np.savez("_wave_j_%s.npz" % key, t=Y["t"], y=Y["y"], iq=Y["iq"],
             jhat=Y.get("jhat", np.array([])), t_j=Y.get("t_j", np.array([])))
    print(key, "saved", flush=True)
    return key

if __name__ == "__main__":
    with Pool(3) as p: p.map(one, CASES)
    print("done")
