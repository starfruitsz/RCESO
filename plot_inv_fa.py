# -*- coding: utf-8 -*-
"""F-A（立即/延时 oracle）与 F-B 的对比图：_inv_fa.json + _inv_fa_delay.json"""
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

fa = json.load(open("_inv_fa.json", encoding="utf-8"))
dl = json.load(open("_inv_fa_delay.json", encoding="utf-8"))
ORDER = ["Base", "FB", "FA", "FA20"]
LABEL = {"Base": "无自适应", "FB": "F-B（D_m+g）",
         "FA": "F-A 立即（τ=0）", "FA20": "F-A 延时 20 ms"}
COLOR = {"Base": "#3a3a3a", "FB": "#16a085", "FA": "#c0392b", "FA20": "#2471a3"}
seeds = [r["seed"] for r in fa["Base"]]
x = np.arange(len(seeds))

fig, ax = plt.subplots(1, 3, figsize=(12.0, 3.6),
                       gridspec_kw={"width_ratios": [1.7, 1.0, 1.15]})

w = 0.2
for j, nm in enumerate(ORDER):
    v = [r["a_echo"] for r in fa[nm]]
    ax[0].bar(x + (j - 1.5) * w, v, w, color=COLOR[nm], label=LABEL[nm])
ax[0].set_xticks(x)
ax[0].set_xticklabels([str(s)[-2:] for s in seeds], fontsize=8)
ax[0].set_xlabel("种子（后两位）")
ax[0].set_ylabel("首周期 10 Hz 回声 (rpm)")
ax[0].set_title("(a) 逐种子：F-B 优于“立即” F-A", fontsize=9.2)
ax[0].legend(fontsize=6.8, ncol=2)
ax[0].grid(alpha=0.22, axis="y")

means = [np.mean([r["a_echo"] for r in fa[n]]) for n in ORDER]
stds = [np.std([r["a_echo"] for r in fa[n]], ddof=1) for n in ORDER]
xx = np.arange(len(ORDER))
ax[1].bar(xx, means, 0.62, color=[COLOR[n] for n in ORDER],
          yerr=stds, capsize=4, error_kw={"lw": 1.0, "ecolor": "#333"})
for i, (m, s) in enumerate(zip(means, stds)):
    ax[1].text(i, m + s + 1.0, "%.1f\n±%.1f" % (m, s), ha="center", fontsize=7.2)
ax[1].set_xticks(xx)
ax[1].set_xticklabels([LABEL[n] for n in ORDER], rotation=18, fontsize=6.8)
ax[1].set_ylabel("首周期 10 Hz 回声 (rpm)")
ax[1].set_title("(b) 均值±标准差（8 种子）", fontsize=9.2)
ax[1].set_ylim(0, max(means) + max(stds) + 8)
ax[1].grid(alpha=0.22, axis="y")

for sd, c in [(20261018, "#c0392b"), (20261021, "#2471a3")]:
    rows = sorted([v for v in dl.values() if v["seed"] == sd], key=lambda r: r["delay"])
    ax[2].plot([r["delay"] * 1e3 for r in rows], [r["a_echo"] for r in rows],
               "o-", color=c, lw=1.2, ms=3.5, label="种子 %d" % (sd % 100))
ax[2].axvline(20, color="#16a085", ls="--", lw=0.9)
ax[2].text(20.5, 18, "F-A 最优\n≈20–25 ms", fontsize=7.2, color="#16a085")
ax[2].set_xlabel("复位延迟 τ (ms)")
ax[2].set_ylabel("首周期 10 Hz 回声 (rpm)")
ax[2].set_title("(c) oracle 延时扫描：非单调", fontsize=9.2)
ax[2].legend(fontsize=7.2)
ax[2].grid(alpha=0.22)

fig.tight_layout()
fig.savefig("fig_inv_fa.png", dpi=200)
print("ok: fig_inv_fa.png")
