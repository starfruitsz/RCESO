# -*- coding: utf-8 -*-
"""在重复通道泵浦口加软死区：挡住 10 rpm 传感器噪声被 beta3 放大"""
import math, os
import numpy as np
from pmsm_dq_sim import sim_dq, band_noise, N_REF
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
t = np.arange(0.0, TEND, DT); n = len(t)
tau_ = np.maximum(t-TL0, 0.0); ph = 2*math.pi*tau_/T; A=0.30
on=(t>=TL0).astype(float); onp=((t>=TL0)&(t<TW)).astype(float)
base_TL=(0.50*on + A*onp*(np.sin(ph)+0.4*np.sin(3*ph)+0.2*np.sin(5*ph)))*0.637
TL = base_TL + band_noise(n, 0.05*0.637, 200.0, DT, 20261017)
for c_rpm in [0.0, 5.0, 10.0, 15.0, 20.0]:
    Y = sim_dq(t, TL, dict(det_eps=0.01, kp_boost=4.0, sig_n=10.0, sig_i=0.5, rc_phi=c_rpm/N_REF))
    e = (Y["y"]-1.0)*N_REF
    rms = float(np.sqrt(np.mean(e[(t>=8)&(t<10)]**2)))
    dip = float(np.min(e[(t>=1.9)&(t<=2.4)]))
    m=(t>=TW)&(t<TW+T); ee=e[m]; tt=t[m]
    a10 = math.hypot(2*np.mean(ee*np.cos(2*math.pi*tt/T)),2*np.mean(ee*np.sin(2*math.pi*tt/T)))
    print("rc_phi=%4.1f rpm  steady=%6.2f rpm (%.2f%%)  dip=%7.1f  10Hz=%.1f" % (c_rpm, rms, 100*rms/600, dip, a10), flush=True)
print("DONE")
