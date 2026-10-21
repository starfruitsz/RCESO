# -*- coding: utf-8 -*-
"""要 3-6 rpm 的真实误差，电流噪声需要多小？"""
import math, os
import numpy as np
from pmsm_dq_sim import sim_dq, band_noise, N_REF
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
t = np.arange(0.0, TEND, DT); n = len(t)
tau_ = np.maximum(t-TL0, 0.0); ph = 2*math.pi*tau_/T; A=0.30
on_step=(t>=TL0).astype(float); on_per=((t>=TL0)&(t<TW)).astype(float)
TL=(0.50*on_step + A*on_per*(np.sin(ph)+0.4*np.sin(3*ph)+0.2*np.sin(5*ph)))*0.637
TL=TL+band_noise(n,0.05*0.637,200.0,DT,20261017)
for sig in [0.5, 0.2, 0.1, 0.05]:
    Y = sim_dq(t, TL, dict(det_eps=0.01, kp_boost=4.0, sig_n=10.0, sig_i=sig))
    e = (Y["y"]-1.0)*N_REF
    rms = float(np.sqrt(np.mean(e[(t>=8)&(t<10)]**2)))
    dip = float(np.min(e[(t>=1.9)&(t<=2.4)]))
    print("sig_i=%.2f A  steady=%6.2f rpm (%.2f%%)  dip=%7.1f" % (sig, rms, 100*rms/600, dip), flush=True)
print("DONE")
