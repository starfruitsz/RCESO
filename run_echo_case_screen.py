# -*- coding: utf-8 -*-
"""run_echo_case_screen.py —— 筛选"回声可辨识"的工况（2026-10-22）

背景：600 rpm / 10 Hz 簇"零交越撤除"在 500 Hz、类 fal 档下回声已埋进稳态残余（回声/稳态 ≈ 1），
      需要换一个能制造出显眼回声的事件。本脚本横向筛 6 类事件：

  removal   零交越撤除（现状）
  reversal  零交越整体反相（值连续、斜率翻转）——正文 §3.7 的"清晰可见"工况
  half      部分撤除（幅值降到 1/3，符号不变）
  boost     反向事件（幅值升到 1.5 倍）
  phase90   相位跳 90°
  freq      频率切换 10 -> 12 Hz（内模 T 固定，失配持续）

可辨识度指标：ratio = 事件后首周期 10 Hz 幅值 / 事件前最后一周期 10 Hz 幅值。
另给 echo_rms/steady_rms（6.0–6.3 s vs 4.0–6.0 s）作为交叉核对。

用法：python run_echo_case_screen.py [--seeds 4] [--out _echo_screen.json]
"""
import argparse
import json
import math
import os
from multiprocessing import Pool

import numpy as np
import noise_cfg as NC

DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
T = 0.1
N_REF = 600.0
SEEDS = [20261018, 20261019, 20261021, 20261022]
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])
AMP = 0.30 * 0.637

KINDS = ["removal", "reversal", "half", "boost", "phase90", "freq"]
ESOS = [("lin", dict(eso_law="linear")), ("fal", dict())]


def cluster(ph, amp=AMP):
    return amp * (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))


def build_tl(kind):
    t = np.arange(0.0, TEND, DT)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    base = 0.50 * on * 0.637
    c_before = cluster(ph) * onp
    after = t >= TW
    if kind == "removal":
        tail = 0.0
    elif kind == "reversal":
        tail = -cluster(ph)
    elif kind == "half":
        tail = cluster(ph) / 3.0
    elif kind == "boost":
        tail = 1.5 * cluster(ph)
    elif kind == "phase90":
        tail = cluster(ph + math.pi / 2)
    elif kind == "freq":
        ph2 = 2 * math.pi * np.maximum(t - TW, 0.0) / (1.0 / 12.0)
        tail = cluster(ph2)
    else:
        raise ValueError(kind)
    return t, base + c_before + np.where(after, tail, 0.0)


def amp10(tt, e, t0, T0=T):
    m = (tt >= t0) & (tt < t0 + T0)
    ee = e[m]; tq = tt[m]
    return float(math.hypot(2 * np.mean(ee * np.cos(2 * math.pi * tq / T0)),
                            2 * np.mean(ee * np.sin(2 * math.pi * tq / T0))))


def run_one(job):
    kind, ename, ekw, seed = job
    from pmsm_inv_sim import sim_inv
    t, TL = build_tl(kind)
    cfg = dict(n_ref=N_REF, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=seed, **LAB)
    cfg.update(ekw)
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
    steady10 = amp10(tt, e, TW - T)          # 事件前最后一周期
    echo10 = amp10(tt, e, TW)                # 事件后首周期
    steady_rms = float(np.sqrt(np.mean(e[(tt >= 4.0) & (tt < TW)] ** 2)))
    echo_rms = float(np.sqrt(np.mean(e[(tt >= TW) & (tt < TW + 0.3)] ** 2)))
    return dict(kind=kind, eso=ename, seed=seed,
                steady10=round(steady10, 2), echo10=round(echo10, 2),
                ratio=round(echo10 / max(steady10, 1e-6), 2),
                steady_rms=round(steady_rms, 2), echo_rms=round(echo_rms, 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--out", default="_echo_screen.json")
    a = ap.parse_args()
    jobs = [(k, e, kw, s) for s in SEEDS[:a.seeds] for k in KINDS for e, kw in ESOS]
    with Pool(min(12, os.cpu_count() or 1)) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault(r["kind"] + "·" + r["eso"], []).append(r)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%-16s %8s %8s %6s %9s %9s" % ("工况·ESO", "steady10", "echo10", "ratio", "steady_rms", "echo_rms"))
    for k in KINDS:
        for e, _ in ESOS:
            rr = out[k + "·" + e]
            m = lambda f: np.mean([x[f] for x in rr])
            print("%-16s %8.2f %8.2f %6.2f %9.2f %9.2f" % (
                k + "·" + e, m("steady10"), m("echo10"), m("ratio"), m("steady_rms"), m("echo_rms")))


if __name__ == "__main__":
    main()
