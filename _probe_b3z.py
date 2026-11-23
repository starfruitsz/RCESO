# -*- coding: utf-8 -*-
"""_probe_b3z.py —— beta3/zeta 网格：让 tanh 不提前饱和，同时保持线性化增益 20000"""
import numpy as np, math, os, sys
import noise_cfg as NC
from pmsm_inv_sim import sim_inv, J_M, I_BASE, W_REF
DT=2e-6; TEND=float(os.environ.get("TEND","8.0")); T0B=3.0
DLAW=os.environ.get("DLAW","1")=="1"
B3=float(os.environ.get("B3","4000")); ZE=float(os.environ.get("ZETA","0.2"))
B0S=float(os.environ.get("B0S","1.0")); DITH=os.environ.get("DITH","1")=="1"
TAG=os.environ.get("TAG","_probe_b3z")
DLEN=float(os.environ.get("DLEN","0.6"))
FD=os.environ.get("FD","")
FAULT=dict(start=2.0,unbalance=dict(M=0.1,e=1e-4,kappa=580.0),
           misalign=dict(M=0.1,beta=0.01745,l=0.05,kappa=67.0),
           parallel=dict(e=1e-4,dk=1.0e5,kappa=100.0))
t=np.arange(0.0,TEND,DT); TL=(0.50*(t>=2.0)).astype(float)*0.637
cfg=dict(n_ref=600.0,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=B3,zeta_inj=ZE,
         Q0=0.98,tau0=20e-3,seed_i=20261018,
         i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],
         sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
         eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,
         rc_bp=5.0,b3_min=B3,b3_max=B3,tl_fault=FAULT,J_true=9.95e-5,
         a_ref=1.0,log_eso=True, b0_scale=B0S,
         j_recheck=DITH,j_recheck_period=9999.0,j_recheck_len=DLEN,j_recheck_amp=0.157,
         j_recheck_nmin=2,j_recheck_t0=T0B,j_recheck_f_auto=(FD==""),
         j_recheck_f=float(FD) if FD else 100.0,j_recheck_f_q=6.0,
         j_recheck_f_alpha=0.35,j_recheck_f_min=50.0,j_recheck_f_max=110.0,
         j_recheck_amp_auto=True,j_recheck_gate=False,j_recheck_apply=os.environ.get("APPLY","0")=="1",
         j_recheck_alpha=1.0,j_recheck_btau=0.0,j_b0_direct=True,j_validate=False,
         j_b0_new=os.environ.get("JNEW","1")=="1",
         j_b0_alg=os.environ.get("JALG","0")=="1",
         j_b0_alt=os.environ.get("JALT","0")=="1",
         j_b0_alt_ratio=float(os.environ.get("ALTR","0.5")))
if DLAW: cfg.update(kp_boost=6.0,det_eps=0.01,kb_eso=3.0,kb_b3=0.0)
if os.environ.get("LAWT","0")=="1":   # 复刻 run_tj_cont 的律T 设置
    cfg.update(T_es=True, es_d0=-0.143, es_step=0.01, es_dith=0.005, es_Pd=1.5,
               es_N=3, es_dead=2e-6, es_dmax=0.20, es_t0=3.0, T_dft=2.0,
               a_ref=0.2, es_cont=True, es_nofreeze=True, rc_src="e1")
Y=sim_inv(t,TL,cfg); lg=np.asarray(Y["lg"]); jn=np.asarray(Y["jnew"])
np.savez(TAG+".npz", lg=lg, jnew=jn, fd=np.asarray(Y["fd"]),
         t=np.asarray(Y["t"]), y=np.asarray(Y["y"]), iq=np.asarray(Y["iq"]))
tk,e1,v,z2,u,B0e,woe=(lg[:,i] for i in range(7))
B0=1.2*0.101*I_BASE/(J_M*W_REF); b_true=B0*J_M/9.95e-5; dB=b_true-B0e[-1]
m=(tk>=3.02)&(tk<3.6)
emax=float(np.max(np.abs(e1[m]))); erms=float(np.sqrt(np.mean(e1[m]**2)))
wme=float(woe[m].mean())            # 注入 tanh 的实际输入幅度（以 zeta 归一）
print("DLAW=%d B3=%6.0f zeta=%.2f (lin=%.0f) | b_true=%.2f dB=%+.2f | |e1|max=%.4f rms=%.4f  e1/zeta max=%.2f  woe=%.0f"
      %(DLAW,B3,ZE,B3/ZE,b_true,dB,emax,erms,emax/ZE,wme))
est=[]
for r in jn:
    tk0,B0w,btn,au=r
    if au<0: continue
    est.append(btn-B0w)
if est:
    est=np.array(est); err=100*(est.mean()/dB-1)
    print("   逐窗 dB_est = %s   均值 %+.2f  误差 %+.2f%%"%(np.array2string(est,precision=1),est.mean(),err))
else:
    print("   (无有效窗)")
