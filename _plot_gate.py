# -*- coding: utf-8 -*-
"""_plot_gate.py —— 三种门控权重对比"""
import numpy as np, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B = 101.89
RUNS = [("o_new", "旧·中位数权重（发生自锁）", "#2c3e50", ":"),
        ("w2", "平台 + 硬截（w=0）", "#e67e22", "-."),
        ("w3", "软底 d2=0.08, dmax=0.30（w=0.082）", "#c0392b", "-"),
        ("w4", "软底 d2=0.20, dmax=0.50（w=0.135）", "#1f4e79", "--")]
def load(tag):
    f = "_tjc_%s.npz" % tag
    if not os.path.exists(f): return None
    z = np.load(f); t = np.asarray(z["t"]); b = np.asarray(z["b0e"])
    st = max(1, int(round(len(t) / float(len(b)))))
    return dict(t=t[::st][:len(b)], b0=b)
D = {k: load(k) for k, _, _, _ in RUNS}
fig, ax = plt.subplots(1, 2, figsize=(10.2, 3.7), gridspec_kw=dict(width_ratios=[2.1, 1]))
a = ax[0]
for tag, lab, c, ls in RUNS:
    if D[tag] is not None:
        a.plot(D[tag]["t"], D[tag]["b0"], color=c, ls=ls, lw=1.7, label=lab)
a.axhline(B, color="#1f4e79", lw=1.2, ls=":", label=r"真值 $b$=101.9")
a.set_xlim(0, 90); a.set_ylim(88, 135); a.set_xlabel("t / s"); a.set_ylabel(r"$\hat b_0$")
a.set_title(r"(a) $\hat b_0$ 轨迹：门控权重的三种设计", fontsize=9)
a.legend(fontsize=7, loc="upper right", framealpha=0.93)
b = ax[1]
labs = []; err = []; sd = []
for tag, lab, c, ls in RUNS:
    if D[tag] is None: continue
    t = D[tag]["t"]; v = D[tag]["b0"]; m = t >= 20
    labs.append(lab.split("（")[0].replace(" + ", "+")); err.append(100*(v[-1]/B-1)); sd.append(v[m].std())
x = np.arange(len(labs))
b.bar(x-0.2, err, 0.4, color="#c0392b", alpha=0.85, label=r"终值误差 / %")
b2 = b.twinx(); b2.bar(x+0.2, sd, 0.4, color="#95a5a6", alpha=0.85, label="20–90 s 标准差")
b.axhline(0, color="k", lw=0.7); b.set_xticks(x)
b.set_xticklabels(["中位数\n(自锁)", "硬截", "软底\nd2=0.08", "软底\nd2=0.20"], fontsize=6.8)
b.set_ylabel(r"$\hat b_0$ 误差 / %", color="#c0392b"); b2.set_ylabel("标准差", color="#555")
b.set_ylim(-4, 3); b.grid(False); b2.grid(False)
b.set_title(r"(b) 终值与抖动", fontsize=9)
for i in range(len(x)):
    b.text(x[i]-0.2, err[i]+(0.15 if err[i]>=0 else -0.35), "%+.2f%%" % err[i], ha="center", fontsize=6.4)
    b2.text(x[i]+0.2, sd[i]+0.05, "%.2f" % sd[i], ha="center", fontsize=6.4, color="#444")
    print("%-28s b0=%7.2f err=%+6.2f%% std=%.2f" % (labs[i], D[[t for t,_,_,_ in RUNS][i]]["b0"][-1], err[i], sd[i]))
plt.tight_layout(); plt.savefig("fig_gate_cmp.png", bbox_inches="tight")
print("saved fig_gate_cmp.png")
