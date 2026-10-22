# -*- coding: utf-8 -*-
"""run_fb_oracle.py —— 类 fal 默认档下，复位时刻 tau 的能力上界（oracle flush）

用 flush_t = 6.0 + tau 直接复位（事件时刻精确已知），扫 tau，量首周期 10 Hz 回声。
目的：判断“F-B 重标定”还有多少空间——若 oracle 在 tau=20 ms 也只有 ~12 rpm，
      则类 fal 档的回声下限本身就是它，检测器再准也没用。

用法：python run_fb_oracle.py [--tau 0,0.01,0.02,0.03,0.04] [--lin]
输出：_fb_oracle.json + 屏幕表
"""
import argparse
import json
import math
import os
from multiprocessing import Pool

import numpy as np

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
SEEDS = [20261018, 20261019, 20261021, 20261022, 20261023, 20261024, 20261025, 20261026]
BASE = dict(i_noise_peak=0.2, fci=500.0, beta3=4000.0, tau0=20e-3)


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
    tau_ms, lin, seed = job
    from pmsm_inv_sim import sim_inv, N_REF
    t, TL = build_case()
    cfg = dict(BASE, flush_t=TW + tau_ms / 1000.0, flush_alpha=0.0)
    cfg["eso_law"] = "linear" if lin else "fal"
    cfg["seed_i"] = seed
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
    return dict(tau=tau_ms, lin=lin, seed=seed,
                echo=round(amp10(tt, e), 2),
                dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tau", default="-1,0,10,20,30,40,60")
    ap.add_argument("--lin", action="store_true", help="同时跑线性档对照")
    ap.add_argument("--out", default="_fb_oracle.json")
    a = ap.parse_args()
    taus = [float(x) for x in a.tau.split(",")]
    jobs = [(tau, lin, s) for lin in ([False, True] if a.lin else [False])
            for tau in taus for s in SEEDS]
    with Pool(min(8, os.cpu_count() or 1)) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault("%s tau=%g ms" % ("lin" if r["lin"] else "fal", r["tau"]), []).append(r)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%-16s %14s %11s %9s" % ("config", "echo 10Hz", "dip", "steady"))
    for k in out:
        rr = out[k]
        f = lambda fld: np.array([x[fld] for x in rr], dtype=float)
        print("%-16s %5.2f±%5.2f %6.1f±%4.1f %4.2f±%3.2f" % (
            k, f("echo").mean(), f("echo").std(ddof=1),
            f("dip").mean(), f("dip").std(ddof=1), f("steady").mean(), f("steady").std(ddof=1)))


if __name__ == "__main__":
    main()
