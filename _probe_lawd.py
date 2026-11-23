# -*- coding: utf-8 -*-
"""_probe_lawd.py —— 律D 门控是否被抖动触发（导致内模反演的 P(jw) 失效）"""
import numpy as np, math, os
import noise_cfg as NC
from pmsm_inv_sim import sim_inv, J_M, I_BASE, W_REF
DT=2e-6; TEND=float(os.environ.get("TEND","8.0")); T0B=3.0
DLAW=os.environ.get("DLAW","1")=="1"
FAULT=dict(start=2.0,unbalance=dict(M=0.1,e=1e-4,kappa=580.0),
           misalign=dict(M=0.1,beta=0.01745,l=0.05,kappa=67.0),
           parallel=dict(e=1e-4,dk=1.0e5,kappa=100.0))
t=np.arange(0.0,TEND,DT); TL=(0.50*(t>=2.0)).astype(float)*0.637
KP=75.36; BTAU=50.0/KP
cfg=dict(n_ref=600.0,T=0.1,T_adapt=True,T_filt=50e-3,fci=500.0,beta3=4000.0,
         Q0=0.98,tau0=20e-3,seed_i=20261018,
         i_noise_peak=NC.NOISE_LAB["i_noise_peak"],sig_n=NC.NOISE_LAB["sig_n_rpm"],
         sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
         eso_law="fal",eso_a=0.75,eso_delta=0.10,eso_lam=10.0,
         rc_bp=5.0,b3_min=4000.0,b3_max=4000.0,tl_fault=FAULT,J_true=9.95e-5,
         a_ref=1.0,log_eso=True,
         j_recheck=True,j_recheck_period=9999.0,j_recheck_len=0.6,j_recheck_amp=0.157,
         j_recheck_nmin=2,j_recheck_t0=T0B,j_recheck_f_auto=True,j_recheck_f_q=6.0,
         j_recheck_f_alpha=0.35,j_recheck_f_min=50.0,j_recheck_f_max=110.0,
         j_recheck_amp_auto=True,j_recheck_gate=False,j_recheck_apply=False,
         j_recheck_alpha=1.0,j_recheck_btau=BTAU,j_b0_direct=True,j_validate=False,
         j_b0_new=True)
if DLAW: cfg.update(kp_boost=6.0,det_eps=0.01,kb_eso=3.0,kb_b3=0.0)
Y=sim_inv(t,TL,cfg); lg=np.asarray(Y["lg"]); jn=np.asarray(Y["jnew"])
tk,e1,v,z2,u,B0e,woe=(lg[:,i] for i in range(7))
B0=1.2*0.101*I_BASE/(J_M*W_REF); b_true=B0*J_M/9.95e-5; dB=b_true-B0e[-1]
print("DLAW=%d  b_true=%.2f  B0e=%.2f  delta_b=%+.2f  fd=%.1f"%(DLAW,b_true,B0e[-1],dB,float(np.asarray(Y["fd"])[-1][1])))
for (ta,tb,nm) in ((2.0,3.0,"pre-burst"),(3.02,3.6,"burst"),(6.0,8.0,"after")):
    m=(tk>=ta)&(tk<tb)
    print("  %-9s woe: mean=%.0f min=%.0f max=%.0f   |e1| rms=%.4f"%(nm,woe[m].mean(),woe[m].min(),woe[m].max(),np.sqrt(np.mean(e1[m]**2))))
print("\n 逐窗（内模反演）:")
print("  tk     woe_m   |U|    db(用woe_m)   db(用500)   db(用pre)")
pre=float(woe[(tk>2.0)&(tk<3.0)].mean())
kap=0.10**(0.75-1.0)
def est(wm):
    lo,hi=wm; b1=2.0*lo*1.0; b2=lo*lo*kap
    return b1,b2
for r in jn:
    tk0,B0w,btn,au=r
    m=(tk>=tk0-0.2)&(tk<tk0)
    wm=float(woe[m].mean())
    E=0.0
    def amp(xx):
        ph=2*math.pi*float(np.asarray(Y["fd"])[-1][1])*tk[m]
        n=len(xx); return (2.0/n)*(np.sum(xx*np.cos(ph))-1j*np.sum(xx*np.sin(ph)))
    w=2*math.pi*float(np.asarray(Y["fd"])[-1][1])
    def db_with(wm_):
        b1=2.0*wm_*1.0; b2=wm_*wm_*kap
        pq=complex(b1,(w*w-b2)/w)
        U=amp(u[m]); 
        return ((amp(v[m])+pq*amp(e1[m]))/U).real
    print("  %.2f  %6.0f  %5.3f  %+10.2f  %+10.2f  %+10.2f"%(tk0,wm,au,db_with(wm),db_with(500.0),db_with(pre)))
print("\n  真值 delta_b = %+.2f"%dB)
