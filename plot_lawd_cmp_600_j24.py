# -*- coding: utf-8 -*-
"""plot_lawd_cmp_600_j24.py —— 真实 J（4.81e-5=2.545 J_nom）+ oracle：律 D 对加载的改善（1920×960）

输入 _wave_lawd_cmp_600_j24.npz（run_realj_tables.py 里 base 与 a3kb6 两例的波形）
输出 fig_lawd_cmp_600.png（报告 §9 用的正式文件名，覆盖旧 J_nom 版）、_lawd_cmp_600_j24_metrics.json
"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

J_TRUE = 4.81e-5
J_NOM = 1.89e-5
d = np.load("_wave_lawd_cmp_600_j24.npz")
t = np.asarray(d["t"])
dec = max(1, int(round(1e-3 / (t[1] - t[0]))))
ts = t[::dec]
y_b = np.asarray(d["y_base"]); y_l = np.asarray(d["y_lawd"])
iq_b = np.asarray(d["iq_base"]); iq_l = np.asarray(d["iq_lawd"])
tl = np.asarray(d["tl"])[::dec]
eb_full = (y_b - 1.0) * N_REF
el_full = (y_l - 1.0) * N_REF
eb = eb_full[::dec]; el = el_full[::dec]
iqb = iq_b[::dec]; iql = iq_l[::dec]


def iq1ms(iq, t):
    n = 100                       # 10 us x 100 = 1 ms（速度环一拍）
    m = len(iq) // n * n
    av = np.abs(iq[:m].reshape(-1, n).mean(axis=1))
    ts_ = t[:m:n] + 0.5e-3
    return float(av.max()), float(ts_[int(av.argmax())])


def metrics(e, iq, tt):
    m = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(e[m]))
    i0 = int(np.where(m)[0][int(np.argmin(e[m]))])
    idx = np.where((np.abs(e) <= 20.0) & (np.arange(len(e)) > i0) & (tt >= 2.0))[0]
    rec = float(tt[idx[0]] - 2.0) * 1e3 if len(idx) else float("nan")
    a1, t1 = iq1ms(iq, tt)
    return dict(dip=dip, rec_ms=rec,
                step_rms=float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))),
                iq_max=float(np.max(np.abs(iq))),
                iq1ms=a1, iq1ms_t=t1,
                steady=float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2))))


mb = metrics(eb_full, iq_b, t)
ml = metrics(el_full, iq_l, t)

fig = plt.figure(figsize=(12.8, 6.4))
gs = fig.add_gridspec(3, 3, left=0.055, right=0.985, top=0.872, bottom=0.075,
                      height_ratios=[1.0, 0.95, 0.95], wspace=0.30, hspace=0.55)
ax_a = fig.add_subplot(gs[0, :2])
ax_b = fig.add_subplot(gs[0, 2])
ax_c = fig.add_subplot(gs[1, :2])
ax_d = fig.add_subplot(gs[1, 2])
ax_e = fig.add_subplot(gs[2, :2])
ax_f = fig.add_subplot(gs[2, 2])

# (a) 0–8 s 绝对转速
ax_a.axvline(2.0, color="#7f8c8d", ls="--", lw=0.9)
ax_a.plot(ts, 600 + eb, color=C_BASE, lw=2.4, alpha=0.55,
          label="无自适应（$k_p$、$\\omega_o$ 固定；跌落 %.0f rpm）" % mb["dip"])
ax_a.plot(ts, 600 + el, color=C_LAWD, lw=1.2,
          label="律 D（$k_b=6$、$a=3$；跌落 %.0f rpm）" % ml["dip"])
ax_a.set_xlim(0, 8); ax_a.set_ylim(420, 680)
ax_a.set_xlabel("时间 / s"); ax_a.set_ylabel("转速 / rpm")
ax_a.legend(fontsize=7.2, loc="lower right", ncol=1)
ax_a.set_title("(a) 加载前后的绝对转速（2 s 阶跃 0.50 额定；其余条件相同）", fontsize=8.8)

# (b) 指标表
ax_b.axis("off")
ax_b.set_title("(b) 加载指标（本图实测；额定 $|i_q|$=6.31 A）", fontsize=8.8)
rows = [
    ("加载跌落 / rpm", "%.1f" % mb["dip"], "%.1f" % ml["dip"],
     "%+.1f%%" % (100 * (ml["dip"] / mb["dip"] - 1)), True),
    ("恢复至 ±20 rpm / ms", "%.1f" % mb["rec_ms"], "%.1f" % ml["rec_ms"],
     "%+.1f%%" % (100 * (ml["rec_ms"] / mb["rec_ms"] - 1)), True),
    ("突变窗 RMS / rpm", "%.1f" % mb["step_rms"], "%.1f" % ml["step_rms"],
     "%+.1f%%" % (100 * (ml["step_rms"] / mb["step_rms"] - 1)), True),
    ("$|i_q|$ 原始峰值 / A（10 us）", "%.2f" % mb["iq_max"], "%.2f" % ml["iq_max"],
     "%+.1f%%" % (100 * (ml["iq_max"] / mb["iq_max"] - 1)), False),
    ("$|i_q|$ 1 ms 均值峰值 / A", "%.2f" % mb["iq1ms"], "%.2f" % ml["iq1ms"],
     "%+.1f%%" % (100 * (ml["iq1ms"] / mb["iq1ms"] - 1)), True),
    ("稳态 7–8 s / rpm", "%.2f" % mb["steady"], "%.2f" % ml["steady"],
     "%+.1f%%" % (100 * (ml["steady"] / mb["steady"] - 1)), True),
]
ax_b.text(0.02, 1.00, "指标", fontsize=7.3, va="top", weight="bold")
ax_b.text(0.47, 1.00, "无自适应", fontsize=7.3, va="top", color=C_BASE, weight="bold")
ax_b.text(0.69, 1.00, "律 D", fontsize=7.3, va="top", color=C_LAWD, weight="bold")
ax_b.text(1.00, 1.00, "变化", fontsize=7.3, va="top", ha="right", weight="bold")
for i, (nm, a, b, ch, good) in enumerate(rows):
    yv = 0.83 - i * 0.165
    ax_b.text(0.02, yv, nm, fontsize=6.9, va="center")
    ax_b.text(0.47, yv, a, fontsize=7.0, va="center", color=C_BASE)
    ax_b.text(0.69, yv, b, fontsize=7.0, va="center", color=C_LAWD)
    ax_b.text(1.00, yv, ch, fontsize=6.7, va="center", ha="right",
              color=("#c0392b" if good else "#7f8c8d"))
ax_b.set_xlim(0, 1.02); ax_b.set_ylim(0, 1.05)

# (c) 负载曲线
ax_c.axvspan(0, 2, color="#bdc3c7", alpha=0.25, lw=0)
ax_c.plot(ts, tl, color=C_LOAD, lw=0.7)
ax_c.text(0.55, 0.06, "空载", fontsize=7.0, color="#7f8c8d")
ax_c.text(2.6, 0.045, "2 s 阶跃 0.3185 N·m（0.50 额定）＋ 圆盘型线 V2（峰值 0.095 N·m）＋ 5.9 Hz 振动（0.03 N·m）＋ 负载噪声",
          fontsize=6.4, color=C_LOAD,
          bbox=dict(facecolor="white", alpha=0.78, edgecolor="none", pad=1.6))
ax_c.set_xlim(0, 8); ax_c.set_ylim(0, 0.5)
ax_c.set_xlabel("时间 / s"); ax_c.set_ylabel("负载转矩 / N·m")
ax_c.set_title("(c) 负载曲线（实测峰值 %.3f N·m）" % float(np.max(tl)), fontsize=8.8)

# (d) 加载瞬态误差
m = (ts >= 1.95) & (ts <= 2.60)
ax_d.plot(ts[m], eb[m], color=C_BASE, lw=1.9, alpha=0.75, label="无自适应")
ax_d.plot(ts[m], el[m], color=C_LAWD, lw=1.1, label="律 D")
ax_d.axhline(-20, color="#7f8c8d", ls=":", lw=0.8)
ax_d.axhline(20, color="#7f8c8d", ls=":", lw=0.8)
ax_d.set_xlabel("时间 / s"); ax_d.set_ylabel("转速误差 / rpm")
ax_d.set_title("(d) 加载瞬态误差（±20 rpm）", fontsize=8.8)
ax_d.legend(fontsize=6.8, loc="lower right", ncol=2)

# (e) iq
m2 = (ts >= 1.8) & (ts <= 3.0)
ax_e.plot(ts[m2], iqb[m2], color=C_BASE, lw=1.6, alpha=0.75, label="无自适应")
ax_e.plot(ts[m2], iql[m2], color=C_LAWD, lw=1.0, label="律 D")
ax_e.axhline(6.31, color="#c0392b", ls=":", lw=0.9)
ax_e.text(1.82, 6.42, "额定 6.31 A", fontsize=6.8, color="#c0392b")
ax_e.set_ylim(-0.6, 7.4)
ax_e.set_xlabel("时间 / s"); ax_e.set_ylabel("$i_q$ / A")
ax_e.set_title("(e) 加载瞬态的 $i_q$（电流代价）", fontsize=8.8)
ax_e.legend(fontsize=6.8, loc="lower right", ncol=2)

# (f) 稳态 7–8 s
m3 = (ts >= 7.0) & (ts <= 8.0)
ax_f.plot(ts[m3], eb[m3], color=C_BASE, lw=1.6, alpha=0.75, label="无自适应")
ax_f.plot(ts[m3], el[m3], color=C_LAWD, lw=0.9, label="律 D")
ax_f.set_xlabel("时间 / s"); ax_f.set_ylabel("转速误差 / rpm")
ax_f.set_title("(f) 稳态 7–8 s（RMS +2.3%）", fontsize=8.8)
ax_f.legend(fontsize=6.8, loc="upper right", ncol=2)

fig.suptitle("600 rpm 实验室工况（J_true=4.81e-5=2.545 J_nom、j_oracle=True，b0 按真实 J 归一；"
             "i_q 取 1 ms 包络）：律 D 对加载的改善（8 s，种子 20261018）",
             fontsize=9.8, y=0.955)
fig.savefig("fig_lawd_cmp_600.png", dpi=150, facecolor="white")
try:
    from PIL import Image
    Image.open("fig_lawd_cmp_600.png").convert("RGB").save("fig_lawd_cmp_600.png")
except Exception:
    pass

json.dump(dict(base=mb, lawd=ml, tl_peak=float(np.max(tl)),
               tl_mean_loaded=float(np.mean(tl[ts >= 3.0]))),
          open("_lawd_cmp_600_j24_metrics.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok: fig_lawd_cmp_600.png")
print("base", mb); print("lawd", ml)