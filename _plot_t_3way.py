# -*- coding: utf-8 -*-
"""_plot_t_3way.py —— 律T 三口径对比（无律T / 巴特沃斯律T / DFT 律T），沿用 ppt_s13 版式。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C_B, C_O, C_G, C_N = "#1f4e79", "#e67e22", "#1e8449", "#c0392b"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.4, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.4,
})
ARCH = r"C:/Users/Administrator/Desktop/RCESO_archive_20261115/"

def load(f):
    z = np.load(f)
    t = np.asarray(z["t"]); dec = max(1, int(round(1e-3 / (t[1] - t[0]))))
    return dict(t=t[::dec], y=np.asarray(z["y"])[::dec], iq=np.asarray(z["iq"])[::dec],
                tl=np.asarray(z["tl"])[::dec], amp=np.asarray(z["amp"])[::dec],
                es=np.asarray(z["es"])[::dec])

def amp10(t, e, f=10.0, a=None, b=None):
    m = (t >= a) & (t < b) if a is not None else np.ones_like(t, bool)
    tt, ee = t[m], e[m]; w = 2*np.pi*f
    return float(np.hypot(2*np.mean(ee*np.cos(w*tt)), 2*np.mean(ee*np.sin(w*tt))))

b = load(ARCH + "_ppt5_s13_base.npz")
p = load(ARCH + "_tdft_bpf.npz")
d = load(ARCH + "_tdft_cal2.npz")
SER = [("无律T（δ≡0）", b, C_B), ("巴特沃斯律T", p, C_O), ("DFT 律T", d, C_G)]

fig = plt.figure(figsize=(12.8, 6.4))
gs = fig.add_gridspec(3, 3, left=0.06, right=0.99, top=0.86, bottom=0.09, wspace=0.24, hspace=0.50)
a1 = fig.add_subplot(gs[0, :]); a2 = fig.add_subplot(gs[1, 0]); a3 = fig.add_subplot(gs[1, 1])
a4 = fig.add_subplot(gs[2, 0]); a5 = fig.add_subplot(gs[2, 1]); a6 = fig.add_subplot(gs[2, 2])

E = {}
for lab, z, c in SER:
    E[lab] = (z["y"] - 1.0) * 600.0
    a1.plot(z["t"], 600 + E[lab], color=c, lw=(1.4 if lab.startswith("无律T") else 0.45),
            alpha=(1.0 if lab.startswith("无律T") else 0.9), label=lab)
a1.set_xlim(0, 30); a1.set_ylim(450, 750); a1.set_xlabel("时间 / s"); a1.set_ylabel("转速 / rpm")
a1.set_title("(a) 30 s 完整转速（2 s 加载 0.50 额定 + 组合故障）", fontsize=8.6)
a1.legend(fontsize=7, ncol=3, loc="upper right")

rms, a10 = [], []
for lab, z, c in SER:
    m = z["t"] >= 25
    rms.append(float(np.sqrt(np.mean(E[lab][m] ** 2))))
    a10.append(amp10(z["t"], E[lab], 10, 25, 30))
x = np.arange(3)
cols = [C_B, C_O, C_G]
a2.bar(x, rms, color=cols, width=0.55)
for i, v in enumerate(rms):
    a2.text(i, v + 0.6, "%.1f" % v, ha="center", fontsize=7.4)
a2.set_xticks(x); a2.set_xticklabels(["无律T", "巴特沃斯", "DFT"], fontsize=7.4)
a2.set_ylim(0, max(rms) * 1.18); a2.set_ylabel("稳态 RMS / rpm")
a2.set_title("(b) RMS  %.1f→%.1f→%.1f" % tuple(rms), fontsize=8.4)

a3.bar(x, a10, color=cols, width=0.55)
for i, v in enumerate(a10):
    a3.text(i, v + 0.6, "%.1f" % v, ha="center", fontsize=7.4)
a3.set_xticks(x); a3.set_xticklabels(["无律T", "巴特沃斯", "DFT"], fontsize=7.4)
a3.set_ylim(0, max(a10) * 1.18); a3.set_ylabel("10 Hz / rpm")
a3.set_title("(c) 10 Hz  %.1f→%.1f→%.1f" % tuple(a10), fontsize=8.4)

a4.plot(b["t"], b["tl"], color="#34495e", lw=0.6)
a4.set_xlim(0, 30); a4.set_ylim(-0.03, 0.62); a4.set_ylabel("$T_L$ / N·m"); a4.set_xlabel("时间 / s")
a4.set_title("(d) 负载：组合故障", fontsize=8.4)

for lab, z, c in SER:
    m = (z["t"] >= 26) & (z["t"] <= 27)
    a5.plot(z["t"][m], E[lab][m], color=c, lw=0.8, label=lab)
a5.set_xlim(26, 27); a5.set_ylim(-75, 75); a5.set_ylabel("误差 / rpm"); a5.set_xlabel("时间 / s")
a5.set_title("(e) 稳态 10 Hz 分量（幅值 %.1f / %.1f / %.1f rpm）" % tuple(a10), fontsize=8.4)

for lab, z, c in SER:
    a6.plot(z["t"], z["es"] * 100.0, color=c, lw=0.9, label=lab)
a6.set_xlim(0, 30); a6.set_ylim(-20.5, 1.5); a6.set_ylabel("δ / %"); a6.set_xlabel("时间 / s")
a6.set_title("(f) δ 收敛：末段 %.2f%% / %.2f%%" % (
    100 * np.mean(p["es"][p["t"] >= 25]), 100 * np.mean(d["es"][d["t"] >= 25])), fontsize=8.4)

fig.suptitle("律T 幅值观测器三口径对比（600 rpm、30 s；不对中 β=1° + 圆盘不平衡）", fontsize=9.8, y=0.965)
fig.savefig("fig_t_3way.png", dpi=150, bbox_inches=None, facecolor="white")
print("RMS", ["%.2f" % v for v in rms])
print("10Hz", ["%.2f" % v for v in a10])
print("delta_end bpf %.3f dft %.3f" % (100*np.mean(p["es"][p["t"] >= 25]), 100*np.mean(d["es"][d["t"] >= 25])))
print("saved fig_t_3way.png")
