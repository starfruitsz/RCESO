# -*- coding: utf-8 -*-
"""plot_b0_adaptive_ppt.py —— b0 自适应三联图（PPT s16）"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 600.0
J = json.load(open("_b0_ppt.json"))
C_FIX, C_AD, C_OR = "#c0392b", "#16a085", "#e67e22"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.0,
})
W = {k: np.load("_wave_b0_%s.npz" % k) for k in ("fixed", "adapt", "oracle")}

fig = plt.figure(figsize=(13.33, 6.67))
gs = fig.add_gridspec(2, 2, width_ratios=[1.55, 1.0], height_ratios=[1, 1],
                      left=0.065, right=0.985, top=0.865, bottom=0.11, wspace=0.18, hspace=0.42)
axa = fig.add_subplot(gs[:, 0]); axb = fig.add_subplot(gs[0, 1]); axd = fig.add_subplot(gs[1, 1])

for k, c, lab, lw in (("fixed", C_FIX, "固定标称 b0", 1.0),
                      ("oracle", C_OR, "oracle 重整定", 1.0),
                      ("adapt", C_AD, "b0 自适应", 1.2)):
    d = W[k]; tt = d["t"]; e = (d["y"] - 1.0) * N; m = (tt >= 9.0) & (tt <= 10.0)
    axa.plot(tt[m], e[m], color=c, lw=lw, label=lab)
axa.set_xlim(9, 10); axa.set_ylim(-95, 100)
axa.set_xlabel("时间 / s"); axa.set_ylabel("转速误差 / rpm")
axa.set_title("(a) 稳态 9–10 s：10 Hz 纹波 %.1f → %.1f rpm" % (J["fixed"]["a10"], J["adapt"]["a10"]), fontsize=10.2, pad=5)
axa.legend(loc="upper right"); axa.axhline(0, color="#999", lw=0.6)

labels = ["固定标称 b0", "b0 自适应", "oracle 重整定"]
vals = [J["fixed"]["a10"], J["adapt"]["a10"], J["oracle"]["a10"]]
cols = [C_FIX, C_AD, C_OR]
bars = axb.bar(range(3), vals, color=cols, width=0.58)
for b, v in zip(bars, vals): axb.text(b.get_x()+b.get_width()/2, v+0.9, "%.1f" % v, ha="center", va="bottom", fontsize=8.2)
axb.set_xticks(range(3)); axb.set_xticklabels(labels, fontsize=7.4)
axb.set_ylabel("10 Hz 转速分量 / rpm"); axb.set_ylim(0, 65)
axb.set_title("(b) 故障抑制：−%.0f%%" % (100*(1-J["adapt"]["a10"]/J["fixed"]["a10"])), fontsize=10.2, pad=5)

d = W["adapt"]; axd.plot(np.asarray(d["t_j"])[::100], np.asarray(d["b0e"]), color=C_AD, lw=1.4, label="b0 自适应")
axd.axhline(643.7, color=C_FIX, ls="--", lw=0.9, label="标称 b0")
axd.axhline(122.3, color=C_OR, ls=":", lw=1.0, label="真实 J 对应 b0")
axd.set_xlim(0, 10); axd.set_ylim(0, 700)
axd.set_xlabel("时间 / s"); axd.set_ylabel(r"$b_0$ / s$^{-1}$")
axd.set_title("(c) b0 收敛：%.1f（真实 122.3）" % J["adapt"]["b0"], fontsize=9.8, pad=5)
axd.legend(loc="center right", fontsize=7.4)

fig.suptitle("b0 自适应：辨识 → b0 更新 → 故障抑制（600 rpm、圆盘不平衡 + 角不对中 β=1° + 平行不对中）",
             fontsize=10.8, y=0.965)
fig.text(0.065, 0.012, "数据：pmsm_inv_sim.py；2 s 内 100 Hz dither 辨识，2 s 后冻结；9–10 s 稳态窗；实验室噪声、种子 20261018。",
         fontsize=6.8, color="#666")
fig.savefig("fig_b0_adaptive_ppt.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok")