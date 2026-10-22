# -*- coding: utf-8 -*-
"""run_eso_speed_trace.py —— 600/900/1200 rpm 的转速波形（供 plot_eso_speed_time.py 出图）

每个转速存 4 条轨迹（同种子 20261018、实验室噪声）：
    Base·lin / Base·fal / F-B·lin / F-B·fal方向
输出：_eso_speed_trace.npz
"""
import math
import numpy as np
from multiprocessing import Pool
import noise_cfg as NC

DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
SEED = 20261018
LAB = dict(i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"])
FB_OLD = dict(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0, ff_gmax=0.05)
FB_DIR = dict(ff_mism=0.30, ff_mism_eps=1e-6, ff_cool=0.30, ff_flush=0.0,
              ff_gmax=0.05, ff_mism_dir=1)
SPEEDS = [(600.0, 10.0), (900.0, 15.0), (1200.0, 20.0)]
CFG = [("Base_lin", dict(det_eps=0.0, eso_law="linear")),
       ("Base_fal", dict(det_eps=0.0)),
       ("FB_lin", dict(FB_OLD, eso_law="linear")),
       ("FB_fal", dict(FB_DIR))]


def build_case(T):
    t = np.arange(0.0, TEND, DT)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    TL = (0.50 * on + 0.30 * onp *
          (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))) * 0.637
    return t, TL


def run_one(job):
    nref, flo, name, kw = job
    from pmsm_inv_sim import sim_inv
    T = 1.0 / flo
    t, TL = build_case(T)
    cfg = dict(n_ref=nref, T=T, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=SEED, **LAB)
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    return {"key": "%d_%s" % (int(nref), name), "t": Y["t"], "y": Y["y"] * nref,
            "trig": np.array([z[0] for z in Y["trig"]], dtype=float)}


if __name__ == "__main__":
    jobs = [(n, f, nm, kw) for (n, f) in SPEEDS for nm, kw in CFG]
    with Pool(8) as p:
        rows = p.map(run_one, jobs)
    out = {}
    for r in rows:
        out["t"] = r["t"]
        out[r["key"]] = r["y"]
        out[r["key"] + "_trig"] = r["trig"]
    np.savez_compressed("_eso_speed_trace.npz", **out)
    print("saved", len(rows), "traces")
