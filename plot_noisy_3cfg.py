# -*- coding: utf-8 -*-
"""真实测量噪声下的三组实验图：每组 2x3 + 对比图"""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 9.5,
                     "xtick.labelsize": 8.2, "ytick.labelsize": 8.2,
                     "legend.fontsize": 8.0, "axes.titlesize": 9.4,
                     "figure.dpi": 140, "savefig.bbox": "tight", "pdf.fonttype": 42})
N = 600.0; I_BASE = 0.637/0.101
T, TW = 0.1, 6.0
COL = {"Base": "#3a3a3a", "LawD": "#c0392b", "FB": "#16a085", "D+FB": "#2471a3"}
LAB = {"Base": "无自适应（基准）", "LawD": "律 D", "FB": "律 F-B", "D+FB": "律 D + 律 F-B"}
D = {}
for k in ["Base", "LawD", "FB", "D+FB"]:
    z = np.load("_noisy_%s.npz" % k)
    D[k] = dict(t=z["t"], y=z["y"], ia=z["ia"], TL=z["TL"], u=z["u"])

def env(t, e, win=0.1):
    nb = max(1, int(round(win/(t[1]-t[0])))); m = len(e)//nb
    return (t[:m*nb].reshape(m, nb).mean(1), e[:m*nb].reshape(m, nb).min(1),
            e[:m*nb].reshape(m, nb).max(1), e[:m*nb].reshape(m, nb).mean(1))

def amp_series(t, e, t0=4.0, t1=8.5, nper=3):
    raw_t, raw_a = [], []
    k0 = int(round(t0/T)); k1 = int(round(t1/T))
    for k in range(k0 - nper + 1, k1):
        m = (t >= k*T) & (t < (k+1)*T); tt = t[m]; ee = e[m]
        c = 2*np.mean(ee*np.cos(2*math.pi*tt/T)); q = 2*np.mean(ee*np.sin(2*math.pi*tt/T))
        raw_t.append((k+0.5)*T); raw_a.append(math.hypot(c, q))
    raw_t = np.array(raw_t); raw_a = np.array(raw_a)
    ts, am = [], []
    for i in range(len(raw_a) - nper + 1):
        if raw_t[i+nper-1] < t0: continue
        ts.append(raw_t[i+nper-1]); am.append(float(np.mean(raw_a[i:i+nper])))
    return np.array(ts), np.array(am)

BASE = dict(color=COL["Base"], ls=(0, (5, 2)), lw=1.25, zorder=15, label=LAB["Base"])

def group_fig(k, tag=""):
    z = D[k]; t = z["t"]; e = (z["y"]-1.0)*N; TL = z["TL"]; ia = z["ia"]; u = z["u"]
    tb = D["Base"]["t"]; eb = (D["Base"]["y"]-1.0)*N
    fig, ax = plt.subplots(2, 3, figsize=(11.6, 6.2))
    a, b, c_ = ax[0,0], ax[0,1], ax[0,2]
    d_, e_, f_ = ax[1,0], ax[1,1], ax[1,2]
    a.plot(t, TL, color="#333", lw=0.9)
    a.axvline(2.0, color="#888", ls=":", lw=0.9); a.axvline(TW, color="#b03030", ls="--", lw=0.9)
    a.axvspan(0, 2.0, color="#eef4ff", zorder=0); a.axvspan(2.0, TW, color="#fdf3e8", zorder=0)
    a.set_xlim(0, 12); a.set_xlabel("时间 (s)"); a.set_ylabel("负载转矩 (N·m)")
    a.set_title("(a) 负载：2 s 阶跃，6 s 零交越撤除"); a.grid(alpha=0.25)
    b.plot(t, ia*I_BASE, color=COL[k], lw=0.6, label="实际 $i_q$（含 0.5 A 采样噪声）")
    b.axhline(6.5, color="#999", ls=":", lw=0.8); b.axhline(-6.5, color="#999", ls=":", lw=0.8)
    b.set_xlim(0, 12); b.set_xlabel("时间 (s)"); b.set_ylabel("电流 (A)")
    b.set_title("(b) 电流（虚线：±6.5 A 额定）"); b.legend(loc="upper right"); b.grid(alpha=0.25)
    tt, lo, hi, me = env(t, e)
    c_.fill_between(tt, lo, hi, color=COL[k], alpha=0.20, lw=0)
    c_.plot(tt, me, color=COL[k], lw=1.1, zorder=20, label=LAB[k])
    ttb, lob, hib, meb = env(tb, eb)
    c_.plot(ttb, meb, **BASE)
    c_.axvline(2.0, color="#888", ls=":", lw=0.9); c_.axvline(TW, color="#b03030", ls="--", lw=0.9)
    c_.set_xlim(0, 12); c_.set_ylim(-300, 160)
    c_.set_xlabel("时间 (s)"); c_.set_ylabel("转速误差 (rpm)")
    c_.set_title("(c) 转速误差（100 ms 包络+均值）"); c_.legend(loc="lower right"); c_.grid(alpha=0.25)
    c_.text(0.02, 0.96, "控制用转速 = 真值 + 15 rpm（带限 200 Hz）", transform=c_.transAxes,
            fontsize=7.2, color="#555", va="top")
    m = (t >= 1.9) & (t <= 2.6); mb = (tb >= 1.9) & (tb <= 2.6)
    d_.fill_between(t[m], e[m], 0, color=COL[k], alpha=0.18, lw=0)
    d_.plot(t[m], e[m], color=COL[k], lw=1.05, zorder=20, label=LAB[k])
    d_.plot(tb[mb], eb[mb], **BASE)
    d_.axvline(2.0, color="#888", ls=":", lw=0.9)
    d_.set_xlabel("时间 (s)"); d_.set_ylabel("转速误差 (rpm)")
    d_.set_title("(d) 加载瞬态放大（1.9–2.6 s）"); d_.legend(loc="lower right"); d_.grid(alpha=0.25)
    m = (t >= 5.9) & (t <= 6.6); mb = (tb >= 5.9) & (tb <= 6.6)
    e_.fill_between(t[m], e[m], 0, color=COL[k], alpha=0.18, lw=0)
    e_.plot(t[m], e[m], color=COL[k], lw=1.05, zorder=20, label=LAB[k])
    e_.plot(tb[mb], eb[mb], **BASE)
    e_.axvline(TW, color="#b03030", ls="--", lw=0.9)
    e_.set_xlabel("时间 (s)"); e_.set_ylabel("转速误差 (rpm)")
    e_.set_title("(e) 回声窗放大（5.9–6.6 s）"); e_.legend(loc="lower right"); e_.grid(alpha=0.25)
    ts, am = amp_series(t, e, 4.0, 8.5); tsb, amb = amp_series(tb, eb, 4.0, 8.5)
    f_.plot(tsb, amb, ls=(0, (5, 2)), lw=1.5, color=COL["Base"], zorder=15, label=LAB["Base"])
    f_.plot(ts, am, "o-", ms=3.0, lw=1.0, color=COL[k], zorder=20, label=LAB[k])
    f_.axvline(TW, color="#b03030", ls="--", lw=0.9)
    f_.set_xlabel("时间 (s)"); f_.set_ylabel("10 Hz 幅值 (rpm，3T 滑窗)")
    f_.set_title("(f) 10 Hz 幅值（3 周期滑窗）"); f_.legend(loc="upper right"); f_.grid(alpha=0.25)
    fig.suptitle("真实测量噪声（$i_q$ 0.5 A、转速 15 rpm）｜配置：%s" % LAB[k], fontsize=10.5)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    fig.savefig("fig_noisy_%s.png" % k, dpi=200)  # 只存 PNG（2026-10-19 约定）
    plt.close(fig)

