# -*- coding: utf-8 -*-
"""检测器 + 反相复位（α=-1）在反相事件下能否触发并抑制首拍回声。

配置：ff_mism=0.20（对称能量判据）、ff_cool=0.30、ff_gmax=0.05、ff_alpha=-1。
对照：同一检测器 + 清空（α=0）、无律。
3 转速 × 4 种子。
"""
import json, math, os
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC

DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])
AMP = 0.30 * 0.637
SEEDS = [20261018, 20261019, 20261021, 20261022]
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
    nref, flo, name, alpha, seed = job
    from pmsm_inv_sim import sim_inv
    T = 1.0 / flo
    t, TL = build_tl(T)
    cfg = dict(n_ref=nref, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=seed, **LAB)
    if name == "Base":
        cfg.update(det_eps=0.0)
    else:
        cfg.update(ff_mism=0.20, ff_mism_eps=1e-6, ff_cool=0.30, ff_flush=0.0,
                   ff_gmax=0.05, ff_alpha=alpha)
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * nref
    return dict(nref=nref, name=name, seed=seed, alpha=alpha,
                c0=round(cyc(tt, e, 0, T), 2), c1=round(cyc(tt, e, 1, T), 2),
                trig=len([x for x in Y["trig"] if TW <= x[0] < TW + 0.5]))


if __name__ == "__main__":
    jobs = [(n, f, nm, a, s) for (n, f) in SPEEDS for s in SEEDS
            for (nm, a) in (("Base", 0.0), ("FB.clear", 0.0), ("FB.inv", -1.0), ("FB.inv.5", -0.5))]
    with Pool(12) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault("%d" % r["nref"], {}).setdefault(r["name"], []).append(r)
    json.dump(out, open("_fb_alpha_test.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for sp, d in out.items():
        print("== %s rpm ==" % sp)
        for nm in ("Base", "FB.clear", "FB.inv", "FB.inv.5"):
            rr = d[nm]
            print("  %-9s c0 %6.1f  c1 %6.1f  trig %.1f" % (
                nm, np.mean([x["c0"] for x in rr]), np.mean([x["c1"] for x in rr]),
                np.mean([x["trig"] for x in rr])))
