# -*- coding: utf-8 -*-
"""run_scan_fix.py —— 补跑 delta 扫描与 300 rpm 扫描（含 rc_bp，A 可算）"""
import json, math
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC
from tl_profile import disc_unbalance_profile
from run_laws_compare import build_loads, N_REF, AMP, ANG_START, TW

VIB_H = (1.0, 0.2654, 0.0408, 0.2245, 0.0612, 0.1837)
BASE = dict(fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
            rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
            i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
            sig_n=NC.NOISE_LAB["sig_n_rpm"],
            sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
            tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
            tl_ang_start=ANG_START, tl_ang_rev=TW,
            eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
            T=0.1, T_adapt=True, T_filt=50e-3)


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kind, d0 = job
    if kind == "scan8":
        t, TL = build_loads()
    else:
        tend = 20.0
        t = np.arange(0.0, tend, 2e-6)
        vib = np.zeros_like(t)
        for n, a in enumerate(VIB_H, start=1):
            vib += a * np.sin(2.0 * math.pi * 5.9 * n * (t - 2.0) * (t >= 2.0))
        TL = (0.5 * (t >= 2.0)).astype(float) * 0.637 + 0.03 * vib
    cfg = dict(BASE)
    cfg.update(n_ref=(300.0 if kind == "r300" else 600.0),
               T=(0.2 if kind == "r300" else 0.1),
               T_es=True, es_d0=d0, es_step=0.0, es_dith=0.0)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); A = np.asarray(Y["amp"])
    nref = float(cfg["n_ref"]); e = (y - 1.0) * nref
    if kind == "scan8":
        mA = float(np.mean(A[(tt >= 5.0) & (tt < 8.0)]))
        mR = float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2)))
    else:
        mA = float(np.mean(A[tt >= 14.0]))
        mR = float(np.sqrt(np.mean(e[tt >= 14.0] ** 2)))
    print(key, "A %.5f  RMS %.2f" % (mA, mR), flush=True)
    return key, dict(A=mA, RMS=mR, d0=d0)


if __name__ == "__main__":
    J = [("d%+d" % pc, "scan8", pc / 100.0) for pc in (-20, -15, -12, -10, -8, -6, -4, 0, 2)]
    J += [("r300_d%+d" % pc, "r300", pc / 100.0) for pc in (-12, -10, -8, -6, -4, -2, 0, 2)]
    with Pool(6) as p:
        res = p.map(one, J)
    json.dump(dict(res), open("_scan_fix.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("done")
