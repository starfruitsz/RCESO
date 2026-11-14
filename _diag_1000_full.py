# -*- coding: utf-8 -*-
"""_diag_1000.py —— 1000 rpm 偏差诊断：冻结 b0 / 慢更新 / 无故障"""
import numpy as np, json, sys
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
mode=sys.argv[1]
TEND=30.0 if mode in ("slow","base") else 20.0
t=np.arange(0.0,TEND,2e-6); TL=np.zeros_like(t)
cfg=dict(n_ref=1000.0,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,Q0=0.98,tau0=20e-3,seed_i=20261018,
 i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
 eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,a_ref=1.0,J_true=9.95e-5,
 tl_fault={"start":0.0,"unbalance":dict(M=0.1,e=1e-4,kappa=580.0)},
 j_recheck=True,j_recheck_period=2.0,j_recheck_len=0.6,j_recheck_amp=0.157,j_recheck_nmin=2,j_recheck_t0=1.0,
 j_recheck_f_auto=True,j_recheck_amp_auto=True,j_recheck_gate=True,j_recheck_gate_ac=10.0,j_recheck_gate_step=10.0,
 j_recheck_apply=True,j_recheck_alpha=0.8)
if mode=="frozen": cfg["j_recheck_apply"]=False
if mode=="slow": cfg["j_recheck_alpha"]=0.2
if mode=="nofault": cfg["tl_fault"]=None; cfg["j_recheck_apply"]=False
Y=sim_inv(t,TL,cfg)
jh=np.asarray(Y["jhat"]); b0=np.asarray(Y["b0e"])
print(mode,TEND,"jfin %.3e"%float(jh[-1]),"b0e %.1f"%float(b0[-1]),"iq %.2f"%float(np.max(np.abs(Y["iq"]))),
      "jmin %.3e"%float(jh.min()),"jmax %.3e"%float(jh.max()),"fd",Y["fd"].tolist(),"abort",Y["abort"].tolist(),"states",sorted(set(int(x) for x in Y["jstate"])),flush=True)
np.savez("_wave_j_diag_%s.npz"%mode,t=Y["t"],y=Y["y"],iq=Y["iq"],jhat=jh,
         t_j=np.asarray(Y["t_j"]),b0e=b0,fd=Y["fd"],abort=Y["abort"],jstate=Y["jstate"])
