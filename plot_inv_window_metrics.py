# -*- coding: utf-8 -*-
"""按窗口指标对比：突变窗（跌落）/ 回声窗（首周期 10 Hz）/ 相对无律变化"""
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

a = json.load(open("_inv_lawd.json", encoding="utf-8"))
b = json.load(open("_inv_mism_g.json", encoding="utf-8"))
c = json.load(open("_inv_fa.json", encoding="utf-8"))
ORDER = ["Base", "LawD", "FB", "FA"]
LABEL = {"Base": "无律", "LawD": "律 D", "FB": "新 F-B", "FA": "F-A 立即"}
COLOR = {"Base": "#3a3a3a", "LawD": "#c0392b", "FB": "#16a085", "FA": "#2471a3"}


def echo(rows):
    return np.array([r["a_echo"] for r in rows])


def dip(rows):
    return np.array([abs(r["dip"]) for r in rows])


dipv = {"Base": dip(a["Base"]), "LawD": dip(a["LawD"]),
        "FB": dip(b["FB_mism_g"]), "FA": dip(c["FA"])}
echov = {"Base": echo(a["Base"]), "LawD": echo(a["LawD"]),
         "FB": echo(b["FB_mism_g"]), "FA": echo(c["FA"])}

fig, ax = plt.subplots(1, 3, figsize=(12.4, 3.7),
                       gridspec_kw={"width_ratios": [1.1, 1.1, 1.0]})
x = np.arange(len(ORDER))

for i, n in enumerate(ORDER):
    ax[0].bar(i, dipv[n].mean(), 0.6, color=COLOR[n],
              yerr=dipv[n].std(ddof=1), capsize=4,
              error_kw={"lw": 1.0, "ecolor": "#333"})
    ax[0].text(i, dipv[n].mean() + 1.2, "%.1f" % dipv[n].mean(), ha="center", fontsize=7.6)
ax[0].set_xticks(x); ax[0].set_xticklabels([LABEL[n] for n in ORDER], fontsize=7.8)
ax[0].set_ylim(325, 345)
ax[0].set_ylabel("加载跌落 |min| (rpm)")
ax[0].set_title("(a) 突变窗：越小越好 → 律 D 最好", fontsize=9.2)
ax[0].grid(alpha=0.22, axis="y")
ax[0].text(0.03, 0.96, "配对：D 比 Base 少跌 5.84±2.79 rpm\nt=5.9（8/8 种子）", transform=ax[0].transAxes, va="top", fontsize=7.0)

base_e = echov["Base"].mean()
for i, n in enumerate(ORDER):
    ax[1].bar(i, echov[n].mean(), 0.6, color=COLOR[n],
              yerr=echov[n].std(ddof=1), capsize=4,
              error_kw={"lw": 1.0, "ecolor": "#333"})
    ax[1].text(i, echov[n].mean() + 1.2, "%.1f" % echov[n].mean(), ha="center", fontsize=7.6)
ax[1].set_xticks(x); ax[1].set_xticklabels([LABEL[n] for n in ORDER], fontsize=7.8)
ax[1].set_ylim(0, 44)
ax[1].set_ylabel("首周期 10 Hz (rpm)")
ax[1].set_title("(b) 回声窗：越小越好 → 新 F-B 最好", fontsize=9.2)
ax[1].grid(alpha=0.22, axis="y")
ax[1].text(0.46, 0.96, "D 仅 −6.9%\nF −84.1%（vs Base）", transform=ax[1].transAxes, va="top", fontsize=7.0)

# 相对无律变化（负=更好）
vals = {"律 D": [100 * (dipv["LawD"].mean() / dipv["Base"].mean() - 1),
                 100 * (echov["LawD"].mean() / base_e - 1)],
        "新 F-B": [100 * (dipv["FB"].mean() / dipv["Base"].mean() - 1),
                   100 * (echov["FB"].mean() / base_e - 1)]}
xx = np.arange(2)
for j, (n, v) in enumerate(vals.items()):
    ax[2].bar(xx + (j - 0.5) * 0.32, v, 0.32, color=COLOR["LawD" if n == "律 D" else "FB"], label=n)
    for k, y in enumerate(v):
        ax[2].text(xx[k] + (j - 0.5) * 0.32, y + (2 if y >= 0 else -5),
                   "%+.1f%%" % y, ha="center", fontsize=7.4)
ax[2].axhline(0, color="#555", lw=0.8)
ax[2].set_xticks(xx); ax[2].set_xticklabels(["突变窗（跌落）", "回声窗（10 Hz）"], fontsize=7.8)
ax[2].set_ylabel("相对无律变化 (%)")
ax[2].set_title("(c) 负值=更好：D 管突变、F 管回声", fontsize=9.2)
ax[2].legend(fontsize=7.4); ax[2].grid(alpha=0.22, axis="y")

fig.tight_layout()
fig.savefig("fig_inv_window_metrics.png", dpi=200)
print("ok: fig_inv_window_metrics.png")
for n in ORDER:
    print(n, "dip %.1f echo %.2f" % (dipv[n].mean(), echov[n].mean()))
