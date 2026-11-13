# -*- coding: utf-8 -*-
import numpy as np
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
import sys
lam = float(sys.argv[1]) if len(sys.argv)>1 else 0.99
R = float(sys.argv[2]) if len(sys.argv)>2 else 1e-3
t = np.arange(0.0, 10.0, 2e-6); TL = np.zeros_like(t)
cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
           beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
           rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0, J_true=9.95e-5,
           tl_fault={"start": 0.0, "unbalance": dict(M=0.1, e=1e-4, kappa=580.0)},
           j_ako=True, j_ako_lam=lam, j_ako_R=R)
Y = sim_inv(t, TL, cfg)
tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
e = (y - 1.0) * 600.0
m = (tt >= 9.0) & (tt < 10.0); tc, ec = tt[m], e[m]
a10 = float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*tc)), 2*np.mean(ec*np.sin(2*np.pi*10*tc))))
rms = float(np.sqrt(np.mean(ec**2)))
jh = np.asarray(Y.get("jhat", [])); jfin = float(jh[-1]) if jh.size else float("nan")
print("lam=%.3f R=%.1e a10 %.2f rms %.2f iq %.2f jfin %.3e (+%.1f%%)" % (lam, R, a10, rms, float(np.max(np.abs(iq))), jfin, 100*(jfin/9.95e-5-1)), flush=True)
np.savez("_wave_j_big_ako_l%.3f_R%.0e.npz" % (lam, R), t=Y["t"], y=Y["y"], iq=Y["iq"],
         jhat=Y.get("jhat", np.array([])), t_j=Y.get("t_j", np.array([])))
