# -*- coding: utf-8 -*-
"""_plot_ripple.py —— 转速波动图（AMP=0.118, b0低通 kp/15, burst 周期 5 s）"""
import numpy as np, os, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.5, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B = 101.89
RUNS = [("m_old", "旧·比值法", "#2c3e50"), ("t_new", "新·代数+电流差分+T 修正", "#c0392b")]
EXTRA = [("m_new", "新·未加 T 修正", "#e67e22")]
D0 = {}
def load(tag):
    f = "_tjc_%s.npz" % tag
    if not os.path.exists(f): return None
    z = np.load(f); t = np.asarray(z["t"]); y = np.asarray(z["y"]) * 600.0
    b = np.asarray(z["b0e"]); st = max(1, int(round(len(t) / float(len(b)))))
    n = min(len(t[::st]), len(b))
    return dict(t=t[::st][:n], e=(y[::st][:n] - 600.0), b0=b[:n])
D = {k: load(k) for k, _, _ in RUNS + EXTRA}
fig, ax = plt.subplots(2, 2, figsize=(10.2, 6.0))
for i, (tag, lab, c) in enumerate(RUNS):
    a = ax[0, i]
    if D[tag] is not None:
        a.plot(D[tag]["t"], D[tag]["e"], color=c, lw=0.6)
        for bt in range(1, 91, 5):
            a.axvline(bt, color=c, alpha=0.13, lw=0.6)
    a.set_xlim(0, 90); a.set_ylim(-45, 45); a.set_xlabel("t / s"); a.set_ylabel("转速误差 / rpm")
    a.set_title("(%s) %s 转速波动（竖线 = burst）" % ("ab"[i], lab), fontsize=9)
c1 = ax[1, 0]
for tag, lab, col in RUNS:
    if D[tag] is None: continue
    t = D[tag]["t"]; e = D[tag]["e"]
    n1 = max(1, int(round(1.0 / max(t[1] - t[0], 1e-9))))
    rms = np.sqrt(np.convolve(e ** 2, np.ones(n1) / n1, mode="same"))
    c1.plot(t, rms, color=col, lw=1.2, label=lab)
    m = t >= 60.0
    print("%-7s 60-90s RMS=%.2f  峰=%.1f" % (tag, np.sqrt(np.mean(e[m]**2)), np.max(np.abs(e[m]))))
c1.set_xlim(0, 90); c1.set_ylim(0, 40); c1.set_xlabel("t / s"); c1.set_ylabel("1 s 滑动 RMS / rpm")
c1.set_title("(c) 波动包络", fontsize=9); c1.legend(fontsize=7, framealpha=0.9)
d = ax[1, 1]
for tag, lab, col in EXTRA:
    if D[tag] is None: continue
    d.plot(D[tag]["t"], D[tag]["b0"], color=col, lw=1.1, ls="--", label=lab)
for tag, lab, col in RUNS:
    if D[tag] is None: continue
    d.plot(D[tag]["t"], D[tag]["b0"], color=col, lw=1.4, label=lab)
    m = D[tag]["t"] >= 20.0
    print("%-7s b0 20-90s: 均值%.1f 标准差%.1f 范围[%.0f,%.0f]  终值%.1f" %
          (tag, D[tag]["b0"][m].mean(), D[tag]["b0"][m].std(),
           D[tag]["b0"][m].min(), D[tag]["b0"][m].max(), D[tag]["b0"][-1]))
d.axhline(B, color="#1f4e79", ls=":", lw=1.1, label=r"真值 $b$=101.9")
d.set_xlim(0, 90); d.set_ylim(80, 170); d.set_xlabel("t / s"); d.set_ylabel(r"$\hat b_0$")
d.set_title(r"(d) $\hat b_0$ 轨迹（$k_p/50$ + 中位数 $\alpha$ + $T$ 修正）", fontsize=9)
d.legend(fontsize=7, framealpha=0.9)
plt.tight_layout(); plt.savefig("fig_ripple.png", bbox_inches="tight")
print("saved fig_ripple.png")
