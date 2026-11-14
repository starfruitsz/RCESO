# -*- coding: utf-8 -*-
"""_test_qcap.py —— 调 q 与 f_max 的扫描"""
import numpy as np, json, sys
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
nref=float(sys.argv[1]); q=float(sys.argv[2]); fmax=float(sys.argv[3]); TEND=float(sys.argv[4]) if len(sys.argv)>4 else 20.0
fmin=float(sys.argv[5]) if len(sys.argv)>5 else 80.0
t=np.arange(0.0,TEND,2e-6); TL=np.zeros_like(t)
cfg=dict(n_ref=nref,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,Q0=0.98,tau0=20e-3,seed_i=20261018,
 i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
 eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,a_ref=1.0,J_true=9.95e-5,
 tl_fault={"start":0.0,"unbalance":dict(M=0.1,e=1e-4,kappa=580.0)},
 j_recheck=True,j_recheck_period=2.0,j_recheck_len=0.6,j_recheck_amp=0.157,j_recheck_nmin=2,j_recheck_t0=1.0,
 j_recheck_f_auto=True,j_recheck_f_q=q,j_recheck_f_alpha=0.35,j_recheck_f_min=fmin,j_recheck_f_max=fmax,j_recheck_amp_auto=True,
 j_recheck_gate=True,j_recheck_gate_ac=10.0,j_recheck_gate_step=10.0,
 j_recheck_apply=True,j_recheck_alpha=0.8)
Y=sim_inv(t,TL,cfg)
jh=np.asarray(Y["jhat"]); b0=np.asarray(Y["b0e"]); fd=np.asarray(Y["fd"])
fdl=float(fd[0,1]) if fd.size else float("nan")
print("n",nref,"q",q,"fmax",fmax,"fmin",fmin,"T",TEND,"fd",fdl,"jfin %.3e"%float(jh[-1]),
      "b0e %.1f"%float(b0[-1]),"iq %.2f"%float(np.max(np.abs(Y["iq"]))),flush=True)
tag="q%.1f_fmax%.0f_fmin%.0f"%(q,fmax,fmin)
np.savez("_wave_j_%d_%s.npz"%(int(nref),tag),t=Y["t"][::100],y=Y["y"][::100],iq=Y["iq"][::100],
         jhat=jh,t_j=np.asarray(Y["t_j"]),b0e=b0)
json.dump(dict(nref=nref,q=q,fmax=fmax,TEND=TEND,fd=fdl,jfin=float(jh[-1]),b0e=float(b0[-1]),
               iq=float(np.max(np.abs(Y["iq"])))),open("_j_%d_%s.json"%(int(nref),tag),"w"),indent=1)
