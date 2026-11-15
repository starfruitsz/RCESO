# -*- coding: utf-8 -*-
"""_t_dft_cmp.py —— 律T 基波幅值：带通 vs 整数周期 DFT 的对比图与统计。"""
import numpy as np, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.28, "grid.linewidth": 0.5,
    "legend.frameon": False, "legend.fontsize": 7.2,
})
Q = 5.0
cases = [("bpf", "带通 Q=5（现方案）", "#8a8f98"),
         ("dft1", "DFT m=1", "#c0392b"),
         ("dft2", "DFT m=2", "#d68910"),
         ("dft4", "DFT m=4", "#2471a3")]
D = {tag: np.load("_tdft_%s.npz" % tag) for tag, _, _ in cases}

# A 的标定：带通在 f0 的增益 = Q，除以 Q 后才能与 DFT 的“真 RMS”同轴比较
stats = {}
for tag, lab, c in cases:
    d = D[tag]; t = d["t"]; a = d["amp"]; es = d["es"]; y = d["y"]
    e = (y - 1.0) * 600.0
    m3 = t >= 3.0
    w = (t >= 25.0) & (t < 30.0)
    x = e[w] - e[w].mean()
    X = np.fft.rfft(x * np.hanning(len(x)))
    fr = np.fft.rfftfreq(len(x), d=float(t[1] - t[0]))
    k10 = int(np.argmin(np.abs(fr - 10.0)))
    amp10 = float(2.0 * np.abs(X[k10]) / np.sum(np.hanning(len(x))))
    q = (t >= 20.0) & (t < 25.0)
    stats[tag] = dict(nA=float(np.std(a[q])),
        
        rms=float(np.sqrt(np.mean(e[m3] ** 2))), amp10=amp10,
        es_end=float(es[-1]), es_mean=float(es[t >= 25].mean()), es_std=float(es[t >= 25].std()),
        A_end=float(a[w].mean()), A_scale=float(a[w].mean() * (Q if tag == "bpf" else 1.0)))

# 带通 vs DFT 的 A 比值（检验 2× 泄漏）
tb = D["bpf"]["t"]; ab = D["bpf"]["amp"] / Q
ad = D["dft2"]["amp"]
mm = (tb >= 6.0) & (tb < 10.0)
ratio = float(np.mean(ab[mm] / np.maximum(ad[mm], 1e-9)))
print("A_bpf/Q ÷ A_dft2 (6-10 s 均值) = %.2f" % ratio)

fig, ax = plt.subplots(1, 3, figsize=(12.6, 3.4), gridspec_kw=dict(width_ratios=[1.2, 1.0, 0.8]))
a0, a1, a2 = ax

for tag, lab, c in cases:
    d = D[tag]; t = d["t"]; a = d["amp"] / (Q if tag == "bpf" else 1.0)
    m = (t >= 5.0) & (t < 9.0)
    a0.plot(t[m], a[m], color=c, lw=0.8, label=lab)
a0.set_xlim(5, 9); a0.set_ylim(0.0005, 0.0048)
a0.set_xlabel("时间 / s"); a0.set_ylabel("$A$（已按 $1/Q$ 标定）")
a0.set_title("(a) 基波幅值：带通 vs 整数周期 DFT（m=1 噪声最大）", fontsize=8.6)
a0.legend(loc="upper left", fontsize=6.6, ncol=2, columnspacing=0.8)

def movmean(x, n):
    c = np.concatenate(([0.0], np.cumsum(x)))
    y = c[n:] - c[:-n]
    return np.concatenate((np.full(n - 1, y[0]), y)) / n

for tag, lab, c in cases:
    d = D[tag]; t = d["t"][::100]; es = d["es"][::100]
    n1p5 = int(round(1.5 / (t[1] - t[0])))
    a1.plot(t, movmean(es, n1p5), color=c, lw=1.2, label=lab)
a1.axhline(-0.143, color="#2e4053", ls=":", lw=0.9)
a1.text(0.6, -0.140, "理论 $\\delta^{*}$ = −14.3%", fontsize=6.3, color="#2e4053", va="bottom")
a1.set_xlim(0, 30); a1.set_ylim(-0.175, -0.095); a1.set_ylabel("$\\hat{\\delta}$")
a1.set_xlabel("时间 / s")
a1.set_title("(b) 极值搜索收敛轨迹（1.5 s 滑动平均去掉 dither）", fontsize=8.6)
a1.legend(loc="upper left", fontsize=6.2, ncol=2, columnspacing=0.8)

x = np.arange(len(cases)); w = 0.38
rms = [stats[k]["rms"] for k, _, _ in cases]
amp10 = [stats[k]["amp10"] for k, _, _ in cases]
b1 = a2.bar(x - w/2, rms, w, color="#7f8c8d", label="3–30 s RMS")
b2 = a2.bar(x + w/2, amp10, w, color="#c0392b", label="25–30 s 10 Hz")
for bb, v in list(zip(b1, rms)) + list(zip(b2, amp10)):
    a2.text(bb.get_x()+bb.get_width()/2, v+0.6, "%.1f" % v, ha="center", fontsize=5.8)
a2.set_xticks(x); a2.set_xticklabels(["带通", "m=1", "m=2", "m=4"], fontsize=7.0)
a2.set_ylabel("rpm"); a2.set_ylim(0, 31)
a2.set_title("(c) 残余指标", fontsize=8.6)
a2.legend(loc="upper right", fontsize=6.0)

fig.suptitle("律T 基波幅值观测器：±10% 带通（Q=5） vs 整数机械周期 DFT（600 rpm、30 s、组合故障、dither ESC）",
             fontsize=9.4, y=1.02)
fig.tight_layout(); fig.savefig("fig_t_dft.png", bbox_inches="tight")
json.dump(dict(ratio=ratio, stats=stats), open("_t_dft_cmp.json", "w"), indent=1)
for tag, lab, c in cases:
    s = stats[tag]
    print("%-5s RMS %5.2f  10Hz %5.2f  es %.4f±%.4f  A_end %.4f  A噪声 %.5f" % (
        tag, s["rms"], s["amp10"], s["es_mean"], s["es_std"], s["A_end"], s["nA"]))
print("saved fig_t_dft.png")
