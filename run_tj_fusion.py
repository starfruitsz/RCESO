# -*- coding: utf-8 -*-
"""run_tj_fusion.py —— 律T(DFT) × 律J 融合实验。
用法: python run_tj_fusion.py <tag> <mode>   mode: base | t | j | fusion
场景：600 rpm、30 s、组合故障（不对中+不平衡，2 s 起）、J_true=9.95e-5=5.26 J_nom、
      2 s 加载 0.50 额定；律J 用周期 DFT 复检 + b0 低通（btau=20 ms），律T 用 dither ESC + DFT 幅值。
"""
import numpy as np, json, sys, time
import noise_cfg as NC
from pmsm_inv_sim import sim_inv

tag = sys.argv[1]; mode = sys.argv[2]
DT = 2e-6; TEND = 30.0
FAULT = dict(start=2.0,
             unbalance=dict(M=0.1, e=1e-4, kappa=580.0),
             misalign=dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0))
t = np.arange(0.0, TEND, DT)
TL = (0.50 * (t >= 2.0)).astype(float) * 0.637

cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=4000.0,
           Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
           rc_bp=5.0, b3_min=4000.0, b3_max=4000.0,
           tl_fault=FAULT, J_true=9.95e-5)

use_t = mode in ("t", "fusion")
use_j = mode in ("j", "fusion")

if use_t:
    cfg.update(T_es=True, es_d0=-0.143, es_step=0.01, es_dith=0.005, es_Pd=1.5, es_N=3,
               es_dead=2e-6, es_dmax=0.20, es_t0=3.0, T_dft=2.0, a_ref=0.2)
else:
    cfg.update(T_es=False, a_ref=1.0)

if use_j:
    cfg.update(j_recheck=True, j_recheck_period=2.0, j_recheck_len=0.6, j_recheck_amp=0.157,
               j_recheck_nmin=2, j_recheck_t0=1.0, j_recheck_f_auto=True, j_recheck_f_q=6.0,
               j_recheck_f_alpha=0.35, j_recheck_f_min=50.0, j_recheck_f_max=110.0,
               j_recheck_amp_auto=True, j_recheck_gate=True, j_recheck_gate_ac=10.0,
               j_recheck_gate_step=10.0, j_recheck_apply=True, j_recheck_alpha=0.8,
               j_recheck_btau=20e-3)

t0 = time.time()
Y = sim_inv(t, TL, cfg)
el = time.time() - t0
tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
es = np.asarray(Y["es"]); amp = np.asarray(Y["amp"]); jh = np.asarray(Y["jhat"])
tj = np.asarray(Y["t_j"]); b0 = np.asarray(Y["b0e"])
np.savez("_tj_%s.npz" % tag, t=tt, y=y, iq=iq, tl=np.asarray(Y["tl"]), b0e=b0,
         amp=amp, es=es, jhat=jh, t_j=tj)

e = (y - 1.0) * 600.0
m = tt >= 25.0
rms = float(np.sqrt(np.mean(e[m] ** 2)))
# 10 Hz 幅值（25-30 s，Hann）
w = (tt >= 25.0) & (tt < 30.0)
x = e[w] - e[w].mean()
X = np.fft.rfft(x * np.hanning(len(x)))
fr = np.fft.rfftfreq(len(x), d=float(tt[1] - tt[0]))
k10 = int(np.argmin(np.abs(fr - 10.0)))
a10 = float(2.0 * np.abs(X[k10]) / np.sum(np.hanning(len(x))))
# iq1ms（t>=2 起）
n1 = int(round(1e-3 / (tt[1] - tt[0])))
iq1 = np.abs(iq[:len(iq)//n1*n1].reshape(-1, n1).mean(axis=1))
t1 = tt[:len(iq1)*n1:n1]
iq1ms = float(iq1[t1 >= 2.0].max())

d = dict(tag=tag, mode=mode, use_t=use_t, use_j=use_j, J_true=9.95e-5,
         jfin=float(jh[-1]), jerr_pct=float(100.0 * (jh[-1] / 9.95e-5 - 1.0)),
         b0e=float(b0[-1]), es_end=float(es[-1] if es.size else 0.0),
         es_mean=float(np.mean(es[tt >= 25.0])) if es.size else 0.0,
         rms=rms, amp10=a10, iq1ms=iq1ms, iq_raw=float(np.abs(iq).max()), runtime_s=el)
json.dump(d, open("_tj_%s.json" % tag, "w"), indent=1)
print("%-8s T=%d J=%d | RMS %6.2f  10Hz %6.2f  iq1ms %5.2f  Jhat %+6.1f%%  b0e %6.1f  es %7.3f  (%.0fs)" % (
    tag, use_t, use_j, rms, a10, iq1ms, d["jerr_pct"], d["b0e"], d["es_mean"], el), flush=True)
