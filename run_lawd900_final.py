# -*- coding: utf-8 -*-
"""run_lawd900_final.py —— 900 rpm 基准与律D(kb6,a3)对比"""
import json
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC
from tl_profile import disc_unbalance_profile
from run_laws_compare import build_loads, N_REF, AMP, ANG_START

BASE = dict(n_ref=900.0, T=1.0/15.0, T_adapt=True, T_filt=50e-3,
            fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
            i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
            sig_n=NC.NOISE_LAB["sig_n_rpm"],
            sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
            tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
            tl_ang_start=ANG_START, tl_ang_rev=29.9,
            eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
            rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0)


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kw = job
    t, TL = build_loads()
    cfg = dict(BASE); cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 900.0
    m = (tt >= 1.9) & (tt <= 2.5)
    i0 = int(np.where(m)[0][int(np.argmin(e[m]))])
    idx = np.where((np.abs(e) <= 20.0) & (np.arange(len(e)) > i0) & (tt >= 2.0))[0]
    d = dict(dip=float(np.min(e[m])), rec=float((tt[idx[0]]-2.0)*1e3),
             step_rms=float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))),
             steady=float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2))),
             iq=float(np.max(np.abs(iq))))
    print(key, json.dumps(d), flush=True)
    return key, d


if __name__ == "__main__":
    jobs = [("base900", {}), ("lawd900", dict(kp_boost=6.0, kb_eso=3.0, kb_b3=0.0, det_eps=0.01))]
    with Pool(2) as p:
        res = p.map(one, jobs)
    json.dump(dict(res), open("_lawd900_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("done")
