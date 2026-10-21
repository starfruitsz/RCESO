# -*- coding: utf-8 -*-
"""F-B 检测器前置软死区 phi(x,c) 的扫描：c = 0/20/40 rpm，看能否压噪声、少误触"""
import math, os, json
import numpy as np
from pmsm_dq_sim import sim_dq, band_noise, I_BASE, N_REF
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
N = N_REF; T_RATED = 0.637
t = np.arange(0.0, TEND, DT); n = len(t)
tau_ = np.maximum(t - TL0, 0.0); ph = 2*math.pi*tau_/T; A = 0.30
on_step = (t >= TL0).astype(float); on_per = ((t >= TL0) & (t < TW)).astype(float)
TL = (0.50*on_step + A*on_per*(np.sin(ph) + 0.4*np.sin(3*ph) + 0.2*np.sin(5*ph)))*T_RATED
TL = TL + band_noise(n, 0.05*T_RATED, 200.0, DT, 20261017)
FB = dict(ff_flush=1.8, ff_tau_f=4e-3, ff_tau_s=0.5, ff_cool=0.3, det_eps=0.01)
CASES = [("Base", dict(det_eps=0.0))]
for c_rpm in [0, 20, 40]:
    CASES.append(("FB_c%d" % c_rpm, dict(FB, ff_phi=c_rpm/N)))
    if c_rpm > 0:
        CASES.append(("DFB_c%d" % c_rpm, dict(FB, kp_boost=4.0, ff_phi=c_rpm/N)))
W = [(2.0,2.5),(2.5,2.6),(3.0,3.5),(3.5,4.0),(4.0,6.0),(7.0,12.0)]
out = {}
for name, kw in CASES:
    Y = sim_dq(t, TL, kw)
    e = (Y["y"]-1.0)*N
    dip = float(np.min(e[(t>=1.9)&(t<=2.4)]))
    m1 = (t>=TW)&(t<TW+T)
    ee = e[m1]; tt = t[m1]
    a_echo = math.hypot(2*np.mean(ee*np.cos(2*math.pi*tt/T)), 2*np.mean(ee*np.sin(2*math.pi*tt/T)))
    fl = Y["fl"]
    n_trig_pre = int(fl[(t>=3)&(t<6)].sum())
    n_trig_echo = int(fl[(t>=6)&(t<7)].sum())
    n_trig_post = int(fl[(t>=7)&(t<12)].sum())
    rms = float(np.sqrt(np.mean(e[(t>=7)&(t<12)]**2)))
    out[name] = dict(dip=round(dip,1), a_echo=round(float(a_echo),1), steady=round(rms,2),
                     trig_pre=n_trig_pre, trig_echo=n_trig_echo, trig_post=n_trig_post)
    print("%-9s dip=%7.1f 10Hz_echo=%6.1f steady=%.2f  trigs 3-6s=%3d 6-7s=%2d 7-12s=%3d" %
          (name, dip, a_echo, rms, n_trig_pre, n_trig_echo, n_trig_post), flush=True)
json.dump(out, open("_phi_sweep.json","w"), ensure_ascii=False, indent=1)
print("DONE")
