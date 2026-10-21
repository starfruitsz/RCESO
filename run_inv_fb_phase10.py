# -*- coding: utf-8 -*-
"""10 Hz 相位复位尝试（负结果）：20 ms 正交解调 v 的相位，按目标相位复位。

目标相位 0 / pi/2 / pi / 3pi/2；检测仍为 D_m>0.2 + g<0.05。
用法：python run_inv_fb_phase10.py → _inv_fb_phase10.json
"""
import math
import json

import numpy as np

from pmsm_inv_sim import sim_inv, N_REF
import noise_cfg as NC

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
SEEDS = [20261018, 20261021]
FB = dict(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0,
          ff_gmax=0.05, ff_phase_tol=0.35, ff_phase_max=0.04)
CFG = [("p0", 0.0), ("p90", math.pi / 2), ("p180", math.pi), ("p270", 3 * math.pi / 2)]


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
    out = {}
    for sd in SEEDS:
        for name, tgt in CFG:
            cfg = dict(base_kw, **FB); cfg["seed_i"] = sd; cfg["ff_phase"] = tgt
            Y = sim_inv(t, TL, cfg)
            tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
            tr = [x for x in Y["trig"] if 6.0 <= x[0] < 7.0]
            row = dict(seed=sd, target=tgt, a_echo=round(amp10(tt, e), 1),
                       dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                       first=(round(tr[0][0], 3) if tr else None),
                       v_reset=(round(tr[0][1], 1) if tr else None))
            out["%d_%s" % (sd, name)] = row
            print("%-6s seed=%d echo=%6.1f first=%s v=%s"
                  % (name, sd, row["a_echo"], row["first"], row["v_reset"]), flush=True)
    json.dump(out, open("_inv_fb_phase10.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("DONE")


if __name__ == "__main__":
    main()

