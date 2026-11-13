# -*- coding: utf-8 -*-
"""plot_j_adaptive_3panel.py —— 自适应 J 三联图（仅保留原 (a)(b)(d)）
(a) 9-10 s 转速误差；(b) 10 Hz 残差；(c) Jhat 收敛（原 (d) 重编号）
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JM, JB = 1.89e-5, 9.95e-5
C_NAVY, C_TEAL, C_RED, C_ORANGE = "#1f4e79", "#16a085", "#c0392b", "#e67e22"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.0,
})
A = json.load(open("_j_adapt.json", encoding="utf-8"))
C = json.load(open("_j_comm.json", encoding="utf-8"))
W = {k: np.load("_wave_j_%s.npz" % k) for k in ("big_fault", "big_oracle", "big_comm")}

fig = plt.figure(figsize=(13.33, 6.67))
gs = fig.add_gridspec(2, 2, width_ratios=[1.55, 1.0], height_ratios=[1.0, 1.0],
                      left=0.065, right=0.985, top=0.875, bottom=0.11, wspace=0.18, hspace=0.42)
axa = fig.add_subplot(gs[:, 0]); axb = fig.add_subplot(gs[0, 1]); axd = fig.add_subplot(gs[1, 1])

# (a) 9-10 s speed error
for k, c, lab, lw in (("big_fault", C_RED, "固定标称 b0", 1.0),
                      ("big_oracle", C_ORANGE, "oracle 重整定", 1.0),
                      ("big_comm", C_TEAL, "辨识 + b0 自适应", 1.25)):
    d = W[k]; tt = d["t"][::100]; e = (d["y"][::100] - 1.0) * 600.0
    m = (tt >= 9.0) & (tt <= 10.0)
    axa.plot(tt[m], e[m], color=c, lw=lw, label=lab)
axa.set_xlim(9.0, 10.0); axa.set_ylim(-70, 82)
axa.set_xlabel("时间 / s"); axa.set_ylabel("转速误差 / rpm")
axa.set_title("(a) 稳态 9–10 s：10 Hz 纹波 33.3 → 4.0 rpm", fontsize=10.2, pad=5)
axa.legend(loc="upper right", ncol=1, fontsize=8.0)
axa.axhline(0, color="#999", lw=0.6)

# (b) 10 Hz residual bars
labels = ["标称 J\n(基准)", "5.26J_nom\n固定 b0", "oracle\n重整定", "辨识+b0\n自适应"]
vals = [A["Jm_fault"]["amp10"], C["big_fault"]["a10"], C["big_oracle"]["a10"], C["big_comm"]["a10"]]
cols = [C_NAVY, C_RED, C_ORANGE, C_TEAL]
bars = axb.bar(range(4), vals, color=cols, width=0.62)
for b, v in zip(bars, vals):
    axb.text(b.get_x() + b.get_width()/2, v + 0.8, "%.1f" % v, ha="center", va="bottom", fontsize=8.2)
axb.set_xticks(range(4)); axb.set_xticklabels(labels, fontsize=7.4)
axb.set_ylabel("10 Hz 转速分量 / rpm"); axb.set_ylim(0, 39)
axb.set_title("(b) 故障抑制：−88%", fontsize=10.2, pad=5)
axb.annotate("", xy=(1, 33.3), xytext=(3, 4.0), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=1.3, connectionstyle="arc3,rad=-0.25"))

# (c) Jhat convergence (原 (d))
d = W["big_comm"]; tj = np.asarray(d["t_j"]); jh = np.asarray(d["jhat"]); jfin = float(jh[-1])
axd.plot(tj, jh * 1e6, color=C_TEAL, lw=1.5, label=r"$\hat J$")
axd.axhline(JB * 1e6, color="#555", ls="--", lw=0.9, label=r"$J_{\rm true}$")
axd.axhspan(JB * 0.9e6, JB * 1.1e6, color=C_TEAL, alpha=0.10, label="±10%")
axd.axvline(2.0, color=C_ORANGE, ls=":", lw=1.1)
axd.set_xlim(0.3, 2.3); axd.set_ylim(0, 125)
axd.set_xlabel("时间 / s"); axd.set_ylabel(r"$\hat J$ / ($10^{-6}$ kg·m$^2$)")
axd.set_title("(c) 辨识收敛：+%.1f%%（2 s 冻结）" % (100*(jfin/JB-1)), fontsize=10.2, pad=5)
axd.legend(loc="lower right", fontsize=7.8)
axd.text(1.18, 101.5, "真实 99.5", color="#555", fontsize=7.6, ha="center")

fig.suptitle("自适应 J：辨识 → $b_0$ 更新 → 故障抑制（600 rpm、$T_1=0.057$ N·m、$J_{\\rm true}=5.26J_{\\rm nom}$ 应力测试）",
             fontsize=11.2, y=0.965)
fig.text(0.065, 0.018, "数据：pmsm_inv_sim.py；实验室噪声、种子 20261018；dither 100 Hz、0.2 s 窗、0–2 s 辨识；9–10 s 稳态窗。",
         fontsize=7.0, color="#666")
fig.savefig("fig_j_adaptive_3panel.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok fig_j_adaptive_3panel.png  jfin_err %.2f%%" % (100*(jfin/JB-1)))
