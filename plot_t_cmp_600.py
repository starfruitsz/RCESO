# -*- coding: utf-8 -*-
"""plot_t_cmp_600.py —— 600 rpm 实验室：T 自适应 vs 无自适应（1920×960）"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

N_REF = 600.0
C_BASE, C_ESC = "#1f4e79", "#16a085"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2,
    "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False,
})

d = np.load("_wave_t_cmp_600.npz")
t = np.asarray(d["t"])
dec = max(1, int(round(1e-3 / (t[1] - t[0]))))
ts = t[::dec]
y_b = np.asarray(d["y_base"]); y_e = np.asarray(d["y_esc"])
A_b = np.asarray(d["amp_base"]); A_e = np.asarray(d["amp_esc"])
es = np.asarray(d["es_esc"])
eb_full = (y_b - 1.0) * N_REF
ee_full = (y_e - 1.0) * N_REF
eb = eb_full[::dec]; ee = ee_full[::dec]
Ab = A_b[::dec]; Ae = A_e[::dec]; es_s = es[::dec]


def metrics(e, A, tt):
    m = tt >= 25.0
    rms = float(np.sqrt(np.mean(e[m] ** 2)))
    tc = tt[m]
    a = 2.0 * np.mean(e[m] * np.sin(2 * np.pi * 10.0 * tc))
    b = 2.0 * np.mean(e[m] * np.cos(2 * np.pi * 10.0 * tc))
    return dict(rms=rms, amp10=float(np.hypot(a, b)), A=float(np.mean(A[tt >= 20.0])))


mb = metrics(eb_full, A_b, t)
me = metrics(ee_full, A_e, t)


def env_minmax(x, tt, bin_s=0.01):
    n = int(round(bin_s / (tt[1] - tt[0])))
    m = (len(x) // n) * n
    r = x[:m].reshape(-1, n)
    return tt[:m].reshape(-1, n).mean(1), r.min(1), r.max(1)


def demod_env(e, tt, f=10.0, win=0.2):
    z = e * np.exp(-1j * 2 * np.pi * f * tt)
    n = max(1, int(round(win / (tt[1] - tt[0]))))
    return 2.0 * np.abs(np.convolve(z, np.ones(n) / n, mode="same"))


def band10(e, tt, f=10.0, win=0.1):
    n = max(1, int(round(win / (tt[1] - tt[0]))))
    k = np.ones(n) / n
    a = 2.0 * np.convolve(e * np.cos(2 * np.pi * f * tt), k, mode="same")
    b = 2.0 * np.convolve(e * np.sin(2 * np.pi * f * tt), k, mode="same")
    return a * np.cos(2 * np.pi * f * tt) + b * np.sin(2 * np.pi * f * tt)


tm_b, mn_b, mx_b = env_minmax(600 + eb, ts)
tm_e, mn_e, mx_e = env_minmax(600 + ee, ts)
env_b = demod_env(eb, ts)
env_e = demod_env(ee, ts)
x10_b = band10(eb, ts)
x10_e = band10(ee, ts)

fig = plt.figure(figsize=(12.8, 6.4))
gs = fig.add_gridspec(2, 3, width_ratios=[1.05, 1.05, 0.9], height_ratios=[1, 1],
                      left=0.055, right=0.985, top=0.855, bottom=0.10,
                      wspace=0.30, hspace=0.48)
ax_a = fig.add_subplot(gs[0, :2])
ax_b = fig.add_subplot(gs[0, 2])
ax_c = fig.add_subplot(gs[1, 0])
ax_d = fig.add_subplot(gs[1, 1])
ax_e = fig.add_subplot(gs[1, 2])

# (a) 完整转速（10 ms 包络）
ax_a.axvspan(25, 30, color="#16a085", alpha=0.07, lw=0)
ax_a.fill_between(tm_b, mn_b, mx_b, color=C_BASE, alpha=0.30, lw=0)
ax_a.fill_between(tm_e, mn_e, mx_e, color=C_ESC, alpha=0.55, lw=0)
ax_a.plot(tm_b, 600 + (mn_b + mx_b) / 2 - 600 + 600, color=C_BASE, lw=0.7, alpha=0.0)
ax_a.axvline(2.0, color="#7f8c8d", ls="--", lw=0.9)
ax_a.axvline(3.0, color="#c0392b", ls=":", lw=1.0)
sel = tm_b >= 1.95
ymin = min(mn_b[sel].min(), mn_e[sel].min()); ymax = max(mx_b[sel].max(), mx_e[sel].max())
pad = 0.08 * (ymax - ymin)
ax_a.set_ylim(ymin - pad, ymax + pad)
ax_a.set_xlim(1.95, 30)
axin = ax_a.inset_axes([0.16, 0.20, 0.29, 0.36])
m2 = (ts >= 1.95) & (ts <= 2.60)
axin.plot(ts[m2], 600 + eb[m2], color=C_BASE, lw=0.9)
axin.plot(ts[m2], 600 + ee[m2], color=C_ESC, lw=0.9)
axin.set_facecolor("white")
axin.tick_params(labelsize=6.0, length=2)
axin.grid(alpha=0.15)
axin.set_title("加载瞬态放大（1.95–2.60 s）", fontsize=6.8, pad=2)
ax_a.set_xlabel("时间 / s"); ax_a.set_ylabel("转速 / rpm")
ax_a.legend(handles=[Patch(color=C_BASE, alpha=0.30, label="无自适应（$\\delta$=0）"),
                     Patch(color=C_ESC, alpha=0.55, label="T 自适应（ESC）")],
            fontsize=7.8, loc="lower right", ncol=2)
ax_a.set_title("(a) 完整转速：10 ms min–max 包络（灰虚线=2 s 加载，红点线=3 s ESC 启动）", fontsize=9.0)

# (b) 残差指标（横向条）
names = ["稳态 RMS\n(25–30 s)", "10 Hz 残余\n(25–30 s)", "基波残余 $A$\n(20–30 s)"]
vb = [mb["rms"], mb["amp10"], mb["A"] * 1e3]
ve = [me["rms"], me["amp10"], me["A"] * 1e3]
ypos = np.arange(3)[::-1]
h = 0.32
ax_b.barh(ypos + h / 2, vb, h, color=C_BASE, alpha=0.9, label="无自适应")
ax_b.barh(ypos - h / 2, ve, h, color=C_ESC, alpha=0.9, label="T 自适应")
vmax = max(vb) * 1.42
for i, yv in enumerate(ypos):
    ax_b.text(vb[i] + 0.02 * vmax, yv + h / 2, "%.2f" % vb[i], va="center", fontsize=7.6, color=C_BASE)
    ax_b.text(ve[i] + 0.02 * vmax, yv - h / 2, "%.2f" % ve[i], va="center", fontsize=7.6, color=C_ESC)
    drop = 100 * (1 - ve[i] / vb[i])
    ax_b.text(vb[i] + 0.16 * vmax, yv, "−%.1f%%" % drop, va="center", fontsize=8.2, color="#c0392b")
ax_b.set_yticks(ypos); ax_b.set_yticklabels(names, fontsize=7.6)
ax_b.set_xlim(0, vmax * 1.18)
ax_b.set_xlabel("数值（rpm / $A\\times10^{-3}$）")
ax_b.legend(fontsize=7.4, loc="lower right")
ax_b.set_title("(b) 残差指标对比", fontsize=9.0)

# (c) 稳态 10 Hz 分量
m = (ts >= 26.0) & (ts <= 27.0)
ax_c.plot(ts[m], x10_b[m], color=C_BASE, lw=1.2, label="无自适应")
ax_c.plot(ts[m], x10_e[m], color=C_ESC, lw=1.2, label="T 自适应")
ax_c.set_xlabel("时间 / s"); ax_c.set_ylabel("10 Hz 分量 / rpm")
ax_c.set_title("(c) 稳态 10 Hz 分量（26–27 s）", fontsize=9.0)
ax_c.legend(fontsize=7.2, loc="upper left", ncol=2, frameon=True, framealpha=0.85, edgecolor="none")

# (d) 10 Hz 包络
ax_d.plot(ts, env_b, color=C_BASE, lw=1.1, label="无自适应")
ax_d.plot(ts, env_e, color=C_ESC, lw=1.1, label="T 自适应")
ax_d.axvspan(25, 30, color="#16a085", alpha=0.07, lw=0)
ax_d.axvline(3.0, color="#c0392b", ls=":", lw=1.0)
ax_d.set_xlim(0, 30); ax_d.set_ylim(0, 80)
ax_d.set_xlabel("时间 / s"); ax_d.set_ylabel("10 Hz 包络 / rpm")
ax_d.set_title("(d) 10 Hz 残余包络（200 ms 滑动解调）", fontsize=9.0)
ax_d.legend(fontsize=7.6, loc="upper right")

# (e) δ 轨迹
ax_e.plot(ts, es_s * 100, color=C_ESC, lw=1.2, label="ESC（$\\Delta$=0.5%，$\\sigma$=1%）")
ax_e.axhline(-12.0, color="#7f8c8d", ls=":", lw=1.0)
ax_e.text(6.0, -11.3, "扫描最优 −12%", fontsize=7.4, color="#7f8c8d")
ax_e.set_xlim(0, 30); ax_e.set_ylim(-17, -9.5)
ax_e.set_xlabel("时间 / s"); ax_e.set_ylabel("$\\delta$ / %")
ax_e.set_title("(e) 周期修正 $\\delta$ 的收敛", fontsize=9.0)
ax_e.text(0.03, 0.06, "末段 $\\delta$≈%.1f%%，峰峰 %.1f%%" % (100*np.mean(es_s[ts>=20.0]),
           100*np.ptp(es_s[ts>=20.0])), transform=ax_e.transAxes, ha="left", fontsize=7.4, color="#c0392b")
ax_e.legend(fontsize=7.4, loc="lower right")

fig.suptitle("600 rpm 实验室工况：T 自适应 vs 无自适应（圆盘型线 V2，$f_{ci}$=500 Hz，30 s）",
             fontsize=11.0, y=0.955)
fig.savefig("fig_t_cmp_600.png", dpi=150, facecolor="white")
try:
    from PIL import Image
    Image.open("fig_t_cmp_600.png").convert("RGB").save("fig_t_cmp_600.png")
except Exception:
    pass

json.dump(dict(base=mb, esc=me, d_mean=float(np.mean(es_s[ts >= 20.0])),
               d_p2p=float(np.ptp(es_s[ts >= 20.0]))),
          open("_t_cmp_600_metrics.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok: fig_t_cmp_600.png")
print("base", mb); print("esc ", me)
