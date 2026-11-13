# -*- coding: utf-8 -*-
"""plot_fault_sweep.py —— κ / e / β 扫描结果（1920×960）"""
import json
import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = json.load(open("_fault_sweep.json", encoding="utf-8"))
C_UNB = "#e67e22"
C_MIS = "#16a085"
C_BASE = "#1f4e79"
C_REC = "#8e44ad"

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9,
    "figure.dpi": 150, "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8,
})

unb = {k: v for k, v in D.items() if v["kind"] == "unb"}
mis = {k: v for k, v in D.items() if v["kind"] == "mis"}
unb_k = sorted([(v["kappa"], v["T1"], v["amp10"]) for k, v in unb.items() if v["e"] == 1e-4])
mis_k = sorted([(v["kappa"], v["T1"], v["amp10"]) for k, v in mis.items()
                if abs(v["beta"] - math.radians(1.0)) < 1e-9])
unb_e = sorted([(v["e"] * 1e3, v["T1"], v["amp10"]) for k, v in unb.items() if abs(v["kappa"] - 300) < 1e-9])
mis_b = sorted([(math.degrees(v["beta"]), v["T1"], v["amp10"]) for k, v in mis.items()
                if abs(v["kappa"] - 20) < 1e-9])

fig, ax = plt.subplots(3, 2, figsize=(12.8, 6.4))
fig.subplots_adjust(left=0.078, right=0.985, top=0.905, bottom=0.105, hspace=0.62, wspace=0.24)

def tri(axx, rows):
    a = np.array(rows, float)
    return a[:, 0], a[:, 1], a[:, 2]

# (a) T1 vs kappa
x, y, _ = tri(None, unb_k); ax[0, 0].semilogx(x, y * 1e3, "o-", color=C_UNB, lw=1.3, ms=4, label="不平衡（e=0.1 mm）")
x, y, _ = tri(None, mis_k); ax[0, 0].semilogx(x, y * 1e3, "s-", color=C_MIS, lw=1.3, ms=4, label="不对中（β=1°）")
ax[0, 0].set_xlabel("等效放大系数 κ"); ax[0, 0].set_ylabel("1× 转矩幅值 / mN·m")
ax[0, 0].set_title("(a) 1× 转矩幅值 vs κ", fontsize=9, pad=4); ax[0, 0].legend(loc="upper left")

# (b) 10 Hz vs kappa
x, _, y = tri(None, unb_k); ax[0, 1].semilogx(x, y, "o-", color=C_UNB, lw=1.3, ms=4)
x, _, y = tri(None, mis_k); ax[0, 1].semilogx(x, y, "s-", color=C_MIS, lw=1.3, ms=4)
ax[0, 1].axhline(1.25, color="#7f8c8d", ls=":", lw=1.0, label="无故障噪声底 1.25 rpm")
ax[0, 1].set_xlabel("等效放大系数 κ"); ax[0, 1].set_ylabel("10 Hz 转速分量 / rpm")
ax[0, 1].set_title("(b) 转速纹波 vs κ", fontsize=9, pad=4)

# (c) T1 vs e
x, y, _ = tri(None, unb_e); ax[1, 0].plot(x, y * 1e3, "o-", color=C_UNB, lw=1.3, ms=4)
ax[1, 0].set_xlabel("偏心距 e / mm"); ax[1, 0].set_ylabel("1× 转矩幅值 / mN·m")
ax[1, 0].set_title("(c) 不平衡：T1 vs e（κ=300）", fontsize=9, pad=4)

# (d) T1 vs beta
x, y, _ = tri(None, mis_b); ax[1, 1].plot(x, y * 1e3, "s-", color=C_MIS, lw=1.3, ms=4)
ax[1, 1].set_xlabel("角不对中 β / °"); ax[1, 1].set_ylabel("1× 转矩幅值 / mN·m")
ax[1, 1].set_title("(d) 不对中：T1 vs β（κ=20）", fontsize=9, pad=4)

# (e) 10 Hz vs e
x, _, y = tri(None, unb_e); ax[2, 0].plot(x, y, "o-", color=C_UNB, lw=1.3, ms=4)
ax[2, 0].set_xlabel("偏心距 e / mm"); ax[2, 0].set_ylabel("10 Hz 转速分量 / rpm")
ax[2, 0].set_title("(e) 不平衡：纹波 vs e（κ=300）", fontsize=9, pad=4)

# (f) 10 Hz vs beta
x, _, y = tri(None, mis_b); ax[2, 1].plot(x, y, "s-", color=C_MIS, lw=1.3, ms=4)
ax[2, 1].set_xlabel("角不对中 β / °"); ax[2, 1].set_ylabel("10 Hz 转速分量 / rpm")
ax[2, 1].set_title("(f) 不对中：纹波 vs β（κ=20）", fontsize=9, pad=4)

# 推荐点：T1≈0.057 N·m
ax[0, 1].plot([580], [26.01], "o", mfc="none", mec=C_REC, ms=10, mew=1.6, zorder=5)
ax[0, 1].plot([67], [26.52], "o", mfc="none", mec=C_REC, ms=10, mew=1.6, zorder=5)
ax[0, 1].annotate("推荐 T1≈0.057 N·m\n(10 Hz≈26 rpm)", xy=(580, 26.01),
                  xytext=(160, 70), fontsize=7.5, color=C_REC,
                  arrowprops=dict(arrowstyle="->", color=C_REC, lw=0.9))
ax[0, 1].legend(loc="upper left")

fig.suptitle("故障模型参数扫描：1× 转矩幅值与 10 Hz 转速纹波（600 rpm、8 s、RC 开）", fontsize=10.5)
fig.savefig("fig_fault_sweep.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok")
