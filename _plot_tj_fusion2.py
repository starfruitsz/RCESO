# -*- coding: utf-8 -*-
"""_plot_tj_fusion2.py —— 新配置（10 s burst、直测 b0、校验关）：四模式对比，六面板。"""
import numpy as np, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = {"base10": "#1f4e79", "t10": "#e67e22", "j10d": "#8e44ad", "f10d": "#1e8449"}
LAB = {"base10": "无律", "t10": "仅律T（DFT）", "j10d": "仅律J（10 s，直测 b0）", "f10d": "律T+律J 融合"}
Q = ["base10", "t10", "j10d", "f10d"]

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.4, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.2,
})

def load(f):
    z = np.load(f)
    t = np.asarray(z["t"]); dec = max(1, int(round(1e-3 / (t[1] - t[0]))))
    return dict(t=t[::dec], y=np.asarray(z["y"])[::dec], iq=np.asarray(z["iq"])[::dec],
                b0=np.asarray(z["b0e"]), t_j=np.asarray(z["t_j"]))

def amp10(t, e, f=10.0, a=None, b=None):
    m = (t >= a) & (t < b)
    tt, ee = t[m], e[m]; w = 2 * np.pi * f
    return float(np.hypot(2 * np.mean(ee * np.cos(w * tt)), 2 * np.mean(ee * np.sin(w * tt))))

D = {k: load("_tj_%s.npz" % k) for k in Q}
J = {k: json.load(open("_tj_%s.json" % k)) for k in Q}

fig = plt.figure(figsize=(12.8, 6.4))
gs = fig.add_gridspec(3, 3, left=0.06, right=0.99, top=0.86, bottom=0.09, wspace=0.26, hspace=0.50)
a1 = fig.add_subplot(gs[0, :]); a2 = fig.add_subplot(gs[1, 0]); a3 = fig.add_subplot(gs[1, 1])
a4 = fig.add_subplot(gs[2, 0]); a5 = fig.add_subplot(gs[2, 1]); a6 = fig.add_subplot(gs[2, 2])

E = {}
for k in Q:
    d = D[k]; E[k] = (d["y"] - 1.0) * 600.0
    a1.plot(d["t"], 600 + E[k], color=C[k], lw=0.6, label=LAB[k])
a1.set_xlim(0, 30); a1.set_ylim(430, 800)
a1.set_xlabel("时间 / s"); a1.set_ylabel("转速 / rpm")
a1.set_title("(a) 30 s 完整转速（2 s 加载 0.50 额定 + 组合故障；$J_{true}$=5.26$J_{nom}$）", fontsize=8.6)
a1.legend(fontsize=6.8, ncol=4, loc="upper right")

rms = [J[k]["rms"] for k in Q]; a10 = [J[k]["amp10"] for k in Q]
x = np.arange(4); cols = [C[k] for k in Q]
a2.bar(x, rms, color=cols, width=0.55)
for i, v in enumerate(rms):
    a2.text(i, v + 0.6, "%.1f" % v, ha="center", fontsize=6.8)
a2.set_xticks(x); a2.set_xticklabels(["无律", "仅T", "仅J", "融合"], fontsize=7.2)
a2.set_ylim(0, max(rms) * 1.2); a2.set_ylabel("稳态 RMS / rpm")
a2.set_title("(b) 稳态 RMS", fontsize=8.4)

a3.bar(x, a10, color=cols, width=0.55)
for i, v in enumerate(a10):
    a3.text(i, v + 0.6, "%.1f" % v, ha="center", fontsize=6.8)
a3.set_xticks(x); a3.set_xticklabels(["无律", "仅T", "仅J", "融合"], fontsize=7.2)
a3.set_ylim(0, max(a10) * 1.2); a3.set_ylabel("10 Hz / rpm")
a3.set_title("(c) 10 Hz 残余", fontsize=8.4)

n1 = int(round(1e-3 / (D["base10"]["t"][1] - D["base10"]["t"][0])))
for k in Q:
    d = D[k]; a = np.abs(d["iq"])
    av = a[:len(a)//n1*n1].reshape(-1, n1).mean(axis=1)
    nb = 50
    av2 = np.array([av[i:i+nb].max() for i in range(0, len(av)-nb, nb)])
    tt = d["t"][:len(av2)*nb*n1:nb*n1] + 25e-3
    a4.plot(tt, av2, color=C[k], lw=0.9, label=LAB[k])
a4.axhline(6.31, color="#c0392b", ls="--", lw=0.8)
a4.text(0.4, 6.45, "额定 6.31", color="#c0392b", fontsize=6.6)
a4.set_xlim(0, 30); a4.set_ylim(0, 9.2)
a4.set_ylabel("$|\\overline{i_q}|$（1 ms） / A"); a4.set_xlabel("时间 / s")
a4.set_title("(d) 电流包络（律J 每 10 s 注入 0.6 s dither）", fontsize=8.4)
a4.legend(fontsize=5.6, ncol=2, loc="upper right")

for k in ("t10", "f10d"):
    d = D[k]
    a5.plot(d["t"], np.asarray(np.load("_tj_%s.npz" % k)["es"])[::100] * 100.0, color=C[k], lw=0.9, label=LAB[k])
a5.axhline(-14.3, color="#2c3e50", ls=":", lw=0.9)
a5.text(0.5, -14.05, "理论 δ*=−14.3%", fontsize=6.2, color="#2c3e50", va="bottom")
a5.set_xlim(0, 30); a5.set_ylim(-22, -8); a5.set_ylabel("δ / %"); a5.set_xlabel("时间 / s")
a5.set_title("(e) 律T 的 δ 收敛（仅 T / 融合）", fontsize=8.4)
a5.legend(fontsize=6.2, ncol=2, loc="lower left")

for k in Q:
    d = D[k]
    a6.plot(d["t_j"], d["b0"], color=C[k], lw=0.8, label=LAB[k])
a6.axhline(122.3, color="#2c3e50", ls=":", lw=0.9)
a6.text(0.6, 132, "真值 122.3", fontsize=6.2, color="#2c3e50")
a6.set_xlim(0, 30); a6.set_ylim(80, 700)
a6.set_ylabel("$b_0$ / s$^{-1}$"); a6.set_xlabel("时间 / s")
a6.set_title("(f) 律J 的 b0 自适应", fontsize=8.4)
a6.legend(fontsize=5.8, ncol=2, loc="center right")

fig.suptitle("律T（DFT）× 律J 融合 vs 单一律 vs 无律（600 rpm、30 s、burst 10 s、直测 b0、校验关、$J_{true}$=5.26$J_{nom}$）",
             fontsize=9.4, y=0.965)
fig.savefig("fig_tj_fusion.png", dpi=150, bbox_inches=None, facecolor="white")
print("RMS ", dict(zip(Q, [round(v, 2) for v in rms])))
print("10Hz", dict(zip(Q, [round(v, 2) for v in a10])))
print("b0  ", dict(zip(Q, [round(J[k]['b0e'], 1) for k in Q])))
