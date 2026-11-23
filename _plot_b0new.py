# -*- coding: utf-8 -*-
"""_plot_b0new.py —— 内模反演自标定 b0 辨识 vs 原比值法（三合一故障 + 三律融合，90 s）"""
import numpy as np, os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B_TRUE = 101.89   # 物理增益 kt*I_BASE/(J_true*w_ref)
RUNS = [("b90alg",  "新·代数法 (t0=3 s)", "#c0392b", "-"),
        ("b90fix",  "递推·反演+欧拉 (t0=3 s)", "#e67e22", "-."),
        ("b90old",  "旧·比值 (t0=3 s)", "#7f8c8d", "--"),
        ("b90alg1", "新·代数法 (t0=1 s)", "#1f4e79", "-")]

def load(tag):
    f = "_tjc_%s.npz" % tag
    if not os.path.exists(f): return None
    z = np.load(f)
    t = np.asarray(z["t"]); y = np.asarray(z["y"]); b = np.asarray(z["b0e"])
    st = max(1, int(round(len(t) / float(len(b)))))
    tb = t[::st][:len(b)]; yb = y[::st][:len(b)]
    n = min(len(tb), len(yb), len(b))
    return dict(t=tb[:n], y=yb[:n], b0=b[:n], jn=np.asarray(z["jnew"]))

def m10(t, e, win=3.0):
    m = t >= (t[-1] - win); x = e[m] - e[m].mean()
    X = np.fft.rfft(x * np.hanning(len(x))); fr = np.fft.rfftfreq(len(x), t[1] - t[0])
    k = int(np.argmin(abs(fr - 10.0)))
    return float(2 * abs(X[k]) / np.hanning(len(x)).sum())

D = {k: load(k) for k, _, _, _ in RUNS}
E = {k: (v["y"] - 1.0) * 600.0 for k, v in D.items() if v is not None}
print("decimated lengths:", {k: len(v["t"]) for k, v in D.items() if v is not None})
fig, ax = plt.subplots(2, 2, figsize=(9.8, 6.2))

a = ax[0, 0]
for tag, lab, c, ls in RUNS:
    if D[tag] is None: continue
    a.plot(D[tag]["t"], D[tag]["b0"], color=c, ls=ls, lw=1.4, label=lab)
a.axhline(B_TRUE, color="#1f4e79", lw=1.1, ls=":", label=r"真值 $b$=101.9 (物理)")
a.set_yscale("log"); a.set_ylim(80, 700); a.set_xlim(0, 90)
a.set_xlabel("t / s"); a.set_ylabel(r"$\hat b_0$（对数）")
a.set_title(r"(a) $\hat b_0$ 轨迹（9 次 burst，故障+负载自 2 s 起）", fontsize=9)
a.legend(fontsize=7, loc="upper right", framealpha=0.92)

b = ax[0, 1]
for tag, lab, c, mk in (("b90alg", "新·代数法 (t0=3 s)", "#c0392b", "o"), ("b90fix", "递推 (t0=3 s)", "#e67e22", "^")):
    if D[tag] is None or D[tag]["jn"].size == 0: continue
    j = D[tag]["jn"]; j = j[j[:, 3] < 0]
    b.plot(j[:, 0], j[:, 2], marker=mk, ms=5.5, lw=1.0, color=c, label=lab)
b.axhline(B_TRUE, color="#1f4e79", lw=1.1, ls=":", label=r"真值 $b$=101.9")
b.set_ylim(85, 140); b.set_xlim(0, 90)
b.set_xlabel("t / s"); b.set_ylabel(r"单次 burst 估计 $\hat b_0$")
b.set_title("(b) 每次 burst 的估计（代数法 2 次即稳定在 100 附近）", fontsize=9)
b.legend(fontsize=7, loc="upper right", framealpha=0.92)

c = ax[1, 0]
for tag, lab, col, ls in RUNS:
    if D[tag] is None: continue
    t = D[tag]["t"]; e = E[tag]; m = (t >= 84.0) & (t <= 90.0)
    c.plot(t[m], e[m], color=col, ls=ls, lw=1.0, label=lab)
c.set_xlabel("t / s"); c.set_ylabel("转速误差 / rpm"); c.set_xlim(84, 90)
c.set_title("(c) 84–90 s 转速误差", fontsize=9)
c.legend(fontsize=6.0, ncol=2, framealpha=0.92, loc="lower center", handlelength=1.6)

d = ax[1, 1]
labs, e0, rm, a10 = [], [], [], []
for tag, lab, col, ls in RUNS:
    if D[tag] is None: continue
    t = D[tag]["t"]; e = E[tag]; m = t >= t[-1] - 3.0
    labs.append(lab); e0.append(100 * (D[tag]["b0"][-1] / B_TRUE - 1))
    rm.append(float(np.sqrt(np.mean(e[m] ** 2)))); a10.append(m10(t, e))
x = np.arange(len(labs))
d.bar(x - 0.21, e0, 0.40, color="#c0392b", alpha=0.85, label=r"$\hat b_0$ 终值误差 / %")
d2 = d.twinx(); d2.bar(x + 0.21, rm, 0.40, color="#95a5a6", alpha=0.85, label="末期 RMS / rpm")
d.axhline(0, color="k", lw=0.7); d.set_xticks(x)
d.set_xticklabels(["%s\n(%+.1f%%)\n10Hz %.1f" % (l.replace(" (", "\n("), e0[i], a10[i])
                   for i, l in enumerate(labs)], fontsize=7)
d.set_ylabel(r"$\hat b_0$ 误差 / %", color="#c0392b"); d2.set_ylabel("RMS / rpm", color="#555")
d.set_ylim(-26, 22)
d.set_title("(d) 终值误差与稳态性能", fontsize=9); d.grid(False); d2.grid(False)


plt.tight_layout()
plt.savefig("fig_b0new_cmp.png", bbox_inches="tight")
js = {}
for tag, lab, col, ls in RUNS:
    if D[tag] is None: continue
    js[tag] = dict(b0=float(D[tag]["b0"][-1]), err=float(100 * (D[tag]["b0"][-1] / B_TRUE - 1)),
                   rms=float(np.sqrt(np.mean(E[tag][D[tag]["t"] >= D[tag]["t"][-1] - 3.0] ** 2))),
                   amp10=m10(D[tag]["t"], E[tag]))
json.dump(js, open("_b0new_cmp.json", "w"), indent=1)
for k, v in js.items():
    print("%-9s b0=%7.1f (%+6.1f%%)  RMS=%6.2f  10Hz=%5.2f" % (k, v["b0"], v["err"], v["rms"], v["amp10"]))
print("saved fig_b0new_cmp.png")
