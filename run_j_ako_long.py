# -*- coding: utf-8 -*-
"""run_j_ako_long.py —— AKO+RLS 长时运行（看收敛/极限环）"""
import numpy as np, json
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
TEND=30.0
t=np.arange(0.0,TEND,2e-6); TL=np.zeros_like(t)
cfg=dict(n_ref=600.0,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,Q0=0.98,tau0=20e-3,seed_i=20261018,
 i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
 eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,a_ref=1.0,J_true=9.95e-5,
 tl_fault={"start":0.0,"unbalance":dict(M=0.1,e=1e-4,kappa=580.0)},
 j_ako=True,j_ako_lam=0.99,j_ako_R=1e-3,j_ako_rho=0.1)
Y=sim_inv(t,TL,cfg)
tt=np.asarray(Y["t"]); y=np.asarray(Y["y"]); iq=np.asarray(Y["iq"]); jh=np.asarray(Y["jhat"]); tj=np.asarray(Y["t_j"])
e=(y-1.0)*600.0
# 1 s sliding 10 Hz amplitude and rms
a10=[]; rms=[]; tc=[]
for s in range(0,int(TEND)-1):
    m=(tt>=s)&(tt<s+1.0)
    if m.sum()<1000: continue
    ec=e[m]; tsec=tt[m]
    a10.append(float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*tsec)),2*np.mean(ec*np.sin(2*np.pi*10*tsec)))))
    rms.append(float(np.sqrt(np.mean(ec**2)))); tc.append(s+0.5)
# last 5 s metrics
m=(tt>=TEND-5)&(tt<TEND); ec=e[m]; tsec=tt[m]
a10f=float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*tsec)),2*np.mean(ec*np.sin(2*np.pi*10*tsec))))
print("TEND",TEND,"jhat min/max/final",float(jh.min()),float(jh.max()),float(jh[-1]),
      "a10_last5",a10f,"iq",float(np.max(np.abs(iq))),flush=True)
np.savez("_wave_j_ako_long.npz", t=tt[::100], y=y[::100], iq=iq[::100], jhat=jh, t_j=tj,
         a10=np.array(a10), rms=np.array(rms), tc=np.array(tc))
json.dump(dict(TEND=TEND,jmin=float(jh.min()),jmax=float(jh.max()),jfin=float(jh[-1]),a10f=a10f,
               iq=float(np.max(np.abs(iq)))),open("_j_ako_long.json","w"),indent=1)
print("saved")
