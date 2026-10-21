# -*- coding: utf-8 -*-
"""真实逆变器对象上律 D 的 8 种子对比（Base vs LawD）

口径：pmsm_inv_sim（10 kHz PWM、死区、±0.3 A dq 采样），
fci=2 kHz、beta3=4000、tau0=20 ms；8 s 工况（2 s 加载、2–6 s 10 Hz 簇、6 s 撤除）。
用法：python run_inv_lawd.py → _inv_lawd.json
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
                   fci=2000.0, beta3=4000.0, tau0=20e-3)
    CFG = [("Base", dict(det_eps=0.0)),
           ("LawD", dict(kp_boost=4.0, det_eps=0.01))]
    out = {"Base": [], "LawD": []}
    for sd in SEEDS:
        for name, kw in CFG:
            cfg = dict(base_kw, **kw); cfg["seed_i"] = sd
            Y = sim_inv(t, TL, cfg)
            tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
            row = dict(seed=sd,
                       a_echo=round(amp10(tt, e), 1),
                       dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                       steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                       iq_std=round(float(np.std(Y["iq"][(tt >= 4) & (tt < 6)])), 2),
                       w7=[round(float(np.sqrt(np.mean(e[(tt >= a) & (tt < b)] ** 2))), 1)
                           for a, b in WIN])
            out[name].append(row)
            print("%-5s seed=%d echo=%6.1f dip=%7.1f steady=%5.2f iqstd=%4.2f"
                  % (name, sd, row["a_echo"], row["dip"], row["steady"], row["iq_std"]),
                  flush=True)
    json.dump(out, open("_inv_lawd.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\n== summary ==")
    for name in ("Base", "LawD"):
        for key in ("a_echo", "dip", "steady", "iq_std"):
            v = np.array([r[key] for r in out[name]])
            print("%-5s %-7s %7.2f ± %5.2f" % (name, key, v.mean(), v.std(ddof=1)))
    print("DONE")


if __name__ == "__main__":
    main()
