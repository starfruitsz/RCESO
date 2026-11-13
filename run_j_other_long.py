# -*- coding: utf-8 -*-
"""run_j_other_long.py —— 30 s 长时：DFT 调试期 / 简化 DO"""
import numpy as np, json, sys
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
mode=sys.argv[1]
TEND=30.0
t=np.arange(0.0,TEND,2e-6); TL=np.zeros_like(t)
base=dict(n_ref=600.0,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,Q0=0.98,tau0=20e-3,seed_i=20261018,
 i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
 eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,a_ref=1.0,J_true=9.95e-5,
 tl_fault={"start":0.0,"unbalance":dict(M=0.1,e=1e-4,kappa=580.0)})
if mode=="dft":
    base.update(j_id=True,j_id_f=100.0,j_id_amp_u=0.157,j_id_win=0.2,j_id_lp=0.4,j_id_tend=2.0,j_adapt_b0=True)
elif mode=="do":
    base.update(j_do=True,j_do_gamma=1e-3,j_do_lpf=0.05,j_do_tau=0.5)
else:
    raise SystemExit("mode")
Y=sim_inv(t,TL,base)
tt=np.asarray(Y["t"]); y=np.asarray(Y["y"]); iq=np.asarray(Y["iq"]); jh=np.asarray(Y["jhat"]); tj=np.asarray(Y["t_j"])
e=(y-1.0)*600.0
# last 5 s
m=(tt>=TEND-5)&(tt<TEND); ec=e[m]; tsec=tt[m]
a10f=float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*tsec)),2*np.mean(ec*np.sin(2*np.pi*10*tsec))))
rmsf=float(np.sqrt(np.mean(ec**2)))
print(mode,"TEND",TEND,"a10_last5",a10f,"rms",rmsf,"iq",float(np.max(np.abs(iq))),
      "jhat min/max/final",float(jh.min()),float(jh.max()),float(jh[-1]),flush=True)
np.savez("_wave_j_%s_long.npz"%mode, t=tt[::100], y=y[::100], iq=iq[::100], jhat=jh, t_j=tj)
json.dump(dict(mode=mode,TEND=TEND,a10f=a10f,rmsf=rmsf,iq=float(np.max(np.abs(iq))),
               jmin=float(jh.min()),jmax=float(jh.max()),jfin=float(jh[-1])),
          open("_j_%s_long.json"%mode,"w"),indent=1)
print("saved",mode)
