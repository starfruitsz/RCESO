# -*- coding: utf-8 -*-
"""run_eso_fal.py —— ESO 校正通道：线性增益 vs 类 fal 增益（真实逆变器对象）

口径与 run_inv_mism_g.py 完全一致（唯一变量是 ESO 增益形状）：
    pmsm_inv_sim.py，fci=500 Hz、beta3=4000、tau0=20 ms、8 s 工况
    （0–2 s 空载；2 s 加载 0.50 额定；2–6 s 叠加 10 Hz 不对中簇 A=0.30；6 s 零交越撤除）
    标准噪声档（dq 电流 ±0.2 A、转速 6 rpm、负载 0.025 N·m），8 个种子。

用法：
    python run_eso_fal.py            # 默认配置组，8 种子，16 进程
    python run_eso_fal.py --seeds 2  # 快速版
输出：_eso_fal.json + 屏幕汇总表
"""
import argparse
import json
import math
import os
from multiprocessing import Pool

import numpy as np

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
SEEDS = [20261018, 20261019, 20261021, 20261022, 20261023, 20261024, 20261025, 20261026]
WIN = [(0.5, 2.0), (2.0, 2.5), (2.5, 2.6), (3.0, 3.5), (3.5, 4.0), (4.0, 6.0), (7.0, 8.0)]
BASE = dict(i_noise_peak=0.2, fci=500.0, beta3=4000.0, tau0=20e-3)

# (名字, 附加配置)：只改 ESO 增益形状，其余逐位相同
CONFIGS = [
    ("lin", dict(eso_law="linear")),
    ("fal a=.75 d=.05 l=10", dict(eso_law="fal", eso_a=0.75, eso_delta=0.05, eso_lam=10.0)),
    ("fal a=.90 d=.05 l=10", dict(eso_law="fal", eso_a=0.90, eso_delta=0.05, eso_lam=10.0)),
    ("fal a=.75 d=.02 l=20", dict(eso_law="fal", eso_a=0.75, eso_delta=0.02, eso_lam=20.0)),
]

# 与律 F-B 叠加档（--fb）：F-B 配置与 run_inv_mism_g.py 逐项相同
FB_MG = dict(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0, ff_gmax=0.05)
CONFIGS_FB = [
    ("F-B (lin)", dict(FB_MG, eso_law="linear")),
    ("F-B + fal a=.75 d=.10", dict(FB_MG, eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)),
    ("F-B + fal a=.80 d=.10", dict(FB_MG, eso_law="fal", eso_a=0.80, eso_delta=0.10, eso_lam=10.0)),
]

# 参数扫描档（--sweep）
SWEEP = [
    ("fal a=.75 d=.10 l=10", dict(eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)),
    ("fal a=.70 d=.10 l=10", dict(eso_law="fal", eso_a=0.70, eso_delta=0.10, eso_lam=10.0)),
    ("fal a=.80 d=.10 l=10", dict(eso_law="fal", eso_a=0.80, eso_delta=0.10, eso_lam=10.0)),
    ("fal a=.75 d=.10 l=20", dict(eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=20.0)),
    ("fal a=.75 d=.15 l=10", dict(eso_law="fal", eso_a=0.75, eso_delta=0.15, eso_lam=10.0)),
    ("fal a=.85 d=.05 l=10", dict(eso_law="fal", eso_a=0.85, eso_delta=0.05, eso_lam=10.0)),
    ("fal a=.75 d=.10 l=10", dict(eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)),
    ("fal a=.75 d=.20 l=10", dict(eso_law="fal", eso_a=0.75, eso_delta=0.20, eso_lam=10.0)),
    ("fal a=.85 d=.10 l=10", dict(eso_law="fal", eso_a=0.85, eso_delta=0.10, eso_lam=10.0)),
    ("fal a=.90 d=.20 l=10", dict(eso_law="fal", eso_a=0.90, eso_delta=0.20, eso_lam=10.0)),
    ("fal a=.75 d=.05 l=10 a1=a", dict(eso_law="fal", eso_a=0.75, eso_a1=0.75, eso_delta=0.05, eso_lam=10.0)),
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
    name, extra, seed = job
    from pmsm_inv_sim import sim_inv, N_REF
    t, TL = build_case()
    cfg = dict(BASE, **extra); cfg["seed_i"] = seed
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
    tr = [x for x in Y["trig"] if TW <= x[0] < TW + 1.0]
    return dict(name=name, seed=seed,
                n_trig=len(tr), first=(round(tr[0][0], 3) if tr else None),
                echo=round(amp10(tt, e), 2),
                dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                iq_std=round(float(np.std(Y["iq"][(tt >= 4) & (tt < 6)])), 2),
                w=[round(float(np.sqrt(np.mean(e[(tt >= a) & (tt < b)] ** 2))), 1) for a, b in WIN])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1))
    ap.add_argument("--out", default="_eso_fal.json")
    ap.add_argument("--sweep", action="store_true", help="跑参数扫描组 SWEEP（另加线性基线）")
    ap.add_argument("--fb", action="store_true", help="跑与律 F-B 的叠加组 CONFIGS_FB")
    a = ap.parse_args()
    cfgs = ((("lin", dict(eso_law="linear")) + tuple(SWEEP)) if a.sweep
            else (CONFIGS_FB if a.fb else CONFIGS))
    seeds = SEEDS[:a.seeds]
    jobs = [(n, kw, s) for s in seeds for n, kw in cfgs]
    with Pool(a.workers) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault(r["name"], []).append(r)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%-22s %14s %10s %9s %8s" % ("config", "echo 10Hz", "dip", "steady", "iq_std"))
    for n, _ in cfgs:
        rr = out[n]
        f = lambda k: np.array([x[k] for x in rr], dtype=float)
        print("%-22s %6.2f±%5.2f %7.1f±%4.1f %4.2f±%3.2f %6.2f±%4.2f" % (
            n, f("echo").mean(), f("echo").std(ddof=1), f("dip").mean(), f("dip").std(ddof=1),
            f("steady").mean(), f("steady").std(ddof=1), f("iq_std").mean(), f("iq_std").std(ddof=1)))


if __name__ == "__main__":
    main()