for k in ["LawD", "FB", "D+FB"]:
    group_fig(k)

fig, ax = plt.subplots(2, 2, figsize=(9.6, 6.0))
a, b, c_, d_ = ax[0,0], ax[0,1], ax[1,0], ax[1,1]
for k in ["Base", "LawD", "FB", "D+FB"]:
    z = D[k]; t = z["t"]; e = (z["y"]-1.0)*N
    tt, lo, hi, me = env(t, e)
    if k == "Base":
        a.fill_between(tt, lo, hi, color=COL[k], alpha=0.14, lw=0, zorder=1)
        a.plot(tt, me, **BASE)
    else:
        a.fill_between(tt, lo, hi, color=COL[k], alpha=0.12, lw=0, zorder=2)
        a.plot(tt, me, color=COL[k], lw=0.9, label=LAB[k], zorder=3)
    m = (t >= 1.9) & (t <= 2.6)
    b.plot(t[m], e[m], color=COL[k], lw=(1.6 if k=="Base" else 0.9),
           ls=((0,(5,2)) if k=="Base" else "-"), zorder=(20 if k=="Base" else 3), label=LAB[k])
    m = (t >= 5.9) & (t <= 6.6)
    c_.plot(t[m], e[m], color=COL[k], lw=(1.6 if k=="Base" else 0.9),
            ls=((0,(5,2)) if k=="Base" else "-"), zorder=(20 if k=="Base" else 3), label=LAB[k])
    ts, am = amp_series(t, e, 5.5, 8.0)
    if k == "Base":
        d_.plot(ts, am, ls=(0, (5, 2)), lw=1.6, color=COL[k], zorder=20, label=LAB[k])
    else:
        d_.plot(ts, am, "o-", ms=2.8, lw=1.0, color=COL[k], zorder=3, label=LAB[k])
for x in (a, b, c_, d_):
    h, l = x.get_legend_handles_labels()
    i0 = l.index(LAB["Base"]); order = [i0] + [i for i in range(len(l)) if i != i0]
    x.legend([h[i] for i in order], [l[i] for i in order], loc="best", fontsize=7.6)
    x.grid(alpha=0.25); x.set_xlabel("时间 (s)")
a.set_ylabel("转速误差 (rpm)"); b.set_ylabel("转速误差 (rpm)")
c_.set_ylabel("转速误差 (rpm)"); d_.set_ylabel("10 Hz 幅值 (rpm)")
for x, ttl in [(a, "(a) 转速误差全景"), (b, "(b) 加载瞬态（1.9–2.6 s）"),
               (c_, "(c) 回声窗（5.9–6.6 s）"), (d_, "(d) 10 Hz 幅值（3 周期滑窗）")]:
    x.set_title(ttl, fontsize=9.2)
a.axvline(2.0, color="#888", ls=":", lw=0.9); a.axvline(TW, color="#b03030", ls="--", lw=0.9)
b.axvline(2.0, color="#888", ls=":", lw=0.9)
c_.axvline(TW, color="#b03030", ls="--", lw=0.9)
d_.axvline(TW, color="#b03030", ls="--", lw=0.9)
a.set_ylim(-300, 160)
fig.suptitle("真实测量噪声下的四配置对比（$i_q$ 0.5 A、转速 15 rpm；灰虚线＝无自适应基准）", fontsize=10.5)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig("fig_noisy_compare.png", dpi=200)  # 只存 PNG（2026-10-19 约定）
print("figs done")
