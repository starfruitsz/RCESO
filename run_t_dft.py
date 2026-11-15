# -*- coding: utf-8 -*-
"""run_t_dft.py —— 律T 的基波幅值：带通 vs 整数周期 DFT。
用法: python run_t_dft.py <tag> <T_dft 周期数>   （0 = 带通）
配置完全沿用 run_ppt5.py 的 s13_esc（600 rpm、30 s、组合故障、dither 极值搜索）。
"""
import numpy as np, json, sys, time
import noise_cfg as NC
from pmsm_inv_sim import sim_inv

tag = sys.argv[1]; Tdft = float(sys.argv[2])
DEAD = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-5
AREF = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
DT = 2e-6; TEND = 30.0
FAULT = dict(start=2.0,
             unbalance=dict(M=0.1, e=1e-4, kappa=580.0),
             misalign=dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0))
t = np.arange(0.0, TEND, DT)
TL = (0.50 * (t >= 2.0)).astype(float) * 0.637
cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3,
           fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
           rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=AREF,
           tl_fault=FAULT,
           T_es=True, es_d0=-0.143, es_step=0.01, es_dith=0.005,
           es_Pd=1.5, es_N=3, es_dead=DEAD, es_dmax=0.20, es_t0=3.0,
           T_dft=Tdft)
t0 = time.time()
Y = sim_inv(t, TL, cfg)
el = time.time() - t0
out = dict(t=Y["t"], y=Y["y"], iq=Y["iq"], tl=Y["tl"], b0e=Y["b0e"], amp=Y["amp"], es=Y["es"])
np.savez("_tdft_%s.npz" % tag, **out)

tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); e = (y - 1.0) * 600.0
iq = np.asarray(Y["iq"]); es = np.asarray(Y["es"]); amp = np.asarray(Y["amp"])
m = tt >= 3.0
rms = float(np.sqrt(np.mean(e[m] ** 2)))
# 10 Hz 幅值：25-30 s 窗 FFT
w = (tt >= 25.0) & (tt < 30.0)
x = e[w] - e[w].mean()
X = np.fft.rfft(x * np.hanning(len(x)))
fr = np.fft.rfftfreq(len(x), d=float(tt[1] - tt[0]))
k10 = np.argmin(np.abs(fr - 10.0))
amp10 = float(2.0 * np.abs(X[k10]) / np.sum(np.hanning(len(x))))
d = dict(tag=tag, T_dft=Tdft, es_dead=DEAD, a_ref=AREF, rms=rms, amp10=amp10, iq=float(np.max(np.abs(iq))),
         es_end=float(es[-1]), es_mean=float(es[tt >= 25].mean()), es_std=float(es[tt >= 25].std()),
         A_end=float(amp[tt >= 25].mean()), runtime_s=el)
json.dump(d, open("_tdft_%s.json" % tag, "w"), indent=1)
print("%-10s T_dft=%.0f  RMS %5.2f rpm  10Hz %5.2f rpm  iq %5.2f  es %.4f±%.4f  A %.4f  (%.0fs)" % (
    tag, Tdft, rms, amp10, d["iq"], d["es_mean"], d["es_std"], d["A_end"], el), flush=True)
