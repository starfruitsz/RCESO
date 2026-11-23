# -*- coding: utf-8 -*-
"""run_b0_ppt.py —— PPT s16：b0 自适应（不对中+圆盘不平衡，600 rpm，10 s）"""
import json
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC
from pmsm_inv_sim import sim_inv

TEND, NREF = 10.0, 600.0
FAULT = {"start": 0.0,
         "unbalance": dict(M=0.1, e=1e-4, kappa=580.0),
         "misalign": dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0),
         "parallel": dict(e=1e-4, dk=1.0e5, kappa=100.0)}
CASES = [("fixed", dict()), ("adapt", dict(j_id=True, j_id_f=100.0, j_id_amp_u=0.157,
          j_id_win=0.2, j_id_lp=0.4, j_id_tend=2.0, j_adapt_b0=True, j_val=False)),
         ("oracle", dict(j_oracle=True))]

def one(job):
    key, kw = job
    t = np.arange(0.0, TEND, 2e-6); TL = np.zeros_like(t)
    cfg = dict(n_ref=NREF, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
               J_true=9.95e-5, tl_fault=FAULT)
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    np.savez("_wave_b0_%s.npz" % key, t=tt[::100], y=y[::100], iq=iq[::100],
             b0e=np.asarray(Y["b0e"])[::100], jhat=np.asarray(Y["jhat"])[::100],
             t_j=np.asarray(Y["t_j"]))
    m = (tt >= 9.0) & (tt < 10.0); e = (y[m]-1.0)*NREF; tc = tt[m]
    a10 = float(np.hypot(2*np.mean(e*np.cos(2*np.pi*10*tc)), 2*np.mean(e*np.sin(2*np.pi*10*tc))))
    return key, dict(a10=a10, rms=float(np.sqrt(np.mean(e**2))), iq=float(np.max(np.abs(iq))),
                     b0=float(np.asarray(Y["b0e"])[-1]), jhat=float(np.asarray(Y["jhat"])[-1]))

if __name__ == "__main__":
    with Pool(3) as p: res = p.map(one, CASES)
    print(res, flush=True)
    json.dump(dict(res), open("_b0_ppt.json","w"), indent=1)