# -*- coding: utf-8 -*-
"""plot_ppt_fig1.py —— PPT 图 1：纯 ESO + 类 fal 增益 应对角度锁相周期负载

三行：负载 / 转速 / iq 与 iq 指令。PPT 规格（16:9 风格、大字号、300 dpi、白底浅网格）。
输出：pptfig/ppt_01_eso_fal_fault.png
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = np.load("_ppt_fig1.npz")
J = json.load(open("_ppt_fig1.json", encoding="utf-8"))
t = D["t"]
N = J["n_ref"]

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 13,
    "figure.dpi": 120, "savefig.dpi": 300, "savefig.bbox": "tight",
    "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 12,
})

C_TL, C_N, C_IQ, C_IQR = "#6c3483", "#1f4e79", "#c0392b", "#16a085"
fig, ax = plt.subplots(3, 1, figsize=(12.8, 9.6), sharex=True,
                       gridspec_kw=dict(hspace=0.18, height_ratios=[1, 1.15, 1.15]))
step = 6      # 10 kHz -> ~1.7 kHz 抽点，够看清 10 Hz 波形

# (1) 负载
ax[0].plot(t[::step], D["TL"][::step], color=C_TL, lw=1.0)
ax[0].set_ylabel("$T_L$ / N·m")
ax[0].set_ylim(-0.02, 0.55)
ax[0].text(0.15, 0.46, "空载", fontsize=13, color="#555")
ax[0].text(2.15, 0.46, "故障投入：角度锁相周期负载 ±0.1 N·m（$T(\\varphi)=T(\\varphi+2\\pi)$）",
           fontsize=13, color="#7d3c98")
ax[0].axvline(2.0, color="#999", ls="--", lw=1.0)

# (2) 转速
y = D["y"] * N
ax[1].plot(t[::step], y[::step], color=C_N, lw=0.9)
ax[1].axhline(N, color="#888", ls=":", lw=1.0)
ax[1].set_ylabel("转速 / rpm")
ax[1].set_ylim(0.55 * N, 1.22 * N)
ax[1].axvline(2.0, color="#999", ls="--", lw=1.0)
ax[1].text(2.18, 0.985 * 1.22 * N - 0.02 * N,
           "稳态转速脉动 %.0f rpm RMS（≈%.1f%% 额定）" % (J["steady_rms"], 100 * J["steady_rms"] / N),
           fontsize=13, color=C_N,
           bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=2.5))

# (3) iq / iq*
ax[2].plot(t[::step], D["iq"][::step], color=C_IQ, lw=0.7, alpha=0.65,
           label="$i_q$（实测，含采样噪声）")
ax[2].plot(t[::step], D["iqr"][::step], color=C_IQR, lw=1.5, label="$i_q^*$（指令）")
ax[2].set_ylabel("电流 / A")
ax[2].set_xlabel("时间 / s")
ax[2].set_xlim(0, 8)
ax[2].axvline(2.0, color="#999", ls="--", lw=1.0)
ax[2].legend(loc="upper left", ncol=2)
ax[2].set_ylim(-0.5, 6.2)

for a in ax:
    a.tick_params(labelsize=12)
fig.suptitle("纯 ESO（无重复通道）+ 类 fal 增益：600 rpm、实验室工况、角度锁相周期负载 ±0.1 N·m\n"
             "实验室噪声：转速 3 rpm、dq 电流 ±0.1 A、负载 0.01 N·m",
             fontsize=15, y=0.985)

# 第三行加一个噪声放大窗：1.00–1.06 s，看清 ±0.1 A 的采样噪声
ins = ax[2].inset_axes([0.63, 0.56, 0.32, 0.40])
ins.set_facecolor("white"); ins.patch.set_alpha(1.0)
for sp in ins.spines.values():
    sp.set_visible(True); sp.set_linewidth(0.8)
m = (t >= 1.000) & (t < 1.002)     # 2 ms：能看清逐个采样点的噪声
ins.plot(t[m] * 1e3, D["iq"][m], color=C_IQ, lw=1.2, label="$i_q$")
ins.plot(t[m] * 1e3, D["iqr"][m], color=C_IQR, lw=1.6, ls="--", label="$i_q^*$")
ins.set_xlabel("t / ms", fontsize=8.5)
ins.set_xlim(1000.0, 1002.0)
ins.tick_params(labelsize=9)
ins.set_title("空载放大 2 ms：$i_q$ 采样噪声 ±0.1 A", fontsize=9.5)
ins.legend(fontsize=7.5, loc="lower left", ncol=2, framealpha=0.9)
ins.grid(alpha=0.2)
fig.align_ylabels(ax)
fig.savefig("pptfig/ppt_01_eso_fal_fault.png")
print("ok: pptfig/ppt_01_eso_fal_fault.png")
