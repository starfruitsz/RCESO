# -*- coding: utf-8 -*-
"""_verify_fault3.py —— 圆盘+角不对中+平行不对中 三合一故障的验证：1×/2× 幅值。"""
import numpy as np, json, time
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
from fault_torque import unbalance_torque, misalign_torque, parallel_torque

TEND = 8.0; DT = 2e-6
U = dict(M=0.1, e=1e-4, kappa=580.0)
M = dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0)
P = dict(e=1e-4, dk=1.0e5, kappa=100.0)
FAULT = dict(start=2.0, unbalance=U, misalign=M, parallel=P)

# 解析波形（600 rpm）
w = 600 * 2 * np.pi / 60
tt = np.arange(5.0, 6.0, 1e-5)
ph = (w * tt) % (2 * np.pi)
Tf = np.array([unbalance_torque(a, w, **U) + misalign_torque(a, w, **M) + parallel_torque(a, w, **P) for a in ph])
X = np.fft.rfft(Tf); fr = np.fft.rfftfreq(len(Tf), d=1e-5)
k1 = np.argmin(np.abs(fr - 10.0)); k2 = np.argmin(np.abs(fr - 20.0))
print("解析: 10Hz %.4f, 20Hz %.4f N·m" % (2*np.abs(X[k1])/len(Tf), 2*np.abs(X[k2])/len(Tf)))

t = np.arange(0.0, TEND, DT)
TL = 0.5 * 0.637 * np.ones_like(t)
cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3,
           fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"], eso_law="fal", eso_a=0.75,
           eso_delta=0.10, eso_lam=10.0, rc_bp=5.0, b3_min=4000.0, b3_max=4000.0,
           a_ref=1.0, tl_fault=FAULT)
Y = sim_inv(t, TL, cfg)
np.savez("_c4_fault3.npz", t=Y["t"], y=Y["y"], iq=Y["iq"], tl=Y["tl"])
tt2 = np.asarray(Y["t"]); tl2 = np.asarray(Y["tl"])
m = (tt2 >= 5.0) & (tt2 < 6.0)
x = tl2[m] - tl2[m].mean()
X2 = np.fft.rfft(x); fr2 = np.fft.rfftfreq(len(x), d=float(tt2[1]-tt2[0]))
k1 = np.argmin(np.abs(fr2 - 10.0)); k2 = np.argmin(np.abs(fr2 - 20.0))
print("仿真: 10Hz %.4f, 20Hz %.4f N·m" % (2*np.abs(X2[k1])/len(x), 2*np.abs(X2[k2])/len(x)))
