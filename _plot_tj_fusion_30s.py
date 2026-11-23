# -*- coding: utf-8 -*-
"""_plot_tj_fusion_30s.py —— 30 s 仿真：(a)-(d)(f) 只画 0-9 s，图 (e) 画 0-30 s 看 δ̂ 是否收敛。

数据：_tjc_{b30c,t30c,j30c,f30c}.npz
输出：fig_tj_fusion.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TAG = {"base": "b30c", "t": "t30c", "j": "j30c", "fusion": "f30c"}
C = {"base": "#1f4e79", "t": "#e67e22", "j": "#8e44ad", "fusion": "#1e8449"}
LAB = {"base": "无律", "t": "仅律T（DFT·连续）", "j": "仅律J（直测 b0，α=1）", "fusion": "律T+律J 融合"}
Q = ["base", "t", "j", "fusion"]
T1 = 9.0            # 前五块面板的截止
TEND = 30.0         # (e) 的全长
A0, A1 = 6.0, 9.0   # 指标窗
ES_T0, ES_PD, ES_DITH = 3.0, 1.5, 0.005

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.4, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.2,
})

def load(tag):
    z = np.load("_tjc_%s.npz" % tag)
    return dict(t=np.asarray(z["t"]), y=np.asarray(z["y"]), iq=np.asarray(z["iq"]),
                b0=np.asarray(z["b0e"]), t_j=np.asarray(z["t_j"]), es=np.asarray(z["es"]))

D = {k: load(v) for k, v in TAG.items()}

def metrics(d):
    t, y = d["t"], d["y"]
    e = (y - 1.0) * 600.0
    m = (t >= A0) & (t <= A1)
    rms = float(np.sqrt(np.mean(e[m] ** 2)))
    w = (t >= A0) & (t < A1)
    x = e[w] - e[w].mean()
    X = np.fft.rfft(x * np.hanning(len(x)))
    fr = np.fft.rfftfreq(len(x), d=float(t[1] - t[0]))
    a10 = float(2 * np.abs(X[np.argmin(np.abs(fr - 10.0))]) / np.sum(np.hanning(len(x))))
    n1 = int(round(1e-3 / (t[1] - t[0])))
    iq1 = np.abs(d["iq"][:len(d["iq"]) // n1 * n1].reshape(-1, n1).mean(axis=1))
    t1 = t[:len(iq1) * n1:n1]
    return rms, a10, float(iq1[t1 >= 2.0].max())

M = {k: metrics(D[k]) for k in Q}

fig = plt.figure(figsize=(12.8, 6.4))
gs = fig.add_gridspec(3, 3, left=0.06, right=0.99, top=0.850, bottom=0.09, wspace=0.26, hspace=0.52)
a1 = fig.add_subplot(gs[0, :]); a2 = fig.add_subplot(gs[1, 0]); a3 = fig.add_subplot(gs[1, 1])
a4 = fig.add_subplot(gs[2, 0]); a5 = fig.add_subplot(gs[2, 1]); a6 = fig.add_subplot(gs[2, 2])

for k in Q:
    d = D[k]; n = int(T1 / 1e-5)
    a1.plot(d["t"][:n:1000], 600 + (d["y"][:n:1000] - 1.0) * 600.0, color=C[k], lw=0.6, label=LAB[k])
a1.set_xlim(0, T1); a1.set_ylim(430, 800)
a1.set_xlabel("时间 / s"); a1.set_ylabel("转速 / rpm")
a1.set_title("(a) 0–9 s 完整转速（2 s 加载 0.50 额定 + 组合故障；$J_{true}$=5.26$J_{nom}$）", fontsize=8.6)
a1.legend(fontsize=6.8, ncol=4, loc="upper right")

rms = [M[k][0] for k in Q]; a10 = [M[k][1] for k in Q]
x = np.arange(4); cols = [C[k] for k in Q]
a2.bar(x, rms, color=cols, width=0.55)
for i, v in enumerate(rms):
    a2.text(i, v + 0.6, "%.1f" % v, ha="center", fontsize=6.8)
a2.set_xticks(x); a2.set_xticklabels(["无律", "仅T", "仅J", "融合"], fontsize=7.2)
a2.set_ylim(0, max(rms) * 1.2); a2.set_ylabel("稳态 RMS / rpm")
a2.set_title("(b) 稳态 RMS（6–9 s）", fontsize=8.4)

a3.bar(x, a10, color=cols, width=0.55)
for i, v in enumerate(a10):
    a3.text(i, v + 0.6, "%.1f" % v, ha="center", fontsize=6.8)
a3.set_xticks(x); a3.set_xticklabels(["无律", "仅T", "仅J", "融合"], fontsize=7.2)
a3.set_ylim(0, max(a10) * 1.2); a3.set_ylabel("10 Hz / rpm")
a3.set_title("(c) 10 Hz 残余（6–9 s）", fontsize=8.4)

n1 = 100; nb = 50
for k in Q:
    d = D[k]; n = int(T1 / 1e-5)
    av = np.abs(d["iq"][:n // n1 * n1]).reshape(-1, n1).mean(axis=1)
    av2 = np.array([av[i:i + nb].max() for i in range(0, len(av) - nb, nb)])
    tt = d["t"][:len(av2) * nb * n1:nb * n1] + 25e-3
    a4.plot(tt, av2, color=C[k], lw=0.9, label=LAB[k])
a4.axhline(6.31, color="#c0392b", ls="--", lw=0.8)
a4.text(0.25, 6.42, "额定 6.31", color="#c0392b", fontsize=6.4)
a4.set_xlim(0, T1); a4.set_ylim(0, 9.2)
a4.set_ylabel("$|\\overline{i_q}|$（1 ms） / A"); a4.set_xlabel("时间 / s")
a4.set_title("(d) 电流包络（律J 在 1 s 注入 0.6 s dither）", fontsize=8.4)
a4.legend(fontsize=5.6, ncol=2, loc="upper right")

for k in ("t", "fusion"):
    d = D[k]
    dhat = np.array(d["es"], dtype=float)
    m = d["t"] >= ES_T0                       # t<3 s 没有叠加 dither，不能减
    dhat[m] = dhat[m] - ES_DITH * np.sin(2 * np.pi * (d["t"][m] - ES_T0) / ES_PD)
    a5.plot(d["t"][::500], dhat[::500] * 100.0, color=C[k], lw=0.9, label=LAB[k])
a5.axhline(-14.3, color="#2c3e50", ls=":", lw=0.9)
a5.text(24.0, -14.45, "理论 δ*=−14.3%", fontsize=6.0, color="#2c3e50", ha="right", va="top")
a5.set_xlim(0, TEND); a5.set_ylim(-15.6, -10.6)
a5.set_ylabel("$\\hat{\\delta}$ / %"); a5.set_xlabel("时间 / s")
a5.set_title("(e) 律T 的 $\\hat{\\delta}$：0–30 s（是否收敛）", fontsize=8.4)
a5.legend(fontsize=5.8, ncol=1, loc="upper left")

for k in Q:
    d = D[k]; m = d["t_j"] <= T1
    a6.plot(d["t_j"][m], d["b0"][m], color=C[k], lw=0.9, label=LAB[k])
a6.axhline(122.3, color="#2c3e50", ls=":", lw=0.9)
a6.text(0.4, 133, "真值 122.3", fontsize=6.2, color="#2c3e50")
a6.set_xlim(0, T1); a6.set_ylim(60, 700)
a6.set_ylabel("$b_0$ / s$^{-1}$"); a6.set_xlabel("时间 / s")
a6.set_title("(f) 律J 的 b0（α=1 一步到位，τ=kp/10）", fontsize=8.4)
a6.legend(fontsize=5.6, ncol=2, loc="center right", bbox_to_anchor=(0.98, 0.62))

fig.suptitle("律T（DFT 连续滑动窗）× 律J（α=1、b0 低通 kp/10）融合 vs 单一律 vs 无律"
             "（600 rpm、30 s 仿真；(a)–(d)(f) 截 0–9 s，(e) 全 30 s）", fontsize=9.2, y=0.962)
fig.savefig("fig_tj_fusion.png", dpi=150, bbox_inches=None, facecolor="white")
print("RMS ", dict(zip(Q, [round(v, 2) for v in rms])))
print("10Hz", dict(zip(Q, [round(v, 2) for v in a10])))
print("iq  ", dict(zip(Q, [round(M[k][2], 2) for k in Q])))
