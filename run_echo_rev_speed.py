# -*- coding: utf-8 -*-
"""run_echo_rev_speed.py —— 反相工况下的 600/900/1200 rpm 转速图数据

事件：10 Hz（15/20 Hz）簇在 t=6.0 s 零交越处整体反号（值连续、斜率翻转）。
四档：
    Base      无律
    LawD      律 D（kp 提升）
    FB.clear  F-B 检测器 + 清空算子 α=0（反相工况下的"负面对照"：能量型判据对反相对称，不触发）
    FA.inv    F-A oracle：事件时刻已知、α=−1 反相复位（反相工况的可达上界）
另存 seed 20261018 的波形，供 plot_echo_rev_speed.py 出图。

用法：python run_echo_rev_speed.py
输出：_echo_rev_speed.json、_wave_rev_<N>_<cfg>.npz
"""
import json
import math
import os
from multiprocessing import Pool

import numpy as np
import noise_cfg as NC

DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
N_REF = 600.0
SEEDS = [20261018, 20261019, 20261021, 20261022]
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])
AMP = 0.30 * 0.637
TAU_MS = 20.0          # 复位滞后（oracle），先按撤除工况的已知最优取，稍后用扫描确认


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


def cfg_of(name, nref, T, seed):
    c = dict(n_ref=nref, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=seed, **LAB)
    if name == "Base":
        c.update(det_eps=0.0)
    elif name == "LawD":
        c.update(kp_boost=4.0, det_eps=0.01)
    elif name == "FB.clear":
        c.update(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0,
                 ff_gmax=0.05, ff_alpha=0.0)
    elif name == "FA.inv":
        c.update(flush_t=TW + TAU_MS / 1000.0, flush_alpha=-1.0)
    return c


def run_one(job):
    name, nref, flo, seed, alpha_override = job
    from pmsm_inv_sim import sim_inv
    T = 1.0 / flo
    t, TL = build_tl(T)
    cfg = cfg_of(name, nref, T, seed)
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * nref
    return dict(name=name, nref=nref, seed=seed,
                pre=round(cyc(tt, e, -1, T), 2),
                post=[round(cyc(tt, e, k, T), 2) for k in range(3)],
                dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                ntrig=len([x for x in Y["trig"] if TW <= x[0] < TW + 1.0]))


NAMES = ["Base", "LawD", "FB.clear", "FA.inv"]


def main():
    from pmsm_inv_sim import sim_inv
    # 0) 先确认反相工况的复位滞后（600 rpm / seed 20261018，α=-1，扫 0/10/20/30/40 ms）
    t, TL = build_tl(0.1)
    best = None
    print("[tau scan] reversal / alpha=-1 / 600 rpm")
    for ms in (0, 10, 20, 30, 40):
        c = dict(n_ref=600.0, T=0.1, fci=500.0, beta3=4000.0, tau0=20e-3,
                 seed_i=20261018, flush_t=TW + ms / 1000.0, flush_alpha=-1.0, **LAB)
        Y = sim_inv(t, TL, c)
        tt = Y["t"]; e = (Y["y"] - 1.0) * 600.0
        a = cyc(tt, e, 0, 0.1)
        print("   tau=%2d ms -> c0=%.1f rpm" % (ms, a))
        if best is None or a < best[1]:
            best = (ms, a)
    tau_best = best[0]
    print("[tau scan] 选 tau = %d ms (c0=%.1f)" % (tau_best, best[1]))
    global TAU_MS
    TAU_MS = float(tau_best)

    # 1) 8 种子统计（4 种子）
    jobs = [(n, nref, flo, s, None) for (nref, flo) in ((600.0, 10.0), (900.0, 15.0), (1200.0, 20.0))
            for s in SEEDS for n in NAMES]
    with Pool(min(12, os.cpu_count() or 1)) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault("%d" % r["nref"], {}).setdefault(r["name"], []).append(r)
    json.dump(out, open("_echo_rev_speed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for sp, d in out.items():
        print("\n== %s rpm ==" % sp)
        for nm in NAMES:
            rr = d[nm]
            m = lambda f: np.mean([x[f] for x in rr])
            c0 = np.mean([x["post"][0] for x in rr])
            c1 = np.mean([x["post"][1] for x in rr])
            print("%-9s pre %6.1f  c0 %6.1f  c1 %6.1f  dip %7.1f  steady %5.2f  trig %.1f" % (
                nm, m("pre"), c0, c1, m("dip"), m("steady"), m("ntrig")))

    # 2) 存 seed 20261018 的波形
    for (nref, flo) in ((600.0, 10.0), (900.0, 15.0), (1200.0, 20.0)):
        T = 1.0 / flo
        t, TL = build_tl(T)
        nT = int(round(t[-1] / 1e-4)) + 2
        TLn = np.zeros(nT)
        for nm in NAMES:
            Y = sim_inv(t, TL, cfg_of(nm, nref, T, 20261018))
            np.savez("_wave_rev_%d_%s.npz" % (int(nref), nm),
                     t=Y["t"], TL=TL[::5], y=Y["y"], trig=np.array([z[0] for z in Y["trig"]]))
        print("waves", int(nref), "done")


if __name__ == "__main__":
    main()
