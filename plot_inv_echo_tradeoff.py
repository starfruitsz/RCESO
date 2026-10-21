# -*- coding: utf-8 -*-
"""回声的两个指标：10 Hz 残余 vs 6.0–6.1 s 峰值（种子 018）
说明 FA 立即：10 Hz 更低但复位尖峰更大；律 D 反之。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.0,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

D = {k: np.load("_wave_%s.npz" % k) for k in ["Base", "LawD", "FB", "FA"]}
t = D["Base"]["t"]
N = 600.0
LABEL = {"Base": "无律", "LawD": "律 D", "FB": "新 F-B", "FA": "F-A 立即"}
COLOR = {"Base": "#3a3a3a", "LawD": "#c0392b", "FB": "#16a085", "FA": "#2471a3"}
ORDER = ["Base", "LawD", "FB", "FA"]

# 6.0–6.1 s：10 Hz 幅值 + 峰值
m = (t >= 6.0) & (t < 6.1)
amp, peak = {}, {}
for k in ORDER:
    e = (D[k]["y"][m] - 1.0) * N
    amp[k] = np.hypot(2 * np.mean(e * np.cos(2 * np.pi * t[m] / 0.1)),
                      2 * np.mean(e * np.sin(2 * np.pi * t[m] / 0.1)))
    peak[k] = np.abs(e).max()

fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.5))
x = np.arange(4)
for col, (vals, title, ylab) in enumerate([
        (amp, "(a) 首周期 10 Hz 残余：越小越好", "10 Hz 幅值 (rpm)"),
        (peak, "(b) 6.0–6.1 s 峰值：越小越平滑", "峰值 |e| (rpm)")]):
    for i, k in enumerate(ORDER):
        ax[col].bar(i, vals[k], 0.6, color=COLOR[k])
        ax[col].text(i, vals[k] + (0.8 if col == 0 else 1.5), "%.1f" % vals[k],
                     ha="center", fontsize=7.6)
    ax[col].set_xticks(x); ax[col].set_xticklabels([LABEL[k] for k in ORDER], fontsize=7.8)
    ax[col].set_ylabel(ylab); ax[col].set_title(title, fontsize=9.0)
    ax[col].grid(alpha=0.22, axis="y")
ax[0].set_ylim(0, 44); ax[1].set_ylim(0, 140)

fig.text(0.5, 0.01, "种子 018：F-A 立即在 (a) 最好、(b) 最差；律 D 在 (b) 更平滑、在 (a) 更差",
         ha="center", fontsize=7.6, color="#555")
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("fig_inv_echo_tradeoff.png", dpi=200)
print("ok")
print("amp10", {k: round(amp[k], 1) for k in ORDER})
print("peak", {k: round(peak[k], 1) for k in ORDER})
