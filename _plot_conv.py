# -*- coding: utf-8 -*-
"""_plot_conv.py —— 120 s 收敛性检查（120 s 后 burst 周期切到 60 min）"""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B = 101.89
z = np.load("_tjc_c120.npz")
t = np.asarray(z["t"]); b = np.asarray(z["b0e"])
st = max(1, int(round(len(t) / float(len(b)))))
tb = t[::st][:len(b)]
def stat(a, c):
    m = (tb >= a) & (tb <= c)
    return b[m].mean(), b[m].std(), b[m].min(), b[m].max()
print("段区间    均值     std     范围")
for a, c in [(0,10),(10,20),(20,40),(40,60),(60,80),(80,100),(100,120),(120,150)]:
    mu, sd, lo, hi = stat(a, c)
    print("%3d-%3d s  %7.2f  %6.2f   %6.1f-%.1f" % (a, c, mu, sd, lo, hi))
bfin = b[(tb >= 119.0) & (tb <= 120.0)].mean()
print("\n120 s 时刻 b0 = %.2f （误差 %+.2f%%）" % (bfin, 100*(bfin/B-1)))
print("150 s 终值 b0 = %.2f" % b[-1])
# 收敛判据：进入 ±2% 且不再离开
band = 0.02*bfin
out = np.abs(b - bfin) > band
idx = np.where(out)[0]
tin = tb[idx[-1]+1] if len(idx) and idx[-1]+1 < len(tb) else 0.0
print("最后一次跳出 ±2%% 带的时刻 = %.1f s；此后保持在带内" % tin)
m120 = (tb >= 120) & (tb <= 150)
print("120-150 s（周期已切 60 min）: std = %.4f  → %s" % (b[m120].std(), "完全冻结" if b[m120].std() < 0.05 else "仍有变化"))

fig, ax = plt.subplots(1, 2, figsize=(10.2, 3.5), gridspec_kw=dict(width_ratios=[2.2, 1]))
a = ax[0]
a.plot(tb, b, color="#c0392b", lw=1.6, label=r"$\hat b_0$")
a.axhline(B, color="#1f4e79", ls=":", lw=1.3, label=r"真值 $b$=101.9")
a.axvspan(120, 150, color="#95a5a6", alpha=0.18)
a.axvline(120, color="#1f4e79", lw=1.4, ls="--")
a.text(121.5, 630, "周期切 60 min", color="#1f4e79", fontsize=7.5)
a.set_xlim(0, 150); a.set_ylim(85, 660); a.set_xlabel("t / s"); a.set_ylabel(r"$\hat b_0$")
a.set_title(r"(a) 全程：前 120 s 辨识，之后冻结", fontsize=9)
a.legend(fontsize=7, loc="upper right", framealpha=0.93)
c1 = ax[1]
c1.plot(tb, b, color="#c0392b", lw=1.5)
c1.axhline(B, color="#1f4e79", ls=":", lw=1.2)
c1.axhline(bfin*(1-band/bfin), color="#e67e22", ls="--", lw=1.0)
c1.axhline(bfin*(1+band/bfin), color="#e67e22", ls="--", lw=1.0, label="±2% 带")
c1.set_xlim(0, 150); c1.set_ylim(90, 130); c1.set_xlabel("t / s")
c1.set_title("(b) 纵轴放大", fontsize=9); c1.legend(fontsize=7, framealpha=0.93)
plt.tight_layout(); plt.savefig("fig_conv120.png", bbox_inches="tight")
print("saved fig_conv120.png")
