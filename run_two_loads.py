# -*- coding: utf-8 -*-
"""run_two_loads.py —— 类 fal 档：两组负载对照（区分“周期/振动单独作用”与“叠加阶跃”）

两组都用类 fal 默认档（a=0.75, delta=0.10, lam=10），参数与噪声完全相同。
周期分量与 5.9 Hz 振动都在 2 s 起投入（都从零值切入，无附加跳变）。

工况 1（事件组）：0.5 额定阶跃（2.0 s）+ 周期分量（2 s 零交越）+ 5.9 Hz 振动（2 s）
                 + 负载噪声；5.982 s 周期分量整体反相 → 回声
工况 2（对照组）：0.5 额定基载自 t=0 起恒定（无阶跃事件）+ 同样的周期分量与振动（2 s 起）
                 + 同样负载噪声；无反相

噪声：3 rpm / 0.1 A；fci=500 Hz、β₃=4000、τ₀=20 ms、种子 20261018。
输出：_wave_two_A.npz、_wave_two_B.npz
"""
import math

import numpy as np

import noise_cfg as NC
from pmsm_inv_sim import sim_inv
from tl_profile import HARMONICS, THD, disc_unbalance_profile

N_REF = 600.0
DT, TEND = 2e-6, 8.0
SEED = 20261018
AMP = 0.095
F_VIB, VIB1 = 5.9, 0.03
VIB_H = tuple([1.0] + [(0.40 / THD) * x for x in HARMONICS[1:]])

t = np.arange(0.0, TEND, DT)

CASES = dict(
    A=dict(name="工况1", step=0.50, t_step=2.0, ang_start=2.01868, rev=5.98361, vib_start=2.0),
    B=dict(name="工况2", step=0.50, t_step=0.0, ang_start=2.02249, rev=None, vib_start=2.0),
)

for key, c in CASES.items():
    # 5.9 Hz 振动：相位以投入时刻为零点，保证切入时值连续
    tau_v = np.maximum(t - c["vib_start"], 0.0)
    vib = np.zeros_like(t)
    for n, a in enumerate(VIB_H, start=1):
        vib += a * np.sin(2.0 * math.pi * F_VIB * n * tau_v)
    vib = VIB1 * vib * (t >= c["vib_start"]).astype(float)
    TL = c["step"] * 0.637 * (t >= c["t_step"]).astype(float) + vib
    kw = dict(n_ref=N_REF, T=1.0 / 10.0, T_adapt=True, T_filt=50e-3,
              i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
              sig_n=NC.NOISE_LAB["sig_n_rpm"],
              sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
              fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=SEED, det_eps=0.0,
              tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
              tl_ang_start=c["ang_start"],
              eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
    if c["rev"] is not None:
        kw["tl_ang_rev"] = c["rev"]
    Y = sim_inv(t, TL, kw)
    tt = np.asarray(Y["t"]); TLapp = np.asarray(Y["tl"])
    np.savez("_wave_two_%s.npz" % key, t=tt, TL=TLapp, y=Y["y"], iq=Y["iq"],
             id=Y["id"], tw=(c["rev"] if c["rev"] is not None else 0.0),
             ang_start=c["ang_start"], vib_start=c["vib_start"])
    e = (Y["y"] - 1.0) * N_REF
    seg = (tt >= 2.30) & (tt < 5.95)
    print("%s %-5s dip %7.1f  steady %5.2f  TL 峰峰 %5.3f N·m"
          % (key, c["name"], float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])),
             float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))),
             float(TLapp[seg].max() - TLapp[seg].min())), flush=True)
print("done")
