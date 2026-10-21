# -*- coding: utf-8 -*-
"""扫 F-B 阈值 k：能不能避开"碰线"（临界触发）"""
import math, os, json
import numpy as np
from pmsm_dq_sim import sim_dq, N_REF
import noise_cfg as NC
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
t = np.arange(0.0, TEND, DT); n = len(t)
tau_=np.maximum(t-TL0,0.0); ph=2*math.pi*tau_/T; A=0.30
on=(t>=TL0).astype(float); onp=((t>=TL0)&(t<TW)).astype(float)
TL=(0.50*on + A*onp*(np.sin(ph)+0.4*np.sin(3*ph)+0.2*np.sin(5*ph)))*0.637
TL=TL+NC.load_noise(n, DT)
KS=[1.4,1.6,1.8,2.0,2.4]
SEEDS=[20261018, 20261021]
out={}
for sd in SEEDS:
    for k in KS:
        Y=sim_dq(t, TL, dict(ff_flush=k, ff_tau_f=4e-3, ff_tau_s=0.5, ff_cool=0.3,
                             det_eps=0.01, **dict(NC.sim_kwargs(), seed_w=sd)))
        e=(Y["y"]-1.0)*N_REF
        m=(t>=TW)&(t<TW+T); ee=e[m]; tt=t[m]
        a=math.hypot(2*np.mean(ee*np.cos(2*math.pi*tt/T)),2*np.mean(ee*np.sin(2*math.pi*tt/T)))
        fl=Y["fl"]
        rec=dict(a_echo=round(float(a),1), dip=round(float(np.min(e[(t>=1.9)&(t<=2.4)])),1),
                 t36=int(fl[(t>=3)&(t<6)].sum()), t67=int(fl[(t>=6)&(t<7)].sum()), t712=int(fl[(t>=7)&(t<12)].sum()))
        out["%d_k%.1f" % (sd, k)]=rec
        print("seed=%d k=%.1f  10Hz=%5.1f dip=%7.1f  trig 3-6=%2d 6-7=%d 7-12=%2d" %
              (sd, k, a, rec["dip"], rec["t36"], rec["t67"], rec["t712"]), flush=True)
json.dump(out, open("_k_sweep.json","w"), ensure_ascii=False, indent=1)
print("DONE")
