# -*- coding: utf-8 -*-
"""_plot_b0_period.py —— burst 周期 2/10 s × 算法（J→b0 / 直接测 b0），t0=4 s。"""
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
CASE = [("o2", "J→b0，周期 2 s", "#8e44ad"),
        ("o10", "J→b0，周期 10 s", "#c39bd3"),
        ("d2", "直测 b0，周期 2 s", "#1e8449"),
        ("d10", "直测 b0，周期 10 s", "#7dcea0")]

def load(tag):
    z = np.load("_tj_%s.npz" % tag)
    t = np.asarray(z["t"]); dec = max(1, int(round(1e-3 / (t[1] - t[0]))))
    return dict(t=t[::dec], y=np.asarray(z["y"])[::dec], iq=np.asarray(z["iq"])[::dec],
                b0=np.asarray(z["b0e"]), t_j=np.asarray(z["t_j"]),
                tf=t, yf=np.asarray(z["y"]))
D = {k: load(k) for k, _, _ in CASE}
J = {k: json.load(open("_tj_%s.json" % k)) for k, _, _ in CASE}

fig = plt.figure(figsize=(12.6, 6.2))
gs = fig.add_gridspec(2, 2, left=0.07, right=0.99, top=0.87, bottom=0.09, wspace=0.24, hspace=0.42)
a1 = fig.add_subplot(gs[0, 0]); a2 = fig.add_subplot(gs[0, 1])
a3 = fig.add_subplot(gs[1, 0]); a4 = fig.add_subplot(gs[1, 1])

for k, lab, c in CASE:
    d = D[k]
    tb = d["t_j"]; bb = d["b0"]
    # 0.2 s 滚动中值：压掉 burst 内的 apply/rollback 抖动，保留趋势
    nb = 200
    med = np.array([np.median(bb[max(0, i-nb//2):i+nb//2]) for i in range(0, len(bb), nb)])
    a1.plot(tb[:len(med)*nb:nb] + 0.1, med, color=c, lw=1.4, label=lab)
a1.axhline(122.3, color="#2c3e50", ls=":", lw=1.0)
a1.text(0.8, 128, "真值 122.3", fontsize=6.8, color="#2c3e50")
a1.axhline(643.7, color="#bdc3c7", ls="--", lw=0.7)
a1.text(0.8, 655, "标称 b0=643.7", fontsize=6.4, color="#7f8c8d")
a1.set_xlim(0, 30); a1.set_ylim(80, 700)
a1.set_xlabel("时间 / s"); a1.set_ylabel("$b_0$ / s$^{-1}$")
a1.set_title("(a) b0 的在线变化（首个 burst 从 4 s 起）", fontsize=9.0)
a1.legend(fontsize=6.6, ncol=2, loc="upper right")

for k, lab, c in CASE:
    d = D[k]
    m = (d["t"] >= 25) & (d["t"] < 29)
    a2.plot(d["t"][m], (d["y"][m] - 1) * 600, color=c, lw=0.8, label=lab)
a2.set_xlim(25, 29); a2.set_ylim(-80, 80)
a2.set_xlabel("时间 / s"); a2.set_ylabel("转速误差 / rpm")
a2.set_title("(b) 稳态 10 Hz 残余（25–29 s）", fontsize=9.0)
a2.legend(fontsize=6.2, ncol=2, loc="upper right")

x = np.arange(4); w = 0.36
rms = [J[k]["rms"] for k, _, _ in CASE]; a10 = [J[k]["amp10"] for k, _, _ in CASE]
cols = [c for _, _, c in CASE]
b1 = a3.bar(x - w/2, rms, w, color=cols)
b2 = a3.bar(x + w/2, a10, w, color=cols, alpha=0.55, hatch="///")
for bb, v in list(zip(b1, rms)) + list(zip(b2, a10)):
    a3.text(bb.get_x()+bb.get_width()/2, v+0.4, "%.1f" % v, ha="center", fontsize=6.6)
a3.set_xticks(x); a3.set_xticklabels(["J→b0\n2s", "J→b0\n10s", "直测\n2s", "直测\n10s"], fontsize=7.2)
a3.set_ylabel("rpm"); a3.set_ylim(0, max(rms + a10) * 1.22)
a3.set_title("(c) RMS（实心）与 10 Hz 残余（斜线）", fontsize=9.0)

iqv = [J[k]["iq1ms"] for k, _, _ in CASE]
b = a4.bar(x, iqv, 0.5, color=cols)
for bb, v in zip(b, iqv):
    a4.text(bb.get_x()+bb.get_width()/2, v+0.08, "%.2f" % v, ha="center", fontsize=7.0)
a4.axhline(6.31, color="#c0392b", ls="--", lw=0.9)
a4.text(3.45, 6.42, "额定 6.31", color="#c0392b", fontsize=6.8, ha="right")
a4.set_xticks(x); a4.set_xticklabels(["J→b0\n2s", "J→b0\n10s", "直测\n2s", "直测\n10s"], fontsize=7.2)
a4.set_ylabel("iq1ms / A"); a4.set_ylim(0, max(iqv) * 1.18)
a4.set_title("(d) 电流代价", fontsize=9.0)

fig.suptitle("律J 的 b0 自适应：burst 周期 2 s vs 10 s，J→b0 换算 vs 直接测 b0（600 rpm、$J_{true}$=5.26$J_{nom}$）",
             fontsize=9.8, y=0.965)
fig.savefig("fig_b0_period.png", dpi=150, bbox_inches=None, facecolor="white")
print("RMS ", dict(zip([k for k,_,_ in CASE], [round(v,2) for v in rms])))
print("10Hz", dict(zip([k for k,_,_ in CASE], [round(v,2) for v in a10])))
print("b0  ", dict(zip([k for k,_,_ in CASE], [round(J[k]['b0e'],1) for k,_,_ in CASE])))
