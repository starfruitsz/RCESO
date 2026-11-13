# -*- coding: utf-8 -*-
"""run_j_recheck.py —— 周期 dither 复检（J 在 15 s 阶跃 5.26→2.545 J_nom）"""
import numpy as np, json, sys
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
mode=sys.argv[1] if len(sys.argv)>1 else "rec"
TEND=30.0
t=np.arange(0.0,TEND,2e-6); TL=np.zeros_like(t)
base=dict(n_ref=600.0,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,Q0=0.98,tau0=20e-3,seed_i=20261018,
 i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
 eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,a_ref=1.0,
 J_true=9.95e-5,j_step_t=15.0,j_step_val=4.81e-5,
 tl_fault={"start":0.0,"unbalance":dict(M=0.1,e=1e-4,kappa=580.0)})
if mode=="rec":
    base.update(j_recheck=True,j_recheck_period=5.0,j_recheck_len=0.6,j_recheck_amp=0.157,
                j_recheck_nmin=2,j_recheck_t0=1.0)
elif mode=="comm":
    base.update(j_id=True,j_id_f=100.0,j_id_amp_u=0.157,j_id_win=0.2,j_id_lp=0.4,j_id_tend=2.0,j_adapt_b0=True)
elif mode=="fixed":
    pass
else:
    raise SystemExit("mode")
Y=sim_inv(t,TL,base)
tt=np.asarray(Y["t"]); y=np.asarray(Y["y"]); iq=np.asarray(Y["iq"]); jh=np.asarray(Y["jhat"]); tj=np.asarray(Y["t_j"])
e=(y-1.0)*600.0
def win(a,b):
    m=(tt>=a)&(tt<b); ec=e[m]; ts=tt[m]
    a10=float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*ts)),2*np.mean(ec*np.sin(2*np.pi*10*ts))))
    return a10,float(np.sqrt(np.mean(ec**2)))
a1,r1=win(10,14); a2,r2=win(25,30)
print(mode,"a10 10-14",a1,"a10 25-30",a2,"rms2",r2,"iq",float(np.max(np.abs(iq))),
      "jhat min/max/final",float(jh.min()),float(jh.max()),float(jh[-1]),flush=True)
np.savez("_wave_j_%s_long.npz"%mode,t=tt[::100],y=y[::100],iq=iq[::100],jhat=jh,t_j=tj)
json.dump(dict(mode=mode,a10_pre=a1,a10_post=a2,rms_post=r2,iq=float(np.max(np.abs(iq))),
               jmin=float(jh.min()),jmax=float(jh.max()),jfin=float(jh[-1])),
          open("_j_%s_long.json"%mode,"w"),indent=1)
print("saved",mode)
