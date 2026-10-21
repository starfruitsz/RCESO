# -*- coding: utf-8 -*-
"""识别 19 rpm 地板：负载噪声 vs 电流噪声 vs 转速噪声"""
import math, os
import numpy as np
from pmsm_dq_sim import sim_dq, band_noise, N_REF
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
t = np.arange(0.0, TEND, DT); n = len(t)
tau_ = np.maximum(t-TL0, 0.0); ph = 2*math.pi*tau_/T; A=0.30
on_step=(t>=TL0).astype(float); on_per=((t>=TL0)&(t<TW)).astype(float)
base_TL=(0.50*on_step + A*on_per*(np.sin(ph)+0.4*np.sin(3*ph)+0.2*np.sin(5*ph)))*0.637
for frac in [0.05, 0.02, 0.01, 0.0]:
    TL = base_TL + band_noise(n, frac*0.637, 200.0, DT, 20261017)
    Y = sim_dq(t, TL, dict(det_eps=0.01, kp_boost=4.0, sig_n=10.0, sig_i=0.5))
    e = (Y["y"]-1.0)*N_REF
    rms = float(np.sqrt(np.mean(e[(t>=8)&(t<10)]**2)))
    print("load noise=%4.1f%%  steady=%6.2f rpm (%.2f%%)  dip=%7.1f" % (100*frac, rms, 100*rms/600,
          float(np.min(e[(t>=1.9)&(t<=2.4)]))), flush=True)
print("DONE")
