# -*- coding: utf-8 -*-
"""目标：稳态误差 3-6 rpm。扫电流反馈滤波截止频率与电流环带宽"""
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
CASES = [("no filter", dict(det_eps=0.01, kp_boost=4.0, sig_n=10.0)),
         ("LPF 1 kHz", dict(det_eps=0.01, kp_boost=4.0, sig_n=10.0, f_ci_fb=1000.0)),
         ("LPF 500 Hz", dict(det_eps=0.01, kp_boost=4.0, sig_n=10.0, f_ci_fb=500.0)),
         ("LPF 200 Hz", dict(det_eps=0.01, kp_boost=4.0, sig_n=10.0, f_ci_fb=200.0)),
         ("LPF 100 Hz", dict(det_eps=0.01, kp_boost=4.0, sig_n=10.0, f_ci_fb=100.0))]
for name, kw in CASES:
    Y = sim_dq(t, TL, kw)
    e = (Y["y"]-1.0)*N_REF
    rms = float(np.sqrt(np.mean(e[(t>=8)&(t<10)]**2)))
    dip = float(np.min(e[(t>=1.9)&(t<=2.4)]))
    m=(t>=TW)&(t<TW+T); ee=e[m]; tt=t[m]
    a10 = math.hypot(2*np.mean(ee*np.cos(2*math.pi*tt/T)),2*np.mean(ee*np.sin(2*math.pi*tt/T)))
    print("%-12s steady=%5.2f rpm (%.2f%%)  dip=%7.1f  10Hz_echo=%5.1f" %
          (name, rms, 100*rms/600, dip, a10), flush=True)
print("DONE")
