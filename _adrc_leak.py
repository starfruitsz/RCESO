# -*- coding: utf-8 -*-
"""_adrc_leak.py —— 自适应律加泄漏项 vs 不加：b̂ 轨迹、转速、跌落/超调。"""
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
TAU_I=5e-4; DT=1e-5; TEND=2.4
W_LO=500*math.pi/30; W_MID=600*math.pi/30; W_HI=1000*math.pi/30
SIG_W=3.0*math.pi/30; SIG_I=0.1; SIG_T=0.01
FC_W=200.0; FC_I=2000.0; FC_T=200.0
K1,K2,K3=3.0,9e-4,3e-6

def fal(e,a=ALPHA,d=DELTA):
    return e/(d**(1-a)) if abs(e)<=d else math.copysign(abs(e)**a,e)

def sim(scenario,jscale,adaptive,leak=0.0,seed=11):
    """scenario: load(加载), down(加载+1000→600), unload(加载+减载)"""
    rng=np.random.default_rng(seed); jt=J_NOM*jscale
    w=W_HI; iq=(B_FRIC*w)/(1.5*NP*PSI)
    z1=w; z2=0.0; v1=w; v2=0.0; db=0.0
    aw=math.exp(-2*math.pi*FC_W*DT); bw=SIG_W*math.sqrt(1-aw*aw)
    ai=math.exp(-2*math.pi*FC_I*DT); bi=SIG_I*math.sqrt(1-ai*ai)
    at=math.exp(-2*math.pi*FC_T*DT); bt=SIG_T*math.sqrt(1-at*at)
    nw=ni=nt=0.0; rec=[]; n=int(TEND/DT)
    for i in range(n):
        t=i*DT
        tm_base = 0.0 if t<0.5 else 0.3
        if scenario=="down": wref = W_HI if t<1.2 else W_MID
        else: wref = W_HI
        if scenario=="unload" and t>=1.2: tm_base=0.0
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
    fig,ax=plt.subplots(2,2,figsize=(11.6,7.0))
    for ci,sc in enumerate(("down","unload")):
        for js,ls in ((1.0,"-"),(4.0,"--")):
            for leak,col in ((0.0,"#1f4e79"),(2.0,"#c0392b"),(5.0,"#e67e22")):
                d=sim(sc,js,True,leak=leak); t=d["t"]
                lab=("无泄漏" if leak==0 else "泄漏 σ=%g"%leak)+(" J×1" if js==1 else " J×4")
                ax[0,ci].plot(t,d["bh"],ls,color=col,lw=0.9,label=lab if js==1 else None)
                ax[1,ci].plot(t,d["w"],ls,color=col,lw=0.8,label=None)
        base=sim(sc,4.0,False)
        ax[0,ci].plot(base["t"],base["bh"],color="#7f8c8d",lw=0.9,ls=":",label="常规 J×4")
        ax[1,ci].plot(base["t"],base["w"],color="#7f8c8d",lw=0.8,ls=":")
        ax[0,ci].set_title(("加载+降速 1000→600" if sc=="down" else "加载+减载")+"：b0+Δb",fontsize=9)
        ax[1,ci].set_title("转速 / rpm",fontsize=9)
        for a in (ax[0,ci],ax[1,ci]):
            a.grid(alpha=0.2); a.set_xlabel("t / s"); a.axvline(0.5,color="#999",ls=":",lw=0.6); a.axvline(1.2,color="#999",ls=":",lw=0.6)
        ax[0,ci].axhline(1154,color="#999",ls="-.",lw=0.7)
        ax[0,ci].axhline(4615,color="#999",ls="-",lw=0.5,alpha=0.5)
    ax[0,0].legend(fontsize=6.0,ncol=2)
    fig.suptitle("泄漏项对比（实线 J×1，虚线 J×4；灰线=常规/真值 1154/标称 4615）",fontsize=9)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig("_adrc_leak.png",dpi=150,facecolor="white")
    print("scenario leak  J   b_end   e1std")
    for sc in ("down","unload"):
        for leak in (0.0,2.0,5.0):
            for js in (1.0,4.0):
                d=sim(sc,js,True,leak=leak); t=d["t"]
                print("%-7s %4g %3.0f %8.1f %7.2f"%(sc,leak,js,d["bh"][-1],d["e1"][t>2.1].std()))
