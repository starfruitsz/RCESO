# -*- coding: utf-8 -*-
"""plot_j_ako_long.py —— AKO+RLS 30 s 长时：收敛/极限环判定"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JM, JB = 1.89e-5, 9.95e-5
C_AKO, C_COMM, C_FIX = "#8e44ad", "#16a085", "#c0392b"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.0,
})
Z = np.load("_wave_j_ako_long.npz")
tj = Z["t_j"]; jh = np.asarray(Z["jhat"]); tc = Z["tc"]; a10 = Z["a10"]
J = json.load(open("_j_ako_long.json"))

fig = plt.figure(figsize=(13.33, 6.67))
gs = fig.add_gridspec(2, 2, left=0.065, right=0.985, top=0.865, bottom=0.10, hspace=0.40, wspace=0.22)
axa = fig.add_subplot(gs[0, :]); axb = fig.add_subplot(gs[1, 0]); axc = fig.add_subplot(gs[1, 1])

# (a) jhat long
axa.plot(tj, jh*1e6, color=C_AKO, lw=1.2)
axa.axhline(JB*1e6, color="#555", ls="--", lw=0.9, label=r"$J_{\rm true}=99.5$")
axa.axhspan(JB*0.9e6, JB*1.1e6, color=C_COMM, alpha=0.08, label="±10%")
axa.axvline(10.0, color="#999", ls=":", lw=0.9)
axa.text(10.2, 110, "10 s", fontsize=7.4, color="#666")
axa.set_xlim(0, 30); axa.set_ylim(0, 125)
axa.set_xlabel("时间 / s"); axa.set_ylabel(r"$\hat J$ / ($10^{-6}$ kg·m$^2$)")
axa.set_title("(a) 30 s 长时：$\\hat J$ 不收敛（min %.1f / max %.1f / 终值 %.1f）" % (J["jmin"]*1e6, J["jmax"]*1e6, J["jfin"]*1e6), fontsize=10.0, pad=5)
axa.legend(loc="upper right", fontsize=7.8)

# (b) a10 sliding
axb.plot(tc, a10, color=C_AKO, lw=1.4, marker="o", ms=2.5)
axb.axhline(33.3, color=C_FIX, ls="--", lw=0.9, label="固定 b0 33.3")
axb.axhline(4.0, color=C_COMM, ls="--", lw=0.9, label="DFT 4.0")
axb.set_xlim(0, 30); axb.set_ylim(0, 55)
axb.set_xlabel("时间 / s"); axb.set_ylabel("10 Hz 分量（1 s 窗）/ rpm")
axb.set_title("(b) 10 Hz 从 13 漂到 51：不是稳定极限环", fontsize=9.8, pad=5)
axb.legend(loc="upper left", fontsize=7.4)
axb.annotate("13.1 @5 s", xy=(5, 13.1), xytext=(7.5, 6), fontsize=7.0, color=C_AKO,
             arrowprops=dict(arrowstyle="->", color=C_AKO, lw=0.7))
axb.annotate("50.9 @29.5 s", xy=(29.5, 50.9), xytext=(20, 44), fontsize=7.0, color=C_AKO,
             arrowprops=dict(arrowstyle="->", color=C_AKO, lw=0.7))

# (c) phase portrait a10 vs jhat
j_at_tc = np.interp(tc, tj, jh) * 1e6
sc = axc.scatter(j_at_tc, a10, c=tc, cmap="viridis", s=16, zorder=3)
axc.plot(j_at_tc, a10, color="#aaa", lw=0.7, zorder=2)
axc.scatter([j_at_tc[0]], [a10[0]], color=C_FIX, s=40, marker="s", zorder=4, label="起点")
axc.scatter([j_at_tc[-1]], [a10[-1]], color=C_AKO, s=40, marker="*", zorder=4, label="终点")
axc.set_xlabel(r"$\hat J$ / ($10^{-6}$ kg·m$^2$)"); axc.set_ylabel("10 Hz / rpm")
axc.set_title("(c) 相图：轨迹缓慢外扩，非闭合环", fontsize=9.8, pad=5)
axc.legend(loc="upper right", fontsize=7.4)
cb = fig.colorbar(sc, ax=axc, pad=0.02); cb.set_label("时间 / s", fontsize=7.6)
cb.ax.tick_params(labelsize=7)

fig.suptitle("Yang 2018 AKO+RLS 长时试跑（30 s）：不收敛、也不是稳定极限环；10 s 短跑的低点只是暂态（600 rpm、$J_{\\rm true}=5.26J_{\\rm nom}$）",
             fontsize=10.4, y=0.965)
fig.text(0.065, 0.012, "数据：pmsm_inv_sim.py；同一 10 s 配置延长到 30 s；AKO 3 状态 KF + a1/b1 RLS，Q/R 取论文值、λ=0.99、B=0。",
         fontsize=6.8, color="#666")
fig.savefig("fig_j_ako_long.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok")
