# -*- coding: utf-8 -*-
"""_plot_es_freeze.py —— 律T 解调冻结/无冻结：1D 理论对照 + 换速工况实测。"""
import numpy as np, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.8, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.4,
})

fig = plt.figure(figsize=(12.8, 4.4))
gs = fig.add_gridspec(1, 3, left=0.06, right=0.99, top=0.84, bottom=0.13, wspace=0.28)
a1 = fig.add_subplot(gs[0, 0]); a2 = fig.add_subplot(gs[0, 1]); a3 = fig.add_subplot(gs[0, 2])

# (a) 1D 对照
z = np.load("_es_1d.npz")
t = z["t"]
a1.plot(t, z["dA"] * 100, color="#8e44ad", lw=1.1, label="事件式（窗内 hold $\\hat\\delta$）")
a1.plot(t, z["dB"] * 100, color="#1e8449", lw=1.1, label="连续滑动窗（无 hold）")
a1.axhline(-14.3, color="#2c3e50", ls=":", lw=0.9)
a1.text(2, -14.05, "δ* = −14.3%", fontsize=6.6, color="#2c3e50", va="bottom")
a1.set_xlim(0, 60); a1.set_ylim(-16.5, -7)
a1.set_xlabel("时间 / s"); a1.set_ylabel("$\\hat\\delta$ / %")
a1.set_title("(a) 1D 搜索模型：hold vs 连续更新", fontsize=9.0)
a1.legend(fontsize=6.6, loc="upper right")

# (b) 换速工况实测
for tag, lab, c in (("fr", "冻结开（含前馈复位）", "#1f4e79"), ("nf", "冻结关", "#e67e22")):
    d = np.load("_esnf_%s.npz" % tag)
    tt = np.asarray(d["t"])[::100]; es = np.asarray(d["es"])[::100]
    a2.plot(tt, es * 100, color=c, lw=1.0, label=lab)
a2.axvline(5.0, color="#7f8c8d", ls="--", lw=0.9)
a2.text(5.15, -8.2, "600→900 rpm", fontsize=6.6, color="#7f8c8d")
a2.axhline(-14.3, color="#2c3e50", ls=":", lw=0.8)
a2.axhline(-17.2, color="#2c3e50", ls=":", lw=0.8)
a2.text(0.4, -14.0, "δ*(600)=−14.3%", fontsize=6.2, color="#2c3e50", va="bottom")
a2.text(11.0, -17.0, "δ*(900)=−17.2%", fontsize=6.2, color="#2c3e50", va="bottom")
a2.set_xlim(0, 20); a2.set_ylim(-19.5, -12)
a2.set_xlabel("时间 / s"); a2.set_ylabel("$\\hat\\delta$ / %")
a2.set_title("(b) 换速工况：冻结开/关", fontsize=9.0)
a2.legend(fontsize=6.6, loc="lower left")

# (c) 指标表 + 稳定判据
J = {k: json.load(open("_esnf_%s.json" % k)) for k in ("fr", "nf")}
rows = [
    ("", "冻结开", "冻结关"),
    ("$\\hat\\delta$ 后段均值", "%+.2f%%" % (100*J["fr"]["es_post"]), "%+.2f%%" % (100*J["nf"]["es_post"])),
    ("|$\\hat\\delta$−$\\delta^*$(900)|", "%.2f pp" % (abs(J["fr"]["es_post"]+0.172)*100), "%.2f pp" % (abs(J["nf"]["es_post"]+0.172)*100)),
    ("RMS 12–20 s / rpm", "%.2f" % J["fr"]["rms_post"], "%.2f" % J["nf"]["rms_post"]),
    ("15 Hz 残余 / rpm", "%.2f" % J["fr"]["amp15_post"], "%.2f" % J["nf"]["amp15_post"]),
]
a3.axis("off")
a3.set_title("(c) 换速后指标与稳定判据", fontsize=9.0)
yy = 0.92
for i, r in enumerate(rows):
    wgt = "bold" if i == 0 else "normal"
    a3.text(0.02, yy, r[0], fontsize=7.6, transform=a3.transAxes, fontweight=wgt)
    a3.text(0.62, yy, r[1], fontsize=7.6, transform=a3.transAxes, ha="right", fontweight=wgt)
    a3.text(0.95, yy, r[2], fontsize=7.6, transform=a3.transAxes, ha="right", fontweight=wgt)
    yy -= 0.115
a3.text(0.02, 0.22, "稳定判据  $\\sigma < \\pi N\\Delta$：0.010 < 0.047（满足）", fontsize=7.4, transform=a3.transAxes)
a3.text(0.02, 0.12, "额外项/主项  $\\sigma/(\\pi N\\Delta)$ = 0.21", fontsize=7.4, transform=a3.transAxes)

fig.suptitle("律T 解调冻结：连续域多出的积分项是否影响 δ 稳定性（1D 模型 + 换速实测）", fontsize=9.8, y=0.97)
fig.savefig("fig_es_freeze.png", dpi=150, bbox_inches=None, facecolor="white")
print("saved fig_es_freeze.png")
