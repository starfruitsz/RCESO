# -*- coding: utf-8 -*-
"""10 rpm 转速噪声下的事件重复性：3 个噪声种子 × {无自适应, F-B}"""
import math, os, json
import numpy as np
from pmsm_dq_sim import sim_dq, band_noise, N_REF
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
t = np.arange(0.0, TEND, DT); n = len(t)
tau_ = np.maximum(t-TL0, 0.0); ph = 2*math.pi*tau_/T; A=0.30
on_step=(t>=TL0).astype(float); on_per=((t>=TL0)&(t<TW)).astype(float)
TL=(0.50*on_step + A*on_per*(np.sin(ph)+0.4*np.sin(3*ph)+0.2*np.sin(5*ph)))*0.637
TL=TL+band_noise(n,0.05*0.637,200.0,DT,20261017)
seeds = [20261018, 20261019, 20261021]
res = {"Base": [], "FB": []}
for sd in seeds:
    for name, kw in [("Base", dict(det_eps=0.0)),
                     ("FB", dict(ff_flush=1.8, ff_tau_f=4e-3, ff_tau_s=0.5, ff_cool=0.3,
                                 det_eps=0.01))]:
        Y = sim_dq(t, TL, dict(kw, sig_n=10.0, seed_w=sd))
        e = (Y["y"]-1.0)*N_REF
        m=(t>=TW)&(t<TW+T); ee=e[m]; tt=t[m]
        a=math.hypot(2*np.mean(ee*np.cos(2*math.pi*tt/T)),2*np.mean(ee*np.sin(2*math.pi*tt/T)))
        fl=Y["fl"]
        res[name].append(dict(seed=sd, a_echo=round(float(a),1),
                              dip=round(float(np.min(e[(t>=1.9)&(t<=2.4)])),1),
                              trig_echo=int(fl[(t>=6)&(t<7)].sum()),
                              trig_post=int(fl[(t>=7)&(t<12)].sum())))
        print("%-4s seed=%d 10Hz=%.1f dip=%.1f trig6-7=%d trig7-12=%d" %
              (name, sd, a, np.min(e[(t>=1.9)&(t<=2.4)]), fl[(t>=6)&(t<7)].sum(), fl[(t>=7)&(t<12)].sum()), flush=True)
json.dump(res, open("_repeat10.json","w"), ensure_ascii=False, indent=1)
print("DONE")
