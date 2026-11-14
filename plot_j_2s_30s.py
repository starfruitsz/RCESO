# -*- coding: utf-8 -*-
"""plot_j_2s_30s.py —— 2 s 周期 + 每 burst 状态4 的 30 s 复核"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JM, JB = 1.89e-5, 9.95e-5
B0 = {500: 772.4, 600: 643.7, 1000: 386.2}
C = {500: "#1f4e79", 600: "#16a085", 1000: "#c0392b"}
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.0, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.0,
})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.33, 5.4))
fig.subplots_adjust(left=0.065, right=0.985, top=0.84, bottom=0.13, wspace=0.22)

for n, f in ((500, "_wave_j_2s_500.npz"), (600, "_wave_j_2s_600.npz"), (1000, "_wave_j_2s_1000_amp.npz")):
    z = np.load(f); t = z["t_j"]; jh = np.asarray(z["jhat"]) * 1e6; b0 = np.asarray(z["b0e"])
    ax1.plot(t, jh, color=C[n], lw=1.3, label="%d rpm" % n)
    ax2.plot(t, b0, color=C[n], lw=1.3, label="%d rpm" % n)
    ax2.axhline(B0[n] * JM / JB, color=C[n], ls="--", lw=0.8, alpha=0.7)
ax1.axhline(JB * 1e6, color="#555", ls="--", lw=0.9, label=r"$J_{\rm true}=99.5$")
ax1.set_xlim(0, 30); ax1.set_ylim(0, 140)
ax1.set_xlabel("时间 / s"); ax1.set_ylabel(r"$\hat J$ / ($10^{-6}$ kg·m$^2$)")
ax1.set_title("(a) $\\hat J$：500/600 rpm 稳定，1000 rpm 漂到 +19%", fontsize=10.0, pad=5)
ax1.legend(loc="lower right", fontsize=7.6)

ax2.set_xlim(0, 30); ax2.set_ylim(0, 820)
ax2.set_xlabel("时间 / s"); ax2.set_ylabel(r"$b_0^{\rm e}$ / s$^{-1}$")
ax2.set_title("(b) $b_0$ 收敛到“估计目标”（虚线为真实 J 对应目标）", fontsize=9.8, pad=5)
ax2.legend(loc="upper right", fontsize=7.6)

fig.suptitle("2 s 复检周期 + 每 burst 状态 4 校验：500/600 rpm 收敛；1000 rpm 仍有 +19% 偏差（600 rpm 口径，30 s）",
             fontsize=10.4, y=0.95)
fig.savefig("fig_j_2s_30s.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok")
