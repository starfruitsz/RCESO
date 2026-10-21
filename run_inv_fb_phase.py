# -*- coding: utf-8 -*-
"""相位等待型 F-B 的负结果：固定延时 vs v 阈值

检测仍用 D_m>0.2 + g<0.05；检测后：
  FB_w10/FB_w20：再等 10/20 ms 复位；
  FB_v50/FB_v70：等 v<-50/-70（上限 30 ms）复位。
2 个种子，说明“简单相位等待”不能稳定闭合与 oracle 的 3.45 rpm 差距。
用法：python run_inv_fb_phase.py → _inv_fb_phase.json
"""
import math
import json

import numpy as np

from pmsm_inv_sim import sim_inv, N_REF
import noise_cfg as NC

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
SEEDS = [20261018, 20261021]
FB = dict(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0,
          ff_gmax=0.05)
CFG = [
    ("FB", dict(FB)),
    ("FB_w10", dict(FB, ff_wait=0.010)),
    ("FB_w20", dict(FB, ff_wait=0.020)),
    ("FB_v50", dict(FB, ff_vphase=-50.0, ff_vwait_max=0.03)),
    ("FB_v70", dict(FB, ff_vphase=-70.0, ff_vwait_max=0.03)),
]


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
    out = {n: [] for n, _ in CFG}
    for sd in SEEDS:
        for name, kw in CFG:
            cfg = dict(base_kw, **kw); cfg["seed_i"] = sd
            Y = sim_inv(t, TL, cfg)
            tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
            tr = [x for x in Y["trig"] if 6.0 <= x[0] < 7.0]
            row = dict(seed=sd, a_echo=round(amp10(tt, e), 1),
                       dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                       first=(round(tr[0][0], 3) if tr else None),
                       v_reset=(round(tr[0][1], 1) if tr else None),
                       f78=int(Y["fl"][(tt >= 7) & (tt < 8)].sum()))
            out[name].append(row)
            print("%-7s seed=%d echo=%6.1f dip=%7.1f first=%s v=%s f78=%d"
                  % (name, sd, row["a_echo"], row["dip"], row["first"],
                     row["v_reset"], row["f78"]), flush=True)
    json.dump(out, open("_inv_fb_phase.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("DONE")


if __name__ == "__main__":
    main()

