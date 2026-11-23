# -*- coding: utf-8 -*-
"""_plot_alpha.py —— 固定 alpha=1 vs 中位数自适应 alpha 的 b0 轨迹对比"""
import numpy as np, os, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B = 101.89
RUNS = [("a1_new", r"$\alpha=1$（固定）", "#2c3e50", "--"),
        ("t_new",  r"$\alpha$ 中位数自适应", "#c0392b", "-")]

def load(tag):
    f = "_tjc_%s.npz" % tag
    if not os.path.exists(f): return None
    z = np.load(f); t = np.asarray(z["t"]); b = np.asarray(z["b0e"])
    st = max(1, int(round(len(t) / float(len(b)))))
    return dict(t=t[::st][:len(b)], b0=b)

D = {k: load(k) for k, _, _, _ in RUNS}
fig, ax = plt.subplots(2, 1, figsize=(8.8, 6.2), gridspec_kw=dict(height_ratios=[1.5, 1]))
for i, (lo, hi) in enumerate([(0, 90), (0, 25)]):
    a = ax[i]
    for tag, lab, c, ls in RUNS:
        if D[tag] is None: continue
        t = D[tag]["t"]; m = (t >= lo) & (t <= hi)
        a.plot(t[m], D[tag]["b0"][m], color=c, ls=ls, lw=1.7, label=lab)
    a.axhline(B, color="#1f4e79", ls=":", lw=1.3, label=r"真值 $b$=101.9")
    a.set_xlim(lo, hi); a.set_ylim(80, 175); a.set_xlabel("t / s"); a.set_ylabel(r"$\hat b_0$")
    ax[0].set_title(r"$\hat b_0$ 轨迹：固定 $\alpha=1$ vs 中位数自适应 $\alpha$", fontsize=10)
    ax[1].set_title("(b) 0–25 s 收敛段放大", fontsize=9)
ax[0].legend(fontsize=8, ncol=3, loc="upper right", framealpha=0.93)
ax[1].legend(fontsize=8, ncol=3, loc="upper right", framealpha=0.93)
txt = []
for tag, lab, c, ls in RUNS:
    if D[tag] is None: continue
    t = D[tag]["t"]; b = D[tag]["b0"]; m = t >= 20.0
    txt.append("%s：终值 %.1f（%+.1f%%）  20–90 s 标准差 %.1f  范围 %.0f–%.0f"
               % (lab.replace("$\\alpha", "α").replace("$", ""), b[-1],
                  100 * (b[-1] / B - 1), b[m].std(), b[m].min(), b[m].max()))
    print(txt[-1])
ax[0].text(0.012, 0.045, "\n".join(txt), transform=ax[0].transAxes, fontsize=7.4,
           va="bottom", ha="left",
           bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#bbb", alpha=0.93))
plt.tight_layout(); plt.savefig("fig_alpha_cmp.png", bbox_inches="tight")
print("saved fig_alpha_cmp.png")
