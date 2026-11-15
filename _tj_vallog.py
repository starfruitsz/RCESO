# -*- coding: utf-8 -*-
import numpy as np, noise_cfg as NC
from pmsm_inv_sim import sim_inv
t=np.arange(0.0,12.0,2e-6); TL=(0.50*(t>=2.0)).astype(float)*0.637
FAULT=dict(start=2.0,unbalance=dict(M=0.1,e=1e-4,kappa=580.0),misalign=dict(M=0.1,beta=0.01745,l=0.05,kappa=67.0))
cfg=dict(n_ref=600.0,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,Q0=0.98,tau0=20e-3,seed_i=20261018,
 i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
 eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,a_ref=0.2,
 tl_fault=FAULT,J_true=9.95e-5,T_es=True,es_d0=-0.143,es_step=0.01,es_dith=0.005,es_Pd=1.5,es_N=3,
 es_dead=2e-6,es_dmax=0.20,es_t0=3.0,T_dft=2.0,
 j_recheck=True,j_recheck_period=2.0,j_recheck_len=0.6,j_recheck_amp=0.157,j_recheck_nmin=2,j_recheck_t0=4.0,
 j_recheck_f_auto=True,j_recheck_f_q=6.0,j_recheck_f_alpha=0.35,j_recheck_f_min=50.0,j_recheck_f_max=110.0,
 j_recheck_amp_auto=True,j_recheck_gate=True,j_recheck_gate_ac=10.0,j_recheck_gate_step=10.0,
 j_recheck_apply=True,j_recheck_alpha=0.8,j_recheck_btau=20e-3,j_b0_direct=True)
Y=sim_inv(t,TL,cfg)
log=Y["jval_log"]
print("t(s)  iq_ratio  amp_ratio  bad_iq bad_a  -> 判定")
for row in log:
    print("%5.2f  %8.3f  %9.3f    %d      %d    %s" % (row[0],row[1],row[2],row[3],row[4],
          "回退" if (row[3] or row[4]) else "接受"))
b0=np.asarray(Y["b0e"]); print("b0 end %.1f" % b0[-1])
