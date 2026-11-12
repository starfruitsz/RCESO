# -*- coding: utf-8 -*-
"""run_two_loads_step.py —— 两组负载对照：只有实验组换速（600→300），对照组参考恒定

工况1（实验组）：0.5 额定阶跃（2 s）+ T(θ) 1–6 次 + 5.9 Hz 振动；**6.0 s 参考 600→300**
工况2（对照组）：0.5 额定恒载（0 s 起）+ 同样周期与振动；**参考恒为 600**
两组都开自适应 T = 2π/ω（50 ms 滤波）；对照组转速不变 ⇒ T 恒为 0.1 s。
输出：_wave_ts_{A,B}.npz
"""
import math
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from tl_profile import HARMONICS, THD, disc_unbalance_profile

DT, TEND, TL0, T_STEP = 2e-6, 8.0, 2.0, 6.0
N_REF, N2 = 600.0, 300.0
AMP = 0.095
ANG_START = 2.01868
F_VIB, VIB1 = 5.9, 0.03
VIB_H = tuple([1.0] + [(0.40 / THD) * x for x in HARMONICS[1:]])

CASES = [("A", "工况1（实验组：换速）", dict(base0=0.0, step_speed=True)),
         ("B", "工况2（对照组：参考不变）", dict(base0=0.50, step_speed=False))]


def build(base0):
    t = np.arange(0.0, TEND, DT)
    tau_v = np.maximum(t - TL0, 0.0)
    vib = np.zeros_like(t)
    for n, a in enumerate(VIB_H, start=1):
        vib += a * np.sin(2.0 * math.pi * F_VIB * n * tau_v)
    step = (0.50 - base0) * (t >= TL0) + base0
    TL = step.astype(float) * 0.637 + VIB1 * vib * (t >= TL0)
    return t, TL


def one(job):
    from pmsm_inv_sim import sim_inv
    key, label, ex = job
    t, TL = build(ex["base0"])
    cfg = dict(n_ref=N_REF, T_adapt=True, T_filt=50e-3,
               T=0.1, fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3,
               seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
               tl_ang_start=ANG_START,
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
    if ex["step_speed"]:
        cfg.update(n_ref2=N2, t_nref=T_STEP)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"])
    np.savez("_wave_ts_%s.npz" % key, t=tt, TL=Y["tl"], y=Y["y"], iq=Y["iq"])
    yref = np.where(tt >= T_STEP, N2 / N_REF, 1.0) if ex["step_speed"] else np.ones_like(tt)
    e = (np.asarray(Y["y"]) - yref) * N_REF
    print("%-2s %-22s 阶跃窗最低 %7.1f  换速窗峰值 %7.1f  末段 RMS %5.1f"
          % (key, label, float(np.min(e[(tt >= 1.9) & (tt <= 2.1)])),
             float(np.max(np.abs(e[(tt >= 5.9) & (tt <= 6.1)]))),
             float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2)))), flush=True)


if __name__ == "__main__":
    with Pool(2) as p:
        p.map(one, CASES)
    print("done")
