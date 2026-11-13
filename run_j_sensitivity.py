# -*- coding: utf-8 -*-
"""run_j_sensitivity.py —— 真实 J 对故障转矩→转速纹波映射的影响

每个 J_true 下：无故障、T1=0.0569（κ=580）、T1=0.1138（κ=1160）三档。
ESO 的 b0 仍由 J_M=1.89e-5 标称给出（与 J_true 解耦）。
"""
import json, math
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC

JM = 1.89e-5
RATIOS = [1, 2, 5, 10, 20, 40]
KAPPAS = [0.0, 580.0, 1160.0]
CASES = [(r, k) for r in RATIOS for k in KAPPAS]

def one(job):
    from pmsm_inv_sim import sim_inv
    ratio, K = job
    t = np.arange(0.0, 8.0, 2e-6); TL = np.zeros_like(t)
    cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
               J_true=JM * ratio)
    if K > 0:
        cfg["tl_fault"] = {"start": 0.0, "unbalance": dict(M=0.1, e=1e-4, kappa=K)}
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 600.0; m = tt >= 7.0; tc, ec = tt[m], e[m]
    a1 = 2*np.mean(ec*np.cos(2*np.pi*10*tc)); b1 = 2*np.mean(ec*np.sin(2*np.pi*10*tc))
    amp = float(np.hypot(a1, b1)); rms = float(np.sqrt(np.mean(ec**2)))
    T1 = 0.1*9.80665*1e-4*K
    print("J/Jm=%2d K=%4.0f T1=%.4f  10Hz %6.2f  RMS %6.2f  iq %5.2f"
          % (ratio, K, T1, amp, rms, float(np.max(np.abs(iq)))), flush=True)
    return dict(ratio=ratio, K=K, T1=T1, amp10=amp, rms=rms,
                iq=float(np.max(np.abs(iq))), Jv=JM*ratio)

if __name__ == "__main__":
    with Pool(6) as p: res = p.map(one, CASES)
    json.dump(res, open("_j_sens.json","w"), indent=1); print("done")
