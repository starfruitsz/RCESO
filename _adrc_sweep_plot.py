# -*- coding: utf-8 -*-
"""_adrc_sweep_plot.py —— k1 扫描：跌落/e1/bhat/超调 vs k1，标出失稳点。"""
import math, numpy as np, importlib.util
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei","SimHei","DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.5})

spec=importlib.util.spec_from_file_location("lab","_adrc_lab.py")
lab=importlib.util.module_from_spec(spec); spec.loader.exec_module(lab)

def met_load(d):
    t=d["t"]; m=t>=0.5
    dip=d["w"][m].min()-1000.0
    tr=(t>=0.5)&(t<=1.1)
    return dip, float(np.sqrt(np.mean(d["e1"][tr]**2))), d["bh"][-1], float(d["w"].max())

def met_speed(d):
    t=d["t"]; m=t>=0.5
    return (d["w"][m].max()/1000.0-1)*100, float(d["w"].max())

base_load=met_load(lab.sim("load",4.0,False))
base_speed=met_speed(lab.sim("speed",1.0,False))

ks=[0.003,0.01,0.03,0.1,0.3,1,3,5,8,12,20,30,50]
dip=[]; e1=[]; bh=[]; over=[]; unstable=[]
for k in ks:
    k2=k*3e-4; k3=k*1e-6
    dl=lab.sim("load",4.0,True,k1=k,k2=k2,k3=k3)
    ds=lab.sim("speed",1.0,True,k1=k,k2=k2,k3=k3)
    d1,e,b,mx=met_load(dl); o,_=met_speed(ds)
    dip.append(d1); e1.append(e); bh.append(b); over.append(o)
    unstable.append(mx>1150 or abs(b)>3*lab.B0)

fig,ax=plt.subplots(2,2,figsize=(11.6,7.0))
x=np.array(ks); u=np.array(unstable)
def mark(a):
    a.axvline(x[np.argmax(u)] if u.any() else x[-1], color="#c0392b", ls=":", lw=0.8)
for i,(y,base,lab_y,ttl) in enumerate([
        (dip, base_load[0], "加载跌落 / rpm", "(a) 加载工况 J×4：跌落 vs k1"),
        (e1, base_load[1], "暂态 e1 RMS / rpm", "(b) 加载工况 J×4：e1 暂态 RMS vs k1"),
        (bh, 1154.0, "末态 b0+Δb", "(c) 末态 b0+Δb vs k1（真值 1154，标称 4615）"),
        (over, base_speed[0], "升速超调 / %", "(d) 升速工况 J×1：超调 vs k1")]):
    a=[ax[0,0],ax[0,1],ax[1,0],ax[1,1]][i]
    a.semilogx(x[~u], np.array(y)[~u], "o-", color="#1f4e79", lw=1.2, ms=4, label="自适应")
    if u.any():
        a.semilogx(x[u], np.array(y)[u], "x", color="#c0392b", ms=7, label="失稳/越界")
    a.axhline(base, color="#7f8c8d", ls="--", lw=0.9, label="常规 ADRC" if i<4 else None)
    a.set_xlabel("$k_1$"); a.set_ylabel(lab_y); a.set_title(ttl, fontsize=9)
    a.grid(alpha=0.25, which="both")
    if i==2:
        a.axhline(1154, color="#e67e22", ls="-.", lw=0.9, label="真值 b=1154")
        a.set_yscale("log")
    a.legend(fontsize=6.5)
fig.suptitle("自适应 ADRC：增益扫描（实验室噪声；$k_2=3\\times10^{-4}k_1$，$k_3=10^{-6}k_1$）", fontsize=10)
fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig("fig_adrc_k1_sweep.png", dpi=150, facecolor="white")
print("saved fig_adrc_k1_sweep.png")
for k,d,e,b,o,uu in zip(ks,dip,e1,bh,over,unstable):
    print("%-6g dip %7.1f e1 %5.2f bh %8.1f over %5.2f %s"%(k,d,e,b,o,"UNST" if uu else ""))
