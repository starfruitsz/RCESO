# -*- coding: utf-8 -*-
"""plot_j_other_long.py —— 30 s 长时对比：DFT / DO / AKO"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JM, JB = 1.89e-5, 9.95e-5
C_DFT, C_DO, C_AKO, C_FIX = "#16a085", "#7f8c8d", "#8e44ad", "#c0392b"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.0,
})
D = {k: np.load("_wave_j_%s_long.npz" % k) for k in ("dft", "do")}
A = np.load("_wave_j_ako_long.npz")
M = {k: json.load(open("_j_%s_long.json" % k)) for k in ("dft", "do", "ako")}

def a10_series(z):
    t = z["t"]; e = (z["y"] - 1.0) * 600.0
    tc = []; av = []
    for s in range(0, 29):
        m = (t >= s) & (t < s + 1.0)
        if m.sum() < 100:
            continue
        ec = e[m]; ts = t[m]
        av.append(float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*ts)), 2*np.mean(ec*np.sin(2*np.pi*10*ts)))))
        tc.append(s + 0.5)
    return np.array(tc), np.array(av)

tc_d, a_d = a10_series(D["dft"])
tc_o, a_o = a10_series(D["do"])
tc_k = np.asarray(A["tc"]); a_k = np.asarray(A["a10"])

fig = plt.figure(figsize=(13.33, 6.67))
gs = fig.add_gridspec(2, 1, left=0.075, right=0.985, top=0.865, bottom=0.09, hspace=0.40)
axa = fig.add_subplot(gs[0]); axb = fig.add_subplot(gs[1])

# (a) jhat
for z, c, lab, lw in ((D["dft"], C_DFT, "调试期 DFT（2 s 冻结）", 1.4),
                      (D["do"], C_DO, "简化 DO+梯度", 1.2),
                      (A, C_AKO, "Yang 2018 AKO+RLS", 1.2)):
    axa.plot(z["t_j"], np.asarray(z["jhat"]) * 1e6, color=c, lw=lw, label=lab)
axa.axhline(JB * 1e6, color="#555", ls="--", lw=0.9, label=r"$J_{\rm true}=99.5$")
axa.axhspan(JB * 0.9e6, JB * 1.1e6, color=C_DFT, alpha=0.08, label="±10%")
axa.set_xlim(0, 30); axa.set_ylim(0, 125)
axa.set_xlabel("时间 / s"); axa.set_ylabel(r"$\hat J$ / ($10^{-6}$ kg·m$^2$)")
axa.set_title("(a) 30 s：只有 DFT 收敛（终值 %.1f，+%.1f%%）；DO/AKO 均漂移" % (M["dft"]["jfin"]*1e6, 100*(M["dft"]["jfin"]/JB-1)), fontsize=10.0, pad=5)
axa.legend(loc="center right", fontsize=7.6)
axa.annotate("DO %.1f" % (M["do"]["jfin"]*1e6), xy=(29.5, M["do"]["jfin"]*1e6), xytext=(22, 62), fontsize=7.2, color=C_DO)
axa.annotate("AKO %.1f" % (M["ako"]["jfin"]*1e6), xy=(29.5, M["ako"]["jfin"]*1e6), xytext=(22, 28), fontsize=7.2, color=C_AKO)

# (b) a10
axb.plot(tc_d, a_d, color=C_DFT, lw=1.6, marker="o", ms=2.5, label="调试期 DFT")
axb.plot(tc_o, a_o, color=C_DO, lw=1.3, marker="s", ms=2.2, label="简化 DO")
axb.plot(tc_k, a_k, color=C_AKO, lw=1.3, marker="^", ms=2.2, label="AKO+RLS")
axb.axhline(33.3, color=C_FIX, ls="--", lw=0.9, label="固定 b0 33.3")
axb.set_xlim(0, 30); axb.set_ylim(0, 58)
axb.set_xlabel("时间 / s"); axb.set_ylabel("10 Hz 分量（1 s 窗）/ rpm")
axb.set_title("(b) 10 Hz：DFT 稳在 %.1f；DO %.1f；AKO 漂到 %.1f" % (a_d[-1], a_o[-1], a_k[-1]), fontsize=10.0, pad=5)
axb.legend(loc="center right", fontsize=7.6)
axb.annotate("%.1f" % a_d[-1], xy=(29.5, a_d[-1]), xytext=(27.2, 9.5), fontsize=7.2, color=C_DFT)
axb.annotate("%.1f" % a_o[-1], xy=(29.5, a_o[-1]), xytext=(25.5, 42.5), fontsize=7.2, color=C_DO)
axb.annotate("%.1f" % a_k[-1], xy=(29.5, a_k[-1]), xytext=(21.5, 54.0), fontsize=7.2, color=C_AKO)

fig.suptitle("J 自适应 30 s 长时对比：调试期 DFT 稳定收敛；简化 DO 与 AKO+RLS 都不收敛（600 rpm、$J_{\\rm true}=5.26J_{\\rm nom}$）",
             fontsize=10.8, y=0.965)
fig.text(0.075, 0.012, "数据：pmsm_inv_sim.py，同一工况延长到 30 s；DFT 2 s 冻结；DO γ=1e-3/lpf=50 ms；AKO 3 状态 KF + a1/b1 RLS（λ=0.99、B=0）。",
         fontsize=6.8, color="#666")
fig.savefig("fig_j_other_long.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok", a_d[-1], a_o[-1], a_k[-1], M["dft"]["jfin"], M["do"]["jfin"], M["ako"]["jfin"])
