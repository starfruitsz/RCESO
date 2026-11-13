# -*- coding: utf-8 -*-
"""plot_j_adaptive_ppt.py —— 自适应 J 六联图（PPT 版，2000x1000）
数据：_j_adapt.json / _j_comm.json / _j_state4.json / _j_state3.json / _wave_j_big_*.npz
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

JM, JB = 1.89e-5, 9.95e-5
C_NAVY, C_TEAL, C_RED, C_ORANGE, C_GRAY = "#1f4e79", "#16a085", "#c0392b", "#e67e22", "#7f8c8d"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.8, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.6,
})
A = json.load(open("_j_adapt.json", encoding="utf-8"))
C = json.load(open("_j_comm.json", encoding="utf-8"))
S4 = json.load(open("_j_state4.json", encoding="utf-8"))
S3 = json.load(open("_j_state3.json", encoding="utf-8"))
W = {k: np.load("_wave_j_%s.npz" % k) for k in ("big_fault", "big_oracle", "big_comm")}

fig = plt.figure(figsize=(13.33, 6.67))
gs = fig.add_gridspec(3, 2, width_ratios=[2.0, 1.0], height_ratios=[1.0, 1.0, 1.0],
                      left=0.055, right=0.985, top=0.875, bottom=0.09, wspace=0.20, hspace=0.46)
axa = fig.add_subplot(gs[0, 0]); axb = fig.add_subplot(gs[0, 1])
axc = fig.add_subplot(gs[1, 0]); axd = fig.add_subplot(gs[1, 1])
axe = fig.add_subplot(gs[2, 0]); axf = fig.add_subplot(gs[2, 1])

# (a) 9-10 s speed error
for k, c, lab, lw in (("big_fault", C_RED, "固定标称 b0", 0.9),
                      ("big_oracle", C_ORANGE, "oracle 重整定", 0.9),
                      ("big_comm", C_TEAL, "辨识 + b0 自适应", 1.1)):
    d = W[k]; tt = d["t"][::100]; e = (d["y"][::100] - 1.0) * 600.0
    m = (tt >= 9.0) & (tt <= 10.0)
    axa.plot(tt[m], e[m], color=c, lw=lw, label=lab)
axa.set_xlim(9.0, 10.0)
axa.set_xlabel("时间 / s"); axa.set_ylabel("转速误差 / rpm")
axa.set_title("(a) 稳态 9–10 s：10 Hz 纹波 33.3 → 4.0 rpm", fontsize=9.2, pad=4)
axa.legend(loc="upper right", ncol=3)
axa.axhline(0, color="#999", lw=0.6)

# (b) 10 Hz residual bars
labels = ["标称 J\n(基准)", "J_true=5.26J\n固定 b0", "oracle\n重整定", "辨识+b0\n自适应"]
vals = [A["Jm_fault"]["amp10"], C["big_fault"]["a10"], C["big_oracle"]["a10"], C["big_comm"]["a10"]]
cols = [C_NAVY, C_RED, C_ORANGE, C_TEAL]
bars = axb.bar(range(4), vals, color=cols, width=0.62)
for b, v in zip(bars, vals):
    axb.text(b.get_x() + b.get_width()/2, v + 0.8, "%.1f" % v, ha="center", va="bottom", fontsize=7.8)
axb.set_xticks(range(4)); axb.set_xticklabels(["标称 J\n(基准)", "5.26J_nom\n固定 b0", "oracle\n重整定", "辨识+b0\n自适应"], fontsize=7.0)
axb.set_ylabel("10 Hz 转速分量 / rpm")
axb.set_ylim(0, 39)
axb.set_title("(b) 故障抑制：−88%", fontsize=9.2, pad=4)
axb.annotate("", xy=(1, 33.3), xytext=(3, 4.0), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=1.2, connectionstyle="arc3,rad=-0.25"))

# (c) dither cost
bars = axc.bar([0, 1], [C["big_comm"]["a100_id"], C["big_comm"]["a100_post"]],
               color=[C_ORANGE, C_TEAL], width=0.55)
for b, v, lab in zip(bars, [C["big_comm"]["a100_id"], C["big_comm"]["a100_post"]], ["18.15", "0.16（×0.009）"]):
    axc.text(b.get_x() + b.get_width()/2, v + 0.4, lab, ha="center", fontsize=8)
axc.set_xticks([0, 1]); axc.set_xticklabels(["调试期 0.5–2 s", "运行段 9–10 s"])
axc.set_ylabel("100 Hz 转速分量 / rpm")
axc.set_ylim(0, 22)
axc.set_title("(c) 注入代价：仅存在于辨识期", fontsize=9.2, pad=4)

# (d) Jhat convergence
d = W["big_comm"]; tj = np.asarray(d["t_j"]); jh = np.asarray(d["jhat"])
jfin = float(jh[-1])
axd.plot(tj, jh * 1e6, color=C_TEAL, lw=1.3, label=r"$\hat J$")
axd.axhline(JB * 1e6, color="#555", ls="--", lw=0.9, label=r"$J_{\rm true}$")
axd.axhspan(JB * 0.9e6, JB * 1.1e6, color=C_TEAL, alpha=0.10, label="±10%")
axd.axvline(2.0, color=C_ORANGE, ls=":", lw=1.0)
axd.set_xlim(0.3, 2.3); axd.set_ylim(0, 125)
axd.set_xlabel("时间 / s"); axd.set_ylabel(r"$\hat J$ / ($10^{-6}$ kg·m$^2$)")
axd.set_title("(d) 辨识收敛：+%.1f%%（2 s 冻结）" % (100*(jfin/JB-1)), fontsize=9.2, pad=4)
axd.legend(loc="lower right")
axd.text(1.18, 101.5, "真实 99.5", color="#555", fontsize=7.2, ha="center")

# (e) b0 step / state timeline
tt = np.linspace(0, 10, 2000)
b0e = np.where(tt < 2.0, 1.0, JM / jfin)
axe.step(tt, b0e, where="post", color=C_NAVY, lw=1.6, label=r"$b_0^{\rm e}/b_0$")
axe.axvspan(0, 2.0, color=C_ORANGE, alpha=0.10)
axe.axvspan(2.0, 10.0, color=C_TEAL, alpha=0.07)
axe.text(1.0, 0.90, "状态 1\n辨识", ha="center", fontsize=7.0, color=C_ORANGE)
axe.text(4.0, 0.90, "状态 2 已应用（冻结）", ha="left", fontsize=7.0, color=C_TEAL)
axe.annotate(r"$b_0\leftarrow b_0 J_{\rm nom}/\hat J$" + "\n" + "= %.3f$b_0$" % (JM/jfin),
             xy=(2.0, JM/jfin), xytext=(2.5, 0.45), fontsize=7.3, color=C_NAVY,
             arrowprops=dict(arrowstyle="->", color=C_NAVY, lw=0.8))
axe.set_xlim(0, 10); axe.set_ylim(0, 1.12)
axe.set_xlabel("时间 / s"); axe.set_ylabel(r"$b_0^{\rm e}/b_0$")
axe.set_title("(e) $b_0$ 更新：2 s 后冻结", fontsize=9.2, pad=4)
axe.legend(loc="center right")

# (f) state-4 validation peaks
cases = ["无故障 A=.157", "无故障 A=.30"]
old = [6.4027, S3["nofault_A30"]["iq"]]
new = [S4["cases"]["nofault_A157_nmin5"]["iq_peak_total"], S4["cases"]["nofault_A30"]["iq_peak_total"]]
x = np.arange(2); wdt = 0.34
b1 = axf.bar(x - wdt/2, old, width=wdt, color=C_RED, alpha=0.75, label="无校验（旧）")
b2 = axf.bar(x + wdt/2, new, width=wdt, color=C_TEAL, label="状态 4 回退")
for b, v in zip(b1, old): axf.text(b.get_x() + b.get_width()/2, v + 0.25, "%.2f" % v, ha="center", fontsize=7.3)
for b, v in zip(b2, new): axf.text(b.get_x() + b.get_width()/2, v + 0.25, "%.2f" % v, ha="center", fontsize=7.3)
axf.axhline(6.31, color=C_RED, ls="--", lw=1.0)
axf.text(1.62, 6.45, "额定 6.31", color=C_RED, fontsize=7.0, ha="right")
axf.set_xticks(x); axf.set_xticklabels(cases, fontsize=7.2)
axf.set_ylabel(r"$|i_q|$ 10 µs 峰值 / A")
axf.set_ylim(0, 13.8)
axf.set_title("(f) 状态 4：过流尖峰被截住", fontsize=9.2, pad=4)
axf.legend(loc="upper right")

fig.suptitle("自适应 J：辨识 → $b_0$ 更新 → 故障抑制 → 状态 4 回退（600 rpm、$T_1=0.057$ N·m、$J_{\\rm true}=5.26J_{\\rm nom}$ 应力测试）",
             fontsize=11.0, y=0.965)
fig.text(0.055, 0.012, "数据：pmsm_inv_sim.py；实验室噪声、种子 20261018；dither 100 Hz、0.2 s 窗、0–2 s 辨识；9–10 s 稳态窗。"
         "（f）为 10 µs 原始峰值（含 PWM 纹波），1 ms 包络见报告 C.7。", fontsize=6.8, color="#666")
fig.savefig("fig_j_adaptive_ppt.png", dpi=150, bbox_inches=None, facecolor="white")
json.dump(dict(a10=dict(nominalJ=A["Jm_fault"]["amp10"], fixed=C["big_fault"]["a10"], oracle=C["big_oracle"]["a10"], adapt=C["big_comm"]["a10"]),
               dither=dict(id=C["big_comm"]["a100_id"], post=C["big_comm"]["a100_post"]),
               jhat_final=jfin, jhat_err=100*(jfin/JB-1), b0_ratio=JM/jfin,
               state4=dict(nofault_A157=dict(old=6.4027, new=S4["cases"]["nofault_A157_nmin5"]["iq_peak_total"]),
                           nofault_A30=dict(old=S3["nofault_A30"]["iq"], new=S4["cases"]["nofault_A30"]["iq_peak_total"]))),
          open("_fig_j_adaptive_numbers.json","w",encoding="utf-8"), indent=1)
print("ok fig_j_adaptive_ppt.png", "jfin_err %.2f%%" % (100*(jfin/JB-1)), "b0 %.3f" % (JM/jfin))
