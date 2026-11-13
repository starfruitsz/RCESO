# -*- coding: utf-8 -*-
"""run_fault_phys.py —— 物理可实现工况验证：M=2 kg，e=3 mm / β=3.4°"""
import json, math
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC

CASES = [
    ("phys_unb", {"unbalance": dict(M=2.0, e=3e-3, kappa=1.0)}),
    ("phys_mis", {"misalign": dict(M=2.0, beta=math.radians(3.4), l=0.05, kappa=1.0)}),
]
def one(job):
    from pmsm_inv_sim import sim_inv
    key, fault = job
    t = np.arange(0.0, 8.0, 2e-6); TL = np.zeros_like(t)
    cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
               tl_fault=dict(fault, start=0.0))
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 600.0; m = tt >= 7.0; tc, ec = tt[m], e[m]
    a1 = 2*np.mean(ec*np.cos(2*np.pi*10*tc)); b1 = 2*np.mean(ec*np.sin(2*np.pi*10*tc))
    amp = float(np.hypot(a1, b1)); rms = float(np.sqrt(np.mean(ec**2)))
    print("%-8s 10Hz %6.2f rpm  RMS %6.2f  iq %5.2f" % (key, amp, rms, float(np.max(np.abs(iq)))), flush=True)
    return key, dict(amp10=amp, rms=rms, iq=float(np.max(np.abs(iq))))
if __name__ == "__main__":
    with Pool(2) as p: res = p.map(one, CASES)
    json.dump(dict(res), open("_fault_phys.json","w"), indent=1); print("done")
