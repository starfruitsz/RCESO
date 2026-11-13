# -*- coding: utf-8 -*-
"""run_j_state.py —— 状态机验证 + 真实 J 下的 T1 扫描（自适应）"""
import json, math
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC

JM = 1.89e-5
JB = 9.95e-5
K = lambda t1: t1 / (0.1 * 9.80665 * 1e-4)
CASES = [
    ("comm_norm", dict(T1=0.057, A=0.157, tend=3.0)),
    ("comm_lowA", dict(T1=0.057, A=0.02, tend=3.0)),
    ("comm_fast", dict(T1=0.057, A=0.157, tend=1.5)),
    ("comm_nofault", dict(T1=0.0, A=0.157, tend=3.0)),
    ("adapt_T010", dict(T1=0.10, A=0.157, tend=3.0)),
    ("adapt_T015", dict(T1=0.15, A=0.157, tend=3.0)),
    ("adapt_T020", dict(T1=0.20, A=0.157, tend=3.0)),
    ("adapt_T030", dict(T1=0.30, A=0.157, tend=3.0)),
    ("fixed_T030", dict(T1=0.30, A=0.0, tend=0.0)),
    ("Js_T010", dict(T1=0.10, A=0.157, tend=3.0, J=4.5e-5)),
    ("Js_T015", dict(T1=0.15, A=0.157, tend=3.0, J=4.5e-5)),
]

def one(job):
    from pmsm_inv_sim import sim_inv
    key, o = job
    t = np.arange(0.0, 10.0, 2e-6); TL = np.zeros_like(t)
    cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0, J_true=o.get("J", JB))
    if o["T1"] > 0:
        cfg["tl_fault"] = {"start": 0.0, "unbalance": dict(M=0.1, e=1e-4, kappa=K(o["T1"]))}
    if o["A"] > 0:
        cfg.update(j_id=True, j_id_f=100.0, j_id_amp_u=o["A"], j_id_win=0.2,
                   j_id_lp=0.4, j_id_t0=0.5, j_id_tend=o["tend"],
                   j_adapt_b0=True, j_id_snr_min=2.0, j_id_nmin=3, j_id_std_max=0.15)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 600.0
    def amp(f, a, b):
        m = (tt >= a) & (tt < b); tc, ec = tt[m], e[m]
        return float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*f*tc)), 2*np.mean(ec*np.sin(2*np.pi*f*tc))))
    a10 = amp(10, 9, 10); aid = amp(100, 0.5, min(3.0, o["tend"] if o["tend"] > 0 else 3.0))
    apost = amp(100, 9, 10)
    rms = float(np.sqrt(np.mean(e[(tt >= 9) & (tt < 10)]**2)))
    js = np.asarray(Y.get("jstate", [])); jf = float(js[-1]) if js.size else 0
    jh = np.asarray(Y.get("jhat", [])); jfin = float(jh[-1]) if jh.size else float("nan")
    print("%-12s T1=%.3f state=%d Jhat=%.2e 10Hz %6.2f 100Hz(id) %5.2f 100Hz(post) %5.2f RMS %6.2f iq %5.2f"
          % (key, o["T1"], jf, jfin, a10, aid, apost, rms, float(np.max(np.abs(iq)))), flush=True)
    return key, dict(T1=o["T1"], state=int(jf), jfin=jfin, a10=a10, aid=aid,
                     apost=apost, rms=rms, iq=float(np.max(np.abs(iq))))

if __name__ == "__main__":
    with Pool(6) as p: res = p.map(one, CASES)
    json.dump(dict(res), open("_j_state.json","w"), indent=1); print("done")
