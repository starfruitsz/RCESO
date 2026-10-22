# -*- coding: utf-8 -*-
"""run_eso_fal_speed.py —— 600/900/1200 rpm（10/15/20 Hz）× 线性/类 fal（实验室噪声，8 种子）

口径与 run_inv_speedcases.py 逐项相同（n_ref 与 T=1/f 同时改），
差别只是把 ESO 增益形状加入变量，并补上重标定后的方向限定 F-B。
输出：_eso_fal_speed.json + 屏幕表
"""
import json
import math
import os
from multiprocessing import Pool

import numpy as np
import noise_cfg as NC

DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
N_REF = 600.0
SEEDS = [20261018, 20261019, 20261021, 20261022, 20261023, 20261024, 20261025, 20261026]
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])
FB_OLD = dict(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0, ff_gmax=0.05)
FB_DIR = dict(ff_mism=0.30, ff_mism_eps=1e-6, ff_cool=0.30, ff_flush=0.0,
              ff_gmax=0.05, ff_mism_dir=1)
SPEEDS = [(600.0, 10.0), (900.0, 15.0), (1200.0, 20.0)]

CFG = [
    ("Base·lin", dict(det_eps=0.0, eso_law="linear")),
    ("Base·fal", dict(det_eps=0.0)),
    ("律D·lin", dict(kp_boost=4.0, det_eps=0.01, eso_law="linear")),
    ("律D·fal", dict(kp_boost=4.0, det_eps=0.01)),
    ("F-B·lin", dict(FB_OLD, eso_law="linear")),
    ("F-B·fal", dict(FB_OLD)),
    ("F-B·fal方向", dict(FB_DIR)),
    ("D+F-B·lin", dict(FB_OLD, kp_boost=4.0, det_eps=0.01, eso_law="linear")),
    ("D+F-B·fal方向", dict(FB_DIR, kp_boost=4.0, det_eps=0.01)),
]


def build_case(T):
    t = np.arange(0.0, TEND, DT)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    TL = (0.50 * on + 0.30 * onp *
          (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))) * 0.637
    return t, TL


def amp(tt, e, T):
    m = (tt >= TW) & (tt < TW + T)
    ee = e[m]; tq = tt[m]
    return float(math.hypot(2 * np.mean(ee * np.cos(2 * math.pi * tq / T)),
                            2 * np.mean(ee * np.sin(2 * math.pi * tq / T))))


def run_one(job):
    nref, flo, name, kw, seed = job
    from pmsm_inv_sim import sim_inv
    T = 1.0 / flo
    t, TL = build_case(T)
    cfg = dict(n_ref=nref, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=seed, **LAB)
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * nref
    tr = [x for x in Y["trig"] if TW <= x[0] < TW + T]
    return dict(nref=nref, flo=flo, name=name, seed=seed,
                echo=round(amp(tt, e, T), 2),
                dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                f78=int(Y["fl"][(tt >= 7) & (tt < 8)].sum()),
                ntrig=len(tr))


def main():
    jobs = [(n, f, nm, kw, s) for (n, f) in SPEEDS for s in SEEDS for nm, kw in CFG]
    with Pool(min(12, os.cpu_count() or 1)) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault("%g rpm" % r["nref"], {}).setdefault(r["name"], []).append(r)
    json.dump(out, open("_eso_fal_speed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for sp, d in out.items():
        print("\n== %s ==" % sp)
        print("%-14s %14s %12s %10s" % ("config", "echo", "dip", "steady"))
        for nm, _ in CFG:
            rr = d[nm]
            f = lambda k: np.array([x[k] for x in rr], dtype=float)
            print("%-14s %5.2f±%5.2f %6.1f±%5.1f %5.2f±%4.2f" % (
                nm, f("echo").mean(), f("echo").std(ddof=1),
                f("dip").mean(), f("dip").std(ddof=1),
                f("steady").mean(), f("steady").std(ddof=1)))


if __name__ == "__main__":
    main()
