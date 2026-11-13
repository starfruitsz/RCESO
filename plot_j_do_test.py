# -*- coding: utf-8 -*-
"""plot_j_do_test.py —— ESO/DO 试跑 vs 调试期 DFT（3 联图）
数据：_wave_j_big_fault / _oracle / _comm / _do（同一 pmsm_inv_sim 工况）
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JM, JB = 1.89e-5, 9.95e-5
C_FIX, C_DO, C_COMM, C_ORACLE = "#c0392b", "#7f8c8d", "#16a085", "#e67e22"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.0,
})
W = {k: np.load("_wave_j_%s.npz" % k) for k in ("big_fault", "big_oracle", "big_comm", "big_do_g1e-03_l50_t5e-01")}
C = json.load(open("_j_comm.json", encoding="utf-8"))
A = json.load(open("_j_adapt.json", encoding="utf-8"))
DOF = "_wave_j_big_do_g1e-03_l50_t5e-01.npz"
# metrics
def met(z):
    t = z["t"]; y = z["y"]; iq = z["iq"]; e = (y-1.0)*600.0
    m = (t >= 9.0) & (t < 10.0); tc, ec = t[m], e[m]
    a10 = float(np.hypot(2*np.mean(ec*np.cos(2*np.pi*10*tc)), 2*np.mean(ec*np.sin(2*np.pi*10*tc))))
    rms = float(np.sqrt(np.mean(ec**2)))
    return a10, rms, float(np.max(np.abs(iq)))
a10_f, rms_f, iq_f = met(W["big_fault"])
a10_o, rms_o, iq_o = met(W["big_oracle"])
a10_c, rms_c, iq_c = met(W["big_comm"])
a10_d, rms_d, iq_d = met(W["big_do_g1e-03_l50_t5e-01"])
jdo = float(np.asarray(W["big_do_g1e-03_l50_t5e-01"]["jhat"])[-1])
print("fixed", a10_f, iq_f, "do", a10_d, iq_d, jdo, "comm", a10_c, iq_c)

fig = plt.figure(figsize=(13.33, 6.67))
gs = fig.add_gridspec(2, 2, width_ratios=[1.55, 1.0], height_ratios=[1.0, 1.0],
                      left=0.065, right=0.985, top=0.865, bottom=0.11, wspace=0.18, hspace=0.42)
axa = fig.add_subplot(gs[:, 0]); axb = fig.add_subplot(gs[0, 1]); axd = fig.add_subplot(gs[1, 1])

# (a) speed error 9-10 s
for key, c, lab, lw in (("big_fault", C_FIX, "固定标称 b0", 0.9),
                        ("big_do_g1e-03_l50_t5e-01", C_DO, "简化 DO+梯度（试跑）", 1.1),
                        ("big_oracle", C_ORACLE, "oracle 重整定", 0.9),
                        ("big_comm", C_COMM, "辨识 + b0 自适应", 1.2)):
    d = W[key]; tt = d["t"][::100]; e = (d["y"][::100] - 1.0) * 600.0
    m = (tt >= 9.0) & (tt <= 10.0)
    axa.plot(tt[m], e[m], color=c, lw=lw, label=lab)
axa.set_xlim(9.0, 10.0); axa.set_ylim(-70, 82)
axa.set_xlabel("时间 / s"); axa.set_ylabel("转速误差 / rpm")
axa.set_title("(a) 稳态 9–10 s：DO 未把 10 Hz 压下去", fontsize=10.2, pad=5)
axa.legend(loc="upper right", fontsize=7.8)
axa.axhline(0, color="#999", lw=0.6)

# (b) 10 Hz bars
labels = ["固定 b0", "DO 试跑", "调试期 DFT", "oracle"]
vals = [a10_f, a10_d, a10_c, a10_o]
cols = [C_FIX, C_DO, C_COMM, C_ORACLE]
bars = axb.bar(range(4), vals, color=cols, width=0.62)
for b, v in zip(bars, vals):
    axb.text(b.get_x() + b.get_width()/2, v + 0.8, "%.1f" % v, ha="center", va="bottom", fontsize=8.2)
axb.set_xticks(range(4)); axb.set_xticklabels(labels, fontsize=7.4)
axb.set_ylabel("10 Hz 转速分量 / rpm"); axb.set_ylim(0, 42)
axb.set_title("(b) DO 与固定 b0 同级：未收敛", fontsize=10.2, pad=5)
axb.annotate("×", xy=(1, a10_d*0.55), fontsize=22, color=C_DO, ha="center", va="center")

# (c) jhat
d = W["big_comm"]; axd.plot(d["t_j"], np.asarray(d["jhat"])*1e6, color=C_COMM, lw=1.4, label="调试期 DFT")
d = W["big_do_g1e-03_l50_t5e-01"]; axd.plot(d["t_j"], np.asarray(d["jhat"])*1e6, color=C_DO, lw=1.2, label="简化 DO+梯度")
axd.axhline(JB*1e6, color="#555", ls="--", lw=0.9, label=r"$J_{\rm true}=99.5$")
axd.axhspan(JB*0.9e6, JB*1.1e6, color=C_COMM, alpha=0.08)
axd.set_xlim(0, 10); axd.set_ylim(0, 125)
axd.set_xlabel("时间 / s"); axd.set_ylabel(r"$\hat J$ / ($10^{-6}$ kg·m$^2$)")
axd.set_title("(c) DO 终值 %.1f（−%.0f%%）；DFT +9.1%%" % (jdo*1e6, 100*(1-jdo/JB)), fontsize=9.6, pad=5)
axd.legend(loc="center right", fontsize=7.4)
axd.text(5.0, 50, "DO 估计被 T_L 观测器吸收\n（J 与 T_L 耦合）", fontsize=7.2, color=C_DO, ha="center")

fig.suptitle("ESO/DO 观测器试跑：简化 DO+梯度在本对象上不收敛；调试期 DFT 仍可用（600 rpm、$J_{\\rm true}=5.26J_{\\rm nom}$）",
             fontsize=10.8, y=0.965)
fig.text(0.065, 0.015, "DO：一阶 DO 估 T_L + J 梯度，γ=1e-3、lpf=50 ms、b0 慢更新 0.5 s；非 Yang 2018 全阶 AKO+RLS。数据：pmsm_inv_sim.py，10 s，种子 20261018。",
         fontsize=6.7, color="#666")
fig.savefig("fig_j_do_test.png", dpi=150, bbox_inches=None, facecolor="white")
print("ok fig_j_do_test.png")
