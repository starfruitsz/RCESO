# -*- coding: utf-8 -*-
"""run_trio.py —— D + T + J 三环同时投运（对比 J 关）"""
import json
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC

JB = 9.95e-5
CASES = [("trio", dict(j=True)), ("d_t_only", dict(j=False))]

def one(job):
    from pmsm_inv_sim import sim_inv
    key, o = job
    t = np.arange(0.0, 12.0, 2e-6); TL = np.zeros_like(t)
    cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0, J_true=JB,
               kp_boost=6.0, kb_eso=3.0, det_eps=0.01,
               tl_fault={"start": 0.0, "unbalance": dict(M=0.1, e=1e-4, kappa=581.0)},
               T_es=True)
    if o["j"]:
        # 应力测试口径：隔离状态 4 校验（应用后校验/回退见 run_j_state4.py）
        cfg.update(j_id=True, j_id_f=100.0, j_id_amp_u=0.157, j_id_win=0.2,
                   j_id_lp=0.4, j_id_t0=1.0, j_id_tend=3.0, j_adapt_b0=True,
                   j_id_snr_min=2.0, j_id_nmin=5, j_id_std_max=0.15, j_val=False)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 600.0
    m = (tt >= 11) & (tt < 12); tc, ec = tt[m], e[m]
    a10 = float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*tc)), 2*np.mean(ec*np.sin(2*np.pi*10*tc))))
    rms = float(np.sqrt(np.mean(ec**2)))
    js = np.asarray(Y["jstate"]); jh = np.asarray(Y["jhat"])
    es = np.asarray(Y["es"])
    print("%-8s 10Hz %6.2f RMS %6.2f iq %5.2f Jhat %.2e state=%d delta=%.3f"
          % (key, a10, rms, float(np.max(np.abs(iq))), float(jh[-1]), int(js[-1]), float(np.mean(es[tt>10]) if tt.size else 0)), flush=True)
    return key, dict(a10=a10, rms=rms, iq=float(np.max(np.abs(iq))), jfin=float(jh[-1]), state=int(js[-1]))
if __name__ == "__main__":
    with Pool(2) as p: res = p.map(one, CASES)
    json.dump(dict(res), open("_trio.json","w"), indent=1); print("done")
