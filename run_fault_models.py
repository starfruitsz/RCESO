# -*- coding: utf-8 -*-
"""run_fault_models.py —— 故障转矩模型接入验证（附录 A/B 的解析式）

600 rpm、8 s、实验室噪声、fci=500 Hz、类 fal ESO、T_adapt=True；
不加载 tl_ang 型线，只加载 tl_fault（unbalance / misalign）。
"""
import json
import math
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from fault_torque import unbalance_torque, misalign_torque

N_REF = 600.0
DT, TEND = 2e-6, 8.0
SEED = 20261018
M_ROT = 0.1          # 转子当量质量 kg
E_UNB = 1e-4         # 偏心距 0.1 mm
BETA = math.radians(1.0)
L_CM = 0.05          # 质心到交点 50 mm
KAPPA_UNB = 580.0    # 等效放大：0.1*9.81*1e-4*580 ≈ 0.0569 N·m
KAPPA_MIS = 67.0     # 等效放大：0.1*9.81*0.05*sin(1°)*67 ≈ 0.0573 N·m

CASES = [
    ("base", None),
    ("unb_phys", {"unbalance": dict(M=M_ROT, e=E_UNB, kappa=1.0)}),
    ("unb_eq", {"unbalance": dict(M=M_ROT, e=E_UNB, kappa=KAPPA_UNB)}),
    ("mis_phys", {"misalign": dict(M=M_ROT, beta=BETA, l=L_CM, kappa=1.0)}),
    ("mis_eq", {"misalign": dict(M=M_ROT, beta=BETA, l=L_CM, kappa=KAPPA_MIS)}),
]


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
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0)
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
    print("%-9s 10Hz %6.2f rpm  RMS %6.2f  iqmax %5.2f" % (key, amp10, rms,
          float(np.max(np.abs(iq)))), flush=True)
    return key, dict(amp10=amp10, rms=rms, iqmax=float(np.max(np.abs(iq))))


if __name__ == "__main__":
    with Pool(5) as p:
        res = p.map(one, CASES)
    json.dump({k: v for k, v in res}, open("_fault_models.json", "w"), indent=1)
    # 解析幅值（1× 重力项）
    print("analytic 1x: unb_phys %.3e  unb_eq %.3e  mis_phys %.3e  mis_eq %.3e N·m"
          % (M_ROT * 9.80665 * E_UNB, M_ROT * 9.80665 * E_UNB * KAPPA_UNB,
             M_ROT * 9.80665 * L_CM * math.sin(BETA),
             M_ROT * 9.80665 * L_CM * math.sin(BETA) * KAPPA_MIS))
    print("done")
