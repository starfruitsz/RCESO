# -*- coding: utf-8 -*-
"""plot_four_cmp_600.py —— 四档对比（负载突变 + 参考转速突变）（1920×960）"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N_REF, N_REF2, TNREF = 600.0, 900.0, 15.0
CFG = [("base", "无自适应", "#1f4e79", "-", 1.5),
       ("T", "T 自适应", "#16a085", (0, (5, 2)), 1.2),
       ("D", "律 D", "#e67e22", "-", 1.2),
       ("DT", "T + 律 D", "#8e44ad", (0, (5, 2)), 1.3)]
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.8,
    "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False,
})

D = {k: np.load("_wave_4cmp2_600_%s.npz" % k) for k, *_ in CFG}
t = np.asarray(D["base"]["t"])
dec = max(1, int(round(1e-3 / (t[1] - t[0]))))
ts = t[::dec]


def series(k):
    spd = np.asarray(D[k]["y"]) * N_REF
    iq = np.asarray(D[k]["iq"])
    A = np.asarray(D[k]["amp"]) * N_REF
    return spd, spd[::dec], iq, A[::dec]


def metrics(spd, iq, A, tt, ta):
    m = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(spd[m] - N_REF))
    i0 = int(np.where(m)[0][int(np.argmin(spd[m] - N_REF))])
    idx = np.where((np.abs(spd - N_REF) <= 20.0) & (np.arange(len(spd)) > i0) & (tt >= 2.0))[0]
    rec = float(tt[idx[0]] - 2.0) * 1e3 if len(idx) else float("nan")
    idx2 = np.where((np.abs(spd - N_REF2) <= 20.0) & (tt >= TNREF))[0]
    tset = float(tt[idx2[0]] - TNREF) * 1e3 if len(idx2) else float("nan")
    over = float(np.max(spd[(tt >= TNREF) & (tt <= TNREF + 6.0)] - N_REF2))
    return dict(dip=dip, rec_ms=rec, tset_ms=tset, overshoot=over,
                step_rms=float(np.sqrt(np.mean((spd[(tt >= 2.0) & (tt < 2.5)] - N_REF) ** 2))),
                amp_res=float(np.mean(A[ta >= 25.0])),
                steady=float(np.sqrt(np.mean((spd[tt >= 25.0] - N_REF2) ** 2))),
                iq_max=float(np.max(np.abs(iq))))


S, Ss, Q, AA = {}, {}, {}, {}
M = {}
for k, *_ in CFG:
    S[k], Ss[k], Q[k], AA[k] = series(k)
    M[k] = metrics(S[k], Q[k], AA[k], t, ts)


def bin_mean(x, tt, bs=0.01):
    n = int(round(bs / (tt[1] - tt[0])))
    m = (len(x) // n) * n
    return tt[:m].reshape(-1, n).mean(1), x[:m].reshape(-1, n).mean(1)


fig = plt.figure(figsize=(12.8, 6.4))
gs = fig.add_gridspec(3, 3, left=0.055, right=0.985, top=0.872, bottom=0.075,
                      height_ratios=[1.05, 1.0, 0.95], wspace=0.30, hspace=0.58)
ax_a = fig.add_subplot(gs[0, :])
ax_b = fig.add_subplot(gs[1, 0])
ax_c = fig.add_subplot(gs[1, 1])
ax_d = fig.add_subplot(gs[1, 2])
ax_e = fig.add_subplot(gs[2, :2])
ax_f = fig.add_subplot(gs[2, 2])

# (a) 完整转速
for k, lab, c, ls, lw in CFG:
    tm, ym = bin_mean(Ss[k], ts)
    ax_a.plot(tm, ym, color=c, ls=ls, lw=lw, label=lab)
ax_a.axvline(2.0, color="#7f8c8d", ls="--", lw=0.9)
ax_a.axvline(TNREF, color="#c0392b", ls=":", lw=1.0)
ax_a.axvspan(25, 30, color="#16a085", alpha=0.06, lw=0)
ax_a.axhline(N_REF2, color="#bdc3c7", ls=":", lw=0.8)
ax_a.set_xlim(0, 30); ax_a.set_ylim(150, 980)
ax_a.text(2.1, 200, "负载突变", fontsize=7.0, color="#7f8c8d")
ax_a.text(TNREF + 0.35, 700, "参考转速 600→900", fontsize=7.0, color="#c0392b")
ax_a.set_xlabel("时间 / s"); ax_a.set_ylabel("转速 / rpm")

ax_a.set_title("(a) 完整转速（10 ms 均值；2 s 负载突变，15 s 参考转速突变；绿底=稳态窗）", fontsize=8.8)

# (b) 负载突变
m = (ts >= 1.95) & (ts <= 2.60)
for k, lab, c, ls, lw in CFG:
    ax_b.plot(ts[m], Ss[k][m] - N_REF, color=c, ls=ls, lw=lw, label=lab)
ax_b.axhline(-20, color="#7f8c8d", ls=":", lw=0.8)
ax_b.axhline(20, color="#7f8c8d", ls=":", lw=0.8)
ax_b.set_xlabel("时间 / s"); ax_b.set_ylabel("转速误差 / rpm")
ax_b.set_title("(b) 负载突变瞬态（±20 rpm）", fontsize=8.8)

# (c) 换速瞬态
m2 = (ts >= 14.5) & (ts <= 18.0)
for k, lab, c, ls, lw in CFG:
    ax_c.plot(ts[m2], Ss[k][m2] - N_REF2, color=c, ls=ls, lw=lw, label=lab)
ax_c.axhline(0, color="#bdc3c7", ls=":", lw=0.9)
ax_c.axhline(20, color="#7f8c8d", ls=":", lw=0.7)
ax_c.axhline(-20, color="#7f8c8d", ls=":", lw=0.7)
ax_c.axvline(TNREF, color="#c0392b", ls=":", lw=0.9)
ax_c.set_xlabel("时间 / s"); ax_c.set_ylabel("相对 900 rpm 的误差 / rpm")
ax_c.set_title("(c) 换速瞬态（600→900 rpm，±20 rpm 带）", fontsize=8.8)

# (d) 基波残余 A
for k, lab, c, ls, lw in CFG:
    ax_d.plot(ts, AA[k], color=c, ls=ls, lw=0.9, label=lab)
ax_d.axvline(TNREF, color="#c0392b", ls=":", lw=0.9)
ax_d.axvspan(25, 30, color="#16a085", alpha=0.06, lw=0)
ax_d.set_xlim(0, 30)
ax_d.set_xlabel("时间 / s"); ax_d.set_ylabel("基波残余 A / rpm")
ax_d.set_title("(d) 基波残余 A（内模带通估计）", fontsize=8.8)

# (e) 指标表
ax_e.axis("off")
ax_e.set_title("(e) 四档指标（跌落/恢复在 2 s；换速在 15 s；其余取 25–30 s）", fontsize=8.8)
cols = [0.02, 0.40, 0.56, 0.72, 0.88]
ax_e.text(cols[0], 1.00, "指标", fontsize=7.4, va="top", weight="bold")
for j, (k, lab, c, ls, lw) in enumerate(CFG):
    ax_e.text(cols[j + 1], 1.00, lab, fontsize=7.2, va="top", color=c, weight="bold")
rows = [
    ("加载跌落 / rpm", ["%.1f" % M[k]["dip"] for k, *_ in CFG]),
    ("加载恢复 / ms", ["%.1f" % M[k]["rec_ms"] for k, *_ in CFG]),
    ("换速调节 / ms", ["%.1f" % M[k]["tset_ms"] for k, *_ in CFG]),
    ("换速超调 / rpm", ["%.1f" % M[k]["overshoot"] for k, *_ in CFG]),
    ("基波残余 / rpm", ["%.2f" % M[k]["amp_res"] for k, *_ in CFG]),
    ("稳态 RMS / rpm", ["%.2f" % M[k]["steady"] for k, *_ in CFG]),
    ("$|i_q|$ 峰值 / A", ["%.2f" % M[k]["iq_max"] for k, *_ in CFG]),
]
for i, (nm, vals) in enumerate(rows):
    yv = 0.84 - i * 0.120
    ax_e.text(cols[0], yv, nm, fontsize=6.9, va="center")
    for j, v in enumerate(vals):
        ax_e.text(cols[j + 1], yv, v, fontsize=6.9, va="center", color=CFG[j][2])
ax_e.set_xlim(0, 1.0); ax_e.set_ylim(0, 1.05)

# (f) δ 轨迹
for k, lab, c in (("T", "T 自适应", "#16a085"), ("DT", "T + 律 D", "#8e44ad")):
    es = np.asarray(D[k]["es"])[::dec]
    ax_f.plot(ts, es * 100, color=c, lw=1.1, label=lab)
ax_f.axvline(TNREF, color="#c0392b", ls=":", lw=0.9)
ax_f.set_xlim(0, 30); ax_f.set_ylim(-19.0, -11.0)
ax_f.set_xlabel("时间 / s"); ax_f.set_ylabel("$\\delta$ / %")
ax_f.set_title("(f) 周期修正 $\\delta$（15 s 前馈重置）", fontsize=8.8)
ax_f.text(TNREF + 0.5, -12.4, "冻结 + 前馈重置\n$\\delta$ → −17.2%", fontsize=6.6, color="#c0392b", va="top")
ax_f.legend(fontsize=6.8, loc="upper left")

from matplotlib.lines import Line2D
h = [Line2D([0], [0], color=c, ls=ls, lw=1.6, label=lab) for k, lab, c, ls, lw in CFG]
fig.legend(handles=h, loc="upper center", ncol=4, fontsize=8.0, bbox_to_anchor=(0.5, 0.935))
fig.suptitle("突变工况四档对比：2 s 负载突变 + 15 s 参考转速突变 600→900 rpm（圆盘型线 V2，30 s）",
             fontsize=10.4, y=0.975)
fig.savefig("fig_four_cmp_600.png", dpi=150, facecolor="white")
try:
    from PIL import Image
    Image.open("fig_four_cmp_600.png").convert("RGB").save("fig_four_cmp_600.png")
except Exception:
    pass

json.dump({k: M[k] for k, *_ in CFG}, open("_four_cmp_600_metrics.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("ok: fig_four_cmp_600.png")
for k, *_ in CFG:
    print(k, {kk: round(vv, 2) for kk, vv in M[k].items()})
