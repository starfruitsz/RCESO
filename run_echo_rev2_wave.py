# -*- coding: utf-8 -*-
"""run_echo_rev2_wave.py —— 反相工况 + 版式四档（无律/律D/F-B/D+F-B）的波形数据

与 run_inv_wave_case.py 同版式；事件改为 6 s 零交越整体反相；
F-B 与 D+F-B 的复位算子取 α=-1（反相复位），检测器为能量失配 D_m=0.20、冷却 0.3 s。
输出：_wave_rev2_<N>_<cfg>.npz（seed 20261018）
"""
import math
import os
from multiprocessing import Pool

import numpy as np
import noise_cfg as NC

DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])
AMP = 0.30 * 0.637
SPEEDS = ((600.0, 10.0), (900.0, 15.0), (1200.0, 20.0))
FB_INV = dict(ff_mism=0.20, ff_mism_eps=1e-6, ff_cool=0.30, ff_flush=0.0,
              ff_gmax=0.05, ff_alpha=-1.0)
CFG = [("Base", dict(det_eps=0.0)),
       ("LawD", dict(kp_boost=4.0, det_eps=0.01)),
       ("FB", dict(FB_INV)),
       ("D+FB", dict(FB_INV, kp_boost=4.0, det_eps=0.01))]


def build_tl(T):
    t = np.arange(0.0, TEND, DT)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    cl = AMP * (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))
    return t, 0.50 * on * 0.637 + cl * onp + np.where(t >= TW, -cl, 0.0)


def run_one(job):
    nref, flo, name, kw = job
    from pmsm_inv_sim import sim_inv
    T = 1.0 / flo
    t, TL = build_tl(T)
    cfg = dict(n_ref=nref, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=20261018, **LAB)
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    np.savez("_wave_rev2_%d_%s.npz" % (int(nref), name),
             t=Y["t"], TL=TL[::5], y=Y["y"], trig=np.array([z[0] for z in Y["trig"]]))
    return (int(nref), name, len(Y["t"]))


if __name__ == "__main__":
    jobs = [(n, f, nm, kw) for (n, f) in SPEEDS for nm, kw in CFG]
    with Pool(12) as p:
        for r in p.map(run_one, jobs):
            print("saved", r, flush=True)
