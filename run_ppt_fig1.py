# -*- coding: utf-8 -*-
"""run_ppt_fig1.py —— PPT 图 1：同一故障工况下 纯 ESO vs 无自适应 RCESO（均用类 fal 增益）

工况（实验室档）：
    额定 600 rpm（10 Hz 机械转频），实验室噪声 3 rpm / 0.1 A / 0.01 N·m
    0–2 s   空载
    2–8 s   加载 0.50 额定（0.3185 N·m）
    2–8 s   叠加**角度锁相**周期分量：T(φ)=A[sinφ+0.4sin3φ+0.2sin5φ]，T(φ)=T(φ+2π)，dφ/dt=ω，A=0.1 N·m

两档（ESO 增益均为类 fal 默认档 a=0.75, δ=0.10, λ=10）：
    纯 ESO   : beta3 = 0（重复通道关闭）
    无自适应 RCESO : beta3 = 4000、Q0 = 0.98、τ0 = 20 ms 固定（无 Q/τ 自适应、无律 D、无 F-B）

输出：_ppt_fig1.npz（t / TL / y_eso / y_rceso / iq_* / iqr_*）、_ppt_fig1.json
"""
import json
import math

import numpy as np

from pmsm_inv_sim import sim_inv
import noise_cfg as NC

DT, TEND, TL0 = 2e-6, 8.0, 2.0
N_REF = 600.0
AMP_ANG = 0.1
T_RATED = 0.637
NPROF = 4096


def profile_unit():
    ph = np.linspace(0.0, 2 * math.pi, NPROF, endpoint=False)
    f = np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph)
    return f / np.max(np.abs(f))


CASES = [("eso", "纯 ESO", dict(beta3=0.0)),
         ("rceso", "无自适应 RCESO", dict(beta3=4000.0, Q0=0.98, tau0=20e-3))]


def main():
    t = np.arange(0.0, TEND, DT)
    TL = (0.50 * (t >= TL0)).astype(float) * T_RATED
    base = dict(n_ref=N_REF, T=0.1, fci=500.0,
                i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
                sig_n=NC.NOISE_LAB["sig_n_rpm"],
                sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
                seed_i=20261018,
                tl_ang=profile_unit(), tl_ang_amp=AMP_ANG, tl_ang_start=TL0,
                eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
    out = {}
    meta = {}
    for key, label, kw in CASES:
        Y = sim_inv(t, TL, dict(base, **kw))
        tt = Y["t"]
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
    np.savez("_ppt_fig1.npz", **out)
    json.dump(dict(n_ref=N_REF, amp_ang=AMP_ANG, fci=500.0, cases=meta),
              open("_ppt_fig1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
