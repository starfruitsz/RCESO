# -*- coding: utf-8 -*-
"""记忆失配 F-B 的 8 种子结果图：_inv_mism.json + _inv_mism_g.json → fig_inv_mism.png"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

a = json.load(open("_inv_mism.json", encoding="utf-8"))
b = json.load(open("_inv_mism_g.json", encoding="utf-8"))
ORDER = ["Base", "LawD", "FB_mism_g", "D+FB_mism_g"]
ROWS = {"Base": a["Base"], "LawD": a["LawD"],
        "FB_mism_g": b["FB_mism_g"], "D+FB_mism_g": b["D+FB_mism_g"]}
LABEL = {"Base": "无自适应", "LawD": "律 D",
         "FB_mism_g": "F-B（记忆失配+g）",
         "D+FB_mism_g": "律 D + F-B（记忆失配+g）"}
COLOR = {"Base": "#3a3a3a", "LawD": "#c0392b",
         "FB_mism_g": "#16a085", "D+FB_mism_g": "#2471a3"}

seeds = [r["seed"] for r in a["Base"]]
x = np.arange(len(seeds))
fig, ax = plt.subplots(1, 3, figsize=(12.0, 3.6),
                       gridspec_kw={"width_ratios": [1.7, 1.0, 1.0]})

w = 0.2
for j, nm in enumerate(["Base", "FB_mism_g", "D+FB_mism_g"]):
    v = [r["a_echo"] for r in ROWS[nm]]
    ax[0].bar(x + (j - 1) * w, v, w, color=COLOR[nm], label=LABEL[nm])
ax[0].set_xticks(x)
ax[0].set_xticklabels([str(s)[-2:] for s in seeds], fontsize=8)
ax[0].set_xlabel("种子（后两位）")
ax[0].set_ylabel("首周期 10 Hz 回声 (rpm)")
ax[0].set_title("(a) 逐种子：记忆失配 8/8 命中", fontsize=9.3)
ax[0].legend(fontsize=7.2)
ax[0].grid(alpha=0.22, axis="y")

means = [np.mean([r["a_echo"] for r in ROWS[n]]) for n in ORDER]
stds = [np.std([r["a_echo"] for r in ROWS[n]], ddof=1) for n in ORDER]
xx = np.arange(len(ORDER))
ax[1].bar(xx, means, 0.62, color=[COLOR[n] for n in ORDER],
          yerr=stds, capsize=4, error_kw={"lw": 1.0, "ecolor": "#333"})
for i, (m, s) in enumerate(zip(means, stds)):
    ax[1].text(i, m + s + 1.0, "%.1f\n±%.1f" % (m, s), ha="center", fontsize=7.4)
ax[1].set_xticks(xx)
ax[1].set_xticklabels([LABEL[n] for n in ORDER], rotation=18, fontsize=7.2)
ax[1].set_ylabel("首周期 10 Hz 回声 (rpm)")
ax[1].set_title("(b) 均值±标准差（8 种子）", fontsize=9.3)
ax[1].set_ylim(0, max(means) + max(stds) + 10)
ax[1].grid(alpha=0.22, axis="y")

for j, nm in enumerate(ORDER):
    dip = np.mean([r["dip"] for r in ROWS[nm]])
    st = np.mean([r["steady"] for r in ROWS[nm]])
    ax[2].bar(j - 0.18, abs(dip), 0.34, color=COLOR[nm], alpha=0.9)
    ax[2].bar(j + 0.18, st, 0.34, color=COLOR[nm], alpha=0.45, hatch="//")
ax[2].set_xticks(xx)
ax[2].set_xticklabels([LABEL[n] for n in ORDER], rotation=18, fontsize=7.2)
ax[2].set_ylabel("rpm")
ax[2].set_title("(c) 加载跌落（实心）/ 稳态（斜纹）", fontsize=9.3)
ax[2].grid(alpha=0.22, axis="y")

fig.tight_layout()
fig.savefig("fig_inv_mism.png", dpi=200)
print("ok: fig_inv_mism.png")
