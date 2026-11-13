# -*- coding: utf-8 -*-
"""run_j_comm.py —— 调试期（0–2 s）转矩注入辨识 J，冻结后应用 b0"""
import json, math
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC

JM, JB = 1.89e-5, 9.95e-5
CASES = [
    ("big_fault", dict(J_true=JB, fault=True)),
    ("big_oracle", dict(J_true=JB, fault=True, j_oracle=True)),
    ("big_comm", dict(J_true=JB, fault=True, comm=True)),
    ("big_comm_nf", dict(J_true=JB, comm=True)),
]
def one(job):
    from pmsm_inv_sim import sim_inv
    key, o = job
    t = np.arange(0.0, 10.0, 2e-6); TL = np.zeros_like(t)
    cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0, J_true=o["J_true"])
    if o.get("fault"):
        cfg["tl_fault"] = {"start": 0.0, "unbalance": dict(M=0.1, e=1e-4, kappa=580.0)}
    if o.get("j_oracle"): cfg.update(j_oracle=True)
    if o.get("comm"):
        cfg.update(j_id=True, j_id_f=100.0, j_id_amp_u=0.157, j_id_win=0.2,
                   j_id_lp=0.4, j_id_tend=2.0, j_adapt_b0=True)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 600.0
    def amp(f, a, b):
        m = (tt >= a) & (tt < b); tc, ec = tt[m], e[m]
        return float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*f*tc)), 2*np.mean(ec*np.sin(2*np.pi*f*tc))))
    a10 = amp(10, 9, 10); a100_id = amp(100, 0.5, 2.0); a100_post = amp(100, 9, 10)
    rms = float(np.sqrt(np.mean(e[(tt >= 9) & (tt < 10)]**2)))
    jh = np.asarray(Y.get("jhat", [])); jfin = float(jh[-1]) if jh.size else float("nan")
    print("%-11s 10Hz %6.2f  100Hz(id) %5.2f  100Hz(post) %5.2f  RMS %6.2f  iq %5.2f  Jhat %.2e"
          % (key, a10, a100_id, a100_post, rms, float(np.max(np.abs(iq))), jfin), flush=True)
    return key, dict(a10=a10, a100_id=a100_id, a100_post=a100_post, rms=rms,
                     iq=float(np.max(np.abs(iq))), jfin=jfin)
if __name__ == "__main__":
    with Pool(4) as p: res = p.map(one, CASES)
    json.dump(dict(res), open("_j_comm.json","w"), indent=1); print("done")
