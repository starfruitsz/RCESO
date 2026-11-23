# -*- coding: utf-8 -*-
"""_plot_onoff.py —— 三种差分方案对比：旧比值 / 双幅值 / 注入前后两段 SDFT"""
import numpy as np, os, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.4, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B = 101.89
RUNS = [("m_old", "旧·比值法", "#2c3e50", "--"),
        ("t_new", "双幅值差分", "#e67e22", "-."),
        ("o_new", "注入前后两段 SDFT", "#c0392b", "-")]
def load(tag):
    f = "_tjc_%s.npz" % tag
    if not os.path.exists(f): return None
    z = np.load(f); t = np.asarray(z["t"]); y = np.asarray(z["y"]) * 600.0
    b = np.asarray(z["b0e"]); st = max(1, int(round(len(t) / float(len(b)))))
    n = min(len(t[::st]), len(b))
    return dict(t=t[::st][:n], e=y[::st][:n] - 600.0, b0=b[:n])
D = {k: load(k) for k, _, _, _ in RUNS}
def met(d, a=60.0, b=90.0):
    t = d["t"]; m = (t >= a) & (t <= b); x = d["e"][m]; n = len(x)
    X = np.fft.rfft(x * np.hanning(n)); fr = np.fft.rfftfreq(n, t[1] - t[0])
    k = int(np.argmin(abs(fr - 10.0)))
    return float(np.sqrt(np.mean(x**2))), float(2*abs(X[k])/np.hanning(n).sum())
fig, ax = plt.subplots(2, 2, figsize=(10.2, 6.2))
a = ax[0, 0]
for tag, lab, c, ls in RUNS:
    if D[tag] is not None: a.plot(D[tag]["t"], D[tag]["b0"], color=c, ls=ls, lw=1.6, label=lab)
a.axhline(B, color="#1f4e79", ls=":", lw=1.2, label=r"真值 $b$=101.9")
a.set_xlim(0, 90); a.set_ylim(80, 170); a.set_xlabel("t / s"); a.set_ylabel(r"$\hat b_0$")
a.set_title(r"(a) $\hat b_0$ 轨迹（burst 周期 5 s）", fontsize=9)
a.legend(fontsize=7, loc="upper right", framealpha=0.93)

b = ax[0, 1]
for tag, lab, c, ls in RUNS:
    if D[tag] is None: continue
    t = D[tag]["t"]; m = (t >= 85) & (t <= 90)
    b.plot(t[m], D[tag]["e"][m], color=c, ls=ls, lw=0.9, label=lab)
b.set_xlim(85, 90); b.set_xlabel("t / s"); b.set_ylabel("转速误差 / rpm")
b.set_title("(b) 85–90 s 转速误差", fontsize=9); b.legend(fontsize=6.6, framealpha=0.93)

c1 = ax[1, 0]
for tag, lab, col, ls in RUNS:
    if D[tag] is None: continue
    t = D[tag]["t"]; e = D[tag]["e"]
    n1 = max(1, int(round(1.0 / max(t[1] - t[0], 1e-9))))
    c1.plot(t, np.sqrt(np.convolve(e**2, np.ones(n1)/n1, mode="same")), color=col, ls=ls, lw=1.2, label=lab)
c1.set_xlim(0, 90); c1.set_ylim(0, 40); c1.set_xlabel("t / s"); c1.set_ylabel("1 s 滑动 RMS / rpm")
c1.set_title("(c) 波动包络", fontsize=9); c1.legend(fontsize=6.8, framealpha=0.93)

d = ax[1, 1]
labs = []; e0 = []; rm = []; a10 = []
for tag, lab, col, ls in RUNS:
    if D[tag] is None: continue
    r, aa = met(D[tag]); labs.append(lab); e0.append(100*(D[tag]["b0"][-1]/B-1)); rm.append(r); a10.append(aa)
    print("%-8s b0=%7.2f (%+6.2f%%)  RMS=%5.2f  10Hz=%4.2f" % (tag, D[tag]["b0"][-1], e0[-1], r, aa))
x = np.arange(len(labs))
d.bar(x-0.2, e0, 0.4, color="#c0392b", alpha=0.85)
d.axhline(0, color="k", lw=0.7); d2 = d.twinx()
d2.bar(x+0.2, rm, 0.4, color="#95a5a6", alpha=0.85)
d.set_xticks(x); d.set_xticklabels([l.replace("·", "\n") for l in labs], fontsize=6.6)
d.set_ylabel(r"$\hat b_0$ 误差 / %", color="#c0392b"); d2.set_ylabel("RMS / rpm", color="#555")
d.set_ylim(-4, 22); d.grid(False); d2.grid(False); d.set_title("(d) 终值与稳态指标", fontsize=9)
for i in range(len(x)):
    d.text(x[i]-0.2, max(e0[i],0)+0.8, "%+.1f%%" % e0[i], ha="center", fontsize=6.2, color="#c0392b")
    d2.text(x[i]+0.2, rm[i]+0.3, "%.1f" % rm[i], ha="center", fontsize=6.2, color="#555")
    d.text(x[i], -2.6, "10Hz %.2f" % a10[i], ha="center", fontsize=6.0, color="#333")
plt.tight_layout(); plt.savefig("fig_onoff_cmp.png", bbox_inches="tight")
print("saved fig_onoff_cmp.png")
