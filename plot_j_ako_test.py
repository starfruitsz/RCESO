# -*- coding: utf-8 -*-
"""plot_j_ako_test.py —— Yang 2018 AKO+RLS 试跑 vs 调试期 DFT（3 联图）"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JM, JB = 1.89e-5, 9.95e-5
C_FIX, C_AKO, C_COMM, C_ORACLE = "#c0392b", "#8e44ad", "#16a085", "#e67e22"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.0,
})
W = {k: np.load("_wave_j_%s.npz" % k) for k in ("big_fault", "big_oracle", "big_comm", "big_ako_l0.990_R1e-03")}
def met(z):
    t=z["t"]; e=(z["y"]-1.0)*600.0; m=(t>=9.0)&(t<10.0); tc,ec=t[m],e[m]
    a10=float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*tc)),2*np.mean(ec*np.sin(2*np.pi*10*tc))))
    return a10, float(np.sqrt(np.mean(ec**2))), float(np.max(np.abs(z["iq"])))
a10_f,rms_f,iq_f=met(W["big_fault"]); a10_o,_,iq_o=met(W["big_oracle"])
a10_c,rms_c,iq_c=met(W["big_comm"]); a10_a,rms_a,iq_a=met(W["big_ako_l0.990_R1e-03"])
jako=float(np.asarray(W["big_ako_l0.990_R1e-03"]["jhat"])[-1]); print(a10_f,a10_a,a10_c,jako)

fig=plt.figure(figsize=(13.33,6.67))
gs=fig.add_gridspec(2,2,width_ratios=[1.55,1.0],height_ratios=[1.0,1.0],
                    left=0.065,right=0.985,top=0.865,bottom=0.11,wspace=0.18,hspace=0.42)
axa=fig.add_subplot(gs[:,0]); axb=fig.add_subplot(gs[0,1]); axd=fig.add_subplot(gs[1,1])

for key,c,lab,lw in (("big_fault",C_FIX,"固定标称 b0",0.9),
                     ("big_ako_l0.990_R1e-03",C_AKO,"AKO+RLS（试跑）",1.1),
                     ("big_oracle",C_ORACLE,"oracle 重整定",0.9),
                     ("big_comm",C_COMM,"辨识 + b0 自适应",1.2)):
    d=W[key]; tt=d["t"][::100]; e=(d["y"][::100]-1.0)*600.0; m=(tt>=9.0)&(tt<=10.0)
    axa.plot(tt[m],e[m],color=c,lw=lw,label=lab)
axa.set_xlim(9.0,10.0); axa.set_ylim(-70,82)
axa.set_xlabel("时间 / s"); axa.set_ylabel("转速误差 / rpm")
axa.set_title("(a) 稳态 9–10 s：AKO 已压到 6.1，但不如 DFT 的 4.0", fontsize=10.2, pad=5)
axa.legend(loc="upper right", fontsize=7.8); axa.axhline(0,color="#999",lw=0.6)

labels=["固定 b0","AKO+RLS","调试期 DFT","oracle"]
vals=[a10_f,a10_a,a10_c,a10_o]; cols=[C_FIX,C_AKO,C_COMM,C_ORACLE]
bars=axb.bar(range(4),vals,color=cols,width=0.62)
for b,v in zip(bars,vals): axb.text(b.get_x()+b.get_width()/2,v+0.8,"%.1f"%v,ha="center",va="bottom",fontsize=8.2)
axb.set_xticks(range(4)); axb.set_xticklabels(labels,fontsize=7.4)
axb.set_ylabel("10 Hz 转速分量 / rpm"); axb.set_ylim(0,42)
axb.set_title("(b) AKO 把 10 Hz 压到 6.1（−82%）", fontsize=10.2, pad=5)

d=W["big_comm"]; axd.plot(d["t_j"],np.asarray(d["jhat"])*1e6,color=C_COMM,lw=1.4,label="调试期 DFT")
d=W["big_ako_l0.990_R1e-03"]; axd.plot(d["t_j"],np.asarray(d["jhat"])*1e6,color=C_AKO,lw=1.1,label="AKO+RLS")
axd.axhline(JB*1e6,color="#555",ls="--",lw=0.9,label=r"$J_{\rm true}=99.5$")
axd.axhspan(JB*0.9e6,JB*1.1e6,color=C_COMM,alpha=0.08)
axd.set_xlim(0,10); axd.set_ylim(0,125)
axd.set_xlabel("时间 / s"); axd.set_ylabel(r"$\hat J$ / ($10^{-6}$ kg·m$^2$)")
axd.set_title("(c) AKO 未收敛：终值 %.1f（−48%%）；DFT +9.1%%" % (jako*1e6), fontsize=9.6, pad=5)
axd.legend(loc="center right", fontsize=7.4)
axd.text(5.0,52,"AKO 的 a1/b1 参数化在 B=0 对象上\n出现偏差；10 Hz 已改善",fontsize=7.2,color=C_AKO,ha="center")

fig.suptitle("Yang 2018 AKO+RLS 试跑：10 Hz 33.3→6.1，但 $\\hat J$ 未收敛；调试期 DFT 仍最优（600 rpm、$J_{\\rm true}=5.26J_{\\rm nom}$）",
             fontsize=10.6, y=0.965)
fig.text(0.065,0.015,"AKO：3 状态 KF [θ,ω,T_L] + a1/b1 RLS；Q=diag(1e-3,1e-2,1e-1)、R=1e-3、e_thr=1e-4、ρ=0.1、λ=0.99、T=1 ms；B=0（本对象无粘滞项）。试跑，非论文 0.1 ms/B>0 原参数。",
         fontsize=6.6,color="#666")
fig.savefig("fig_j_ako_test.png",dpi=150,bbox_inches=None,facecolor="white")
print("ok")
