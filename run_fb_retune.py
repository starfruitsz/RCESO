# -*- coding: utf-8 -*-
"""run_fb_retune.py —— 类 fal 默认档下重标定律 F-B 的检测器

背景：类 fal 增益改变了 e1/E_v 轨迹，记忆失配 D_m>0.2 的触发由 12–21 ms 推迟到最迟 240 ms，
      F-B 的回声抑制从 7.92 退化到 15.13。本脚本扫 D_m 阈值 / 冷却 / 门控，把触发拉回最优窗。

口径：真实逆变器对象（pmsm_inv_sim），8 s 工况、8 种子、标准噪声、ESO 默认（类 fal）。
输出：_fb_retune.json + 屏幕表
用法：python run_fb_retune.py [--quick]
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

# 每档：(名字, F-B 参数)。eso 一律 默认 fal，不写 eso_law。
GRID = [
    # 第四轮：方向限定检测器（ff_mism_dir=1）——只认"旧记忆强于当前"的方向
    ("对称 D_m=.30 (上轮最优)", dict(ff_mism=0.30, ff_cool=0.30)),
    ("方向 D_m=.15", dict(ff_mism=0.15, ff_cool=0.30, ff_mism_dir=1)),
    ("方向 D_m=.20", dict(ff_mism=0.20, ff_cool=0.30, ff_mism_dir=1)),
    ("方向 D_m=.30", dict(ff_mism=0.30, ff_cool=0.30, ff_mism_dir=1)),
    ("方向 D_m=.40", dict(ff_mism=0.40, ff_cool=0.30, ff_mism_dir=1)),
    ("方向 D_m=.30 cool=.45", dict(ff_mism=0.30, ff_cool=0.45, ff_mism_dir=1)),
]


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
    name, kw, seed = job
    from pmsm_inv_sim import sim_inv, N_REF
    t, TL = build_case()
    cfg = dict(BASE, ff_flush=0.0, ff_gmax=0.05)
    cfg.update(kw); cfg["seed_i"] = seed
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
    tr = [x for x in Y["trig"] if TW <= x[0] < TW + 1.0]
    return dict(name=name, seed=seed,
                echo=round(amp10(tt, e), 2),
                dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                f26=int(Y["fl"][(tt >= 2.5) & (tt < 6)].sum()),
                f78=int(Y["fl"][(tt >= 7) & (tt < 8)].sum()),
                trig=len(tr), first=(round(tr[0][0], 4) if tr else None))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", default="_fb_retune.json")
    a = ap.parse_args()
    seeds = SEEDS[:3] if a.quick else SEEDS
    jobs = [(n, kw, s) for s in seeds for n, kw in GRID]
    with Pool(min(8, os.cpu_count() or 1)) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault(r["name"], []).append(r)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%-24s %12s %10s %8s %6s %6s %s" % ("config", "echo", "dip", "steady", "f26", "trig", "first/s"))
    for n, _ in GRID:
        rr = out[n]
        f = lambda k: np.array([x[k] for x in rr], dtype=float)
        firsts = [x["first"] for x in rr if x["first"]]
        print("%-24s %5.2f±%5.2f %6.1f±%4.1f %4.2f±%3.2f %6.1f %6.1f %s" % (
            n, f("echo").mean(), f("echo").std(ddof=1), f("dip").mean(), f("dip").std(ddof=1),
            f("steady").mean(), f("steady").std(ddof=1), f("f26").sum() / len(rr), f("trig").mean(),
            ",".join("%.3f" % x for x in firsts)))


if __name__ == "__main__":
    main()
