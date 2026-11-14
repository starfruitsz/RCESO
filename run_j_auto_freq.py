# -*- coding: utf-8 -*-
"""run_j_auto_freq.py —— 转速自适应 dither 频率表（门控关闭，先验证频率）"""
import numpy as np, json, sys
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
nref=float(sys.argv[1]) if len(sys.argv)>1 else 600.0
TEND=10.0
t=np.arange(0.0,TEND,2e-6); TL=np.zeros_like(t)
cfg=dict(n_ref=nref,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,Q0=0.98,tau0=20e-3,seed_i=20261018,
 i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
 eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,a_ref=1.0,J_true=9.95e-5,
 tl_fault={"start":0.0,"unbalance":dict(M=0.1,e=1e-4,kappa=580.0)},
 j_recheck=True,j_recheck_period=5.0,j_recheck_len=0.6,j_recheck_amp=0.157,j_recheck_nmin=2,j_recheck_t0=1.0,
 j_recheck_f_auto=True,j_recheck_gate=False)
Y=sim_inv(t,TL,cfg)
tt=np.asarray(Y["t"]); y=np.asarray(Y["y"]); jh=np.asarray(Y["jhat"]); fd=np.asarray(Y["fd"])
e=(y-1.0)*600.0
print("nref",nref,"fd",fd.tolist(),"jfin %.3e"%float(jh[-1]),"iq %.2f"%float(np.max(np.abs(Y["iq"]))))
np.savez("_wave_j_auto_%d.npz"%int(nref),t=tt[::100],y=y[::100],iq=np.asarray(Y["iq"])[::100],jhat=jh,t_j=np.asarray(Y["t_j"]),fd=fd)
json.dump(dict(nref=nref,fd=fd.tolist(),jfin=float(jh[-1]),iq=float(np.max(np.abs(Y["iq"])))),open("_j_auto_%d.json"%int(nref),"w"),indent=1)
print("saved")
