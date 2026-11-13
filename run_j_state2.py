# -*- coding: utf-8 -*-
"""run_j_state2.py —— 更保守的门限：t0=1.0、nmin=5"""
import json
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC

JB = 9.95e-5
CASES = [("norm_n5", dict(T1=0.057, fault=True)), ("nofault_n5", dict(T1=0.0, fault=False))]
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
               j_id=True, j_id_f=100.0, j_id_amp_u=0.157, j_id_win=0.2,
               j_id_lp=0.4, j_id_t0=1.0, j_id_tend=3.0, j_adapt_b0=True,
               j_id_snr_min=2.0, j_id_nmin=5, j_id_std_max=0.15)
    if o["fault"]:
        cfg["tl_fault"] = {"start": 0.0, "unbalance": dict(M=0.1, e=1e-4, kappa=581.0)}
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 600.0
    m = (tt >= 9) & (tt < 10); tc, ec = tt[m], e[m]
    a10 = float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*tc)), 2*np.mean(ec*np.sin(2*np.pi*10*tc))))
    js = np.asarray(Y["jstate"]); jh = np.asarray(Y["jhat"])
    print("%-11s state=%d Jhat=%.2e 10Hz %6.2f iq %5.2f" % (key, int(js[-1]), float(jh[-1]), a10, float(np.max(np.abs(iq)))), flush=True)
    return key, dict(state=int(js[-1]), jfin=float(jh[-1]), a10=a10, iq=float(np.max(np.abs(iq))))
if __name__ == "__main__":
    with Pool(2) as p: res = p.map(one, CASES)
    json.dump(dict(res), open("_j_state2.json","w"), indent=1); print("done")
