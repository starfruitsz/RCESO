# -*- coding: utf-8 -*-
"""run_case_eso_rceso.py —— 纯 ESO vs 无自适应 RCESO（振动 + 阶跃 + 周期负载）

工况（实验室档，600 rpm / 10 Hz）：
    0–2 s   空载
    2–8 s   0.50 额定阶跃（0.3185 N·m）
    2–8 s   T(θ) 角度锁相周期分量：1–6 次 (1.00, 0.39, 0.06, 0.33, 0.09, 0.27)，
            THD 58.79%，峰值 0.095 N·m（峰峰 0.19）；2.0187 s 零交越投入
    2–8 s   5.9 Hz 振动：基波 0.03 N·m、THD 40%（1–6 次同族），相位以 2 s 为零点
    全段    负载噪声 0.01 N·m / 200 Hz；转速噪声 3 rpm；dq 电流噪声 0.1 A
    fci = 500 Hz；ESO 增益均取类 fal 默认档（a=0.75, δ=0.10, λ=10）

两档：纯 ESO（β₃=0）/ 无自适应 RCESO（β₃=4000、Q₀=0.98、τ₀=20 ms 固定）
输出：_case_eso_rceso.npz、_case_eso_rceso.json
"""
import json
import math

import numpy as np

import noise_cfg as NC
from pmsm_inv_sim import sim_inv
from tl_profile import HARMONICS, THD, MODE_NAME, disc_unbalance_profile

DT, TEND, TL0 = 2e-6, 8.0, 2.0
N_REF = 600.0
T_RATED = 0.637
AMP_ANG = 0.095
ANG_START = 2.01868
F_VIB, VIB1 = 5.9, 0.03
VIB_H = tuple([1.0] + [(0.40 / THD) * x for x in HARMONICS[1:]])

CASES = [("eso", "纯 ESO", dict(beta3=0.0)),
         ("rceso", "无自适应 RCESO", dict(beta3=4000.0, Q0=0.98, tau0=20e-3))]


def main():
    t = np.arange(0.0, TEND, DT)
    tau_v = np.maximum(t - TL0, 0.0)
    vib = np.zeros_like(t)
    for n, a in enumerate(VIB_H, start=1):
        vib += a * np.sin(2.0 * math.pi * F_VIB * n * tau_v)
    TL = (0.50 * (t >= TL0)).astype(float) * T_RATED + VIB1 * vib * (t >= TL0)

    base = dict(n_ref=N_REF, T=0.1, fci=500.0,
                i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
                sig_n=NC.NOISE_LAB["sig_n_rpm"],
                sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
                seed_i=20261018,
                tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP_ANG,
                tl_ang_start=ANG_START,
                eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
    out = {}
    meta = {}
    for key, label, kw in CASES:
        Y = sim_inv(t, TL, dict(base, **kw))
        tt = np.asarray(Y["t"])
        e = (Y["y"] - 1.0) * N_REF
        out["t"] = tt
        out["TL"] = Y["tl"]
        out["y_" + key] = Y["y"]
        out["iq_" + key] = Y["iq"]
        out["iqr_" + key] = Y["iqr"]
        m = (tt >= 5.0) & (tt < 6.0)
        meta[key] = dict(label=label,
                         steady_rms=round(float(np.sqrt(np.mean(e[m] ** 2))), 2),
                         iq_std=round(float(np.std(Y["iq"][m])), 3),
                         iq_max=round(float(np.max(np.abs(Y["iq"][m]))), 2),
                         iqr_max=round(float(np.max(np.abs(Y["iqr"][m]))), 2),
                         beta3=kw["beta3"])
        print(key, meta[key], flush=True)
    np.savez("_case_eso_rceso.npz", **out)
    json.dump(dict(mode=MODE_NAME, harmonics=list(HARMONICS), thd=round(THD, 6),
                   vib=dict(f=F_VIB, amp=VIB1,
                            thd=round(math.sqrt(sum(a * a for a in VIB_H[1:])) / VIB_H[0], 4)),
                   amp_ang=AMP_ANG, ang_start=ANG_START,
                   n_ref=N_REF, fci=500.0, cases=meta),
              open("_case_eso_rceso.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
