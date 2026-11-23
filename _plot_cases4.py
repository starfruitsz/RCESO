# -*- coding: utf-8 -*-
"""_plot_cases4.py —— 四工况对照：对照组 / 负载突变 / b0 严重失配 / T 失配。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = dict(ctrl="#7f8c8d", load="#e67e22", b0="#c0392b", tm="#1f4e79")
LAB = dict(ctrl="对照组（恒载、恒 600）", load="负载突变（2 s 阶跃）",
           b0="b0 严重失配（J=5.26J$_{nom}$）", tm="T 失配（6 s 换速）")
LS = dict(ctrl="-", load="-", b0="--", tm=":")

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.4,
})

def load(c):
    z = np.load("_c4_%s.npz" % c)
    t = np.asarray(z["t"]); dec = max(1, int(round(1e-5 / (t[1] - t[0]))))
    return dict(t=t[::dec], y=np.asarray(z["y"])[::dec] * 600.0,
                tl=np.asarray(z["tl"])[::dec], iq=np.asarray(z["iq"])[::dec])

D = {c: load(c) for c in ("ctrl", "load", "b0", "tm")}

fig, ax = plt.subplots(2, 2, figsize=(12.8, 6.4))
fig.subplots_adjust(left=0.07, right=0.99, top=0.86, bottom=0.10, wspace=0.22, hspace=0.40)

for c in ("ctrl", "load", "b0", "tm"):
    ax[0, 0].plot(D[c]["t"], D[c]["tl"], color=C[c], lw=(1.3 if c == "ctrl" else 1.0),
                  ls=LS[c], label=LAB[c])
ax[0, 0].set_xlim(0, 8); ax[0, 0].set_ylim(-0.03, 0.62)
ax[0, 0].set_ylabel("$T_L$ / N·m"); ax[0, 0].set_title("(a) 四工况负载", fontsize=8.8)
ax[0, 0].legend(fontsize=6.6, loc="upper left")

for c in ("ctrl", "load", "b0", "tm"):
    ax[0, 1].plot(D[c]["t"], D[c]["y"], color=C[c], lw=0.7, label=LAB[c])
ax[0, 1].axhline(600, color="#888", ls=":", lw=0.8)
ax[0, 1].axvline(2.0, color="#888", ls="--", lw=0.7, alpha=0.7)
ax[0, 1].axvline(6.0, color="#888", ls="--", lw=0.7, alpha=0.7)
ax[0, 1].text(2.05, 748, "2 s 加载", fontsize=6.4, color="#555")
ax[0, 1].text(6.05, 748, "6 s 换速", fontsize=6.4, color="#555")
ax[0, 1].set_xlim(0, 8); ax[0, 1].set_ylim(150, 760)
ax[0, 1].set_ylabel("转速 / rpm"); ax[0, 1].set_title("(b) 全程转速", fontsize=8.8)
ax[0, 1].legend(fontsize=6.4, loc="lower left", ncol=1)

for c in ("ctrl", "load", "b0", "tm"):
    d = D[c]; m = (d["t"] >= 1.9) & (d["t"] <= 2.5)
    ax[1, 0].plot(d["t"][m], d["y"][m] - 600.0, color=C[c], lw=0.9, label=LAB[c])
ax[1, 0].set_xlim(1.9, 2.5); ax[1, 0].set_ylim(-520, 160)
ax[1, 0].set_ylabel("转速误差 / rpm"); ax[1, 0].set_title("(c) 加载窗 1.9–2.5 s", fontsize=8.8)
ax[1, 0].legend(fontsize=6.2, loc="lower right")

for c in ("ctrl", "load", "b0", "tm"):
    d = D[c]; m = (d["t"] >= 5.8) & (d["t"] <= 6.4)
    ax[1, 1].plot(d["t"][m], d["y"][m], color=C[c], lw=0.9, label=LAB[c])
ax[1, 1].set_xlim(5.8, 6.4); ax[1, 1].set_ylim(150, 760)
ax[1, 1].set_ylabel("转速 / rpm"); ax[1, 1].set_title("(d) 换速窗 5.8–6.4 s", fontsize=8.8)
ax[1, 1].legend(fontsize=6.2, loc="lower left")

fig.suptitle("四工况对照：对照组 / 负载突变 / b0 严重失配 / T 失配（600 rpm；不对中 β=1° + 圆盘不平衡）",
             fontsize=9.8, y=0.965)
fig.savefig("ppt_s8_4cases.png", dpi=150, bbox_inches=None, facecolor="white")
print("saved ppt_s8_4cases.png")

# 关键指标
for c in ("ctrl", "load", "b0", "tm"):
    d = D[c]; t = d["t"]; e = d["y"] - 600
    m = (t >= 1.9) & (t <= 2.5)
    s = (t >= 6.2) & (t <= 6.4)
    print("%-5s 加载跌落 %6.0f rpm | 6.2–6.4 s 均值 %6.0f rpm | 全程 RMS %5.1f rpm" % (
        c, e[m].min(), e[s].mean(), float(np.sqrt(np.mean(e[t >= 5] ** 2)))))
