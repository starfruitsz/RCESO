# -*- coding: utf-8 -*-
"""plot_j_law_compare_qual.py —— J 自适应律定性对比（雷达 + 加权总分）
说明：评分依据文献路线与实现复杂度，非闭环仿真；闭环数据对比需在 pmsm_inv_sim 中实现各律后另出。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

labels = ["实时性", "负载转矩解耦", "噪声鲁棒性", "无需额外激励", "实现简单"]
methods = ["DFT 调试期辨识", "RLS（AKO+RLS）", "MRAS", "ESO/DO 观测器"]
scores = np.array([
    [1, 2, 3, 2, 5],   # DFT commissioning
    [5, 4, 3, 4, 3],   # RLS
    [5, 3, 3, 4, 4],   # MRAS
    [5, 3, 4, 5, 2],   # ESO/DO
], dtype=float)
weights = np.array([0.25, 0.25, 0.20, 0.15, 0.15])
total = scores @ weights
colors = ["#1f4e79", "#16a085", "#e67e22", "#c0392b"]

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.5, "figure.dpi": 150,
})
fig = plt.figure(figsize=(12.8, 6.0))
ax1 = fig.add_subplot(1, 2, 1, polar=True)
ax2 = fig.add_subplot(1, 2, 2)

N = len(labels)
ang = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
ang += ang[:1]
for i, (m, c) in enumerate(zip(methods, colors)):
    vals = scores[i].tolist(); vals += vals[:1]
    ax1.plot(ang, vals, color=c, lw=1.6, label=m)
    ax1.fill(ang, vals, color=c, alpha=0.06)
ax1.set_xticks(ang[:-1]); ax1.set_xticklabels(labels, fontsize=9)
ax1.set_ylim(0, 5); ax1.set_yticks([1, 2, 3, 4, 5]); ax1.set_yticklabels(["1","2","3","4","5"], fontsize=7, color="#888")
ax1.set_title("(a) 五维定性评分（1–5，越高越好）", fontsize=10.5, pad=16)
ax1.legend(loc="upper right", bbox_to_anchor=(1.18, 1.10), fontsize=8.2)
ax1.grid(alpha=0.25)

order = np.argsort(total)
bars = ax2.barh(range(len(methods)), total[order], color=[colors[i] for i in order], height=0.55)
for b, v in zip(bars, total[order]):
    ax2.text(v + 0.05, b.get_y() + b.get_height()/2, "%.2f" % v, va="center", fontsize=8.5)
ax2.set_yticks(range(len(methods))); ax2.set_yticklabels([methods[i] for i in order], fontsize=8.8)
ax2.set_xlim(0, 4.6); ax2.set_xlabel("加权总分（权重：实时 .25 / 解耦 .25 / 噪声 .20 / 无激励 .15 / 简单 .15）", fontsize=8.4)
ax2.set_title("(b) 加权总分：RLS 略优", fontsize=10.5, pad=8)
ax2.grid(axis="x", alpha=0.2)
for s in ["top","right"]: ax2.spines[s].set_visible(False)

fig.suptitle("J 自适应律定性对比（依据文献路线与实现复杂度；非闭环仿真）", fontsize=11.5, y=0.98)
fig.text(0.5, 0.015, "注：闭环数据对比需在 pmsm_inv_sim 中实现 RLS/MRAS/ESO 后另出；本图只用于选型讨论。", ha="center", fontsize=7.2, color="#666")
fig.subplots_adjust(left=0.06, right=0.98, top=0.86, bottom=0.10, wspace=0.28)
fig.savefig("fig_j_law_compare_qual.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok", total.tolist())
