# -*- coding: utf-8 -*-
"""真实逆变器对象上的四档对比：Base / 律 D / 新 F-B / D+新 F-B

口径：pmsm_inv_sim（三相 PWM、死区、器件压降、反电动势、编码器量化、
dq 采样噪声 U(±0.3 A)），fci=2 kHz、beta3=4000、tau0=20 ms。
工况：0–2 s 空载，2 s 加载 0.50 额定；2–6 s 叠加 10 Hz 簇（A=0.30），6 s 撤除。
用法：python run_inv_study.py [nseeds]  → _inv_study.json
"""
import math
import json
import sys

import numpy as np

from pmsm_inv_sim import sim_inv, N_REF
import noise_cfg as NC
from fb_cfg import FB_NEW

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
SEEDS_ALL = [20261018, 20261019, 20261021, 20261022,
             20261023, 20261024, 20261025, 20261026]
WIN = [(0.5, 2.0), (2.0, 2.5), (2.5, 2.6), (3.0, 3.5),
       (3.5, 4.0), (4.0, 6.0), (7.0, 8.0)]

CFG = [
    ("Base", dict(det_eps=0.0)),
    ("LawD", dict(kp_boost=4.0, det_eps=0.01)),
    ("FB", dict(FB_NEW)),
    ("D+FB", dict(FB_NEW, kp_boost=4.0)),
    # 重扫尝试：k=1.3 + 短冷却 + |v| 门控（会触发 6.004，但加载段误触发多）
    ("FB_lowk", dict(FB_NEW, ff_flush=1.3, ff_cool=0.02,
                     ff_gmax=-1.0, ff_amin=0.0, ff_vmax=20.0)),
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
    nseed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    seeds = SEEDS_ALL[:nseed]
    t, TL = build_case()
    base_kw = dict(i_noise_peak=NC.NOISE["i_noise_peak"],
                   fci=2000.0, beta3=4000.0, tau0=20e-3)
    out = {name: [] for name, _ in CFG}
    for sd in seeds:
        for name, kw in CFG:
            cfg = dict(base_kw, **kw)
            cfg["seed_i"] = sd
            Y = sim_inv(t, TL, cfg)
            tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
            tr = [x for x in Y["trig"] if TW <= x[0] < TW + 1.0]
            row = dict(seed=sd,
                       a_echo=round(amp10(tt, e), 1),
                       dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                       steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                       n_trig=len(tr),
                       first=(round(tr[0][0], 3) if tr else None),
                       f712=int(Y["fl"][(tt >= 7) & (tt < 8)].sum()),
                       w7=[round(float(np.sqrt(np.mean(e[(tt >= a) & (tt < b)] ** 2))), 1)
                           for a, b in WIN])
            out[name].append(row)
            print("%-5s seed=%d echo=%6.1f dip=%7.1f steady=%5.2f nTr=%d first=%s"
                  % (name, sd, row["a_echo"], row["dip"], row["steady"],
                     row["n_trig"], row["first"]), flush=True)
    json.dump(out, open("_inv_study.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("DONE", nseed)


if __name__ == "__main__":
    main()
