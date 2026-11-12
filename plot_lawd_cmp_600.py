# -*- coding: utf-8 -*-
"""plot_lawd_cmp_600.py —— 律 D（带宽自适应）对加载的改善（1920×960）"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

N_REF = 600.0
C_BASE, C_LAWD, C_LOAD = "#1f4e79", "#e67e22", "#34495e"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.8,
    "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False,
})

d = np.load("_wave_lawd_cmp_600.npz")
t = np.asarray(d["t"])
dec = max(1, int(round(1e-3 / (t[1] - t[0]))))
ts = t[::dec]
y_b = np.asarray(d["y_base"]); y_l = np.asarray(d["y_lawd"])
iq_b = np.asarray(d["iq_base"]); iq_l = np.asarray(d["iq_lawd"])
tl = np.asarray(d["tl"])
eb_full = (y_b - 1.0) * N_REF
el_full = (y_l - 1.0) * N_REF
eb = eb_full[::dec]; el = el_full[::dec]
iqb = iq_b[::dec]; iql = iq_l[::dec]


def metrics(e, iq, tt):
    m = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(e[m]))
    i0_full = int(np.where(m)[0][int(np.argmin(e[m]))])
    idx = np.where((np.abs(e) <= 20.0) & (np.arange(len(e)) > i0_full) & (tt >= 2.0))[0]
    rec = float(tt[idx[0]] - 2.0) * 1e3 if len(idx) else np.nan
    return dict(dip=dip, rec_ms=rec,
                step_rms=float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))),
                iq_max=float(np.max(np.abs(iq))),
                steady=float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2))))


mb = metrics(eb_full, iq_b, t)
ml = metrics(el_full, iq_l, t)

fig = plt.figure(figsize=(12.8, 6.4))
gs = fig.add_gridspec(2, 3, width_ratios=[1.05, 1.05, 0.9],
                      left=0.055, right=0.985, top=0.865, bottom=0.095,
                      wspace=0.30, hspace=0.42)
ax_a = fig.add_subplot(gs[0, :2])
ax_b = fig.add_subplot(gs[0, 2])
ax_c = fig.add_subplot(gs[1, 0])
ax_d = fig.add_subplot(gs[1, 1])
ax_e = fig.add_subplot(gs[1, 2])

# (a) 0–8 s 绝对转速
ax_a.axvline(2.0, color="#7f8c8d", ls="--", lw=0.9)
ax_a.plot(ts, 600 + eb, color=C_BASE, lw=2.4, alpha=0.55, label="无自适应（$k_p$、$\\omega_o$ 固定；跌落 %.0f rpm）" % mb["dip"])
ax_a.plot(ts, 600 + el, color=C_LAWD, lw=1.2, label="律 D（$k_p$×8 + $\\omega_o$×3 调度；跌落 %.0f rpm）" % ml["dip"])
tdip_b = ts[int(np.argmin(eb[(ts >= 1.9) & (ts <= 2.5)])) + int(np.where(ts >= 1.9)[0][0])]

ax_a.set_xlim(0, 8); ax_a.set_ylim(150, 700)
ax_a.set_xlabel("时间 / s"); ax_a.set_ylabel("转速 / rpm")
ax_a.legend(fontsize=7.4, loc="lower right", ncol=2)
ax_a.set_title("(a) 加载前后的绝对转速（2 s 阶跃 0.50 额定；其余条件相同）", fontsize=8.8)

# (b) 指标表
ax_b.axis("off")
ax_b.set_title("(b) 加载指标（本图实测）", fontsize=8.8)
rows = [
    ("加载跌落 / rpm", "%.1f" % mb["dip"], "%.1f" % ml["dip"],
     "%+.1f%%" % (100 * (ml["dip"] / mb["dip"] - 1)), True),
    ("恢复至 ±20 rpm / ms", "%.1f" % mb["rec_ms"], "%.1f" % ml["rec_ms"],
     "%+.1f%%" % (100 * (ml["rec_ms"] / mb["rec_ms"] - 1)), True),
    ("突变窗 RMS / rpm", "%.1f" % mb["step_rms"], "%.1f" % ml["step_rms"],
     "%+.1f%%" % (100 * (ml["step_rms"] / mb["step_rms"] - 1)), True),
    ("$|i_q|$ 峰值 / A（额定 6.31）", "%.2f" % mb["iq_max"], "%.2f" % ml["iq_max"],
     "%+.1f%%" % (100 * (ml["iq_max"] / mb["iq_max"] - 1)), False),
    ("稳态 7–8 s / rpm", "%.2f" % mb["steady"], "%.2f" % ml["steady"],
     "%+.1f%%" % (100 * (ml["steady"] / mb["steady"] - 1)), True),
]
ax_b.text(0.02, 1.00, "指标", fontsize=7.4, va="top", weight="bold")
ax_b.text(0.47, 1.00, "无自适应", fontsize=7.4, va="top", color=C_BASE, weight="bold")
ax_b.text(0.69, 1.00, "律 D", fontsize=7.4, va="top", color=C_LAWD, weight="bold")
ax_b.text(1.00, 1.00, "变化", fontsize=7.4, va="top", ha="right", weight="bold")
for i, (nm, a, b, ch, good) in enumerate(rows):
    yv = 0.83 - i * 0.165
    ax_b.text(0.02, yv, nm, fontsize=7.0, va="center")
    ax_b.text(0.47, yv, a, fontsize=7.0, va="center", color=C_BASE)
    ax_b.text(0.69, yv, b, fontsize=7.0, va="center", color=C_LAWD)
    ax_b.text(1.00, yv, ch, fontsize=6.8, va="center", ha="right",
              color=("#c0392b" if good else "#7f8c8d"))
ax_b.set_xlim(0, 1.02); ax_b.set_ylim(0, 1.05)

# (c) 转速误差放大
m = (ts >= 1.95) & (ts <= 2.60)
ax_c.plot(ts[m], eb[m], color=C_BASE, lw=1.9, alpha=0.75, label="无自适应")
ax_c.plot(ts[m], el[m], color=C_LAWD, lw=1.1, label="律 D")
ax_c.axhline(-20, color="#7f8c8d", ls=":", lw=0.8)
ax_c.axhline(20, color="#7f8c8d", ls=":", lw=0.8)
ax_c.set_xlabel("时间 / s"); ax_c.set_ylabel("转速误差 / rpm")
ax_c.set_title("(c) 加载瞬态误差（±20 rpm 为恢复判据）", fontsize=8.8)
ax_c.legend(fontsize=7.0, loc="lower right", ncol=2)

# (d) iq 电流
ax_d.plot(ts[m], iqb[m], color=C_BASE, lw=1.1, label="无自适应")
ax_d.plot(ts[m], iql[m], color=C_LAWD, lw=1.1, label="律 D")
ax_d.axhline(6.31, color="#c0392b", ls=":", lw=0.9)
ax_d.text(1.97, 6.42, "额定 6.31 A", fontsize=6.8, color="#c0392b")
ax_d.set_ylim(-0.6, 7.0)
ax_d.set_xlabel("时间 / s"); ax_d.set_ylabel("$i_q$ / A")
ax_d.set_title("(d) 加载瞬态的 $i_q$（电流代价）", fontsize=8.8)
ax_d.legend(fontsize=7.0, loc="upper right", ncol=2)

# (e) 稳态 7–8 s
m2 = (ts >= 7.0) & (ts <= 8.0)
ax_e.plot(ts[m2], eb[m2], color=C_BASE, lw=1.6, alpha=0.75, label="无自适应")
ax_e.plot(ts[m2], el[m2], color=C_LAWD, lw=0.9, label="律 D")
ax_e.set_xlabel("时间 / s"); ax_e.set_ylabel("转速误差 / rpm")
ax_e.set_title("(e) 稳态 7–8 s（不劣化）", fontsize=8.8)
ax_e.legend(fontsize=7.0, loc="upper right", ncol=2)

fig.suptitle("600 rpm 实验室工况：律 D（$k_p$ + ESO 带宽自适应）对加载的改善（8 s，种子 20261018）",
             fontsize=10.6, y=0.955)
fig.savefig("fig_lawd_cmp_600.png", dpi=150, facecolor="white")
try:
    from PIL import Image
    Image.open("fig_lawd_cmp_600.png").convert("RGB").save("fig_lawd_cmp_600.png")
except Exception:
    pass

json.dump(dict(base=mb, lawd=ml), open("_lawd_cmp_600_metrics.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("ok: fig_lawd_cmp_600.png")
print("base", mb); print("lawd", ml)
