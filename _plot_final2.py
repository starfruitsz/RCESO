# -*- coding: utf-8 -*-
"""_plot_final2.py —— 最终版全套图：b0 收敛 + 转速波动"""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.3, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B = 101.89; SW = 120.0
z = np.load("_tjc_final.npz")
t = np.asarray(z["t"]); y = np.asarray(z["y"]) * 600.0; b = np.asarray(z["b0e"])
st = max(1, int(round(len(t) / float(len(b)))))
tb = t[::st][:len(b)]; e = y[::st][:len(b)] - 600.0
bfin = b[-1]
def spec(a, c):
    m = (tb >= a) & (tb <= c); x = e[m]; n = len(x)
    X = np.fft.rfft(x * np.hanning(n)); fr = np.fft.rfftfreq(n, tb[1]-tb[0])
    k = int(np.argmin(abs(fr - 10.0)))
    return float(np.sqrt(np.mean(x**2))), float(2*abs(X[k])/np.hanning(n).sum()), float(np.max(np.abs(x)))
r1, a1, pk1 = spec(100, 130)
r0, a0, pk0 = spec(20, 60)
print("20-60s: RMS %.2f  10Hz %.2f  峰值 %.1f" % (r0, a0, pk0))
print("100-130s: RMS %.2f  10Hz %.2f  峰值 %.1f" % (r1, a1, pk1))
print("b0 终值 %.2f (%+.2f%%)" % (bfin, 100*(bfin/B-1)))

fig = plt.figure(figsize=(10.8, 7.0))
gs = fig.add_gridspec(3, 3, hspace=0.55, wspace=0.30)
a = fig.add_subplot(gs[0, :2])
a.plot(tb, b, color="#c0392b", lw=1.7, label=r"$\hat b_0$")
a.axhline(B, color="#1f4e79", ls=":", lw=1.3, label=r"真值 $b$=101.9")
a.axvline(SW, color="#1f4e79", ls="--", lw=1.2)
a.axvspan(SW, 150, color="#95a5a6", alpha=0.16)
a.set_xlim(0, 150); a.set_ylim(85, 660); a.set_xlabel("t / s"); a.set_ylabel(r"$\hat b_0$")
a.set_title(r"(a) $\hat b_0$ 收敛（前 120 s 每 5 s 辨识，之后周期 60 min）", fontsize=9)
a.legend(fontsize=7, loc="upper right", framealpha=0.93)

b1 = fig.add_subplot(gs[0, 2])
b1.plot(tb, b, color="#c0392b", lw=1.6)
b1.axhline(B, color="#1f4e79", ls=":", lw=1.2)
b1.axvline(SW, color="#1f4e79", ls="--", lw=1.0)
b1.set_xlim(0, 150); b1.set_ylim(92, 112); b1.set_xlabel("t / s")
b1.set_title("(b) 纵轴放大", fontsize=9)

c = fig.add_subplot(gs[1, :])
c.plot(tb, e, color="#2c3e50", lw=0.5)
c.axvline(SW, color="#c0392b", ls="--", lw=1.1)
c.axvspan(20, 60, color="#e67e22", alpha=0.10)
c.axvspan(100, 130, color="#1f4e79", alpha=0.10)
c.set_xlim(0, 150); c.set_ylim(-50, 50); c.set_xlabel("t / s"); c.set_ylabel("转速误差 / rpm")
c.set_title("(c) 转速波动全程（橙=辨识期，蓝=冻结后）", fontsize=9)

d = fig.add_subplot(gs[2, 0])
m = (tb >= 100) & (tb <= 110)
d.plot(tb[m], e[m], color="#1f4e79", lw=0.9)
d.set_xlim(100, 110); d.set_ylim(-50, 50); d.set_xlabel("t / s"); d.set_ylabel("rpm")
d.set_title("(d) 104–110 s 放大", fontsize=9)

e1 = fig.add_subplot(gs[2, 1])
n1 = max(1, int(round(1.0 / max(tb[1]-tb[0], 1e-9))))
e1.plot(tb, np.sqrt(np.convolve(e**2, np.ones(n1)/n1, mode="same")), color="#c0392b", lw=1.1)
e1.axvline(SW, color="#1f4e79", ls="--", lw=1.0)
e1.set_xlim(0, 150); e1.set_ylim(0, 45); e1.set_xlabel("t / s"); e1.set_ylabel("rpm")
e1.set_title("(e) 1 s 滑动 RMS", fontsize=9)

f = fig.add_subplot(gs[2, 2]); f.axis("off")
txt = ("最终指标\n\n"
       r"$\hat b_0$ = %.2f   （$b$=101.9，%+.2f%%）" % (bfin, 100*(bfin/B-1)) + "\n\n"
       "辨识期 20–60 s\n"
       "  RMS %.2f rpm   10 Hz %.2f rpm\n" % (r0, a0) +
       "冻结后 100–130 s\n"
       "  RMS %.2f rpm   10 Hz %.2f rpm\n" % (r1, a1) +
       "\n配置：正弦 65 Hz / 0.118\n两段式 0.2+0.2 s，周期 5 s\n"
       "低通 $k_p$/50，平台+软底门控\n冻结取最后 20 s 均值")
f.text(0.02, 0.96, txt, va="top", ha="left", fontsize=7.4, linespacing=1.7,
       bbox=dict(boxstyle="round,pad=0.5", fc="#fbfbfb", ec="#bbb"))
plt.savefig("fig_final_all.png", bbox_inches="tight")
print("saved fig_final_all.png")
