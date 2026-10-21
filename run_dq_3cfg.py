# -*- coding: utf-8 -*-
"""dq 模型（含 id、交叉耦合、双 PI、电压限幅）下的四配置实验"""
import math, os, json
import numpy as np
from pmsm_dq_sim import sim_dq, band_noise, I_BASE, N_REF
import noise_cfg as NC          # 三路噪声的单一入口（可调）
from fb_cfg import FB_NEW       # 律 F-B 官方配置（2026-10-19 定稿）
os.chdir(os.path.dirname(os.path.abspath(__file__)))

T, DT, TEND, TL0, TW = 0.1, 1e-5, 12.0, 2.0, 6.0
N = N_REF; T_RATED = 0.637
t = np.arange(0.0, TEND, DT); n = len(t)
rng_tau = np.maximum(t - TL0, 0.0); ph = 2*math.pi*rng_tau/T; A = 0.30
on_step = (t >= TL0).astype(float); on_per = ((t >= TL0) & (t < TW)).astype(float)
TL = (0.50*on_step + A*on_per*(np.sin(ph) + 0.4*np.sin(3*ph) + 0.2*np.sin(5*ph)))*T_RATED
TL = TL + NC.load_noise(n, DT)          # 负载噪声：见 noise_cfg.NOISE["sig_T_pct"]
NK = NC.sim_kwargs()                     # 电流/转速噪声：见 noise_cfg.NOISE
CFG = [("Base", dict(det_eps=0.0)),
       ("LawD", dict(kp_boost=4.0, det_eps=0.01)),
       ("FB",   dict(FB_NEW)),
       ("D+FB", dict(FB_NEW, kp_boost=4.0))]
W = [(0.5,2.0),(2.0,2.5),(2.5,2.6),(3.0,3.5),(3.5,4.0),(4.0,6.0),(7.0,12.0)]
res = {}
for name, kw in CFG:
    Y = sim_dq(t, TL, dict(kw, **NK))
    np.savez("_dq_%s.npz" % name, t=t, y=Y["y"], id=Y["id"], iq=Y["iq"], TL=TL,
             vd=Y["vd"], vq=Y["vq"], v=Y["v"])
    e = (Y["y"]-1.0)*N
    rms = [float(np.sqrt(np.mean(e[(t>=a)&(t<b)]**2))) for a,b in W]
    seg = (t>=1.9)&(t<=2.4); dip = float(np.min(e[seg]))
    m1 = (t>=TW)&(t<TW+T); rms1 = float(np.sqrt(np.mean(e[m1]**2)))
    def amp(a0,b0):
        m=(t>=a0)&(t<b0); tt=t[m]; ee=e[m]
        return float(math.hypot(2*np.mean(ee*np.cos(2*math.pi*tt/T)), 2*np.mean(ee*np.sin(2*math.pi*tt/T))))
    res[name] = dict(w7=[round(v,2) for v in rms], dip=round(dip,1), rms1=round(rms1,1),
                     a_echo=round(amp(TW,TW+T),1), steady=round(float(np.sqrt(np.mean(e[(t>=8)&(t<10)]**2))),2),
                     id_rms=round(float(np.sqrt(np.mean(Y["id"]**2))),2),
                     iq_max=round(float(np.max(np.abs(Y["iq"]))),2),
                     v_max=round(float(np.max(np.hypot(Y["vd"],Y["vq"]))),1))
    print("DQ %-5s dip=%.1f echoRMS=%.1f 10Hz=%.1f steady=%.2f id_rms=%.2f iqmax=%.2f vmax=%.1f" %
          (name, dip, rms1, res[name]["a_echo"], res[name]["steady"], res[name]["id_rms"],
           res[name]["iq_max"], res[name]["v_max"]), flush=True)
json.dump(res, open("_dq_metrics.json","w"), ensure_ascii=False, indent=1)
print("DONE")
