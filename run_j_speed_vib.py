# -*- coding: utf-8 -*-
"""run_j_speed_vib.py —— 500 rpm 窗口正交性 + 非倍频振动泄漏试跑"""
import numpy as np, json, sys
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
mode=sys.argv[1]
TEND=10.0
nref=500.0 if (mode.startswith("speed") or mode.endswith("500")) else 600.0
win=0.12 if mode.endswith("012") else 0.2
t=np.arange(0.0,TEND,2e-6); TL=np.zeros_like(t)
if mode=="vib":
    TL = 0.02*np.sin(2*np.pi*97.3*t)
if mode.startswith("vib100"):
    TL = 0.02*np.sin(2*np.pi*100.0*t)
cfg=dict(n_ref=nref,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,Q0=0.98,tau0=20e-3,seed_i=20261018,
 i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
 eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,a_ref=1.0,J_true=9.95e-5,
 tl_fault={"start":0.0,"unbalance":dict(M=0.1,e=1e-4,kappa=580.0)},
 j_recheck=True,j_recheck_period=5.0,j_recheck_len=0.6,j_recheck_amp=0.157,j_recheck_nmin=2,j_recheck_t0=1.0,
 j_recheck_win=win)
Y=sim_inv(t,TL,cfg)
tt=np.asarray(Y["t"]); y=np.asarray(Y["y"]); iq=np.asarray(Y["iq"]); jh=np.asarray(Y["jhat"]); tj=np.asarray(Y["t_j"])
e=(y-1.0)*600.0
ff=nref/60.0
def amp(f,a,b):
    m=(tt>=a)&(tt<b); ec=e[m]; ts=tt[m]
    return float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*f*ts)),2*np.mean(ec*np.sin(2*np.pi*f*ts))))
print(mode,"nref",nref,"win",win,"ff",round(ff,3),"a_fault",round(amp(ff,8,9),2),"a100",round(amp(100,6.0,6.2),2),
      "jfin %.3e"%float(jh[-1]),"jmin %.3e"%float(jh.min()),"jmax %.3e"%float(jh.max()),flush=True)
np.savez("_wave_j_%s.npz"%mode,t=tt[::100],y=y[::100],iq=iq[::100],jhat=jh,t_j=tj,
         nref=nref,win=win,ff=ff)
json.dump(dict(mode=mode,nref=nref,win=win,ff=ff,a_fault=amp(ff,8,9),a100=amp(100,6.0,6.2),
               jfin=float(jh[-1]),jmin=float(jh.min()),jmax=float(jh.max())),open("_j_%s.json"%mode,"w"),indent=1)
print("saved",mode)
