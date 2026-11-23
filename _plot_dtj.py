# -*- coding: utf-8 -*-
"""_plot_dtj.py —— 律D×律T×律J 三律融合 vs 律T+律J vs 无律（三合一故障，90 s）。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TAG = {"base": "b90o3", "tj": "f90o3", "dtj": "d90o3"}
C = {"base": "#1f4e79", "tj": "#1e8449", "dtj": "#c0392b"}
LAB = {"base": "无律", "tj": "律T+律J", "dtj": "律D+律T+律J"}
Q = ["base", "tj", "dtj"]

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.4, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.2,
})

def load(tag):
    z = np.load("_tjc_%s.npz" % tag)
    t = np.asarray(z["t"]); dec = max(1, int(round(1e-4 / (t[1] - t[0]))))
    return dict(t=t[::dec], y=np.asarray(z["y"])[::dec] * 600.0,
                iq=np.asarray(z["iq"])[::dec])

D = {k: load(v) for k, v in TAG.items()}

def amp10(t, e, a=6.0, b=9.0):
    m = (t >= a) & (t < b); tt = t[m]; ee = e[m]; w = 2 * np.pi * 10
    return float(np.hypot(2 * np.mean(ee * np.cos(w * tt)), 2 * np.mean(ee * np.sin(w * tt))))

M = {}
for k in Q:
    t, y = D[k]["t"], D[k]["y"]; e = y - 600.0
    m = (t >= 6.0) & (t <= 9.0)
    mm = (t >= 1.9) & (t <= 2.5)
    dip = float(e[mm].min()); i0 = int(np.argmin(e[mm])); tq = t[mm]
    after = (tq > tq[i0]) & (np.abs(e[mm]) < 20)
    rec = float(tq[after][0] - tq[i0]) if after.any() else np.nan
    M[k] = dict(rms=float(np.sqrt(np.mean(e[m] ** 2))), a10=amp10(t, e), dip=dip, rec=rec)

fig = plt.figure(figsize=(12.8, 6.4))
gs = fig.add_gridspec(3, 3, left=0.06, right=0.99, top=0.855, bottom=0.09, wspace=0.26, hspace=0.52)
a1 = fig.add_subplot(gs[0, :]); a2 = fig.add_subplot(gs[1, 0]); a3 = fig.add_subplot(gs[1, 1])
a4 = fig.add_subplot(gs[1, 2]); a5 = fig.add_subplot(gs[2, 0]); a6 = fig.add_subplot(gs[2, 1]); a7 = fig.add_subplot(gs[2, 2])

for k in Q:
    d = D[k]; n = int(9.0 / 1e-4)
    a1.plot(d["t"][:n], d["y"][:n], color=C[k], lw=0.6, label=LAB[k])
a1.set_xlim(0, 9); a1.set_ylim(450, 760)
a1.set_xlabel("时间 / s"); a1.set_ylabel("转速 / rpm")
a1.set_title("(a) 0–9 s 完整转速（三合一故障从 2 s 起、2 s 加载 0.50 额定）", fontsize=8.8)
a1.legend(fontsize=7.2, ncol=3, loc="lower right")

for k in Q:
    d = D[k]; m = (d["t"] >= 1.9) & (d["t"] <= 2.5)
    a2.plot(d["t"][m], d["y"][m] - 600.0, color=C[k], lw=0.9, label=LAB[k])
a2.set_xlim(1.9, 2.5); a2.set_ylim(-260, 80)
a2.set_ylabel("转速误差 / rpm"); a2.set_xlabel("时间 / s")
a2.set_title("(b) 加载窗 1.9–2.5 s", fontsize=8.6)
a2.legend(fontsize=6.4, loc="lower right")

n1 = 10; nb = 50                      # 0.1 ms 采样：10 点 = 1 ms；50 ms 取 max
for k in Q:
    d = D[k]; n = int(9.0 / 1e-4)
    av = np.abs(d["iq"][:n // n1 * n1]).reshape(-1, n1).mean(axis=1)
    av2 = np.array([av[i:i + nb].max() for i in range(0, len(av) - nb, nb)])
    tt = d["t"][:len(av2) * nb * n1:nb * n1] + 25e-3
    a3.plot(tt, av2, color=C[k], lw=0.9, label=LAB[k])
a3.axhline(6.31, color="#c0392b", ls="--", lw=0.7)
a3.text(0.2, 6.45, "额定 6.31", fontsize=6.0, color="#c0392b")
a3.set_xlim(0, 9); a3.set_ylim(0, 9.0)
a3.set_ylabel("$|\\overline{i_q}|$ / A"); a3.set_xlabel("时间 / s")
a3.set_title("(c) 电流包络（1 ms 均值）", fontsize=8.6)
a3.legend(fontsize=6.2, loc="lower right")

x = np.arange(3); cols = [C[k] for k in Q]
rms = [M[k]["rms"] for k in Q]
a4.bar(x, rms, color=cols, width=0.55)
for i, v in enumerate(rms):
    a4.text(i, v * 1.02 + 0.4, "%.2f" % v, ha="center", fontsize=6.8)
a4.set_xticks(x); a4.set_xticklabels(["无律", "T+J", "D+T+J"], fontsize=7.0)
a4.set_ylim(0, max(rms) * 1.2); a4.set_ylabel("RMS / rpm")
a4.set_title("(d) 稳态 RMS（6–9 s）", fontsize=8.6)

a10 = [M[k]["a10"] for k in Q]
a5.bar(x, a10, color=cols, width=0.55)
for i, v in enumerate(a10):
    a5.text(i, v * 1.03 + 0.3, "%.2f" % v, ha="center", fontsize=6.8)
a5.set_xticks(x); a5.set_xticklabels(["无律", "T+J", "D+T+J"], fontsize=7.0)
a5.set_ylim(0, max(a10) * 1.2); a5.set_ylabel("10 Hz / rpm")
a5.set_title("(e) 10 Hz 残余（6–9 s）", fontsize=8.6)

dip = [-M[k]["dip"] for k in Q]
a6.bar(x, dip, color=cols, width=0.55)
for i, v in enumerate(dip):
    a6.text(i, v + 2, "%.0f" % v, ha="center", fontsize=6.8)
a6.set_xticks(x); a6.set_xticklabels(["无律", "T+J", "D+T+J"], fontsize=7.0)
a6.set_ylim(0, max(dip) * 1.2); a6.set_ylabel("加载跌落 / rpm")
a6.set_title("(f) 加载跌落（1.9–2.5 s）", fontsize=8.6)

rec = [M[k]["rec"] * 1000 for k in Q]
a7.bar(x, rec, color=cols, width=0.55)
for i, v in enumerate(rec):
    a7.text(i, v + 0.5, "%.0f" % v, ha="center", fontsize=6.8)
a7.set_xticks(x); a7.set_xticklabels(["无律", "T+J", "D+T+J"], fontsize=7.0)
a7.set_ylim(0, max(rec) * 1.2); a7.set_ylabel("恢复时间（回 ±20 rpm）/ ms")
a7.set_title("(g) 跌落恢复时间", fontsize=8.6)

fig.suptitle("律D × 律T × 律J 三律融合 vs 律T+律J vs 无律（三合一故障；600 rpm、90 s、"
             "burst 10 s 仅 1 次、α=1、b0 低通 kp/50）", fontsize=9.2, y=0.962)
fig.savefig("fig_dtj_fusion.png", dpi=150, bbox_inches=None, facecolor="white")
print("saved fig_dtj_fusion.png")
print("RMS", dict(zip(Q, [round(v, 2) for v in rms])))
print("10Hz", dict(zip(Q, [round(v, 2) for v in a10])))
print("dip", dict(zip(Q, [round(v, 0) for v in dip])))
print("rec(ms)", dict(zip(Q, [round(v, 1) for v in rec])))
