# -*- coding: utf-8 -*-
"""F-B 辅助判据对比（8 种子）：e1 残差 vs 跟踪误差 + g 门控 + 绝对下限

口径（与 noise_cfg 一致）：dq 两轴 + 三速率（10us/50us/1ms）、
电流噪声 0.2 A、转速噪声 5 rpm、负载噪声 2.5% 额定。
工况：0–2 s 空载，2 s 加载 0.50 额定，2–6 s 叠加不对中 10 Hz 簇（A=0.30），
6 s 零交越撤除 → 回声窗 6.0–6.1 s，稳态窗 7–12 s。

只做对比实验，结果写 _fb_gate.json；官方配置见 fb_cfg.FB_NEW。
用法：python run_fb_gate.py
"""
import math
import json

import numpy as np

from pmsm_dq_sim import sim_dq, N_REF
import noise_cfg as NC
from fb_cfg import FB_NEW, FB_OLD

T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
SEEDS = [20261018, 20261019, 20261021, 20261022,
         20261023, 20261024, 20261025, 20261026]
WIN = [(0.5, 2.0), (2.0, 2.5), (2.5, 2.6), (3.0, 3.5),
       (3.5, 4.0), (4.0, 6.0), (7.0, 12.0)]

CFG = [
    ("Base", dict(det_eps=0.0)),
    ("FB_e1", dict(FB_OLD)),
    ("FB_et_g", dict(ff_flush=1.8, ff_tau_f=4e-3, ff_tau_s=0.5,
                     ff_cool=0.3, det_eps=0.01,
                     ff_src="et", ff_gmax=0.05)),
    ("FB_et_ga", dict(ff_flush=1.8, ff_tau_f=4e-3, ff_tau_s=0.5,
                      ff_cool=0.3, det_eps=0.01,
                      ff_src="et", ff_gmax=0.05, ff_amin=0.08)),
    ("FB_et_gav", dict(FB_NEW)),
]


def build_case():
    t = np.arange(0.0, TEND, DT)
    n = len(t)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    TL = (0.50 * on + 0.30 * onp *
          (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))) * 0.637
    TL = TL + NC.load_noise(n, DT)
    return t, TL


def amp10(t, e):
    m = (t >= TW) & (t < TW + T)
    ee = e[m]
    tt = t[m]
    c = 2 * np.mean(ee * np.cos(2 * math.pi * tt / T))
    s = 2 * np.mean(ee * np.sin(2 * math.pi * tt / T))
    return float(math.hypot(c, s))


def main():
    t, TL = build_case()
    out = {name: [] for name, _ in CFG}
    for sd in SEEDS:
        for name, kw in CFG:
            cfg = dict(kw, **NC.sim_kwargs())
            cfg["seed_w"] = sd
            Y = sim_dq(t, TL, cfg)
            e = (Y["y"] - 1.0) * N_REF
            fl = Y["fl"]
            tr = [x for x in Y["trig"] if TW <= x[0] < TW + 1.0]
            row = dict(
                seed=sd,
                a_echo=round(amp10(t, e), 1),
                rms_echo=round(float(np.sqrt(np.mean(
                    e[(t >= TW) & (t < TW + T)] ** 2))), 1),
                dip=round(float(np.min(e[(t >= 1.9) & (t <= 2.4)])), 1),
                steady=round(float(np.sqrt(np.mean(e[(t >= 8) & (t < 10)] ** 2))), 2),
                iq_max=round(float(np.max(np.abs(Y["iq"]))), 2),
                n_trig=int(fl[(t >= TW) & (t < TW + 1.0)].sum()),
                first_trig=(round(tr[0][0], 3) if tr else None),
                first_ch=(tr[0][5] if tr else None),
                f36=int(fl[(t >= 3) & (t < 6)].sum()),
                f712=int(fl[(t >= 7) & (t < 12)].sum()),
                w7=[round(float(np.sqrt(np.mean(e[(t >= a) & (t < b)] ** 2))), 2)
                    for a, b in WIN],
            )
            out[name].append(row)
            print("%-9s seed=%d 10Hz=%5.1f dip=%7.1f steady=%5.2f "
                  "nTr=%d first=%s f36=%d f712=%d"
                  % (name, sd, row["a_echo"], row["dip"], row["steady"],
                     row["n_trig"], row["first_trig"], row["f36"], row["f712"]),
                  flush=True)
    json.dump(out, open("_fb_gate.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print("\n== summary (mean ± std over %d seeds) ==" % len(SEEDS))
    for name, _ in CFG:
        a = np.array([r["a_echo"] for r in out[name]])
        d = np.array([r["dip"] for r in out[name]])
        s = np.array([r["steady"] for r in out[name]])
        f = np.array([r["f712"] for r in out[name]])
        print("%-9s 10Hz=%5.1f±%4.1f  dip=%7.1f±%5.1f  steady=%5.2f±%4.2f  "
              "false7-12=%4.1f±%4.1f" % (name, a.mean(), a.std(ddof=1),
                                        d.mean(), d.std(ddof=1),
                                        s.mean(), s.std(ddof=1),
                                        f.mean(), f.std(ddof=1)))
    base = np.array([r["a_echo"] for r in out["Base"]])
    for name, _ in CFG[1:]:
        a = np.array([r["a_echo"] for r in out[name]])
        dif = a - base
        tstat = dif.mean() / (dif.std(ddof=1) / math.sqrt(len(dif)))
        print("paired vs Base %-9s diff=%6.1f±%5.1f rpm  t=%6.2f" %
              (name, dif.mean(), dif.std(ddof=1), tstat))
    print("DONE")


if __name__ == "__main__":
    main()
