# -*- coding: utf-8 -*-
"""run_es_nofreeze.py —— 换速工况 600→900 rpm：ESC 冻结 开/关 对照。
用法: python run_es_nofreeze.py <tag> <nofreeze 0|1>
配置：融合（律T DFT + 律J 10 s 直测 b0、校验关）、组合故障、5 s 换速、20 s。"""
import numpy as np, json, sys, time
import noise_cfg as NC
from pmsm_inv_sim import sim_inv

tag = sys.argv[1]; NOF = (sys.argv[2] == "1")
DT = 2e-6; TEND = 20.0
FAULT = dict(start=2.0, unbalance=dict(M=0.1, e=1e-4, kappa=580.0),
             misalign=dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0))
t = np.arange(0.0, TEND, DT)
TL = (0.50 * (t >= 2.0)).astype(float) * 0.637
cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=4000.0,
           Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
           rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=0.2,
           tl_fault=FAULT, J_true=9.95e-5,
           n_ref2=900.0, t_nref=5.0,
           T_es=True, es_d0=-0.143, es_step=0.01, es_dith=0.005, es_Pd=1.5, es_N=3,
           es_dead=2e-6, es_dmax=0.20, es_t0=3.0, T_dft=2.0,
           es_ff=True, es_freeze=2.0, es_nofreeze=NOF,
           j_recheck=True, j_recheck_period=10.0, j_recheck_len=0.6, j_recheck_amp=0.157,
           j_recheck_nmin=2, j_recheck_t0=1.0, j_recheck_f_auto=True, j_recheck_f_q=6.0,
           j_recheck_f_alpha=0.35, j_recheck_f_min=50.0, j_recheck_f_max=110.0,
           j_recheck_amp_auto=True, j_recheck_gate=True, j_recheck_gate_ac=10.0,
           j_recheck_gate_step=10.0, j_recheck_apply=True, j_recheck_alpha=0.8,
           j_recheck_btau=20e-3, j_b0_direct=True, j_validate=False)
t0 = time.time()
Y = sim_inv(t, TL, cfg)
el = time.time() - t0
tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); es = np.asarray(Y["es"])
nref = np.where(tt >= 5.0, 900.0, 600.0)
e = (y - 1.0) * nref
np.savez("_esnf_%s.npz" % tag, t=tt, y=y, es=es, nref=nref, iq=np.asarray(Y["iq"]))
m1 = (tt >= 3.5) & (tt < 5.0); m2 = (tt >= 12.0) & (tt < 20.0)
d = dict(tag=tag, nofreeze=int(NOF),
         es_pre=float(np.mean(es[m1])), es_post=float(np.mean(es[m2])),
         es_post_std=float(np.std(es[m2])),
         rms_pre=float(np.sqrt(np.mean(e[m1] ** 2))), rms_post=float(np.sqrt(np.mean(e[m2] ** 2))),
         dstar900=-0.172, runtime_s=el)
json.dump(d, open("_esnf_%s.json" % tag, "w"), indent=1)
print("%-5s nofreeze=%d  δ 换速前 %.4f  换速后 %.4f±%.4f (理论 %.3f)  RMS %.1f→%.1f  (%.0fs)" % (
    tag, int(NOF), d["es_pre"], d["es_post"], d["es_post_std"], d["dstar900"], d["rms_pre"], d["rms_post"], el), flush=True)
