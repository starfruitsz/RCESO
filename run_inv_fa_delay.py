# -*- coding: utf-8 -*-
"""F-A oracle 的复位时刻扫描：6.0+tau ms，tau=0..40

用于说明真实对象上“越早复位越好”不成立：最优复位时刻在 20–25 ms。
用法：python run_inv_fa_delay.py → _inv_fa_delay.json
"""
import math
import json

import numpy as np

from pmsm_inv_sim import sim_inv, N_REF
import noise_cfg as NC

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
SEEDS = [20261018, 20261021]
DELAYS = [0.0, 0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.040]


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
    out = {}
    for sd in SEEDS:
        for dly in DELAYS:
            cfg = dict(base_kw, seed_i=sd, flush_t=6.0 + dly, flush_alpha=0.0)
            Y = sim_inv(t, TL, cfg)
            tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
            key = "%d_%.3f" % (sd, dly)
            out[key] = dict(seed=sd, delay=dly, a_echo=round(amp10(tt, e), 1),
                            dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1))
            print(key, "echo", out[key]["a_echo"], flush=True)
    json.dump(out, open("_inv_fa_delay.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("DONE")


if __name__ == "__main__":
    main()
