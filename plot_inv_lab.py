# -*- coding: utf-8 -*-
"""实验室工况：Base / 律 D / F-B / D+F-B 对比 → fig_inv_lab.png"""
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

d = json.load(open("_inv_lab.json", encoding="utf-8"))
ORDER = ["Base", "LawD", "FB", "D+FB"]
LABEL = {"Base": "无律", "LawD": "律 D", "FB": "新 F-B", "D+FB": "D+F-B"}
COLOR = {"Base": "#3a3a3a", "LawD": "#c0392b", "FB": "#16a085", "D+FB": "#8e44ad"}

fig, ax = plt.subplots(1, 3, figsize=(11.8, 3.5))
x = np.arange(4)
for col, (key, title, ylab, ylim) in enumerate([
        ("a_echo", "(a) 首周期 10 Hz：越小越好", "10 Hz (rpm)", None),
        ("dip", "(b) 加载跌落：越小越好", "|min| (rpm)", None),
        ("steady", "(c) 稳态 7–8 s", "RMS (rpm)", None)]):
    vals = [np.array([r[key] for r in d[n]]) for n in ORDER]
    for i, v in enumerate(vals):
        if key == "dip":
            v = np.abs(v)
        ax[col].bar(i, v.mean(), 0.6, color=COLOR[ORDER[i]],
                    yerr=v.std(ddof=1), capsize=4,
                    error_kw={"lw": 1.0, "ecolor": "#333"})
        ax[col].text(i, v.mean() + (1.0 if key != "steady" else 0.2),
                     "%.1f" % v.mean(), ha="center", fontsize=7.4)
    ax[col].set_xticks(x)
    ax[col].set_xticklabels([LABEL[n] for n in ORDER], fontsize=7.8)
    ax[col].set_ylabel(ylab); ax[col].set_title(title, fontsize=9.2)
    ax[col].grid(alpha=0.22, axis="y")
    if ylim:
        ax[col].set_ylim(*ylim)

fig.tight_layout()
fig.savefig("fig_inv_lab.png", dpi=200)
print("ok: fig_inv_lab.png")
for n in ORDER:
    a = np.array([r["a_echo"] for r in d[n]])
    p = np.array([abs(r["dip"]) for r in d[n]])
    print("%-5s echo %.2f dip %.2f" % (n, a.mean(), p.mean()))
