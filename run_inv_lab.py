# -*- coding: utf-8 -*-
"""实验室工况：Base / 律 D / F-B / D+F-B，8 种子

噪声：转速 0.5%×600=3 rpm，dq 电流 ±0.1 A，负载 0.01 N·m。
输出 _inv_lab.json。
"""
import math
import json

import numpy as np

from pmsm_inv_sim import sim_inv, N_REF
import noise_cfg as NC

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
SEEDS = [20261018, 20261019, 20261021, 20261022,
         20261023, 20261024, 20261025, 20261026]
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])


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
    base_kw = dict(fci=500.0, beta3=4000.0, tau0=20e-3, **LAB)
    CFG = [
        ("Base", dict(det_eps=0.0)),
        ("LawD", dict(kp_boost=4.0, det_eps=0.01)),
        ("FB", dict(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3,
                    ff_flush=0.0, ff_gmax=0.05)),
        ("D+FB", dict(kp_boost=4.0, det_eps=0.01, ff_mism=0.2,
                      ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0,
                      ff_gmax=0.05)),
    ]
    out = {n: [] for n, _ in CFG}
    for sd in SEEDS:
        for name, kw in CFG:
            cfg = dict(base_kw, **kw); cfg["seed_i"] = sd
            Y = sim_inv(t, TL, cfg)
            tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
            tr = [x for x in Y["trig"] if TW <= x[0] < TW + 1.0]
            row = dict(seed=sd, a_echo=round(amp10(tt, e), 1),
                       dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                       steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                       iq_std=round(float(np.std(Y["iq"][(tt >= 4) & (tt < 6)])), 2),
                       n_trig=len(tr),
                       first=(round(tr[0][0], 3) if tr else None),
                       f78=int(Y["fl"][(tt >= 7) & (tt < 8)].sum()))
            out[name].append(row)
            print("%-5s seed=%d echo=%6.1f dip=%7.1f steady=%5.2f nTr=%d f78=%d"
                  % (name, sd, row["a_echo"], row["dip"], row["steady"],
                     row["n_trig"], row["f78"]), flush=True)
    json.dump(out, open("_inv_lab.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\n== summary ==")
    for name, _ in CFG:
        a = np.array([r["a_echo"] for r in out[name]])
        d = np.array([r["dip"] for r in out[name]])
        s = np.array([r["steady"] for r in out[name]])
        print("%-5s echo %6.2f±%4.2f dip %7.2f±%5.2f steady %5.2f±%4.2f"
              % (name, a.mean(), a.std(ddof=1), d.mean(), d.std(ddof=1),
                 s.mean(), s.std(ddof=1)))
    base = np.array([r["a_echo"] for r in out["Base"]])
    for name in ("LawD", "FB", "D+FB"):
        v = np.array([r["a_echo"] for r in out[name]])
        print("%-5s vs Base %6.2f (%5.1f%%)" % (name, (v - base).mean(),
                                               100 * (1 - v.mean() / base.mean())))
    print("DONE")


if __name__ == "__main__":
    main()

