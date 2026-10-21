# -*- coding: utf-8 -*-
"""新 F-B（D_m+g）与 F-A oracle 的对比：8 种子

F-A：在 6.0 s 事件时刻直接复位（α=0）；FA20：延后到 6.02 s（模拟 20 ms 检测滞后的 oracle）。
F-B：D_m>0.2 且 g<0.05，冷却 0.3 s，自主触发。
用法：python run_inv_fa.py → _inv_fa.json
"""
import math
import json

import numpy as np

from pmsm_inv_sim import sim_inv, N_REF
import noise_cfg as NC

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
SEEDS = [20261018, 20261019, 20261021, 20261022,
         20261023, 20261024, 20261025, 20261026]
WIN = [(0.5, 2.0), (2.0, 2.5), (2.5, 2.6), (3.0, 3.5),
       (3.5, 4.0), (4.0, 6.0), (7.0, 8.0)]
FB_MG = dict(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0,
             ff_gmax=0.05)


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


def main():
    t, TL = build_case()
    base_kw = dict(i_noise_peak=NC.NOISE["i_noise_peak"],
                   fci=500.0, beta3=4000.0, tau0=20e-3)
    CFG = [("Base", dict(det_eps=0.0)),
           ("FB", dict(FB_MG)),
           ("FA", dict(flush_t=6.0, flush_alpha=0.0)),
           ("FA20", dict(flush_t=6.02, flush_alpha=0.0))]
    out = {n: [] for n, _ in CFG}
    for sd in SEEDS:
        for name, kw in CFG:
            cfg = dict(base_kw, **kw); cfg["seed_i"] = sd
            Y = sim_inv(t, TL, cfg)
            tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
            tr = [x for x in Y["trig"] if TW <= x[0] < TW + 1.0]
            row = dict(seed=sd,
                       a_echo=round(amp10(tt, e), 1),
                       dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                       steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                       iq_std=round(float(np.std(Y["iq"][(tt >= 4) & (tt < 6)])), 2),
                       n_trig=len(tr),
                       first=(round(tr[0][0], 3) if tr else None),
                       f78=int(Y["fl"][(tt >= 7) & (tt < 8)].sum()),
                       w7=[round(float(np.sqrt(np.mean(e[(tt >= a) & (tt < b)] ** 2))), 1)
                           for a, b in WIN])
            out[name].append(row)
            print("%-5s seed=%d echo=%6.1f dip=%7.1f steady=%5.2f nTr=%d first=%s f78=%d"
                  % (name, sd, row["a_echo"], row["dip"], row["steady"],
                     row["n_trig"], row["first"], row["f78"]), flush=True)
    json.dump(out, open("_inv_fa.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\n== summary ==")
    for name, _ in CFG:
        a = np.array([r["a_echo"] for r in out[name]])
        d = np.array([r["dip"] for r in out[name]])
        s = np.array([r["steady"] for r in out[name]])
        print("%-5s echo %6.2f±%4.2f  dip %7.2f±%5.2f  steady %5.2f±%4.2f"
              % (name, a.mean(), a.std(ddof=1), d.mean(), d.std(ddof=1),
                 s.mean(), s.std(ddof=1)))
    base = np.array([r["a_echo"] for r in out["Base"]])
    for name in ("FB", "FA", "FA20"):
        v = np.array([r["a_echo"] for r in out[name]])
        print("%-5s vs Base diff %6.2f  reduction %5.1f%%"
              % (name, (v - base).mean(), 100 * (1 - v.mean() / base.mean())))
    print("DONE")


if __name__ == "__main__":
    main()

