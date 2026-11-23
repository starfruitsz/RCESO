# -*- coding: utf-8 -*-
"""_plot_final.py —— 定稿版完整对照图（旧比值法 vs 新代数法全栈）"""
import numpy as np, os, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.2, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B = 101.89
TAGS = [("m_old", "旧·比值法", "#2c3e50"), ("t_new", "新·代数全栈", "#c0392b")]
AUX = [("m_new", "新·未加 T 修正", "#e67e22")]

def load(tag):
    f = "_tjc_%s.npz" % tag
    if not os.path.exists(f): return None
    z = np.load(f); t = np.asarray(z["t"]); y = np.asarray(z["y"]) * 600.0
    b = np.asarray(z["b0e"]); st = max(1, int(round(len(t) / float(len(b)))))
    n = min(len(t[::st]), len(b))
    jn = np.asarray(z["jnew"])
    return dict(t=t[::st][:n], e=y[::st][:n] - 600.0, b0=b[:n], jn=jn)

D = {k: load(k) for k, _, _ in TAGS + AUX}
def met(d, a=60.0, b=90.0):
    t = d["t"]; e = d["e"]; m = (t >= a) & (t <= b); x = e[m]
    n = len(x); X = np.fft.rfft(x * np.hanning(n)); fr = np.fft.rfftfreq(n, t[1] - t[0])
    k = int(np.argmin(abs(fr - 10.0)))
    return dict(rms=float(np.sqrt(np.mean(x ** 2))), pk=float(np.max(np.abs(x))),
                a10=float(2 * abs(X[k]) / np.hanning(n).sum()))
M = {k: met(v) for k, v in D.items() if v is not None}

fig = plt.figure(figsize=(10.6, 7.4))
gs = GridSpec(3, 3, figure=fig, hspace=0.52, wspace=0.30)

a = fig.add_subplot(gs[0, :2])
for tag, lab, c in TAGS:
    if D[tag] is None: continue
    a.plot(D[tag]["t"], D[tag]["e"], color=c, lw=0.6, label=lab)
for bt in range(1, 91, 5):
    a.axvline(bt, color="#888", alpha=0.10, lw=0.5)
a.set_xlim(0, 90); a.set_ylim(-45, 45); a.set_ylabel("转速误差 / rpm")
a.set_title("(a) 转速波动全程（竖线 = burst 时刻，每 5 s）", fontsize=9)
a.legend(fontsize=7, ncol=2, loc="lower right", framealpha=0.9)

b = fig.add_subplot(gs[0, 2])
for tag, lab, c in TAGS:
    if D[tag] is None: continue
    t = D[tag]["t"]; m = (t >= 85) & (t <= 90)
    b.plot(t[m], D[tag]["e"][m], color=c, lw=0.9, label=lab)
b.set_xlim(85, 90); b.set_title("(b) 85–90 s 放大", fontsize=9); b.set_xlabel("t / s")
b.legend(fontsize=6.5, framealpha=0.9)

c1 = fig.add_subplot(gs[1, 0])
for tag, lab, col in TAGS:
    if D[tag] is None: continue
    t = D[tag]["t"]; e = D[tag]["e"]
    n1 = max(1, int(round(1.0 / max(t[1] - t[0], 1e-9))))
    c1.plot(t, np.sqrt(np.convolve(e ** 2, np.ones(n1) / n1, mode="same")), color=col, lw=1.2, label=lab)
c1.set_xlim(0, 90); c1.set_ylim(0, 40); c1.set_xlabel("t / s"); c1.set_ylabel("1 s 滑动 RMS / rpm")
c1.set_title("(c) 波动包络", fontsize=9); c1.legend(fontsize=6.5, framealpha=0.9)

d = fig.add_subplot(gs[1, 1:])
for tag, lab, col in AUX:
    if D[tag] is not None:
        d.plot(D[tag]["t"], D[tag]["b0"], color=col, lw=1.1, ls="--", label=lab)
