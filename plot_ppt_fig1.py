# -*- coding: utf-8 -*-
"""plot_ppt_fig1.py —— PPT 图 1（三张）：纯 ESO / 无自适应 RCESO / 两者合并

用法：
    python plot_ppt_fig1.py eso     -> pptfig/ppt_01a_pure_eso_fault.png
    python plot_ppt_fig1.py rceso   -> pptfig/ppt_01b_rceso_fault.png
    python plot_ppt_fig1.py both    -> pptfig/ppt_01c_eso_vs_rceso.png

数据来自 run_ppt_fig1.py 产出的 _ppt_fig1.npz / .json。
三行：负载 / 转速 / iq 与 iq 指令；PPT 规格（300 dpi、白底、大字号）。
"""
import json
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

MODE = sys.argv[1] if len(sys.argv) > 1 else "both"
D = np.load("_ppt_fig1.npz")
J = json.load(open("_ppt_fig1.json", encoding="utf-8"))
t = D["t"]
N = J["n_ref"]
C_TL = "#6c3483"
C = {"eso": "#1f4e79", "rceso": "#c0392b"}
LAB = {"eso": "纯 ESO", "rceso": "无自适应 RCESO"}
FN = {"eso": "pptfig/ppt_01a_pure_eso_fault.png",
      "rceso": "pptfig/ppt_01b_rceso_fault.png",
      "both": "pptfig/ppt_01c_eso_vs_rceso.png"}

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 13,
    "figure.dpi": 120, "savefig.dpi": 300, "savefig.bbox": "tight",
    "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 11.5,
})

fig, ax = plt.subplots(3, 1, figsize=(12.8, 9.6), sharex=True,
                       gridspec_kw=dict(hspace=0.18, height_ratios=[1, 1.15, 1.15]))
step = 6

# ---------- (1) 负载 ----------
ax[0].plot(t[::step], D["TL"][::step], color=C_TL, lw=1.0)
ax[0].set_ylabel("$T_L$ / N·m")
ax[0].set_ylim(-0.04, 0.55)
ax[0].text(0.15, 0.46, "空载", fontsize=13, color="#555")
ax[0].text(2.15, 0.485, "故障投入：圆盘质量不对中模式 ±0.1 N·m（1–6 次谐波，THD 77.5%）",
           fontsize=13, color="#7d3c98")
ax[0].axvline(2.0, color="#999", ls="--", lw=1.0)

# ---------- (2) 转速 ----------
keys = ["eso", "rceso"] if MODE == "both" else [MODE]
for k in keys:
    ax[1].plot(t[::step], (D["y_" + k] * N)[::step], color=C[k], lw=0.9, label=LAB[k])
ax[1].axhline(N, color="#888", ls=":", lw=1.0)
ax[1].axvline(2.0, color="#999", ls="--", lw=1.0)
ax[1].set_ylabel("转速 / rpm")
ax[1].set_ylim(0, 1.42 * N)
ax[1].yaxis.set_major_locator(MultipleLocator(100))
ax[1].yaxis.set_minor_locator(MultipleLocator(50))

def rms_of(k):
    e = (D["y_" + k] - 1.0) * N
    m = (t >= 5.0) & (t < 6.0)
    return float(np.sqrt(np.mean(e[m] ** 2)))

def amp10(k):
    e = (D["y_" + k] - 1.0) * N
    m = (t >= 5.0) & (t < 6.0)
    tt, yy = t[m], e[m]
    w = 2.0 * np.pi * 10.0
    c = 2.0 * np.mean(yy * np.cos(w * tt))
    s = 2.0 * np.mean(yy * np.sin(w * tt))
    return float(np.hypot(c, s))

if MODE == "both":
    txt = ("5–6 s：10 Hz 幅值 %.0f → %.0f rpm；转速 RMS %.0f → %.0f rpm（−%.0f%%）"
           % (amp10("eso"), amp10("rceso"), rms_of("eso"), rms_of("rceso"),
              100 * (1 - rms_of("rceso") / rms_of("eso"))))
else:
    txt = "5–6 s：10 Hz 幅值 %.0f rpm；转速 RMS %.0f rpm（%.1f%% 额定）" % (
        amp10(MODE), rms_of(MODE), 100 * rms_of(MODE) / N)
ax[1].text(0.012, 0.955, txt, transform=ax[1].transAxes, fontsize=12.5, color="#333", va="top",
           bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=2.5))
if MODE == "both":
    ax[1].legend(loc="lower left", ncol=1, fontsize=11.5)

# ---------- (3) 电流 ----------
for k in keys:
    ax[2].plot(t[::step], D["iq_" + k][::step], color=C[k], lw=0.6, alpha=0.45, label=LAB[k] + "：$i_q$")
    ax[2].plot(t[::step], D["iqr_" + k][::step], color=C[k], lw=1.3, ls="--", label=LAB[k] + "：$i_q^*$")
ax[2].set_ylabel("电流 / A")
ax[2].set_xlabel("时间 / s")
ax[2].set_xlim(0, 8)
ax[2].axvline(2.0, color="#999", ls="--", lw=1.0)
ax[2].set_ylim(-0.5, 6.4)
if MODE == "both":
    ax[2].legend(loc="upper left", ncol=2, fontsize=9.5)
else:
    ax[2].legend(loc="upper left", ncol=2, fontsize=10.5)

for a in ax:
    a.tick_params(labelsize=12)

title = {"eso": "纯 ESO（无重复通道）+ 类 fal 增益：圆盘质量不对中模式 ±0.1 N·m",
         "rceso": "无自适应 RCESO（重复通道 $\\beta_3$=4000、$Q_0$=0.98、$\\tau_0$=20 ms 固定）+ 类 fal 增益：同一圆盘质量不对中模式",
         "both": "同一圆盘质量不对中模式：纯 ESO vs 无自适应 RCESO（ESO 增益均为类 fal）"}[MODE]
fig.suptitle(title + "\n" + "600 rpm、实验室工况、±0.1 N·m；实验室噪声：转速 3 rpm、dq 电流 ±0.1 A、负载 0.01 N·m",
             fontsize=15, y=0.985)
fig.align_ylabels(ax)
fig.savefig(FN[MODE])
print("ok:", FN[MODE])
