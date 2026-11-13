# -*- coding: utf-8 -*-
"""realj_plot_oracle_cmp.py —— 附录 B：J 自适应投运前/后的故障→纹波映射（唯一命名，避免与他人图重名）

输入 _fault_sweep_j24.json（b0=J_nom，未投运）/ _fault_sweep_j24_oracle.json（oracle，已投运）
输出 fig_realj_oracle_cmp.png
"""
import json
import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

J_TRUE, J_NOM = 4.81e-5, 1.89e-5
A = json.load(open("_fault_sweep_j24.json", encoding="utf-8"))
B = json.load(open("_fault_sweep_j24_oracle.json", encoding="utf-8"))
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8,
})
C0, C1 = "#7f8c8d", "#c0392b"


def sel(D, kind, key, val):
    rows = []
    for v in D.values():
        if v.get("kind") != kind:
            continue
        if key is None:
            rows.append((v["kappa"], v["amp10"], v["rms"]))
        elif abs(v[key] - val) < 1e-12:
            rows.append((v["kappa"], v["amp10"], v["rms"]))
    rows.sort()
    return np.array(rows)


a, b = sel(A, "unb", "e", 1e-4), sel(B, "unb", "e", 1e-4)
am, bm = sel(A, "mis", "beta", math.radians(1.0)), sel(B, "mis", "beta", math.radians(1.0))
fig, ax = plt.subplots(2, 2, figsize=(11.5, 7.0))
fig.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.09, hspace=0.36, wspace=0.24)
ax[0, 0].semilogx(a[:, 0], a[:, 1], "o-", color=C0, lw=1.3, ms=4, label="b0=J_nom（未投运）")
ax[0, 0].semilogx(b[:, 0], b[:, 1], "s-", color=C1, lw=1.3, ms=4, label="b0=J_true（已投运）")
ax[0, 0].set_xlabel("κ"); ax[0, 0].set_ylabel("10 Hz / rpm")
ax[0, 0].set_title("(a) 不平衡（e=0.1 mm）：10 Hz", fontsize=9.5); ax[0, 0].legend(loc="upper left")
ax[0, 1].semilogx(a[:, 0], a[:, 2], "o-", color=C0, lw=1.3, ms=4)
ax[0, 1].semilogx(b[:, 0], b[:, 2], "s-", color=C1, lw=1.3, ms=4)
ax[0, 1].set_xlabel("κ"); ax[0, 1].set_ylabel("稳态 RMS / rpm")
ax[0, 1].set_title("(b) 不平衡：稳态 RMS", fontsize=9.5)
ax[1, 0].semilogx(am[:, 0], am[:, 1], "o-", color=C0, lw=1.3, ms=4)
ax[1, 0].semilogx(bm[:, 0], bm[:, 1], "s-", color=C1, lw=1.3, ms=4)
ax[1, 0].set_xlabel("κ"); ax[1, 0].set_ylabel("10 Hz / rpm")
ax[1, 0].set_title("(c) 不对中（β=1°）：10 Hz", fontsize=9.5)
r = np.where(a[:, 1] > 1e-9, b[:, 1] / a[:, 1], np.nan)
ax[1, 1].semilogx(a[:, 0], r, "^-", color="#8e44ad", lw=1.3, ms=4)
ax[1, 1].axhline(J_NOM / J_TRUE, color="#555", ls=":", lw=1.0, label="1/2.545=0.393")
ax[1, 1].set_xlabel("κ"); ax[1, 1].set_ylabel("已投运/未投运")
ax[1, 1].set_title("(d) 抑制比", fontsize=9.5); ax[1, 1].legend(loc="upper right")
fig.suptitle("故障→转速纹波：J 自适应投运前/后（J_true=4.81e-5=2.545 J_nom，600 rpm、8 s、RC 开）", fontsize=10.5)
fig.savefig("fig_realj_oracle_cmp.png", dpi=150, facecolor="white")
print("ok fig_realj_oracle_cmp.png")
