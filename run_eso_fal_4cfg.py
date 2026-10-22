# -*- coding: utf-8 -*-
"""run_eso_fal_4cfg.py —— 四档算法 × 两种 ESO 增益（真实逆变器对象，8 种子）

口径与 run_inv_mism_g.py / 正文 §6.3 完全一致。2026-10-22 起 ESO 默认档 = fal。
    Base / 律 D / F-B / D+F-B  ×  {fal（默认）, linear（旧定稿）}
输出：_eso_fal_4cfg.json + 屏幕表
"""
import json
import math
import os
from multiprocessing import Pool

import numpy as np

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
SEEDS = [20261018, 20261019, 20261021, 20261022, 20261023, 20261024, 20261025, 20261026]
WIN = [(0.5, 2.0), (2.0, 2.5), (2.5, 2.6), (3.0, 3.5), (3.5, 4.0), (4.0, 6.0), (7.0, 8.0)]
BASE = dict(i_noise_peak=0.2, fci=500.0, beta3=4000.0, tau0=20e-3)
FB_MG = dict(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0, ff_gmax=0.05)

ALGS = [("Base", {}),
        ("律D", dict(kp_boost=4.0, det_eps=0.01)),
        ("F-B", dict(FB_MG)),
        ("D+F-B", dict(FB_MG, kp_boost=4.0, det_eps=0.01))]
ESO = [("fal", dict(eso_law="fal")), ("lin", dict(eso_law="linear"))]


def build_case():
    t = np.arange(0.0, TEND, DT)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    TL = (0.50 * on + 0.30 * onp *
          (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))) * 0.637
    return t, TL


def amp10(tt, e):
    m = (tt >= TW) & (tt < TW + T)
    ee = e[m]; tq = tt[m]
    return float(math.hypot(2 * np.mean(ee * np.cos(2 * math.pi * tq / T)),
                            2 * np.mean(ee * np.sin(2 * math.pi * tq / T))))


def run_one(job):
    alg, akw, ename, ekw, seed = job
    from pmsm_inv_sim import sim_inv, N_REF
    t, TL = build_case()
    cfg = dict(BASE, **akw); cfg.update(ekw); cfg["seed_i"] = seed
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
    tr = [x for x in Y["trig"] if TW <= x[0] < TW + 1.0]
    return dict(alg=alg, eso=ename, seed=seed,
                echo=round(amp10(tt, e), 2),
                dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                iq_std=round(float(np.std(Y["iq"][(tt >= 4) & (tt < 6)])), 2),
                n_trig=len(tr), first=(round(tr[0][0], 3) if tr else None),
                w=[round(float(np.sqrt(np.mean(e[(tt >= a) & (tt < b)] ** 2))), 1) for a, b in WIN])


def main():
    jobs = [(a, akw, e, ekw, s) for s in SEEDS for a, akw in ALGS for e, ekw in ESO]
    with Pool(min(8, os.cpu_count() or 1)) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault(r["alg"] + "·" + r["eso"], []).append(r)
    json.dump(out, open("_eso_fal_4cfg.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%-12s %13s %11s %9s %7s %5s" % ("config", "echo 10Hz", "dip", "steady", "iq_std", "trig"))
    for a, _ in ALGS:
        for e, _ in ESO:
            rr = out[a + "·" + e]
            f = lambda k: np.array([x[k] for x in rr], dtype=float)
            print("%-12s %5.2f±%5.2f %6.1f±%4.1f %4.2f±%3.2f %5.2f±%4.2f %5.1f" % (
                a + "·" + e, f("echo").mean(), f("echo").std(ddof=1),
                f("dip").mean(), f("dip").std(ddof=1),
                f("steady").mean(), f("steady").std(ddof=1),
                f("iq_std").mean(), f("iq_std").std(ddof=1), f("n_trig").mean()))


if __name__ == "__main__":
    main()
