# -*- coding: utf-8 -*-
"""plot_echo_rev_speed_case.py —— 反相工况下的四联图（负载/完整转速/突变窗/反相窗）

与 plot_eso_fal_speed_case.py 同版式，事件由"撤除"改为"反相"。
四档：无律 / 律 D / F-B（清空，α=0，反相下不触发）/ F-A（α=−1，oracle 上界）
用法：python plot_echo_rev_speed_case.py 900 15
输出：fig_echo_rev_speed_900.png
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = float(sys.argv[1]) if len(sys.argv) > 1 else 600.0
F = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
NAMES = ["Base", "LawD", "FB.clear", "FA.inv"]
D = {k: np.load("_wave_rev_%d_%s.npz" % (int(N), k)) for k in NAMES}
t = D["Base"]["t"]
CFG = [("Base", "无律", "#3a3a3a"), ("LawD", "律 D", "#c0392b"),
       ("FB.clear", "F-B 清空（反相下不触发）", "#16a085"),
       ("FA.inv", "F-A 反相复位 α=−1（oracle）", "#8e44ad")]

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

fig = plt.figure(figsize=(12.2, 9.0))
gs = fig.add_gridspec(3, 2, height_ratios=[0.7, 1.0, 1.0], hspace=0.36, wspace=0.22)
ax_load = fig.add_subplot(gs[0, :])
ax_full = fig.add_subplot(gs[1, :])
ax_tr = fig.add_subplot(gs[2, 0])
ax_ec = fig.add_subplot(gs[2, 1])

ax_load.plot(t, D["Base"]["TL"], color="#8e44ad", lw=0.7)
ax_load.axvline(2.0, color="#555", ls="--", lw=0.7)
ax_load.axvline(6.0, color="#555", ls="--", lw=0.7)
ax_load.set_xlim(0, 8); ax_load.set_ylim(-0.55, 0.55)
ax_load.set_xlabel("时间 (s)"); ax_load.set_ylabel("$T_L$ (N·m)")
ax_load.set_title("(a) 负载转矩：2 s 阶跃、2–6 s %.0f Hz 簇、6 s 零交越整体反相（值连续）" % F, fontsize=9.4)
ax_load.grid(alpha=0.22)

for k, lab, c in CFG:
    ax_full.plot(t, D[k]["y"] * N, color=c, lw=0.7, label=lab)
ax_full.axhline(N, color="#888", lw=0.7, ls=":")
ax_full.axvline(2.0, color="#555", ls="--", lw=0.7)
ax_full.axvline(6.0, color="#555", ls="--", lw=0.7)
ax_full.set_xlim(0, 8); ax_full.set_ylim(0.72 * N, 1.22 * N)
ax_full.set_xlabel("时间 (s)"); ax_full.set_ylabel("转速 (rpm)")
ax_full.set_title("(b) 完整转速：0–8 s（%d rpm / %.0f Hz，实验室工况，类 fal ESO）" % (N, F), fontsize=9.4)
ax_full.legend(fontsize=7.2, ncol=4, loc="lower center"); ax_full.grid(alpha=0.22)

for k, lab, c in CFG:
    m = (t >= 1.9) & (t <= 2.5)
    ax_tr.plot(t[m], D[k]["y"][m] * N, color=c, lw=0.9, label=lab)
ax_tr.axhline(N, color="#888", lw=0.7, ls=":")
ax_tr.axvline(2.0, color="#555", ls="--", lw=0.8)
ax_tr.set_xlim(1.9, 2.5); ax_tr.set_ylim(0.38 * N, 1.30 * N)
ax_tr.set_xlabel("时间 (s)"); ax_tr.set_ylabel("转速 (rpm)")
ax_tr.set_title("(c) 突变窗：加载阶跃 1.9–2.5 s", fontsize=9.4)
ax_tr.grid(alpha=0.22)

for k, lab, c in CFG:
    m = (t >= 5.9) & (t <= 6.4)
    ax_ec.plot(t[m], D[k]["y"][m] * N, color=c, lw=0.9, label=lab)
tr = D["FB.clear"]["trig"]
sel = tr[(tr >= 5.9) & (tr <= 6.4)]
if len(sel):
    ax_ec.vlines(sel, 0.74 * N, 0.79 * N, color="#16a085", lw=1.6, alpha=0.95)
ax_ec.axhline(N, color="#888", lw=0.7, ls=":")
ax_ec.axvline(6.0, color="#555", ls="--", lw=0.8)
ax_ec.set_xlim(5.9, 6.4); ax_ec.set_ylim(0.72 * N, 1.22 * N)
ax_ec.set_xlabel("时间 (s)"); ax_ec.set_ylabel("转速 (rpm)")
ax_ec.set_title("(d) 反相窗：事件 5.9–6.4 s", fontsize=9.4)
ax_ec.grid(alpha=0.22)

fn = "fig_echo_rev_speed_%d.png" % int(N)
fig.savefig(fn, dpi=200)
print("ok:", fn)
