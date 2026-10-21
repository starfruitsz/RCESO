# -*- coding: utf-8 -*-
"""归因：转速噪声对真实稳态误差的贡献"""
import math, os
import numpy as np
from pmsm_dq_sim import sim_dq, band_noise, N_REF
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
t = np.arange(0.0, TEND, DT); n = len(t)
tau_ = np.maximum(t-TL0, 0.0); ph = 2*math.pi*tau_/T; A=0.30
on=(t>=TL0).astype(float); onp=((t>=TL0)&(t<TW)).astype(float)
base_TL=(0.50*on + A*onp*(np.sin(ph)+0.4*np.sin(3*ph)+0.2*np.sin(5*ph)))*0.637
for sn, si, ld in [(0.0,0.1,0.01),(3.0,0.1,0.01),(10.0,0.1,0.01),(10.0,0.05,0.005)]:
    TL = base_TL + band_noise(n, ld*0.637, 200.0, DT, 20261017)
    Y = sim_dq(t, TL, dict(det_eps=0.01, kp_boost=4.0, sig_n=sn, sig_i=si))
    e = (Y["y"]-1.0)*N_REF
    rms = float(np.sqrt(np.mean(e[(t>=8)&(t<10)]**2)))
    print("sig_n=%4.1f sig_i=%.2f load=%.1f%%  steady=%6.2f rpm (%.2f%%)" % (sn, si, 100*ld, rms, 100*rms/600), flush=True)
print("DONE")
