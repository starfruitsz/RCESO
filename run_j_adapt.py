# -*- coding: utf-8 -*-
"""run_j_adapt.py —— J 自适应方案对比：固定标称 / oracle 重整定 / 在线辨识

J_true = 9.95e-5 kg·m²（电机 1.89e-5 + 联轴器 1.5e-6 + 圆盘 6.75e-5 + 轴承 1.16e-5）
故障：不平衡等效 T1=0.0569 N·m（κ=580, M=0.1, e=1e-4），10 s、600 rpm。
"""
import json, math
from multiprocessing import Pool
import numpy as np
import noise_cfg as NC

JM = 1.89e-5
J_BIG = 9.95e-5
CASES = [
    ("Jm_nofault", dict(J_true=JM)),
    ("Jm_fault", dict(J_true=JM, fault=True)),
    ("big_nofault", dict(J_true=J_BIG)),
    ("big_fault", dict(J_true=J_BIG, fault=True)),
    ("big_oracle", dict(J_true=J_BIG, fault=True, j_oracle=True)),
    ("big_adapt", dict(J_true=J_BIG, fault=True, j_id=True)),
    ("big_adapt_nf", dict(J_true=J_BIG, j_id=True)),
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
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
               J_true=o["J_true"])
    if o.get("fault"):
        cfg["tl_fault"] = {"start": 0.0, "unbalance": dict(M=0.1, e=1e-4, kappa=580.0)}
    if o.get("j_id"):
        cfg.update(j_id=True, j_adapt_b0=True, j_adapt_kp=False, j_id_f=200.0, j_id_amp_u=0.0314, j_id_win=0.4, j_id_lp=0.3)
    if o.get("j_oracle"):
        cfg.update(j_oracle=True)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 600.0
    m = (tt >= 9.0) & (tt < 10.0); tc, ec = tt[m], e[m]
    amp10 = float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*tc)),
                           2*np.mean(ec*np.sin(2*np.pi*10*tc))))
    amp100 = float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*200*tc)),
                            2*np.mean(ec*np.sin(2*np.pi*200*tc))))
    rms = float(np.sqrt(np.mean(ec**2)))
    jh = np.asarray(Y.get("jhat", [])); tj = np.asarray(Y.get("t_j", []))
    jfin = float(jh[-1]) if jh.size else float("nan")
    tconv = float("nan")
    if jh.size and o.get("j_id"):
        band = np.abs(jh - o["J_true"]) / o["J_true"] <= 0.10
        idx = np.where(band)[0]
        if idx.size:
            # 首次进入且此后保持
            for i0 in idx:
                if band[i0:].all():
                    tconv = float(tj[i0]); break
    print("%-13s 10Hz %6.2f  100Hz %5.2f  RMS %6.2f  iq %5.2f  Jhat %.2e  tconv %.2f"
          % (key, amp10, amp100, rms, float(np.max(np.abs(iq))), jfin, tconv), flush=True)
    return key, dict(amp10=amp10, amp100=amp100, rms=rms, iq=float(np.max(np.abs(iq))),
                     jfin=jfin, tconv=tconv, Jtrue=o["J_true"])

if __name__ == "__main__":
    with Pool(7) as p: res = p.map(one, CASES)
    json.dump(dict(res), open("_j_adapt.json","w"), indent=1); print("done")
