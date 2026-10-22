# -*- coding: utf-8 -*-
"""run_echo_reversal.py —— 反相突变工况的 8 种子复核 + 出图轨迹（2026-10-22）

反相：10 Hz 簇在 t=6.0 s（零交越）整体反号，值连续、斜率翻转。
与"撤除"并列，用于证明反相工况造出的回声在 500 Hz/类 fal 档下仍清晰可见。
输出：_echo_reversal.json（8 种子）+ _echo_reversal_trace.npz（seed 20261018 的轨迹）
"""
import json
import math
import os
from multiprocessing import Pool

import numpy as np
import noise_cfg as NC

DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
T, N_REF = 0.1, 600.0
SEEDS = [20261018, 20261019, 20261021, 20261022, 20261023, 20261024, 20261025, 20261026]
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])
AMP = 0.30 * 0.637
KINDS = ["removal", "reversal"]
ESOS = [("lin", dict(eso_law="linear")), ("fal", dict())]


def cluster(ph, amp=AMP):
    return amp * (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))


def build_tl(kind):
    t = np.arange(0.0, TEND, DT)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    tail = np.zeros_like(t) if kind == "removal" else -cluster(ph)
    return t, 0.50 * on * 0.637 + cluster(ph) * onp + np.where(t >= TW, tail, 0.0)


def cyc_amp(tt, e, k):
    t0 = TW + k * T
    m = (tt >= t0) & (tt < t0 + T)
    ee = e[m]; tq = tt[m]
    return float(math.hypot(2 * np.mean(ee * np.cos(2 * math.pi * tq / T)),
                            2 * np.mean(ee * np.sin(2 * math.pi * tq / T))))


def run_one(job):
    kind, ename, ekw, seed = job
    from pmsm_inv_sim import sim_inv
    t, TL = build_tl(kind)
    cfg = dict(n_ref=N_REF, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=seed, **LAB)
    cfg.update(ekw)
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
    r = dict(kind=kind, eso=ename, seed=seed,
             pre=round(cyc_amp(tt, e, -1), 2),
             post=[round(cyc_amp(tt, e, k), 2) for k in range(4)],
             echo_rms=round(float(np.sqrt(np.mean(e[(tt >= TW) & (tt < TW + 0.3)] ** 2))), 2))
    r["ratio"] = round(r["post"][0] / max(r["pre"], 1e-6), 2)
    return r


if __name__ == "__main__":
    jobs = [(k, e, kw, s) for s in SEEDS for k in KINDS for e, kw in ESOS]
    with Pool(min(12, os.cpu_count() or 1)) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault(r["kind"] + "·" + r["eso"], []).append(r)
    json.dump(out, open("_echo_reversal.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%-15s %8s %8s %8s %8s %8s %6s" % ("工况·ESO", "pre", "c0", "c1", "c2", "c3", "ratio"))
    for k in KINDS:
        for e, _ in ESOS:
            rr = out[k + "·" + e]
            m = lambda f: np.mean([x[f] for x in rr])
            cs = [np.mean([x["post"][i] for x in rr]) for i in range(4)]
            print("%-15s %8.2f %8.2f %8.2f %8.2f %8.2f %6.2f" % (
                k + "·" + e, m("pre"), cs[0], cs[1], cs[2], cs[3],
                np.mean([x["ratio"] for x in rr])))

    # 存一份出图轨迹（seed 20261018，四档：两种事件 × 两种 ESO）
    from pmsm_inv_sim import sim_inv
    store = {}
    t = None
    for kind in KINDS:
        tt_, TL_ = build_tl(kind)
        t = tt_
        store["TL_" + kind] = TL_[::5]
        for ename, ekw in ESOS:
            cfg = dict(n_ref=N_REF, T=T, fci=500.0, beta3=4000.0, tau0=20e-3,
                       seed_i=20261018, **LAB); cfg.update(ekw)
            Y = sim_inv(tt_, TL_, cfg)
            store["%s_%s" % (kind, ename)] = (Y["y"] - 1.0) * N_REF
    store["t"] = Y["t"]
    np.savez_compressed("_echo_reversal_trace.npz", **store)
    print("trace saved")
