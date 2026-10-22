# -*- coding: utf-8 -*-
"""补跑：方向限定检测器（D_m=.30, dir=1, cool=.30）下的 F-B 与 D+F-B（8 种子）"""
import json, os
from multiprocessing import Pool
import numpy as np
import run_eso_fal_4cfg as R

FB_NEW = dict(ff_mism=0.30, ff_mism_eps=1e-6, ff_cool=0.30, ff_flush=0.0, ff_gmax=0.05, ff_mism_dir=1)
ALGS = [("F-B", dict(FB_NEW)), ("D+F-B", dict(FB_NEW, kp_boost=4.0, det_eps=0.01))]


def run_one(job):
    alg, kw, seed = job
    from pmsm_inv_sim import sim_inv, N_REF
    t, TL = R.build_case()
    cfg = dict(R.BASE, **kw); cfg["seed_i"] = seed
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]; e = (Y["y"] - 1.0) * N_REF
    tr = [x for x in Y["trig"] if R.TW <= x[0] < R.TW + 1.0]
    return dict(alg=alg, seed=seed, echo=round(R.amp10(tt, e), 2),
                dip=round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
                steady=round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2),
                f26=int(Y["fl"][(tt >= 2.5) & (tt < 6)].sum()),
                first=(round(tr[0][0], 4) if tr else None))


if __name__ == "__main__":
    jobs = [(a, kw, s) for s in R.SEEDS for a, kw in ALGS]
    with Pool(8) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out.setdefault(r["alg"], []).append(r)
    json.dump(out, open("_fb_retune_dir.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for k, rr in out.items():
        f = lambda fld: np.array([x[fld] for x in rr], dtype=float)
        print("%-8s echo %6.2f±%4.2f  dip %7.1f±%5.1f  steady %5.2f±%4.2f  f26 %.1f  first %s"
              % (k, f("echo").mean(), f("echo").std(ddof=1), f("dip").mean(), f("dip").std(ddof=1),
                 f("steady").mean(), f("steady").std(ddof=1), f("f26").sum() / len(rr),
                 ",".join("%.3f" % x["first"] for x in rr if x["first"])))
