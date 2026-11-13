# -*- coding: utf-8 -*-
"""run_fault_sweep.py —— 故障模型参数扫描：κ / e / β

固定 600 rpm、8 s、实验室噪声、RC 开（T_adapt=True）、不加载型线；
每个工况只加载一个故障模型，统计 7–8 s 的 10 Hz 转速分量与稳态 RMS。

2026-11-13 口径（定稿台架，默认）：
  J_TRUE  : 主循环真实传动链惯量（默认 4.81e-5 = 2.545 J_nom，小圆盘定稿台架）
  ORACLE  : =1 时 j_oracle=True（b0 按真实 J 归一，J 自适应投运后的口径；默认 1）
  OUT     : 结果 json 名（默认 _fault_sweep.json）
  另：κ=1 纳入扫描，共 28 例。κ=1 时 10 Hz/rpm 与稳态 RMS/rpm：
      已投运（b0=J_true）0.51/6.49；未投运（b0=J_nom）1.92/12.04。
  应力测试（大圆盘 5.26 J_nom）与未投运对照：
      J_TRUE=9.95e-5 ORACLE=0 OUT=_fault_sweep_stress.json python run_fault_sweep.py
"""
import json
import math
import os
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from fault_torque import unbalance_torque, misalign_torque

N_REF = 600.0
DT, TEND = 2e-6, 8.0
SEED = 20261018
J_M = 1.89e-5
J_TRUE = float(os.environ.get("J_TRUE", "4.81e-5"))
OUT = os.environ.get("OUT", "_fault_sweep.json")
ORACLE = os.environ.get("ORACLE", "1") == "1"
M_ROT = 0.1
BETA1 = math.radians(1.0)
L_CM = 0.05
OMEGA = 2 * math.pi * N_REF / 60.0


def T1_analytic(kind, **p):
    if kind == "unb":
        return M_ROT * 9.80665 * p["e"] * p["kappa"]
    return M_ROT * 9.80665 * L_CM * math.sin(p["beta"]) * p["kappa"]


CASES = []
for K in (1, 50, 100, 200, 300, 450, 580, 800, 1000):
    CASES.append(("unb_k%d" % K, "unb", dict(M=M_ROT, e=1e-4, kappa=float(K))))
for E in (5e-5, 1e-4, 2e-4, 5e-4, 1e-3):
    CASES.append(("unb_e%.0fum" % (E * 1e6), "unb", dict(M=M_ROT, e=E, kappa=300.0)))
for K in (10, 20, 50, 67, 100, 200, 400, 600):
    CASES.append(("mis_k%d" % K, "mis", dict(M=M_ROT, beta=BETA1, l=L_CM, kappa=float(K))))
for BD in (0.5, 1.0, 2.0, 4.0, 8.0, 15.0):
    CASES.append(("mis_b%.1fdeg" % BD, "mis", dict(M=M_ROT, beta=math.radians(BD), l=L_CM, kappa=20.0)))


def one(case):
    from pmsm_inv_sim import sim_inv
    key, kind, p = case
    t = np.arange(0.0, TEND, DT)
    TL = np.zeros_like(t)
    cfg = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3, J_true=J_TRUE,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=SEED,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
               j_oracle=ORACLE,
               tl_fault={"start": 0.0, "unbalance" if kind == "unb" else "misalign": p})
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * N_REF
    m = tt >= 7.0
    tc, ec = tt[m], e[m]
    a1 = 2.0 * np.mean(ec * np.cos(2 * np.pi * 10.0 * tc))
    b1 = 2.0 * np.mean(ec * np.sin(2 * np.pi * 10.0 * tc))
    amp = float(np.hypot(a1, b1))
    rms = float(np.sqrt(np.mean(ec ** 2)))
    T1 = T1_analytic(kind, **p)
    print("%-12s T1 %.4f N·m  10Hz %6.2f rpm  RMS %6.2f  iq %5.2f"
          % (key, T1, amp, rms, float(np.max(np.abs(iq)))), flush=True)
    return key, dict(kind=kind, T1=T1, amp10=amp, rms=rms,
                     iq=float(np.max(np.abs(iq))), J_true=J_TRUE,
                     J_ratio=J_TRUE / J_M, j_oracle=bool(ORACLE),
                     **{k: v for k, v in p.items()})


if __name__ == "__main__":
    print("J_true=%.4e  j_oracle=%s  n_cases=%d  out=%s"
          % (J_TRUE, ORACLE, len(CASES), OUT), flush=True)
    with Pool(5) as pool:
        res = pool.map(one, CASES)
    out = dict(res)
    out["_meta"] = dict(J_true=J_TRUE, J_nom=J_M, J_ratio=J_TRUE / J_M,
                        j_oracle=bool(ORACLE), n_cases=len(CASES), protocol="600 rpm, 8 s, lab noise, RC on")
    json.dump(out, open(OUT, "w"), indent=1)
    print("done")
