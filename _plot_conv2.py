# -*- coding: utf-8 -*-
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B = 101.89
R = [("c120", "5 s 周期 / 120 s 窗口", "#c0392b", 120),
     ("c60p3", "3 s 周期 / 60 s 窗口", "#1f4e79", 60)]
fig, ax = plt.subplots(1, 2, figsize=(10.4, 3.6))
for i, (lo, hi) in enumerate([(0, 130), (85, 125)]):
    a = ax[i]
    for tag, lab, c, sw in R:
        z = np.load("_tjc_%s.npz" % tag); t = np.asarray(z["t"]); b = np.asarray(z["b0e"])
        st = max(1, int(round(len(t) / float(len(b)))))
        a.plot(t[::st][:len(b)], b, color=c, lw=1.6, label=lab)
        a.axvline(sw, color=c, ls="--", lw=1.0, alpha=0.7)
    a.axhline(B, color="#1f4e79", ls=":", lw=1.2, label=r"真值 $b$=101.9")
    a.set_xlim(lo, hi); a.set_xlabel("t / s"); a.set_ylabel(r"$\hat b_0$")
    if i == 0:
        a.set_ylim(85, 660); a.set_title("(a) 全程（虚线 = 周期切 60 min 的时刻）", fontsize=9)
        a.legend(fontsize=7, loc="upper right", framealpha=0.93)
    else:
        a.set_ylim(92, 112); a.set_title("(b) 放大：切换前后", fontsize=9)
plt.tight_layout(); plt.savefig("fig_conv_cmp.png", bbox_inches="tight")
print("saved")
