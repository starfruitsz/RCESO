# -*- coding: utf-8 -*-
"""plot_j_adapt.py —— J 自适应：辨识收敛、10 Hz 抑制、注入代价、时域对比"""
import json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JM, JB = 1.89e-5, 9.95e-5
C_BASE, C_FAULT, C_ORACLE, C_ADAPT = "#1f4e79", "#c0392b", "#e67e22", "#16a085"

A = json.load(open("_j_adapt.json", encoding="utf-8"))
C = json.load(open("_j_comm.json", encoding="utf-8"))
D = {k: np.load("_wave_j_%s.npz" % k) for k in ("big_fault", "big_oracle", "big_comm")}

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8,
})

fig, ax = plt.subplots(2, 2, figsize=(12.8, 6.4))
fig.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.10, hspace=0.42, wspace=0.24)

# (a) jhat
d = D["big_comm"]; tj, jh = d["t_j"], d["jhat"]
ax[0, 0].plot(tj, jh * 1e6, color=C_ADAPT, lw=1.6, label=r"$\hat J$（在线辨识）")
ax[0, 0].axhline(JB * 1e6, color="#555", ls="--", lw=1.0, label=r"$J_{\rm true}=99.5$")
ax[0, 0].axhspan(JB * 0.9e6, JB * 1.1e6, color=C_ADAPT, alpha=0.10, label="±10%")
ax[0, 0].axvline(2.0, color=C_ORACLE, ls=":", lw=1.0)
ax[0, 0].text(2.08, 60, "2 s 冻结、关闭 dither", color=C_ORACLE, fontsize=7.5)
ax[0, 0].set_xlabel("时间 / s"); ax[0, 0].set_ylabel(r"$\hat J$ / ($10^{-6}$ kg·m²)")
ax[0, 0].set_title("(a) 辨识收敛（0–2 s 注入 100 Hz dither）", fontsize=9, pad=4)
ax[0, 0].legend(loc="lower right")

# (b) 10 Hz bars
labels = ["标称 J\n(基准)", "J_true=5.3J\n固定", "oracle\n重整定", "辨识+b0\n自适应"]
vals = [A["Jm_fault"]["amp10"], C["big_fault"]["a10"], C["big_oracle"]["a10"], C["big_comm"]["a10"]]
cols = [C_BASE, C_FAULT, C_ORACLE, C_ADAPT]
bars = ax[0, 1].bar(labels, vals, color=cols, width=0.6)
for b, v in zip(bars, vals):
    ax[0, 1].text(b.get_x() + b.get_width()/2, v + 0.8, "%.1f" % v, ha="center", fontsize=8)
ax[0, 1].set_ylabel("10 Hz 转速分量 / rpm")
ax[0, 1].set_title("(b) 故障抑制：10 Hz 纹波（T1=0.057 N·m）", fontsize=9, pad=4)

# (c) dither cost
bars = ax[1, 0].bar(["调试期 0.5–2 s", "运行段 9–10 s"],
                    [C["big_comm"]["a100_id"], C["big_comm"]["a100_post"]],
                    color=[C_ADAPT, C_BASE], width=0.5)
for b, v in zip(bars, [C["big_comm"]["a100_id"], C["big_comm"]["a100_post"]]):
    ax[1, 0].text(b.get_x() + b.get_width()/2, v + 0.5, "%.2f" % v, ha="center", fontsize=8)
ax[1, 0].set_ylabel("100 Hz 转速分量 / rpm")
ax[1, 0].set_title("(c) 注入代价：仅调试期存在", fontsize=9, pad=4)

# (d) time domain 9-10 s
for k, c, lab in (("big_fault", C_FAULT, "固定标称"), ("big_oracle", C_ORACLE, "oracle 重整定"),
                  ("big_comm", C_ADAPT, "辨识+b0 自适应")):
    d = D[k]; tt = d["t"]; e = (d["y"] - 1.0) * 600
    m = (tt >= 9.0) & (tt <= 10.0)
    ax[1, 1].plot(tt[m], e[m], color=c, lw=1.0, label=lab)
ax[1, 1].set_xlabel("时间 / s"); ax[1, 1].set_ylabel("转速误差 / rpm")
ax[1, 1].set_title("(d) 稳态 9–10 s 时域对比", fontsize=9, pad=4)
ax[1, 1].legend(loc="upper right", ncol=1)

fig.suptitle("真实 J 失配下的 J 辨识与 b0 自适应（600 rpm、T1=0.057 N·m、J_true=5.3 J_nom）", fontsize=10.5)
fig.savefig("fig_j_adapt.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok")
