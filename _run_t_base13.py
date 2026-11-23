# -*- coding: utf-8 -*-
"""_run_t_base13.py —— 图二配套：无律T 基线（与 run_t_dft.py / run_ppt5 s13_base 完全同配置）。"""
import numpy as np, json, sys, time
import noise_cfg as NC
from pmsm_inv_sim import sim_inv

mode = sys.argv[1] if len(sys.argv) > 1 else "none"
TEND = 30.0; DT = 2e-6
FAULT = dict(start=2.0,
             unbalance=dict(M=0.1, e=1e-4, kappa=580.0),
             misalign=dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0),
             parallel=dict(e=1e-4, dk=1.0e5, kappa=100.0))
t = np.arange(0.0, TEND, DT)
TL = (0.50 * (t >= 2.0)).astype(float) * 0.637
cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3,
           fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
           rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
           tl_fault=FAULT,
           T_es=True, es_d0=0.0, es_step=0.0, es_dith=0.0,
           es_Pd=1.5, es_N=3, es_dead=1e-5, es_dmax=0.20, es_t0=3.0)
t0 = time.time()
Y = sim_inv(t, TL, cfg)
el = time.time() - t0
np.savez("_tpair_%s.npz" % mode, t=Y["t"], y=Y["y"], iq=Y["iq"], tl=Y["tl"],
         amp=Y["amp"], es=Y["es"], b0e=Y["b0e"])
print("saved _tpair_%s.npz  (%.0fs)" % (mode, el), flush=True)
