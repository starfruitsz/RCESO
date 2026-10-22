# -*- coding: utf-8 -*-
"""run_echo_freq.py —— "变频"工况：10 Hz 簇在 6 s 切到 12 Hz

机理：内模周期 T=0.1 s 固定，切到 12 Hz 后，输出里任何 10 Hz 分量都没有物理来源，
      只能是重复通道在重放旧记忆 —— 这就是最纯的"回声"，且应当逐周期衰减。
对照：撤除（回声低于稳态，看不见）、反相（回声抬高但稳态残余不变）。

用法：python run_echo_freq.py
输出：_echo_freq.json
"""
import json
import math
import os
from multiprocessing import Pool

import numpy as np
import noise_cfg as NC

DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
T, N_REF = 0.1, 600.0
F_NEW = 12.0
KIND = os.environ.get("ECHO_KIND", "phase90")
PHI_JUMP = {"phase90": math.pi / 2, "phase60": math.pi / 3, "phase150": 5 * math.pi / 6}.get(KIND, 0.0)
SEEDS = [20261018, 20261019, 20261021, 20261022, 20261023, 20261024, 20261025, 20261026]
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])
AMP = 0.30 * 0.637
ESOS = [("lin", dict(eso_law="linear")), ("fal", dict())]


def cluster(ph, amp=AMP):
    return amp * (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))


def build_tl():
    t = np.arange(0.0, TEND, DT)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    ph2 = ph + PHI_JUMP
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    return t, 0.50 * on * 0.637 + cluster(ph) * onp + np.where(t >= TW, cluster(ph2), 0.0)


def cyc(tt, e, k, f=10.0):
    t0 = TW + k * T
    m = (tt >= t0) & (tt < t0 + T)
    ee = e[m]; tq = tt[m]
    return float(math.hypot(2 * np.mean(ee * np.cos(2 * math.pi * f * tq)),
                            2 * np.mean(ee * np.sin(2 * math.pi * f * tq))))


def run_one(job):
    ename, ekw, seed = job
    from pmsm_inv_sim import sim_inv
    t, TL = build_tl()
    cfg = dict(n_ref=N_REF, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=seed, **LAB)
    cfg.update(ekw)
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
    return dict(eso=ename, seed=seed,
                pre=round(cyc(tt, e, -1), 2),
                at10=[round(cyc(tt, e, k), 2) for k in range(4)],
                at12=[round(cyc(tt, e, k, F_NEW), 2) for k in range(4)])


if __name__ == "__main__":
    jobs = [(e, kw, s) for s in SEEDS for e, kw in ESOS]
    with Pool(min(12, os.cpu_count() or 1)) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault(r["eso"], []).append(r)
    json.dump(out, open("_echo_%s.json" % KIND, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("KIND =", KIND)
    print("%-6s %8s %8s %8s %8s %8s" % ("ESO", "pre@10", "c0@10", "c1@10", "c2@10", "c3@10"))
    for e, _ in ESOS:
        rr = out[e]
        m = lambda f, i=None: np.mean([x[f][i] if i is not None else x[f] for x in rr])
        print("%-6s %8.2f %8.2f %8.2f %8.2f %8.2f" % (
            e, m("pre"), m("at10", 0), m("at10", 1), m("at10", 2), m("at10", 3)))
