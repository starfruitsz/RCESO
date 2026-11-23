# -*- coding: utf-8 -*-
"""_adrc_unload.py —— 加载(0.5s) 后减载(1.2s, 0.3→0)，实验室噪声，k1=3。"""
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
W_HI=1000*math.pi/30
SIG_W=3.0*math.pi/30; SIG_I=0.1; SIG_T=0.01
FC_W=200.0; FC_I=2000.0; FC_T=200.0

def fal(e,a=ALPHA,d=DELTA):
    return e/(d**(1-a)) if abs(e)<=d else math.copysign(abs(e)**a,e)

def sim(jscale,adaptive,k1,k2,k3,seed=11,t_load=0.5,t_un=1.2,reverse=False):
    rng=np.random.default_rng(seed); jt=J_NOM*jscale
    w=W_HI; iq=(B_FRIC*w)/(1.5*NP*PSI)
    z1=w; z2=0.0; v1=w; v2=0.0; db=0.0
    aw=math.exp(-2*math.pi*FC_W*DT); bw=SIG_W*math.sqrt(1-aw*aw)
    ai=math.exp(-2*math.pi*FC_I*DT); bi=SIG_I*math.sqrt(1-ai*ai)
    at=math.exp(-2*math.pi*FC_T*DT); bt=SIG_T*math.sqrt(1-at*at)
    nw=ni=nt=0.0; rec=[]; n=int(TEND/DT)
    for i in range(n):
        t=i*DT
        if t<t_load: tm_base=0.0
        elif t<t_un: tm_base=0.3
        else: tm_base=(-0.3 if reverse else 0.0)
        nw=aw*nw+bw*rng.normal(); ni=ai*ni+bi*rng.normal(); nt=at*nt+bt*rng.normal()
        tm=tm_base+nt; wm=w+nw
        e1=z1-wm; e0=v1-z1
        bh=B0+(db if adaptive else 0.0)
        f1=fal(e1); f0=fal(e0); u0=KP*f0; u=(u0-z2)/bh
        iq+=DT*(u-iq)/TAU_I
        te=1.5*NP*PSI*(iq+ni)
        w+=DT*(te-tm-B_FRIC*w)/jt
        z1+=DT*(z2-BETA1*f1+bh*u); z2+=DT*(-BETA2*f1)
        v1+=DT*v2; v2+=DT*(-R_TD*R_TD*(v1-W_HI*30/math.pi*math.pi/30)-2*R_TD*v2)
        if adaptive:
            rhs=(-k1*z1*(-BETA1*f1+KP*bh*f0)+k2*z2*BETA2*f1
                 +k3*v2*R_TD*R_TD*(v1-W_HI))
            db+=DT*rhs/bh; db=min(max(db,-0.9*B0),9*B0)
        if i%20==0: rec.append((t,w*30/math.pi,iq,z1*30/math.pi,z2,v1*30/math.pi,v2,bh,e1*30/math.pi))
    a=np.array(rec)
    return dict(t=a[:,0],w=a[:,1],iq=a[:,2],z1=a[:,3],z2=a[:,4],v1=a[:,5],v2=a[:,6],bh=a[:,7],e1=a[:,8])

if __name__=="__main__":
    K1,K2,K3=3.0,9e-4,3e-6
    cfg=[("常规 J×1",False,1.0),("常规 J×4",False,4.0),("自适应 J×1",True,1.0),("自适应 J×4",True,4.0)]
    cols=["#1f4e79","#7f8c8d","#c0392b","#e67e22"]
    fig,ax=plt.subplots(2,4,figsize=(15.5,6.2))
    for (name,ad,js),c in zip(cfg,cols):
        d=sim(js,ad,K1,K2,K3); t=d["t"]
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
        for te in (0.5,1.2): a.axvline(te,color="#999",ls=":",lw=0.7,alpha=0.7)
    ax[0,0].legend(fontsize=6.2)
    fig.suptitle("加载 0.3 N·m（0.5 s）→ 减载（1.2 s）；NOISE_LAB；k1=3",fontsize=9.5)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig("_adrc_unload.png",dpi=150,facecolor="white"); plt.close(fig)
    print("controller   load_dip  unload_over  b_end  e1std")
    for name,ad,js in cfg:
        d=sim(js,ad,K1,K2,K3); t=d["t"]
        dip=d["w"][(t>=0.5)&(t<=0.9)].min()-1000
        over=d["w"][(t>=1.2)&(t<=1.8)].max()-1000
        print("%-12s %8.1f %9.1f %9.1f %7.2f"%(name,dip,over,d["bh"][-1],d["e1"][t>2.1].std()))
