# -*- coding: utf-8 -*-
"""_adrc_leak_long.py —— 24 s 反复加载/卸载：无泄漏时 b̂ 的"棘轮"漂移 vs 泄漏回锚。"""
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
TAU_I=5e-4; DT=1e-5; TEND=24.0
W_HI=1000*math.pi/30
SIG_W=3.0*math.pi/30; SIG_I=0.1; SIG_T=0.01
FC_W=200.0; FC_I=2000.0; FC_T=200.0
K1,K2,K3=3.0,9e-4,3e-6

def fal(e,a=ALPHA,d=DELTA):
    return e/(d**(1-a)) if abs(e)<=d else math.copysign(abs(e)**a,e)

def sim(jscale,adaptive,leak=0.0,seed=11,toggle=2.0):
    rng=np.random.default_rng(seed); jt=J_NOM*jscale
    w=W_HI; iq=0.0; z1=w; z2=0.0; v1=w; v2=0.0; db=0.0
    aw=math.exp(-2*math.pi*FC_W*DT); bw=SIG_W*math.sqrt(1-aw*aw)
    ai=math.exp(-2*math.pi*FC_I*DT); bi=SIG_I*math.sqrt(1-ai*ai)
    at=math.exp(-2*math.pi*FC_T*DT); bt=SIG_T*math.sqrt(1-at*at)
    nw=ni=nt=0.0; rec=[]; n=int(TEND/DT)
    for i in range(n):
        t=i*DT
        tm_base = 0.3 if (int(t/toggle)%2==1) else 0.0
        nw=aw*nw+bw*rng.normal(); ni=ai*ni+bi*rng.normal(); nt=at*nt+bt*rng.normal()
        tm=tm_base+nt; wm=w+nw
        e1=z1-wm; e0=v1-z1
        bh=B0+(db if adaptive else 0.0)
        f1=fal(e1); f0=fal(e0); u0=KP*f0; u=(u0-z2)/bh
        iq+=DT*(u-iq)/TAU_I
        te=1.5*NP*PSI*(iq+ni)
        w+=DT*(te-tm-B_FRIC*w)/jt
        z1+=DT*(z2-BETA1*f1+bh*u); z2+=DT*(-BETA2*f1)
        v1+=DT*v2; v2+=DT*(-R_TD*R_TD*(v1-W_HI)-2*R_TD*v2)
        if adaptive:
            rhs=(-K1*z1*(-BETA1*f1+KP*bh*f0)+K2*z2*BETA2*f1
                 +K3*v2*R_TD*R_TD*(v1-W_HI))
            db+=DT*(rhs/bh - leak*db)
            db=min(max(db,-0.9*B0),9*B0)
        if i%100==0: rec.append((t,w*30/math.pi,iq,bh,e1*30/math.pi))
    a=np.array(rec)
    return dict(t=a[:,0],w=a[:,1],iq=a[:,2],bh=a[:,3],e1=a[:,4])

if __name__=="__main__":
    fig,ax=plt.subplots(2,2,figsize=(11.6,6.8))
    for leak,col,lab in ((0.0,"#1f4e79","无泄漏"),(2.0,"#c0392b","泄漏 σ=2"),(5.0,"#e67e22","泄漏 σ=5")):
        d=sim(4.0,True,leak)
        ax[0,0].plot(d["t"],d["bh"],color=col,lw=1.1,label=lab)
        ax[0,1].plot(d["t"],d["iq"],color=col,lw=0.5,alpha=0.8)
        ax[1,0].plot(d["t"],d["w"],color=col,lw=0.5,alpha=0.8)
    d=sim(4.0,False,0.0)
    ax[0,0].plot(d["t"],d["bh"],color="#7f8c8d",lw=0.9,ls=":",label="常规")
    ax[0,1].plot(d["t"],d["iq"],color="#7f8c8d",lw=0.5,ls=":",alpha=0.8)
    ax[1,0].plot(d["t"],d["w"],color="#7f8c8d",lw=0.5,ls=":",alpha=0.8)
    ax[0,0].axhline(4615,color="#999",lw=0.5); ax[0,0].axhline(1154,color="#e67e22",lw=0.6,ls="-.")
    ax[0,0].set_title("b0+Δb（24 s 反复加载/卸载）"); ax[0,0].set_ylabel("b0+Δb"); ax[0,0].legend(fontsize=6.5)
    ax[0,1].set_title("i_q / A"); ax[0,1].set_ylabel("i_q")
    ax[1,0].set_title("转速 / rpm（同一工况）"); ax[1,0].set_ylabel("rpm")
    ax[1,1].set_title("末 4 s：b̂ 与 i_q 散布")
    for leak,col,lab in ((0.0,"#1f4e79","无泄漏"),(2.0,"#c0392b","σ=2"),(5.0,"#e67e22","σ=5")):
        d=sim(4.0,True,leak); m=d["t"]>20
        ax[1,1].scatter(d["bh"][m],d["iq"][m],s=3,color=col,alpha=0.5,label=lab)
    ax[1,1].set_xlabel("b0+Δb"); ax[1,1].set_ylabel("i_q / A"); ax[1,1].legend(fontsize=6.5)
    for a in ax.ravel(): a.grid(alpha=0.2); a.set_xlabel("t / s") if a is not ax[1,1] else None
    fig.suptitle("24 s 反复加载/卸载：无泄漏 b̂ 的棘轮漂移 vs 泄漏回锚（J×4；真实 b=1154）",fontsize=9.5)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig("fig_adrc_leak_long.png",dpi=150,facecolor="white")
    print("leak  b_min  b_max  b_end  e1std_last  iq_max")
    for leak in (0.0,2.0,5.0):
        d=sim(4.0,True,leak); t=d["t"]; m=t>20
        print("%4g %7.1f %7.1f %7.1f %10.2f %7.2f"%(leak,d["bh"].min(),d["bh"].max(),d["bh"][-1],d["e1"][m].std(),np.abs(d["iq"]).max()))
    d=sim(4.0,False,0.0); t=d["t"]; m=t>20
    print("conv %7.1f %7.1f %7.1f %10.2f %7.2f"%(d["bh"].min(),d["bh"].max(),d["bh"][-1],d["e1"][m].std(),np.abs(d["iq"]).max()))
