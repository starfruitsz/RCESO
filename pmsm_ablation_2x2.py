# -*- coding: utf-8 -*-
"""2x2 ablation figure (Law B, Law D) - English labels, for the IEEE draft."""
import numpy as np, matplotlib, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.unicode_minus": False,
                     "font.size": 9.0, "xtick.labelsize": 7.6, "ytick.labelsize": 7.6,
                     "legend.fontsize": 7.0, "axes.titlesize": 8.8,
                     "figure.dpi": 150, "savefig.bbox": "tight", "pdf.fonttype": 42})
A = np.load("ablation.npz")
K = ["000", "001", "010", "011"]
LB = {"000": "baseline", "010": "Law B", "001": "Law D", "011": "B+D"}
CO = {"000": "#7f8c8d", "001": "#c0392b", "010": "#16a085", "011": "#2471a3"}
R = {k: np.asarray(A[k], dtype=float) for k in K}
WN = ["NL", "Step", "Ev1", "Ev2", "Post", "Sust", "St.st"]

fig, ax = plt.subplots(1, 2, figsize=(6.6, 3.2))
a, b = ax[0], ax[1]
xs = np.arange(7); wd = 0.20
for i, k in enumerate(K):
    a.bar(xs + (i - 1.5) * wd, R[k], wd, color=CO[k], label=LB[k])
a.set_xticks(xs); a.set_xticklabels(WN, fontsize=7.2); a.set_yscale("log")
a.set_ylabel("Speed-error RMS (rpm)"); a.grid(alpha=0.25, axis="y")
a.legend(fontsize=6.8, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.22), frameon=False)
a.set_ylim(8, 90); a.set_title("(a) Four groups, seven windows", fontsize=8.6)

mB = 0.5 * (R["010"] + R["011"]) - 0.5 * (R["000"] + R["001"])
mD = 0.5 * (R["001"] + R["011"]) - 0.5 * (R["000"] + R["010"])
iBD = R["011"] - R["010"] - R["001"] + R["000"]
for i, (v, nm, col) in enumerate([(mB, "Law B", "#16a085"), (mD, "Law D", "#c0392b"), (iBD, "B x D", "#8e44ad")]):
    b.bar(xs + (i - 1) * 0.26, v, 0.26, color=col, label=nm)
b.axhline(0, color="#333", lw=0.8)
b.set_xticks(xs); b.set_xticklabels(WN, fontsize=7.2)
b.set_ylabel("Effect on RMS error (rpm)"); b.grid(alpha=0.25, axis="y")
b.legend(fontsize=6.8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.22), frameon=False)
b.set_title("(b) Main effects and B x D interaction", fontsize=8.6)
fig.tight_layout(pad=0.6, w_pad=1.6)
for e in (a, b):
    e.tick_params(length=2.5)
fig.savefig("fig_ablation_2x2.png", dpi=200)  # 只存 PNG（2026-10-19 约定）
print("wrote fig_ablation_2x2.pdf")
print("mB", " ".join("%.2f" % v for v in mB))
print("mD", " ".join("%.2f" % v for v in mD))
print("iBD", " ".join("%.2f" % v for v in iBD))
