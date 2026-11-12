# -*- coding: utf-8 -*-
"""run_t_es_ff.py —— 解冻时理论值前馈重置的验证（600→300）"""
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from tl_profile import disc_unbalance_profile
from run_t_es_speedstep import build, T_STEP, N_REF, N2, AMP

CASES = [("A_ff", dict(T_es=True, es_ff=True)),
         ("B_ff_nofreeze", dict(T_es=True, es_ff=True, es_freeze=0.0)),
         ("C_frozen", dict(T_es=True, es_ff=False)),
         ("D_fix12", dict(T_es=False, es_d0=-0.12, es_step=0.0, es_dith=0.0))]


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kw = job
    t, TL = build()
    cfg = dict(n_ref=N_REF, n_ref2=N2, t_nref=T_STEP, T_adapt=True, T_filt=50e-3,
               T=0.1, fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3,
               seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
               tl_ang_start=2.01868,
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
               es_d0=-0.143, es_dith=0.005, es_step=0.01, es_Pd=1.5, es_N=3,
               es_dead=1e-5, es_dmax=0.20, es_t0=3.0, es_freeze=2.0)
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"])
    yref = np.where(tt >= T_STEP, N2 / N_REF, 1.0)
    e = (np.asarray(Y["y"]) - yref) * N_REF
    dl = np.asarray(Y["es"]); A = np.asarray(Y["amp"])
    m1 = (tt >= 10.0) & (tt < 14.9)
    m2 = (tt >= 30.0)
    print("%-14s δ前 %+.4f  δ后 %+.4f  A后 %.5f  RMS后 %5.2f  RMS 15-20 %5.1f"
          % (key, float(np.mean(dl[m1])), float(np.mean(dl[m2])),
             float(np.mean(A[m2])), float(np.sqrt(np.mean(e[(tt >= 35.0)] ** 2))),
             float(np.sqrt(np.mean(e[(tt >= 15.5) & (tt < 20.0)] ** 2)))), flush=True)
    np.savez("_wave_ss2_%s.npz" % key, t=tt, y=Y["y"], es=dl, amp=A)


if __name__ == "__main__":
    with Pool(2) as p:
        p.map(one, CASES)
    print("done")
