# -*- coding: utf-8 -*-
"""画 F-B 辅助判据对比：_fb_gate.json → fig_fb_gate.png
用法：python plot_fb_gate.py
"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.5,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

d = json.load(open("_fb_gate.json", encoding="utf-8"))
ORDER = ["Base", "FB_e1", "FB_et_g", "FB_et_ga", "FB_et_gav"]
LABEL = {"Base": "无自适应", "FB_e1": "F-B（e1 残差）",
         "FB_et_g": "F-B（跟踪误差+g）",
         "FB_et_ga": "F-B（+绝对下限）",
         "FB_et_gav": "F-B（+下限+|v|门控）"}
COLOR = {"Base": "#3a3a3a", "FB_e1": "#c0392b",
         "FB_et_g": "#2980b9", "FB_et_ga": "#8e44ad",
         "FB_et_gav": "#16a085"}

seeds = [r["seed"] for r in d["Base"]]
fig, ax = plt.subplots(1, 3, figsize=(11.4, 3.5),
                       gridspec_kw={"width_ratios": [1.65, 1.0, 1.0]})

# (a) 逐种子
x = np.arange(len(seeds))
w = 0.16
for j, nm in enumerate(ORDER):
    v = [r["a_echo"] for r in d[nm]]
    ax[0].bar(x + (j - 2.0) * w, v, w, color=COLOR[nm], label=LABEL[nm])
ax[0].set_xticks(x)
ax[0].set_xticklabels([str(s)[-2:] for s in seeds], fontsize=8)
ax[0].set_xlabel("种子（后两位）")
ax[0].set_ylabel("首周期 10 Hz 回声 (rpm)")
ax[0].set_title("(a) 逐种子：e1 残差判据双峰，跟踪误差判据收敛", fontsize=9.4)
ax[0].legend(fontsize=7.2, ncol=2, loc="upper left")
ax[0].grid(alpha=0.22, axis="y")

# (b) 均值±标准差
means = []
stds = []
for nm in ORDER:
    v = np.array([r["a_echo"] for r in d[nm]])
    means.append(v.mean())
    stds.append(v.std(ddof=1))
xx = np.arange(len(ORDER))
ax[1].bar(xx, means, 0.62, color=[COLOR[n] for n in ORDER],
          yerr=stds, capsize=4, error_kw={"lw": 1.0, "ecolor": "#333"})
for i, (m, s) in enumerate(zip(means, stds)):
    ax[1].text(i, m + s + 1.2, "%.1f\n±%.1f" % (m, s),
               ha="center", fontsize=7.6)
ax[1].set_xticks(xx)
ax[1].set_xticklabels([LABEL[n] for n in ORDER], rotation=18, fontsize=7.4)
ax[1].set_ylabel("首周期 10 Hz 回声 (rpm)")
ax[1].set_title("(b) 均值±标准差（8 种子）", fontsize=9.4)
ax[1].set_ylim(0, max(means) + max(stds) + 18)
ax[1].grid(alpha=0.22, axis="y")

# (c) 跌落与稳态：确认辅助判据不劣化
for j, nm in enumerate(ORDER):
    dip = np.mean([r["dip"] for r in d[nm]])
    st = np.mean([r["steady"] for r in d[nm]])
    ax[2].bar(j - 0.18, abs(dip), 0.34, color=COLOR[nm], alpha=0.9)
    ax[2].bar(j + 0.18, st, 0.34, color=COLOR[nm], alpha=0.45, hatch="//")
ax[2].set_xticks(xx)
ax[2].set_xticklabels([LABEL[n] for n in ORDER], rotation=18, fontsize=7.4)
ax[2].set_ylabel("rpm")
ax[2].set_title("(c) 加载跌落（实心）/ 稳态（斜纹）", fontsize=9.4)
ax[2].grid(alpha=0.22, axis="y")

fig.tight_layout()
fig.savefig("fig_fb_gate.png", dpi=200)
print("ok: fig_fb_gate.png")
