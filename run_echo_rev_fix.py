# -*- coding: utf-8 -*-
"""修正：反相工况下 F-A oracle 的复位滞后应取 tau=0（扫描最优），
但 run_echo_rev_speed.py 里 TAU_MS 的 global 更新没有传到 spawn 出来的子进程，
导致 FA.inv 实际跑的是 tau=20 ms。本脚本重跑 FA.inv 并回写 JSON + 波形。
"""
import json
import math
import os
from multiprocessing import Pool

import numpy as np
import noise_cfg as NC

DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])
AMP = 0.30 * 0.637
TAU_MS = 0.0
SPEEDS = ((600.0, 10.0), (900.0, 15.0), (1200.0, 20.0))


def build_tl(T):
    t = np.arange(0.0, TEND, DT)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    cl = AMP * (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))
    return t, 0.50 * on * 0.637 + cl * onp + np.where(t >= TW, -cl, 0.0)


def cyc(tt, e, k, T):
    t0 = TW + k * T
    m = (tt >= t0) & (tt < t0 + T)
    ee = e[m]; tq = tt[m]
    return float(math.hypot(2 * np.mean(ee * np.cos(2 * math.pi * tq / T)),
                            2 * np.mean(ee * np.sin(2 * math.pi * tq / T))))


def run_one(job):
    nref, flo, seed = job
    from pmsm_inv_sim import sim_inv
    T = 1.0 / flo
    t, TL = build_tl(T)
    cfg = dict(n_ref=nref, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=seed, **LAB,
               flush_t=TW + TAU_MS / 1000.0, flush_alpha=-1.0)
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * nref
    return dict(name="FA.inv", nref=nref, seed=seed,
                pre=round(cyc(tt, e, -1, T), 2),
                post=[round(cyc(tt, e, k, T), 2) for k in range(3)],
                dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                ntrig=0)


if __name__ == "__main__":
    seeds = [20261018, 20261019, 20261021, 20261022]
    jobs = [(n, f, s) for (n, f) in SPEEDS for s in seeds]
    with Pool(12) as p:
        rows = p.map(run_one, jobs)
    by = {}
    for r in rows:
        by.setdefault("%d" % r["nref"], []).append(r)
    j = json.load(open("_echo_rev_speed.json", encoding="utf-8"))
    for sp, rr in by.items():
        j[sp]["FA.inv"] = rr
        print(sp, "FA.inv tau=0 -> c0 %.1f  c1 %.1f" % (
            np.mean([x["post"][0] for x in rr]), np.mean([x["post"][1] for x in rr])))
    json.dump(j, open("_echo_rev_speed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    from pmsm_inv_sim import sim_inv
    for (nref, flo) in SPEEDS:
        T = 1.0 / flo
        t, TL = build_tl(T)
        cfg = dict(n_ref=nref, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=20261018, **LAB,
                   flush_t=TW, flush_alpha=-1.0)
        Y = sim_inv(t, TL, cfg)
        np.savez("_wave_rev_%d_FA.inv.npz" % int(nref),
                 t=Y["t"], TL=TL[::5], y=Y["y"], trig=np.array([z[0] for z in Y["trig"]]))
    print("waves FA.inv updated")
