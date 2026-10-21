# -*- coding: utf-8 -*-
"""抓取 F-B 档的 e1 与触发标志，用于画双尺度包络原理图"""
import math, os
import numpy as np
from adrc_eso_closed import adrc_sim
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
KT, J_M, T_RATED = 0.101, 1.89e-5, 0.637
N = 600.0; W_REF = N*math.pi/30.0; I_BASE = T_RATED/KT
B = KT*I_BASE/(J_M*W_REF); B0 = 1.2*B
T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
KP, WO, FCI, B3, T0 = 75.36, 500.0, 1000.0, 2000.0, 5e-3
t = np.arange(0.0, TEND, DT); n = len(t)
def bn(sig, fc, sd):
    rng = np.random.default_rng(sd); x = rng.standard_normal(n)
    a = 1.0 - math.exp(-2.0*math.pi*fc*DT); nk = max(1, int(math.ceil(6.0/(2.0*math.pi*fc*DT))))
    y = np.convolve(x, a*np.power(1.0-a, np.arange(nk)))[:n]; return y/y.std()*sig
NI = bn(0.01, 2000.0, 20261016); NT = bn(0.05, 200.0, 20261017)
tau = np.maximum(t - TL0, 0.0); ph = 2*math.pi*tau/T; A = 0.30
on_step = (t >= TL0).astype(float); on_per = ((t >= TL0) & (t < TW)).astype(float)
TL = 0.50*on_step + A*on_per*(np.sin(ph) + 0.4*np.sin(3*ph) + 0.2*np.sin(5*ph))
d = -B*TL; r = np.full_like(t, 1.0); DN = -B*NT
Y = adrc_sim(t, r, d, B, B0, WO, KP, T, 0.2, B3, T0, 0.1, 0.98, 1.0, 1e5, 5.0, 0.0,
             adapt=0, warm=2.0, taumax=5.0, taumin=0.2, law="decupled", qmax=1.8,
             qmodel_max=1.0, drive_mode="bpw", theta_sign=1.0, bpw_fa=5.0, bpw_sa=50.0,
             bpw_fb=1.0, bpw_sb=10.0, qd_mode=2, qmin=0.2, norm_floor=6.5,
             eo_def="meansq", theta_drive="bnorm", q_drive="bnorm", q_rest_tau="none",
             e1src="estimation", c1=0.1, c2=0.1, b_filt=1.0, b0_tau=1.0,
             cur_tau=1.0/(2*math.pi*FCI), cur_noise=NI, d_noise=DN,
             ff_flush=1.8, ff_tau_f=4e-3, ff_tau_s=0.5, ff_cool=0.3)
e1 = np.asarray(Y["e1"]); fl = np.asarray(Y.get("_fl", np.zeros(n)))
np.savez("_fb_e1.npz", t=t, e1=e1, fl=fl)
print("saved; flush samples:", int(np.sum(fl > 0)), "first at", float(t[np.argmax(fl > 0)]) if np.any(fl > 0) else None)
print("DONE")
