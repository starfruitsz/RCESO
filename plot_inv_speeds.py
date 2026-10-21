# -*- coding: utf-8 -*-
"""600/900/1200 rpm（10/15/20 Hz）对比：回声、跌落、稳态"""
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

SPEEDS = [600, 900, 1200]
FREQ = {600: "10 Hz", 900: "15 Hz", 1200: "20 Hz"}
D = {}
for s in SPEEDS:
    j = json.load(open("_inv_speed_%d.json" % s, encoding="utf-8"))
    D[s] = j["data"]
CFG = [("Base", "无律", "#3a3a3a", "o"), ("LawD", "律 D", "#c0392b", "s"),
       ("FB", "新 F-B", "#16a085", "^"), ("D+FB", "D+F-B", "#8e44ad", "D")]

fig, ax = plt.subplots(1, 3, figsize=(12.4, 3.6))
x = np.arange(3)
for col, (key, title, ylab, neg) in enumerate([
        ("a_echo", "(a) 首周期 10 Hz：越小越好", "10 Hz (rpm)", False),
        ("dip", "(b) 加载跌落：越小越好", "|min| (rpm)", True),
        ("steady", "(c) 稳态 7–8 s", "RMS (rpm)", False)]):
    for name, lab, c, mk in CFG:
        m = []
        e = []
        for s in SPEEDS:
            v = np.array([r[key] for r in D[s][name]])
            if neg:
                v = np.abs(v)
            m.append(v.mean()); e.append(v.std(ddof=1))
        ax[col].errorbar(x, m, yerr=e, marker=mk, color=c, lw=1.1, ms=4,
                         capsize=3, label=lab)
    ax[col].set_xticks(x)
    ax[col].set_xticklabels(["600\n(10 Hz)", "900\n(15 Hz)", "1200\n(20 Hz)"], fontsize=7.8)
    ax[col].set_xlabel("额定转速 rpm（负载频率）")
    ax[col].set_ylabel(ylab); ax[col].set_title(title, fontsize=9.2)
    ax[col].grid(alpha=0.22)
ax[0].legend(fontsize=7.0, ncol=2)
fig.tight_layout()
fig.savefig("fig_inv_speeds.png", dpi=200)
print("ok: fig_inv_speeds.png")
for s in SPEEDS:
    print(s, {n: round(float(np.mean([r["a_echo"] for r in D[s][n]])), 1) for n, *_ in CFG})
