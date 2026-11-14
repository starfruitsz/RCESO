# -*- coding: utf-8 -*-
"""_test_1000_cap.py —— 1000 rpm，f_d 上限 155 Hz + 幅度补偿，30 s"""
import numpy as np, json
import noise_cfg as NC
from pmsm_inv_sim import sim_inv
nref=1000.0; TEND=30.0
t=np.arange(0.0,TEND,2e-6); TL=np.zeros_like(t)
cfg=dict(n_ref=nref,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,Q0=0.98,tau0=20e-3,seed_i=20261018,
 i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
 eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,a_ref=1.0,J_true=9.95e-5,
 tl_fault={"start":0.0,"unbalance":dict(M=0.1,e=1e-4,kappa=580.0)},
 j_recheck=True,j_recheck_period=2.0,j_recheck_len=0.6,j_recheck_amp=0.157,j_recheck_nmin=2,j_recheck_t0=1.0,
 j_recheck_f_auto=True,j_recheck_f_max=125.0,j_recheck_amp_auto=True,
 j_recheck_gate=True,j_recheck_gate_ac=10.0,j_recheck_gate_step=10.0,j_recheck_gate_pre=0.3,j_recheck_gate_bad_ms=20)
Y=sim_inv(t,TL,cfg)
jh=np.asarray(Y["jhat"]); b0=np.asarray(Y["b0e"]); js=np.asarray(Y["jstate"])
print("fd",Y["fd"].tolist(),"abort",Y["abort"].tolist())
print("jfin %.3e b0e %.1f iq %.2f"%(float(jh[-1]),float(b0[-1]),float(np.max(np.abs(Y["iq"])))))
print("states",sorted(set(int(x) for x in js)),"state4",int(np.sum(js==4)))
np.savez("_wave_j_2s_1000_cap125.npz",t=Y["t"][::100],y=Y["y"][::100],iq=Y["iq"][::100],jhat=jh,
         t_j=np.asarray(Y["t_j"]),b0e=b0,jstate=js,fd=Y["fd"],abort=Y["abort"])
json.dump(dict(nref=nref,fd=Y["fd"].tolist(),abort=Y["abort"].tolist(),jfin=float(jh[-1]),
               b0e=float(b0[-1]),iq=float(np.max(np.abs(Y["iq"]))),state4=int(np.sum(js==4))),
          open("_j_2s_1000_cap125.json","w"),indent=1)
