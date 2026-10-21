# -*- coding: utf-8 -*-
"""四者对比图：无律 / 律 D / 新 F-B（D_m+g） / F-A（立即）

数据：_inv_lawd.json（Base, LawD）、_inv_mism_g.json（FB_mism_g）、_inv_fa.json（FA, FA20）。
8 种子：018/019/021/022/023/024/025/026。
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.3,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

a = json.load(open("_inv_lawd.json", encoding="utf-8"))
b = json.load(open("_inv_mism_g.json", encoding="utf-8"))
c = json.load(open("_inv_fa.json", encoding="utf-8"))

SEEDS = [20261018, 20261019, 20261021, 20261022,
         20261023, 20261024, 20261025, 20261026]


def pick(rows, sd):
    return [r for r in rows if r["seed"] == sd][0]


DATA = {
    "无律": [pick(a["Base"], s) for s in SEEDS],
    "律 D": [pick(a["LawD"], s) for s in SEEDS],
    "新 F-B": [pick(b["FB_mism_g"], s) for s in SEEDS],
    "F-A 立即": [pick(c["FA"], s) for s in SEEDS],
}
FA20 = [pick(c["FA20"], s) for s in SEEDS]
LABEL = {"无律": "无律（Base）", "律 D": "律 D",
         "新 F-B": "新 F-B（D_m+g）", "F-A 立即": "F-A 立即（τ=0）"}
COLOR = {"无律": "#3a3a3a", "律 D": "#c0392b",
         "新 F-B": "#16a085", "F-A 立即": "#2471a3"}
ORDER = ["无律", "律 D", "新 F-B", "F-A 立即"]

x = np.arange(len(SEEDS))
fig, ax = plt.subplots(2, 2, figsize=(12.0, 7.0))

# (a) 逐种子回声
w = 0.2
for j, nm in enumerate(ORDER):
    v = [r["a_echo"] for r in DATA[nm]]
    ax[0, 0].bar(x + (j - 1.5) * w, v, w, color=COLOR[nm], label=LABEL[nm])
ax[0, 0].set_xticks(x)
ax[0, 0].set_xticklabels([str(s)[-2:] for s in SEEDS], fontsize=8)
ax[0, 0].set_xlabel("种子（后两位）")
ax[0, 0].set_ylabel("首周期 10 Hz 回声 (rpm)")
ax[0, 0].set_title("(a) 逐种子：首周期回声", fontsize=9.4)
ax[0, 0].legend(fontsize=7.0, ncol=2)
ax[0, 0].grid(alpha=0.22, axis="y")

# (b) 均值±std
means = [np.mean([r["a_echo"] for r in DATA[n]]) for n in ORDER]
stds = [np.std([r["a_echo"] for r in DATA[n]], ddof=1) for n in ORDER]
xx = np.arange(len(ORDER))
ax[0, 1].bar(xx, means, 0.6, color=[COLOR[n] for n in ORDER],
             yerr=stds, capsize=4, error_kw={"lw": 1.0, "ecolor": "#333"})
for i, (m, s) in enumerate(zip(means, stds)):
    ax[0, 1].text(i, m + s + 1.0, "%.1f\n±%.1f" % (m, s), ha="center", fontsize=7.4)
ax[0, 1].set_xticks(xx)
ax[0, 1].set_xticklabels([LABEL[n] for n in ORDER], rotation=15, fontsize=7.6)
ax[0, 1].set_ylabel("首周期 10 Hz 回声 (rpm)")
ax[0, 1].set_title("(b) 均值±标准差（8 种子）", fontsize=9.4)
ax[0, 1].set_ylim(0, max(means) + max(stds) + 8)
ax[0, 1].grid(alpha=0.22, axis="y")

# (c) 加载跌落（绝对值）
dips = [np.mean([abs(r["dip"]) for r in DATA[n]]) for n in ORDER]
ax[1, 0].bar(xx, dips, 0.6, color=[COLOR[n] for n in ORDER])
for i, d in enumerate(dips):
    ax[1, 0].text(i, d + 1.0, "%.1f" % d, ha="center", fontsize=7.6)
ax[1, 0].set_xticks(xx)
ax[1, 0].set_xticklabels([LABEL[n] for n in ORDER], rotation=15, fontsize=7.6)
ax[1, 0].set_ylabel("加载跌落 |min| (rpm)")
ax[1, 0].set_title("(c) 加载跌落（越小越好）", fontsize=9.4)
ax[1, 0].grid(alpha=0.22, axis="y")

# (d) 稳态
st = [np.mean([r["steady"] for r in DATA[n]]) for n in ORDER]
ax[1, 1].bar(xx, st, 0.6, color=[COLOR[n] for n in ORDER])
for i, s in enumerate(st):
    ax[1, 1].text(i, s + 0.1, "%.2f" % s, ha="center", fontsize=7.6)
ax[1, 1].set_xticks(xx)
ax[1, 1].set_xticklabels([LABEL[n] for n in ORDER], rotation=15, fontsize=7.6)
ax[1, 1].set_ylabel("稳态 7–8 s RMS (rpm)")
ax[1, 1].set_title("(d) 稳态（越小越好）", fontsize=9.4)
ax[1, 1].grid(alpha=0.22, axis="y")

note = "参考：F-A 延时 20 ms（相位最优 oracle）回声 %.2f rpm" % np.mean([r["a_echo"] for r in FA20])
fig.text(0.5, 0.01, note, ha="center", fontsize=8.2, color="#555")
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("fig_inv_compare4.png", dpi=200)
print("ok: fig_inv_compare4.png")
print("means:", {n: round(float(np.mean([r["a_echo"] for r in DATA[n]])), 2) for n in ORDER})
