# -*- coding: utf-8 -*-
"""plot_ppt5.py —— 余下 5 张 PPT 图，2:1（1920x960），组合故障"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C_B, C_A, C_N = "#1f4e79", "#e67e22", "#c0392b"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.4, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.4,
})

def load(f):
    z = np.load(f)
    t = np.asarray(z["t"]); dec = max(1, int(round(1e-3 / (t[1]-t[0]))))
    return dict(t=t[::dec], y=np.asarray(z["y"])[::dec], iq=np.asarray(z["iq"])[::dec],
                tl=np.asarray(z["tl"])[::dec], amp=np.asarray(z["amp"])[::dec],
                es=np.asarray(z["es"])[::dec])

def amp10(t, e, f=10.0, a=None, b=None):
    m = (t >= a) & (t < b) if a is not None else np.ones_like(t, bool)
    tt, ee = t[m], e[m]; w = 2*np.pi*f
    return float(np.hypot(2*np.mean(ee*np.cos(w*tt)), 2*np.mean(ee*np.sin(w*tt))))

# ---------------- s5 ----------------
fig, ax = plt.subplots(2, 3, figsize=(12.8, 6.4))
fig.subplots_adjust(left=0.055, right=0.99, top=0.84, bottom=0.10, wspace=0.24, hspace=0.45)
cases = [("load", "(a) 负载突变 2 s（0.50 额定）", (1.9, 2.6)), ("speed", "(b) 参考 600→900 rpm（5 s）", (4.8, 6.0)), ("echo", "(c) 5.98 s 组合故障反相", (5.9, 6.6))]
for i, (case, title, zr) in enumerate(cases):
    d1 = load("_ppt5_s5_%s_lpf.npz" % case); d0 = load("_ppt5_s5_%s_nolpf.npz" % case)
    t = d1["t"]; e1 = (d1["y"]-1)*600; e0 = (d0["y"]-1)*600
    ax[0,i].plot(t, 600+e0, color=C_N, lw=0.6, alpha=0.8, label="无低通（τ=0）")
    ax[0,i].plot(t, 600+e1, color=C_B, lw=1.0, label="有低通（τ=20 ms）")
    ax[0,i].set_xlim(0,8); ax[0,i].set_ylim(-2500,3500)
    ax[0,i].set_title(title, fontsize=8.8); ax[0,i].set_xlabel("时间 / s"); ax[0,i].set_ylabel("转速 / rpm")
    if i == 0:
        ax[0,i].legend(loc="lower right", fontsize=6.8)
    m=(t>=zr[0])&(t<=zr[1])
    ax[1,i].plot(t[m], e0[m], color=C_N, lw=0.9, label="无低通")
    ax[1,i].plot(t[m], e1[m], color=C_B, lw=1.1, label="有低通")
    ax[1,i].set_xlim(*zr); ax[1,i].set_xlabel("时间 / s"); ax[1,i].set_ylabel("转速误差 / rpm")
    ax[1,i].set_title("局部：RMS %.0f vs %.0f rpm" % (np.sqrt(np.mean(e0[m]**2)), np.sqrt(np.mean(e1[m]**2))), fontsize=7.8)
fig.suptitle("无自适应 RCESO：保留低通 vs 去掉低通（圆盘不平衡 + 角不对中 β=1° + 平行不对中，600 rpm，8 s）", fontsize=10.4, y=0.965)
fig.savefig("ppt_s5_combined.png", dpi=150, bbox_inches=None, facecolor="white")
plt.close(fig)

# ---------------- s6 ----------------
D = np.load("_ppt_fig1.npz"); t = np.asarray(D["t"]); dec = max(1,int(round(1e-3/(t[1]-t[0]))))
ts=t[::dec]; N=600.0
fig, ax = plt.subplots(3,1, figsize=(12.8,6.4), sharex=True)
fig.subplots_adjust(left=0.075, right=0.99, top=0.86, bottom=0.09, hspace=0.20)
ax[0].plot(ts, np.asarray(D["TL"])[::dec], color="#7d3c98", lw=0.9)
ax[0].set_ylabel("$T_L$ / N·m"); ax[0].set_ylim(-0.03,0.62)
ax[0].text(0.15,0.50,"空载",fontsize=8.5); ax[0].text(2.2,0.55,"组合故障投入",fontsize=8.5,color="#7d3c98")
for k,c,lab in (("eso",C_B,"纯 ESO"),("rceso",C_A,"无自适应 RCESO")):
    ax[1].plot(ts, np.asarray(D["y_"+k])[::dec]*N, color=c, lw=0.8, label=lab)
    ax[2].plot(ts, np.asarray(D["iq_"+k])[::dec], color=c, lw=0.5, alpha=0.55, label=lab+" $i_q$")
ax[1].axhline(N,color="#888",ls=":",lw=0.8); ax[1].set_ylabel("转速 / rpm"); ax[1].set_ylim(0,1.35*N)
eE=(np.asarray(D["y_eso"])-1)*N; eR=(np.asarray(D["y_rceso"])-1)*N
m=(t>=5)&(t<6)
txt="5–6 s：RMS %.0f → %.0f rpm；10 Hz %.0f → %.0f rpm"%(np.sqrt(np.mean(eE[m]**2)),np.sqrt(np.mean(eR[m]**2)),amp10(t,eE,10,5,6),amp10(t,eR,10,5,6))
ax[1].text(0.01,0.95,txt,transform=ax[1].transAxes,fontsize=8.0,va="top",bbox=dict(facecolor="white",edgecolor="none",alpha=0.85))
ax[1].legend(loc="lower left",fontsize=7.2)
ax[2].set_ylabel("电流 / A"); ax[2].set_xlabel("时间 / s"); ax[2].set_xlim(0,8); ax[2].set_ylim(-0.5,6.4)
ax[2].legend(loc="upper left",fontsize=7.0,ncol=2)
fig.suptitle("同一组合故障：纯 ESO vs 无自适应 RCESO（600 rpm，8 s；圆盘不平衡 + 角不对中 + 平行不对中）", fontsize=10.2, y=0.965)
fig.savefig("ppt_s6_combined.png", dpi=150, bbox_inches=None, facecolor="white")
plt.close(fig)

# ---------------- s8 ----------------
A=load("_ppt5_s8_A.npz"); B=load("_ppt5_s8_B.npz")
fig, ax = plt.subplots(2,2, figsize=(12.8,6.4))
fig.subplots_adjust(left=0.07,right=0.99,top=0.86,bottom=0.10,wspace=0.22,hspace=0.40)
ax[0,0].plot(A["t"],A["tl"],color=C_A,lw=0.8,label="工况1（实验组）")
ax[0,0].plot(B["t"],B["tl"],color="#7f8c8d",lw=0.8,label="工况2（对照组）")
ax[0,0].set_xlim(0,8);ax[0,0].set_ylim(-0.03,0.62);ax[0,0].set_ylabel("$T_L$ / N·m");ax[0,0].set_title("(a) 两组负载",fontsize=8.8);ax[0,0].legend(fontsize=7)
ax[0,1].plot(A["t"],A["y"]*600,color=C_A,lw=0.7,label="工况1：6 s 换速 600→300")
ax[0,1].plot(B["t"],B["y"]*600,color="#7f8c8d",lw=0.7,label="工况2：恒 600")
ax[0,1].axhline(600,color="#888",ls=":",lw=0.8);ax[0,1].set_xlim(0,8);ax[0,1].set_ylim(150,760);ax[0,1].set_ylabel("转速 / rpm");ax[0,1].set_title("(b) 全程转速（T 自适应）",fontsize=8.8);ax[0,1].legend(fontsize=7)
for d,c,lab in ((A,C_A,"工况1"),(B,"#7f8c8d","工况2")):
    m=(d["t"]>=1.9)&(d["t"]<=2.5);ax[1,0].plot(d["t"][m],(d["y"][m]-1)*600,color=c,lw=0.9,label=lab)
ax[1,0].set_xlim(1.9,2.5);ax[1,0].set_ylabel("转速误差 / rpm");ax[1,0].set_title("(c) 加载窗 1.9–2.5 s",fontsize=8.8);ax[1,0].legend(fontsize=7)
for d,c,lab in ((A,C_A,"工况1"),(B,"#7f8c8d","工况2")):
    m=(d["t"]>=5.8)&(d["t"]<=6.4);ax[1,1].plot(d["t"][m],d["y"][m]*600,color=c,lw=0.9,label=lab)
ax[1,1].set_xlim(5.8,6.4);ax[1,1].set_ylabel("转速 / rpm");ax[1,1].set_title("(d) 换速窗 5.8–6.4 s",fontsize=8.8);ax[1,1].legend(fontsize=7)
fig.suptitle("两组对照：只有实验组换速 600→300（T 自适应；圆盘不平衡 + 角不对中 + 平行不对中）", fontsize=10.0, y=0.965)
fig.savefig("ppt_s8_combined.png", dpi=150, bbox_inches=None, facecolor="white")
plt.close(fig)

# ---------------- s10 ----------------
b=load("_ppt5_s10_base.npz"); l=load("_ppt5_s10_lawd.npz")
fig=plt.figure(figsize=(12.8,6.4)); gs=fig.add_gridspec(3,3,left=0.06,right=0.99,top=0.86,bottom=0.09,wspace=0.30,hspace=0.55)
aa=fig.add_subplot(gs[0,:2]); ab=fig.add_subplot(gs[0,2]); ac=fig.add_subplot(gs[1,:2]); ad=fig.add_subplot(gs[1,2]); ae=fig.add_subplot(gs[2,:2]); af=fig.add_subplot(gs[2,2])
def met(d):
    e=(d["y"]-1)*600; m=(d["t"]>=1.9)&(d["t"]<=2.5); dip=float(np.min(e[m])); i0=int(np.where(m)[0][np.argmin(e[m])])
    idx=np.where((np.abs(e)<=20)&(np.arange(len(e))>i0)&(d["t"]>=2))[0]; rec=(d["t"][idx[0]]-2)*1e3 if len(idx) else np.nan
    return dip,rec,float(np.sqrt(np.mean(e[(d["t"]>=2)&(d["t"]<2.5)]**2))),float(np.sqrt(np.mean(e[(d["t"]>=7)&(d["t"]<8)]**2))),float(np.max(np.abs(d["iq"])))
mb=met(b); ml=met(l)
aa.plot(b["t"],600+(b["y"]-1)*600,color=C_B,lw=1.8,alpha=0.6,label="无自适应（跌落 %.0f）"%mb[0]);aa.plot(l["t"],600+(l["y"]-1)*600,color=C_A,lw=1.0,label="律 D（跌落 %.0f）"%ml[0])
aa.set_xlim(0,8);aa.set_ylim(100,720);aa.set_xlabel("时间 / s");aa.set_ylabel("转速 / rpm");aa.set_title("(a) 加载前后绝对转速（2 s 0.50 额定）",fontsize=8.6);aa.legend(fontsize=7)
ab.axis("off");ab.text(0,1,"指标 | 无自适应 | 律D\n跌落/rpm | %.0f | %.0f\n恢复/ms | %.0f | %.0f\n突变RMS | %.1f | %.1f\n稳态RMS | %.1f | %.1f\n|iq|/A | %.2f | %.2f"%(mb[0],ml[0],mb[1],ml[1],mb[2],ml[2],mb[3],ml[3],mb[4],ml[4]),fontsize=7.0,va="top")
ac.plot(b["t"],b["tl"],color="#34495e",lw=0.7);ac.set_xlim(0,8);ac.set_ylim(-0.03,0.62);ac.set_ylabel("$T_L$ / N·m");ac.set_title("(c) 负载：组合故障",fontsize=8.6)
m=(b["t"]>=1.9)&(b["t"]<=2.6);ad.plot(b["t"][m],(b["y"][m]-1)*600,color=C_B,lw=0.9);ad.plot(l["t"][m],(l["y"][m]-1)*600,color=C_A,lw=0.9);ad.set_xlim(1.9,2.6);ad.set_ylabel("误差 / rpm");ad.set_title("(d) 加载窗",fontsize=8.6)
ae.plot(b["t"],b["iq"],color=C_B,lw=0.5,alpha=0.6,label="无自适应");ae.plot(l["t"],l["iq"],color=C_A,lw=0.5,label="律D");ae.axhline(6.31,color=C_N,ls="--",lw=0.8);ae.set_xlim(0,8);ae.set_ylim(0,7.5);ae.set_ylabel("$i_q$ / A");ae.set_xlabel("时间 / s");ae.set_title("(e) 电流代价",fontsize=8.6);ae.legend(fontsize=7)
m=(b["t"]>=7)&(b["t"]<=8);af.plot(b["t"][m],(b["y"][m]-1)*600,color=C_B,lw=0.8);af.plot(l["t"][m],(l["y"][m]-1)*600,color=C_A,lw=0.8);af.set_xlim(7,8);af.set_ylabel("误差 / rpm");af.set_title("(f) 稳态 7–8 s",fontsize=8.6)
fig.suptitle("律 D（$k_p$+ESO 带宽自适应）对加载的改善（600 rpm、8 s；圆盘不平衡+角不对中+平行不对中）",fontsize=9.8,y=0.965)
fig.savefig("ppt_s10_combined.png",dpi=150,bbox_inches=None,facecolor="white");plt.close(fig)

# ---------------- s13 ----------------
b=load("_ppt5_s13_base.npz"); e=load("_ppt5_s13_esc.npz")
fig=plt.figure(figsize=(12.8,6.4)); gs=fig.add_gridspec(3,3,left=0.06,right=0.99,top=0.86,bottom=0.09,wspace=0.24,hspace=0.50)
a1=fig.add_subplot(gs[0,:]);a2=fig.add_subplot(gs[1,0]);a3=fig.add_subplot(gs[1,1]);a4=fig.add_subplot(gs[2,0]);a5=fig.add_subplot(gs[2,1]);a6=fig.add_subplot(gs[2,2])
eb=(b["y"]-1)*600; ee=(e["y"]-1)*600
a1.plot(b["t"],600+eb,color=C_B,lw=0.7,label="无自适应");a1.plot(e["t"],600+ee,color=C_A,lw=0.8,label="T 自适应")
a1.set_xlim(0,30);a1.set_ylim(450,750);a1.set_xlabel("时间 / s");a1.set_ylabel("转速 / rpm");a1.set_title("(a) 30 s 完整转速（2 s 加载 0.50 额定 + 组合故障）",fontsize=8.6);a1.legend(fontsize=7)
m=b["t"]>=25; rb=float(np.sqrt(np.mean(eb[m]**2)));re=float(np.sqrt(np.mean(ee[m]**2)));ab10=amp10(b["t"],eb,10,25,30);ae10=amp10(e["t"],ee,10,25,30)
a2.bar([0,1],[rb,re],color=[C_B,C_A],width=0.55);a2.set_xticks([0,1]);a2.set_xticklabels(["无自适应","T 自适应"]);a2.set_ylabel("稳态 RMS / rpm");a2.set_title("(b) RMS %.1f→%.1f"%(rb,re),fontsize=8.4)
a3.bar([0,1],[ab10,ae10],color=[C_B,C_A],width=0.55);a3.set_xticks([0,1]);a3.set_xticklabels(["无自适应","T 自适应"]);a3.set_ylabel("10 Hz / rpm");a3.set_title("(c) 10 Hz %.1f→%.1f"%(ab10,ae10),fontsize=8.4)
a4.plot(b["t"],b["tl"],color="#34495e",lw=0.6);a4.set_xlim(0,30);a4.set_ylim(-0.03,0.62);a4.set_ylabel("$T_L$ / N·m");a4.set_xlabel("时间 / s");a4.set_title("(d) 负载：组合故障",fontsize=8.4)
m=(e["t"]>=26)&(e["t"]<=27);a5.plot(e["t"][m],ee[m],color=C_A,lw=0.8);a5.set_xlim(26,27);a5.set_ylabel("误差 / rpm");a5.set_xlabel("时间 / s");a5.set_title("(e) 稳态 10 Hz 分量",fontsize=8.4)
a6.plot(e["t"],e["es"]*100,color=C_A,lw=0.9);a6.set_xlim(0,30);a6.set_ylabel(r"$\delta$ / %");a6.set_xlabel("时间 / s");a6.set_title("(f) δ 收敛：末段 %.2f%%"%(100*np.mean(e["es"][e["t"]>=25])),fontsize=8.4)
fig.suptitle("T 自适应 vs 无自适应（600 rpm、30 s；圆盘不平衡 + 角不对中 + 平行不对中）",fontsize=9.8,y=0.965)
fig.savefig("ppt_s13_combined.png",dpi=150,bbox_inches=None,facecolor="white");plt.close(fig)
print("ok")