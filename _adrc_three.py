# -*- coding: utf-8 -*-
"""_adrc_three.py —— 加载/减载/参考转速突变 三工况：泄漏 vs 无泄漏 vs 常规。"""
import math, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei","SimHei","DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.5})

J_NOM=6.5e-5; PSI=0.1; NP=2; B0=1.5*NP*PSI/J_NOM
B_FRIC=1e-4; KP=30.0
WO=300.0; BETA1=2*WO; BETA2=WO*WO
R_TD=60.0; ALPHA=0.75; DELTA=0.5
TAU_I=5e-4; DT=1e-5; TEND=2.0
W_LO=500*math.pi/30; W_MID=600*math.pi/30; W_HI=1000*math.pi/30
SIG_W=3.0*math.pi/30; SIG_I=0.1; SIG_T=0.01
FC_W=200.0; FC_I=2000.0; FC_T=200.0
K1,K2,K3=3.0,9e-4,3e-6

def fal(e,a=ALPHA,d=DELTA):
    return e/(d**(1-a)) if abs(e)<=d else math.copysign(abs(e)**a,e)

def sim(sc,jscale=4.0,adaptive=True,leak=2.0,seed=11):
    rng=np.random.default_rng(seed); jt=J_NOM*jscale
    w=W_HI
    tm0 = 0.3 if sc=="unload" else 0.0
    iq=(tm0+B_FRIC*w)/(1.5*NP*PSI)
    z2 = -tm0/jt if sc=="unload" else 0.0
    z1=w; v1=w; v2=0.0; db=0.0
    aw=math.exp(-2*math.pi*FC_W*DT); bw=SIG_W*math.sqrt(1-aw*aw)
    ai=math.exp(-2*math.pi*FC_I*DT); bi=SIG_I*math.sqrt(1-ai*ai)
    at=math.exp(-2*math.pi*FC_T*DT); bt=SIG_T*math.sqrt(1-at*at)
    nw=ni=nt=0.0; rec=[]; n=int(TEND/DT)
    for i in range(n):
        t=i*DT
        if sc=="load":   tm_base = 0.0 if t<0.5 else 0.3
        elif sc=="unload": tm_base = 0.3 if t<0.5 else 0.0
        else: tm_base = 0.0
        if sc=="ref": wref = W_HI if t<0.5 else W_MID
        else: wref = W_HI
        nw=aw*nw+bw*rng.normal(); ni=ai*ni+bi*rng.normal(); nt=at*nt+bt*rng.normal()
        tm=tm_base+nt; wm=w+nw
        e1=z1-wm; e0=v1-z1
        bh=B0+(db if adaptive else 0.0)
        f1=fal(e1); f0=fal(e0); u0=KP*f0; u=(u0-z2)/bh
        iq+=DT*(u-iq)/TAU_I
        te=1.5*NP*PSI*(iq+ni)
        w+=DT*(te-tm-B_FRIC*w)/jt
        z1+=DT*(z2-BETA1*f1+bh*u); z2+=DT*(-BETA2*f1)
        v1+=DT*v2; v2+=DT*(-R_TD*R_TD*(v1-wref)-2*R_TD*v2)
        if adaptive:
            rhs=(-K1*z1*(-BETA1*f1+KP*bh*f0)+K2*z2*BETA2*f1
                 +K3*v2*R_TD*R_TD*(v1-wref))
            db+=DT*(rhs/bh - leak*db)
            db=min(max(db,-0.9*B0),9*B0)
        if i%20==0: rec.append((t,w*30/math.pi,iq,bh,e1*30/math.pi))
    a=np.array(rec)
    return dict(t=a[:,0],w=a[:,1],iq=a[:,2],bh=a[:,3],e1=a[:,4])

if __name__=="__main__":
    scs=[("load","加载 0→0.3 N·m"),("unload","减载 0.3→0 N·m"),("ref","参考 1000→600 rpm")]
    fig,ax=plt.subplots(2,3,figsize=(13.6,6.6))
    for ci,(sc,title) in enumerate(scs):
        for leak,col,ls,lab in ((0.0,"#1f4e79","-","无泄漏"),(2.0,"#c0392b","-","泄漏 σ=2")):
            d=sim(sc,4.0,True,leak)
            ax[0,ci].plot(d["t"],d["bh"],color=col,lw=1.0,ls=ls,label=lab)
            ax[1,ci].plot(d["t"],d["w"],color=col,lw=0.8,ls=ls,label=lab)
        d=sim(sc,4.0,False,0.0)
        ax[0,ci].plot(d["t"],d["bh"],color="#7f8c8d",lw=0.9,ls=":",label="常规")
        ax[1,ci].plot(d["t"],d["w"],color="#7f8c8d",lw=0.8,ls=":",label="常规")
        ax[0,ci].set_title(title+"：b0+Δb",fontsize=8.8)
        ax[1,ci].set_title(title+"：转速 / rpm",fontsize=8.8)
        ax[0,ci].axhline(B0,color="#999",lw=0.5,alpha=0.6)
        ax[0,ci].axhline(1154,color="#e67e22",lw=0.6,ls="-.")
        ax[0,ci].set_ylim(0,8000)
        for a in (ax[0,ci],ax[1,ci]):
            a.grid(alpha=0.2); a.set_xlabel("t / s"); a.axvline(0.5,color="#999",ls=":",lw=0.6)
    ax[0,0].legend(fontsize=6.3); ax[1,0].legend(fontsize=6.3)
    fig.suptitle("三工况：泄漏 vs 无泄漏（J×4，k1=3，NOISE_LAB；橙虚线=真值 b=1154，灰实线=标称 4615）",fontsize=9.2)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig("fig_adrc_leak_three.png",dpi=150,facecolor="white")
    print("scen   leak  metric      b_end   e1std")
    for sc,_ in scs:
        for leak in (0.0,2.0):
            d=sim(sc,4.0,True,leak); t=d["t"]; m=(t>=0.5)&(t<=0.9)
            if sc=="load": key="dip %.1f"%(d["w"][m].min()-1000)
            elif sc=="unload": key="over %.1f"%(d["w"][m].max()-1000)
            else: key="under %.1f"%(d["w"][m].min()-600)
            print("%-7s %4g  %-11s %7.1f %7.2f"%(sc,leak,key,d["bh"][-1],d["e1"][t>1.5].std()))
        d=sim(sc,4.0,False,0.0); t=d["t"]; m=(t>=0.5)&(t<=0.9)
        if sc=="load": key="dip %.1f"%(d["w"][m].min()-1000)
        elif sc=="unload": key="over %.1f"%(d["w"][m].max()-1000)
        else: key="under %.1f"%(d["w"][m].min()-600)
        print("%-7s %4s  %-11s %7.1f %7.2f"%(sc,"conv",key,d["bh"][-1],d["e1"][t>1.5].std()))