for tag, lab, col in TAGS:
    if D[tag] is not None:
        d.plot(D[tag]["t"], D[tag]["b0"], color=col, lw=1.5, label=lab)
d.axhline(B, color="#1f4e79", ls=":", lw=1.2, label=r"真值 $b$=101.9")
d.set_xlim(0, 90); d.set_ylim(80, 170); d.set_xlabel("t / s"); d.set_ylabel(r"$\hat b_0$")
d.set_title(r"(d) $\hat b_0$ 轨迹（$k_p/50$ + 中位数自适应 $\alpha$ + $T$ 修正）", fontsize=9)
d.legend(fontsize=7, loc="upper right", framealpha=0.9)

e = fig.add_subplot(gs[2, :2])
if D["t_new"] is not None and D["t_new"]["jn"].size:
    j = D["t_new"]["jn"]; j = j[j[:, 3] > 0]
    jj = np.array([[r[0], r[5]] for r in j if r[5] > 0])
    e.scatter(jj[:, 0], jj[:, 1], s=14, color="#c0392b", zorder=3,
              label="新法逐窗差分估计（剔除前）")
    e.plot(D["t_new"]["t"], D["t_new"]["b0"], color="#1f4e79", lw=1.3, label=r"剔除后 $\hat b_0$")
e.axhline(B, color="#1f4e79", ls=":", lw=1.1, label=r"真值 $b$=101.9")
e.set_xlim(0, 90); e.set_ylim(80, 130); e.set_xlabel("t / s"); e.set_ylabel(r"$\hat b_0$")
e.set_title("(e) 新法原始逐窗估计 vs 剔除后的 $\\hat b_0$（中位数自适应 $\\alpha$ 的作用）", fontsize=9)
e.legend(fontsize=6.8, ncol=3, framealpha=0.9, loc="upper right")

f = fig.add_subplot(gs[2, 2])
labs = ["旧·比值", "新·全栈"]
b0e = [100 * (D[k]["b0"][-1] / B - 1) for k, _, _ in TAGS]
rm = [M[k]["rms"] for k, _, _ in TAGS]
a10 = [M[k]["a10"] for k, _, _ in TAGS]
x = np.arange(2)
f.bar(x - 0.22, b0e, 0.42, color="#c0392b", alpha=0.85, label=r"$\hat b_0$ 误差 / %")
f.axhline(0, color="k", lw=0.7)
f2 = f.twinx()
f2.bar(x + 0.22, rm, 0.42, color="#95a5a6", alpha=0.85, label="RMS / rpm")
f.set_xticks(x); f.set_xticklabels(labs, fontsize=7.5)
f.set_ylabel(r"$\hat b_0$ 误差 / %", color="#c0392b"); f2.set_ylabel("RMS / rpm", color="#555")
f.set_ylim(-4, 20); f.grid(False); f2.grid(False)
f.set_title("(f) 终值与稳态指标", fontsize=9)
for i in range(2):
    f.text(x[i] - 0.22, max(b0e[i], 0) + 0.8, "%+.1f%%" % b0e[i], ha="center", fontsize=6.4, color="#c0392b")
    f2.text(x[i] + 0.22, rm[i] + 0.3, "%.1f" % rm[i], ha="center", fontsize=6.4, color="#555")
    f.text(x[i], -2.6, "10Hz %.2f" % a10[i], ha="center", fontsize=6.2, color="#333")

plt.savefig("fig_final_cmp.png", bbox_inches="tight")
out = {k: dict(b0=float(D[k]["b0"][-1]), err=float(100 * (D[k]["b0"][-1] / B - 1)),
               **M[k]) for k in M}
json.dump(out, open("_final_metrics.json", "w"), indent=1)
for k, v in out.items():
    print("%-7s b0=%7.2f (%+6.2f%%)  RMS=%5.2f  峰值=%5.1f  10Hz=%4.2f"
          % (k, v["b0"], v["err"], v["rms"], v["pk"], v["a10"]))
print("saved fig_final_cmp.png")
