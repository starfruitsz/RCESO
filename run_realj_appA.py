# -*- coding: utf-8 -*-
"""run_realj_appA.py —— 附录 A.9 / B.9 κ=1 标量验证在真实 J（4.81e-5=2.545 J_nom）+ j_oracle 下复算

协议逐项同 run_fault_models.py：600 rpm、8 s、实验室噪声、fci=500 Hz、类 fal ESO、
T_adapt=True、不加载 tl_ang 型线，只加载 tl_fault（unbalance / misalign，start=0）。
对照（J_nom 旧值，见 _fault_models.json）：
  base     1.247 rpm / 15.571 RMS
  unb_phys 1.088 rpm / 15.132 RMS   (M=0.1, e=1e-4, κ=1 → T1=9.8e-5 N·m)
  mis_phys 1.704 rpm / 14.902 RMS   (M=0.1, β=1°, l=0.05, κ=1 → T1=8.6e-4 N·m)
输出 _realj_appA.json
"""
import json
import math

import numpy as np

import noise_cfg as NC

N_REF = 600.0
DT, TEND = 2e-6, 8.0
SEED = 20261018
M_ROT = 0.1
E_UNB = 1e-4
BETA = math.radians(1.0)
L_CM = 0.05
J_TRUE = 4.81e-5
CASES = [("base", None),
         ("unb_phys", {"unbalance": dict(M=M_ROT, e=E_UNB, kappa=1.0)}),
         ("mis_phys", {"misalign": dict(M=M_ROT, beta=BETA, l=L_CM, kappa=1.0)})]


def one(job):
    from pmsm_inv_sim import sim_inv
    key, fault = job
    t = np.arange(0.0, TEND, DT)
    TL = np.zeros_like(t)
    cfg = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=SEED,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
               J_true=J_TRUE, j_oracle=True)
    if fault is not None:
        cfg["tl_fault"] = dict(fault, start=0.0)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * N_REF
    m = tt >= 7.0
    tc, ec = tt[m], e[m]
    a1 = 2.0 * np.mean(ec * np.cos(2 * np.pi * 10.0 * tc))
    b1 = 2.0 * np.mean(ec * np.sin(2 * np.pi * 10.0 * tc))
    amp10 = float(np.hypot(a1, b1))
    rms = float(np.sqrt(np.mean(ec ** 2)))
    n = 100
    iqa = np.abs(iq)
    iq1 = float(np.abs(iq[:len(iq) // n * n].reshape(-1, n).mean(axis=1)).max())
    print("%-9s 10Hz %6.2f rpm  RMS %6.2f  iq_raw %5.2f  iq1ms %5.2f"
          % (key, amp10, rms, float(iqa.max()), iq1), flush=True)
    return key, dict(amp10=amp10, rms=rms, iqmax=float(iqa.max()), iq1ms=iq1)


if __name__ == "__main__":
    import hashlib
    from multiprocessing import Pool
    sha = hashlib.sha256(open("pmsm_inv_sim.py", "rb").read()).hexdigest()
    with Pool(3) as p:
        res = p.map(one, CASES)
    out = dict(res)
    out["_meta"] = dict(J_true=J_TRUE, j_oracle=True, sim_sha256=sha,
                        old_Jnom=dict(base=[1.247, 15.571], unb_phys=[1.088, 15.132],
                                      mis_phys=[1.704, 14.902]))
    json.dump(out, open("_realj_appA.json", "w"), indent=1)
    print("done  sha=%s" % sha)
