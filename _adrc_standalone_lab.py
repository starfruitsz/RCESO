# -*- coding: utf-8 -*-
"""_adrc_standalone.py —— 独立复现 TII2025 自适应 ADRC（不入原工程）。
仅阶跃 + 测量噪声、无周期故障；对照常规 ADRC；J_true = J 或 4J。
"""
import math, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei","SimHei","DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.5})

J_NOM=6.5e-5; PSI=0.1; NP=2
B0=1.5*NP*PSI/J_NOM
B_FRIC=1e-4; KP=30.0
WO=300.0; BETA1=2*WO; BETA2=WO*WO
R_TD=60.0; ALPHA=0.75; DELTA=0.5
TAU_I=5e-4; SIG=3.0*math.pi/30   # 实验室口径 3 rpm
DT=1e-5; TEND=2.0
W_LO=500*math.pi/30; W_HI=1000*math.pi/30

def fal(e,a=ALPHA,d=DELTA):
    return e/(d**(1-a)) if abs(e)<=d else math.copysign(abs(e)**a,e)

def sim(case,jscale,adaptive,k1=0.01,k2=3e-6,k3=1e-8,seed=3,tstep=0.5):
    rng=np.random.default_rng(seed); jt=J_NOM*jscale
    w=W_LO if case=="speed" else W_HI
    tm=0.0
    iq=(tm+B_FRIC*w)/(1.5*NP*PSI)
    z1=w; z2=0.0; v1=w; v2=0.0; db=0.0
    rec=[]
    n=int(TEND/DT)
    for i in range(n):
        t=i*DT
        if case=="speed": wref=W_LO if t<tstep else W_HI
        else:
            wref=W_HI; tm=0.0 if t<tstep else 0.3
        wm=w+rng.normal(0,SIG); e1=z1-wm; e0=v1-z1
        bh=B0+(db if adaptive else 0.0)
        f1=fal(e1); f0=fal(e0); u0=KP*f0; u=(u0-z2)/bh
        iq+=DT*(u-iq)/TAU_I
        w+=DT*(1.5*NP*PSI*iq-tm-B_FRIC*w)/jt
        z1+=DT*(z2-BETA1*f1+bh*u); z2+=DT*(-BETA2*f1)
        v1+=DT*v2; v2+=DT*(-R_TD*R_TD*(v1-wref)-2*R_TD*v2)
        if adaptive:
            rhs=(-k1*z1*(-BETA1*f1+KP*bh*f0)+k2*z2*BETA2*f1
                 +k3*v2*R_TD*R_TD*(v1-wref))
            db+=DT*rhs/bh; db=min(max(db,-0.9*B0),9*B0)
        if i%20==0: rec.append((t,w*30/math.pi,iq,z1*30/math.pi,z2,v1*30/math.pi,v2,bh,e1*30/math.pi,e0*30/math.pi))
    a=np.array(rec)
    return dict(t=a[:,0],w=a[:,1],iq=a[:,2],z1=a[:,3],z2=a[:,4],v1=a[:,5],v2=a[:,6],bh=a[:,7],e1=a[:,8],e0=a[:,9],wref=wref)

def met(d,tstep=0.5):
    t=d["t"]; ref=1000.0 if d["wref"]==W_HI else 500.0
    m=t>=tstep; seg=d["w"][m]; ts=t[m]
    over=(seg.max()/ref-1)*100
    band=abs(seg-ref)/ref; idx=np.where(band<=0.02)[0]
    settle=float(ts[idx[0]]-tstep) if len(idx) else float("nan")
    ss=(t>tstep+1.0)
    return over, settle, float(d["e1"][ss].std()), float(d["bh"][-1])

if __name__=="__main__":
    K1,K2,K3=0.1,3e-5,1e-9
    cfg=[("常规 J×1",False,1.0),("常规 J×4",False,4.0),("自适应 J×1",True,1.0),("自适应 J×4",True,4.0)]
    cols=["#1f4e79","#7f8c8d","#c0392b","#e67e22"]
    for case in ("speed","load"):
        fig,ax=plt.subplots(2,4,figsize=(15.5,6.2))
        for (name,ad,js),c in zip(cfg,cols):
            d=sim(case,js,ad,k1=K1,k2=K2,k3=K3)
            t=d["t"]
            ax[0,0].plot(t,d["w"],color=c,lw=0.8,label=name)
            ax[0,1].plot(t,d["iq"],color=c,lw=0.8)
            ax[0,2].plot(t,d["z1"],color=c,lw=0.8)
            ax[0,3].plot(t,d["z2"],color=c,lw=0.8)
            ax[1,0].plot(t,d["v1"],color=c,lw=0.9)
            ax[1,1].plot(t,d["v2"],color=c,lw=0.9)
            ax[1,2].plot(t,d["bh"],color=c,lw=1.0)
            ax[1,3].plot(t,d["e1"],color=c,lw=0.7)
        for a,tit in zip(ax.ravel(),["转速 / rpm","i_q / A","z1 / rpm","z2","v1（TD）/ rpm","v2（TD）","b0+Δb","e1 / rpm"]):
            a.set_title(tit); a.grid(alpha=0.2); a.set_xlabel("t / s")
        ax[0,0].legend(fontsize=6.2)
        fig.suptitle(("升速 500→1000 rpm" if case=="speed" else "1000 rpm 加载 0.3 N·m")
                     +"（TD r=60；噪声 σ=0.05 rad/s；k1=0.1）",fontsize=10)
        fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig("_adrc_%s.png"%case,dpi=150,facecolor="white"); plt.close(fig)
    print("case  ctrl        dip(rpm)  over(%)  settle(s)  e1std  bhat")
    for case in ("speed","load"):
        for name,ad,js in cfg:
            d=sim(case,js,ad,k1=K1,k2=K2,k3=K3)
            t=d["t"]; ref=1000.0 if d["wref"]==W_HI else 500.0
            m=t>=0.5; seg=d["w"][m]; ts=t[m]
            dip=seg.min()-ref; over=(seg.max()/ref-1)*100
            bad=np.where(abs(seg-ref)/ref>0.02)[0]
            settle=float(ts[bad[-1]]-0.5) if len(bad) else 0.0
            ss=t>1.5
            print("%-5s %-11s %8.1f %8.2f %10.3f %7.2f %8.1f"%(case,name,dip,over,settle,d["e1"][ss].std(),d["bh"][-1]))
