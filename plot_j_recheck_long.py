# -*- coding: utf-8 -*-
"""plot_j_recheck_long.py —— 周期复检在 J 阶跃下的 30 s 表现"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JM, J1, J2 = 1.89e-5, 9.95e-5, 4.81e-5
C_REC, C_COMM, C_FIX = "#16a085", "#e67e22", "#c0392b"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.0, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.8,
})
D = {k: np.load("_wave_j_%s_long.npz" % k) for k in ("rec", "comm", "fixed")}
M = {k: json.load(open("_j_%s_long.json" % k)) for k in ("rec", "comm", "fixed")}

def series(z):
    t = z["t"]; e = (z["y"] - 1.0) * 600.0
    tc, av, rv = [], [], []
    for s in range(0, 29):
        m = (t >= s) & (t < s + 1.0)
        if m.sum() < 100: continue
        ec = e[m]; ts = t[m]
        av.append(float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*ts)), 2*np.mean(ec*np.sin(2*np.pi*10*ts)))))
        rv.append(float(np.sqrt(np.mean(ec**2)))); tc.append(s + 0.5)
    return np.array(tc), np.array(av), np.array(rv)

S = {k: series(v) for k, v in D.items()}

fig = plt.figure(figsize=(13.33, 7.4))
gs = fig.add_gridspec(3, 1, left=0.075, right=0.985, top=0.885, bottom=0.075, hspace=0.42)
axa = fig.add_subplot(gs[0]); axb = fig.add_subplot(gs[1]); axc = fig.add_subplot(gs[2])

# (a) jhat
for k, c, lab, lw in (("rec", C_REC, "周期复检（0.6 s / 5 s）", 1.5),
                      ("comm", C_COMM, "调试期一次（2 s 冻结）", 1.2),
                      ("fixed", C_FIX, "固定 b0", 1.0)):
    axa.plot(D[k]["t_j"], np.asarray(D[k]["jhat"]) * 1e6, color=c, lw=lw, label=lab)
axa.plot([0, 15], [J1*1e6, J1*1e6], color="#555", ls="--", lw=0.9)
axa.plot([15, 30], [J2*1e6, J2*1e6], color="#555", ls="--", lw=0.9, label="真实 J（15 s 阶跃）")
axa.axvline(15.0, color="#999", ls=":", lw=0.9)
axa.set_xlim(0, 30); axa.set_ylim(0, 125)
axa.set_xlabel("时间 / s"); axa.set_ylabel(r"$\hat J$ / ($10^{-6}$ kg·m$^2$)")
axa.set_title("(a) 复检跟踪 J 阶跃（5.26→2.545 J_nom @15 s）；冻结版停在旧值", fontsize=9.8, pad=5)
axa.legend(loc="center right", fontsize=7.3)

# (b) a10
for k, c, lab in (("rec", C_REC, "周期复检"), ("comm", C_COMM, "一次冻结"), ("fixed", C_FIX, "固定 b0")):
    tc, av, rv = S[k]; axb.plot(tc, av, color=c, lw=1.3, marker="o", ms=2.0, label=lab)
axb.axvline(15.0, color="#999", ls=":", lw=0.9)
axb.set_xlim(0, 30); axb.set_ylim(0, 40)
axb.set_xlabel("时间 / s"); axb.set_ylabel("10 Hz（1 s 窗）/ rpm")
axb.set_title("(b) 10 Hz 均值：复检 4.0→8.6；冻结 4.4→8.4（J 变小，故障响应本身变大）", fontsize=9.6, pad=5)
axb.legend(loc="center right", fontsize=7.3)
axb.annotate("15 s J 阶跃", xy=(15, 36), xytext=(16.0, 36), fontsize=7.0, color="#666")

# (c) rms
for k, c, lab in (("rec", C_REC, "周期复检"), ("comm", C_COMM, "一次冻结"), ("fixed", C_FIX, "固定 b0")):
    tc, av, rv = S[k]; axc.plot(tc, rv, color=c, lw=1.4, marker="s", ms=2.0, label=lab)
axc.axvline(15.0, color="#999", ls=":", lw=0.9)
axc.set_xlim(0, 30); axc.set_ylim(0, 200)
axc.set_xlabel("时间 / s"); axc.set_ylabel("转速误差 RMS（1 s 窗）/ rpm")
axc.set_title("(c) RMS（末 1 s）：复检 %.1f vs 冻结 %.1f vs 固定 %.1f" % (S["rec"][2][-1], S["comm"][2][-1], S["fixed"][2][-1]), fontsize=9.6, pad=5)
axc.legend(loc="upper left", fontsize=7.3)
axc.annotate("%.0f" % S["comm"][2][-1], xy=(29.5, S["comm"][2][-1]), xytext=(25.8, 180), fontsize=7.2, color=C_COMM)

fig.suptitle("周期 dither 复检（0.6 s burst / 5 s）在 J 阶跃下的 30 s 表现：能跟踪 J，冻结版则失稳",
             fontsize=11.0, y=0.965)
fig.text(0.075, 0.012, "数据：pmsm_inv_sim.py；J_true 15 s 由 9.95e-5 阶跃到 4.81e-5；复检每 5 s 开 0.6 s 100 Hz dither、0.2 s DFT 窗、nmin=2；冻结版 2 s 后不再辨识。",
         fontsize=6.7, color="#666")
fig.savefig("fig_j_recheck_long.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok", S["rec"][1][-1], S["rec"][2][-1], S["comm"][2][-1], S["fixed"][2][-1])
