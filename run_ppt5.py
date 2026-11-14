# -*- coding: utf-8 -*-
"""run_ppt5.py —— PPT 余下 5 图的组合故障数据：不对中 β=1° + 圆盘不平衡"""
import numpy as np, json
from multiprocessing import Pool
import noise_cfg as NC

DT = 2e-6
FAULT = dict(start=2.0,
             unbalance=dict(M=0.1, e=1e-4, kappa=580.0),
             misalign=dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0))
FAULT_REV = dict(FAULT, rev=5.98361)


def sim_one(job):
    from pmsm_inv_sim import sim_inv
    key, TEND, nref, TL, kw = job
    t = np.arange(0.0, TEND, DT)
    TL = np.asarray(TL, dtype=float)
    if len(TL) < len(t) + 5:
        TL = np.concatenate([TL, np.full(len(t) + 5 - len(TL), TL[-1])])
    cfg = dict(n_ref=nref, T=0.1, T_adapt=True, T_filt=50e-3,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0)
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    out = dict(t=Y["t"], y=Y["y"], iq=Y["iq"], tl=Y["tl"], b0e=Y["b0e"])
    for k in ("amp", "es"):
        if k in Y: out[k] = Y[k]
    np.savez("_ppt5_%s.npz" % key, **out)
    e = (np.asarray(Y["y"]) - 1.0) * nref
    return key, float(np.sqrt(np.mean(e ** 2))), float(np.max(np.abs(Y["iq"])))


def build_jobs():
    jobs = []
    # s5: 3 cases x 2 low-pass
    for case in ("load", "speed", "echo"):
        TL = (0.50 * (np.arange(0, 8.0, DT) >= 2.0)).astype(float) * 0.637
        for ck, tau in (("lpf", 20e-3), ("nolpf", 2e-6)):
            kw = dict(tau0=tau, tl_fault=(FAULT_REV if case == "echo" else FAULT))
            if case == "speed": kw.update(n_ref2=900.0, t_nref=5.0)
            jobs.append(("s5_%s_%s" % (case, ck), 8.0, 600.0, TL, kw))
    # s8: A step, B constant load
    t8 = np.arange(0, 8.0, DT)
    TL_A = (0.50 * (t8 >= 2.0)).astype(float) * 0.637
    TL_B = 0.50 * 0.637 * np.ones_like(t8)
    jobs.append(("s8_A", 8.0, 600.0, TL_A, dict(tl_fault=FAULT, n_ref2=300.0, t_nref=6.0)))
    jobs.append(("s8_B", 8.0, 600.0, TL_B, dict(tl_fault=FAULT)))
    # s10: base/lawd
    for key, kw in (("s10_base", dict(det_eps=0.0)),
                    ("s10_lawd", dict(kp_boost=6.0, det_eps=0.01, kb_eso=3.0, kb_b3=0.0))):
        jobs.append((key, 8.0, 600.0, TL_A, dict(tl_fault=FAULT, **kw)))
    # s13: base/esc 30 s
    for key, kw in (("s13_base", dict(T_es=True, es_d0=0.0, es_step=0.0, es_dith=0.0)),
                    ("s13_esc", dict(T_es=True, es_d0=-0.143, es_step=0.01, es_dith=0.005,
                                     es_Pd=1.5, es_N=3, es_dead=1e-5, es_dmax=0.20, es_t0=3.0))):
        jobs.append((key, 30.0, 600.0, TL_A, dict(tl_fault=FAULT, **kw)))
    return jobs

if __name__ == "__main__":
    with Pool(5) as p:
        out = p.map(sim_one, build_jobs())
    print(out, flush=True)
    json.dump(dict(out), open("_ppt5.json", "w"), indent=1)
