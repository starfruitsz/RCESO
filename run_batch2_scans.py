# -*- coding: utf-8 -*-
"""run_batch2_scans.py —— r-z1 控制律下的表格重跑：1D/2D/900/beta3/delta 扫描/300 rpm"""
import json
import math
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from tl_profile import disc_unbalance_profile
from run_laws_compare import build_loads, N_REF, AMP, ANG_START, TW
from run_t_es import build as build30

VIB_H = (1.0, 0.2654, 0.0408, 0.2245, 0.0612, 0.1837)
BASE = dict(fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
            i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
            sig_n=NC.NOISE_LAB["sig_n_rpm"],
            sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
            tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
            tl_ang_start=ANG_START, tl_ang_rev=TW,
            eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
            T=0.1, T_adapt=True, T_filt=50e-3)


def met8(tt, y, iq, nref=600.0):
    e = (y - 1.0) * nref
    m = (tt >= 1.9) & (tt <= 2.5)
    i0 = int(np.where(m)[0][int(np.argmin(e[m]))])
    idx = np.where((np.abs(e) <= 20.0) & (np.arange(len(e)) > i0) & (tt >= 2.0))[0]
    return dict(dip=float(np.min(e[m])),
                rec=float((tt[idx[0]] - 2.0) * 1e3) if len(idx) else float("nan"),
                step_rms=float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))),
                steady=float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2))),
                iq=float(np.max(np.abs(iq))))


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kind, kw = job
    if kind == "load8":
        t, TL = build_loads(); tend = 8.0
    elif kind == "scan8":
        t, TL = build_loads(); tend = 8.0
    elif kind == "r300":
        tend = 20.0
        t = np.arange(0.0, tend, 2e-6)
        vib = np.zeros_like(t)
        for n, a in enumerate(VIB_H, start=1):
            vib += a * np.sin(2.0 * math.pi * 5.9 * n * (t - 2.0) * (t >= 2.0))
        TL = (0.5 * (t >= 2.0)).astype(float) * 0.637 + 0.03 * vib
    cfg = dict(BASE); cfg.update(n_ref=(300.0 if kind == "r300" else 600.0),
                                 T=(0.2 if kind == "r300" else 0.1))
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    nref = float(cfg.get("n_ref", 600.0))
    e = (y - 1.0) * nref
    if kind in ("load8", "scan8"):
        m = met8(tt, y, iq, nref)
        A = float(np.mean(np.asarray(Y["amp"])[(tt >= 5.0)])) if kind == "scan8" else float("nan")
        m["A"] = A
    else:
        ms = tt >= 14.0
        tc = tt[ms]; em = e[ms]
        a1 = 2 * np.mean(em * np.sin(2 * np.pi * 5.0 * tc))
        b1 = 2 * np.mean(em * np.cos(2 * np.pi * 5.0 * tc))
        m = dict(A=float(np.mean(np.asarray(Y["amp"])[ms])),
                 rms=float(np.sqrt(np.mean(em ** 2))), fund=float(np.hypot(a1, b1)))
    print(key, json.dumps(m, ensure_ascii=False), flush=True)
    return key, m


def jobs():
    J = []
    # 1D
    for k, kw in [("base", {}), ("kb4", dict(kp_boost=4.0, det_eps=0.01)),
                  ("kb8", dict(kp_boost=8.0, det_eps=0.01)),
                  ("kb16", dict(kp_boost=16.0, det_eps=0.005)),
                  ("kb8de005", dict(kp_boost=8.0, det_eps=0.005))]:
        J.append((k, "load8", kw))
    # 2D
    for k, kw in [("a2kb8", dict(kp_boost=8.0, kb_eso=2.0, det_eps=0.01)),
                  ("a15kb6", dict(kp_boost=6.0, kb_eso=1.5, det_eps=0.01)),
                  ("a3kb6", dict(kp_boost=6.0, kb_eso=3.0, det_eps=0.01)),
                  ("a25kb4", dict(kp_boost=4.0, kb_eso=2.5, det_eps=0.01)),
                  ("a3kb10", dict(kp_boost=10.0, kb_eso=3.0, det_eps=0.01))]:
        J.append((k, "load8", kw))
    # 900 rpm
    J.append(("base900", "load8", dict(n_ref=900.0, T=1.0 / 15.0)))
    J.append(("lawd900", "load8", dict(n_ref=900.0, T=1.0 / 15.0,
                                       kp_boost=8.0, kb_eso=2.0, det_eps=0.01)))
    # beta3
    for k, kw in [("b0_a05", dict(kp_boost=8.0, kb_eso=0.5, kb_b3=0.0, det_eps=0.01)),
                  ("b1_a05", dict(kp_boost=8.0, kb_eso=0.5, kb_b3=1.0, det_eps=0.01)),
                  ("b3_a05", dict(kp_boost=8.0, kb_eso=0.5, kb_b3=3.0, det_eps=0.01)),
                  ("b0_a1", dict(kp_boost=8.0, kb_eso=1.0, kb_b3=0.0, det_eps=0.01)),
                  ("b3_a1", dict(kp_boost=8.0, kb_eso=1.0, kb_b3=3.0, det_eps=0.01))]:
        J.append((k, "load8", kw))
    # delta scan (8 s, fixed delta)
    for pc in (-20, -15, -12, -10, -8, -6, -4, 0, 2):
        J.append(("d%+d" % pc, "scan8", dict(T_es=True, es_d0=pc / 100.0,
                                             es_step=0.0, es_dith=0.0)))
    # 300 rpm scan
    for pc in (-12, -10, -8, -6, -4, -2, 0, 2):
        J.append(("r300_d%+d" % pc, "r300", dict(T_es=True, es_d0=pc / 100.0,
                                                 es_step=0.0, es_dith=0.0)))
    return J


if __name__ == "__main__":
    with Pool(6) as p:
        res = p.map(one, jobs())
    json.dump(dict(res), open("_batch2_metrics.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("done")
