# -*- coding: utf-8 -*-
"""plot_ppt_fig1.py —— PPT 图 1：同一故障工况下 纯 ESO vs 无自适应 RCESO（均类 fal 增益）

三行：负载 / 转速 / iq 与 iq 指令。PPT 规格（300 dpi、白底、大字号）。
输出：pptfig/ppt_01_eso_fal_fault.png
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

D = np.load("_ppt_fig1.npz")
J = json.load(open("_ppt_fig1.json", encoding="utf-8"))
t = D["t"]
N = J["n_ref"]
C_ESO, C_RC = "#1f4e79", "#c0392b"
C_TL = "#6c3483"

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

# (1) 负载（两档共用同一条）
ax[0].plot(t[::step], D["TL"][::step], color=C_TL, lw=1.0, label="施加负载 $T_L$")
ax[0].set_ylabel("$T_L$ / N·m")
ax[0].set_ylim(-0.04, 0.55)
ax[0].text(0.15, 0.46, "空载", fontsize=13, color="#555")
ax[0].text(2.15, 0.485, "故障投入：角度锁相周期负载 ±0.1 N·m（$T(\\varphi)=T(\\varphi+2\\pi)$）",
           fontsize=13, color="#7d3c98")
ax[0].axvline(2.0, color="#999", ls="--", lw=1.0)

# (2) 转速
y_eso = D["y_eso"] * N
y_rc = D["y_rceso"] * N
ax[1].plot(t[::step], y_eso[::step], color=C_ESO, lw=0.9, label="纯 ESO")
ax[1].plot(t[::step], y_rc[::step], color=C_RC, lw=0.9, label="无自适应 RCESO")
ax[1].axhline(N, color="#888", ls=":", lw=1.0)
ax[1].axvline(2.0, color="#999", ls="--", lw=1.0)
ax[1].set_ylabel("转速 / rpm")
ax[1].set_ylim(0, 1.42 * N)
ax[1].yaxis.set_major_locator(MultipleLocator(100))
ax[1].yaxis.set_minor_locator(MultipleLocator(50))
e_eso = J["cases"]["eso"]["steady_rms"]
e_rc = J["cases"]["rceso"]["steady_rms"]
ax[1].text(0.012, 0.955,
           "5–6 s：10 Hz 幅值 82 → 31 rpm；转速 RMS %.0f → %.0f rpm（−%.0f%%）"
           % (e_eso, e_rc, 100 * (1 - e_rc / e_eso)),
           transform=ax[1].transAxes, fontsize=12.5, color="#333", va="top",
           bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=2.5))
ax[1].legend(loc="lower left", ncol=1, fontsize=11.5)


# (3) 电流：两档的 iq 实线 + iq* 虚线
ax[2].plot(t[::step], D["iq_eso"][::step], color=C_ESO, lw=0.6, alpha=0.45, label="纯 ESO：$i_q$")
ax[2].plot(t[::step], D["iq_rceso"][::step], color=C_RC, lw=0.6, alpha=0.45, label="RCESO：$i_q$")
ax[2].plot(t[::step], D["iqr_eso"][::step], color=C_ESO, lw=1.3, ls="--", label="纯 ESO：$i_q^*$")
ax[2].plot(t[::step], D["iqr_rceso"][::step], color=C_RC, lw=1.3, ls="--", label="RCESO：$i_q^*$")
ax[2].set_ylabel("电流 / A")
ax[2].set_xlabel("时间 / s")
ax[2].set_xlim(0, 8)
ax[2].axvline(2.0, color="#999", ls="--", lw=1.0)
ax[2].legend(loc="upper left", ncol=2, fontsize=9.5)
ax[2].set_ylim(-0.5, 6.4)

for a in ax:
    a.tick_params(labelsize=12)
fig.suptitle("同一角度锁相故障工况：纯 ESO vs 无自适应 RCESO（ESO 增益均为类 fal）\n"
             "600 rpm、实验室工况、±0.1 N·m；实验室噪声：转速 3 rpm、dq 电流 ±0.1 A、负载 0.01 N·m",
             fontsize=15, y=0.985)
fig.align_ylabels(ax)
fig.savefig("pptfig/ppt_01_eso_fal_fault.png")
print("ok: pptfig/ppt_01_eso_fal_fault.png")
