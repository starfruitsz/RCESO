# -*- coding: utf-8 -*-
"""plot_case_eso_rceso.py —— 纯 ESO vs 无自适应 RCESO（振动 + 阶跃 + 周期负载）

三行：负载 / 转速 / 电流（i_q 与 i_q*）。输出 1920×960（12.8 in × 6.4 in @150 dpi）。
数据：_case_eso_rceso.npz（run_case_eso_rceso.py 生成）
输出：fig_case_eso_rceso_600.png
"""
import json
import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

D = np.load("_case_eso_rceso.npz")
J = json.load(open("_case_eso_rceso.json", encoding="utf-8"))
t = D["t"]
N = J["n_ref"]
STEP = 4
C_TL = "#6c3483"
C = {"eso": "#1f4e79", "rceso": "#c0392b"}
LAB = {"eso": "纯 ESO", "rceso": "无自适应 RCESO"}
FN = "fig_case_eso_rceso_600.png"

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 10,
    "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.2,
})

fig, ax = plt.subplots(3, 1, figsize=(12.8, 6.4), sharex=True,
                       gridspec_kw=dict(hspace=0.20, height_ratios=[1.0, 1.15, 1.15]))
fig.subplots_adjust(left=0.058, right=0.986, top=0.855, bottom=0.098)

# ---------- (1) 负载 ----------
ax[0].plot(t[::STEP], D["TL"][::STEP], color=C_TL, lw=0.9)
ax[0].set_ylabel("$T_L$ / N·m", fontsize=10)
ax[0].set_ylim(-0.06, 0.70)
ax[0].axvline(2.0, color="#999", ls="--", lw=0.9)
ax[0].text(0.12, 0.50, "空载", fontsize=9.6, color="#555")
ax[0].text(2.12, 0.615, "故障投入：阶跃 0.5 额定 + $T(\\theta)$ 1–6 次谐波（THD 58.8%）+ 5.9 Hz 振动（基波 0.03 N·m，THD 40%）",
           fontsize=9.0, color="#7d3c98")

# ---------- (2) 转速 ----------
for k in ("eso", "rceso"):
    ax[1].plot(t[::STEP], (D["y_" + k] * N)[::STEP], color=C[k], lw=0.8, label=LAB[k])
ax[1].axhline(N, color="#888", ls=":", lw=0.9)
ax[1].axvline(2.0, color="#999", ls="--", lw=0.9)
ax[1].set_ylabel("转速 / rpm", fontsize=10)
ax[1].set_ylim(250, 840)
ax[1].yaxis.set_major_locator(MultipleLocator(100))


def amps(k):
    e = (D["y_" + k] - 1.0) * N
    m = (t >= 5.0) & (t < 6.0)
    tt, yy = t[m], e[m]
    A = np.vstack([np.ones_like(tt),
                   np.cos(2 * math.pi * 5.9 * tt), np.sin(2 * math.pi * 5.9 * tt),
                   np.cos(2 * math.pi * 10 * tt), np.sin(2 * math.pi * 10 * tt)]).T
    c, *_ = np.linalg.lstsq(A, yy, rcond=None)
    return float(np.hypot(c[1], c[2])), float(np.hypot(c[3], c[4]))


def rms_of(k):
    e = (D["y_" + k] - 1.0) * N
    m = (t >= 5.0) & (t < 6.0)
    return float(np.sqrt(np.mean(e[m] ** 2)))


v_e, a10_e = amps("eso")
v_r, a10_r = amps("rceso")
ax[1].text(0.012, 0.955,
           "5–6 s：10 Hz 幅值 %.0f → %.0f rpm（−%.0f%%）；5.9 Hz 幅值 %.1f → %.1f rpm；转速 RMS %.0f → %.0f rpm"
           % (a10_e, a10_r, 100 * (1 - a10_r / a10_e), v_e, v_r, rms_of("eso"), rms_of("rceso")),
           transform=ax[1].transAxes, fontsize=8.8, color="#333", va="top",
           bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=2.0))
ax[1].legend(loc="lower left", ncol=2, fontsize=8.4)

# ---------- (3) 电流 ----------
for k in ("eso", "rceso"):
    ax[2].plot(t[::STEP], D["iq_" + k][::STEP], color=C[k], lw=0.5, alpha=0.45,
               label=LAB[k] + "：$i_q$")
    ax[2].plot(t[::STEP], D["iqr_" + k][::STEP], color=C[k], lw=1.1, ls="--",
               label=LAB[k] + "：$i_q^*$")
ax[2].set_ylabel("电流 / A", fontsize=10)
ax[2].set_xlabel("时间 / s", fontsize=10)
ax[2].set_xlim(0, 8)
ax[2].axvline(2.0, color="#999", ls="--", lw=0.9)
ax[2].set_ylim(-0.6, 7.2)
ax[2].legend(loc="upper left", ncol=2, fontsize=7.8)

for a in ax:
    a.tick_params(labelsize=9.5)

fig.suptitle("同一负载工况：纯 ESO vs 无自适应 RCESO（ESO 增益均为类 fal）\n"
             "600 rpm、实验室工况：阶跃 0.5 额定 + $T(\\theta)$ 1–6 次谐波 + 5.9 Hz 振动；实验室噪声 3 rpm / 0.1 A / 0.01 N·m",
             fontsize=10.6, y=0.972)
fig.align_ylabels(ax)
fig.savefig(FN, dpi=150, bbox_inches=None, facecolor="white")
try:
    from PIL import Image
    Image.open(FN).convert("RGB").save(FN)
except Exception:
    pass
print("ok:", FN, "10Hz %.1f -> %.1f, 5.9Hz %.1f -> %.1f" % (a10_e, a10_r, v_e, v_r))
