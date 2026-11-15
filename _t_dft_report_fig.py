# -*- coding: utf-8 -*-
"""_t_dft_report_fig.py —— 报告 §T 用的正式配图（两栏、字号偏大）。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 10.0, "figure.dpi": 160,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
    "legend.frameon": False, "legend.fontsize": 8.0,
})
Q = 5.0
D = {k: np.load("_tdft_%s.npz" % k) for k in ("bpf", "dft1", "dft2", "cal2")}

def movmean(x, n):
    c = np.concatenate(([0.0], np.cumsum(x)))
    y = c[n:] - c[:-n]
    return np.concatenate((np.full(n - 1, y[0]), y)) / n

fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.5), gridspec_kw=dict(width_ratios=[1.0, 1.05]))

a0, a1 = ax
for key, lab, col, lw in (("bpf", "带通 $Q_{\\rm bp}$=5（÷$Q$）", "#7f8c8d", 0.8),
                          ("dft1", "DFT $m$=1", "#c0392b", 0.6),
                          ("dft2", "DFT $m$=2", "#d68910", 0.8)):
    d = D[key]; t = d["t"]; a = d["amp"] / (Q if key == "bpf" else 1.0)
    m = (t >= 5.0) & (t < 9.0)
    a0.plot(t[m], a[m], color=col, lw=lw, label=lab)
a0.set_xlim(5, 9); a0.set_ylim(0.0005, 0.0048)
a0.set_xlabel("时间 / s"); a0.set_ylabel("$A$")
a0.set_title("(a) 基波幅值（已按 $1/Q$ 标定到真实 RMS）", fontsize=9.6)
a0.legend(loc="upper left", ncol=1, fontsize=7.6)

for key, lab, col in (("bpf", "带通（现口径）", "#7f8c8d"),
                      ("dft2", "DFT $m$=2，$I_{\\rm dead}$=1e−5", "#d68910"),
                      ("cal2", "DFT $m$=2，重标定 2e−6", "#1e8449")):
    d = D[key]; t = d["t"][::100]; es = d["es"][::100]
    n = int(round(1.5 / (t[1] - t[0])))
    a1.plot(t, movmean(es, n), color=col, lw=1.4, label=lab)
a1.axhline(-0.143, color="#2e4053", ls=":", lw=0.9)
a1.text(0.5, -0.1405, "理论 $\\delta^{*}$=−14.3%", fontsize=7.6, color="#2e4053", va="bottom")
a1.set_xlim(0, 30); a1.set_ylim(-0.175, -0.10)
a1.set_xlabel("时间 / s"); a1.set_ylabel("$\\hat{\\delta}$")
a1.set_title("(b) 极值搜索：三种幅值观测口径", fontsize=9.6)
a1.legend(loc="lower left", fontsize=7.4)

fig.tight_layout()
fig.savefig("fig_t_dft_report.png", bbox_inches="tight")
print("saved fig_t_dft_report.png")
