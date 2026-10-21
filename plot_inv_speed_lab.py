# -*- coding: utf-8 -*-
"""实验室工况转速排版：第一行负载、第二行完整转速、第三行左突变/右回声"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

NAMES = ["Base", "LawD", "FB", "D+FB"]
D = {k: np.load("_wave_lab_%s.npz" % k) for k in NAMES}
t = D["Base"]["t"]
N = 600.0
CFG = [("Base", "无律", "#3a3a3a"), ("LawD", "律 D", "#c0392b"),
       ("FB", "新 F-B（D_m+g）", "#16a085"), ("D+FB", "D+F-B", "#8e44ad")]

fig = plt.figure(figsize=(12.2, 9.0))
gs = fig.add_gridspec(3, 2, height_ratios=[0.7, 1.0, 1.0],
                      hspace=0.36, wspace=0.22)
ax_load = fig.add_subplot(gs[0, :])
ax_full = fig.add_subplot(gs[1, :])
ax_tr = fig.add_subplot(gs[2, 0])
ax_ec = fig.add_subplot(gs[2, 1])

# (a) 负载
ax_load.plot(t, D["Base"]["TL"], color="#8e44ad", lw=0.7)
ax_load.axvline(2.0, color="#555", ls="--", lw=0.7)
ax_load.axvline(6.0, color="#555", ls="--", lw=0.7)
ax_load.set_xlim(0, 8); ax_load.set_ylim(-0.05, 0.7)
ax_load.set_xlabel("时间 (s)"); ax_load.set_ylabel("$T_L$ (N·m)")
ax_load.set_title("(a) 负载转矩：0–2 s 空载，2 s 阶跃，2–6 s 10 Hz 簇，6 s 撤除", fontsize=9.4)
ax_load.grid(alpha=0.22)

# (b) 完整转速
for k, lab, c in CFG:
    ax_full.plot(t, D[k]["y"] * N, color=c, lw=0.7, label=lab)
ax_full.axhline(600, color="#888", lw=0.7, ls=":")
ax_full.axvline(2.0, color="#555", ls="--", lw=0.7)
ax_full.axvline(6.0, color="#555", ls="--", lw=0.7)
nall = np.concatenate([D[k]['y'] * N for k in NAMES])
ax_full.set_xlim(0, 8); ax_full.set_ylim(max(0, nall.min() - 30), nall.max() + 30)
ax_full.set_xlabel("时间 (s)"); ax_full.set_ylabel("转速 (rpm)")
ax_full.set_title("(b) 完整转速：0–8 s（实验室工况，600 rpm 给定）", fontsize=9.4)
ax_full.legend(fontsize=7.4, ncol=4); ax_full.grid(alpha=0.22)

# (c) 突变
for k, lab, c in CFG:
    m = (t >= 1.9) & (t <= 2.5)
    ax_tr.plot(t[m], D[k]["y"][m] * N, color=c, lw=0.9, label=lab)
ax_tr.axhline(600, color="#888", lw=0.7, ls=":")
ax_tr.axvline(2.0, color="#555", ls="--", lw=0.8)
ntr = np.concatenate([D[k]['y'][(t >= 1.9) & (t <= 2.5)] * N for k in NAMES])
ax_tr.set_xlim(1.9, 2.5); ax_tr.set_ylim(max(0, ntr.min() - 30), ntr.max() + 30)
ax_tr.set_xlabel("时间 (s)"); ax_tr.set_ylabel("转速 (rpm)")
ax_tr.set_title("(c) 突变窗：加载阶跃 1.9–2.5 s", fontsize=9.4)
ax_tr.grid(alpha=0.22)

# (d) 回声
for k, lab, c in CFG:
    m = (t >= 5.9) & (t <= 6.4)
    ax_ec.plot(t[m], D[k]["y"][m] * N, color=c, lw=0.9, label=lab)
ax_ec.axhline(600, color="#888", lw=0.7, ls=":")
ax_ec.axvline(6.0, color="#555", ls="--", lw=0.8)
nec = np.concatenate([D[k]['y'][(t >= 5.9) & (t <= 6.4)] * N for k in NAMES])
ax_ec.set_xlim(5.9, 6.4); ax_ec.set_ylim(max(0, nec.min() - 30), nec.max() + 30)
ax_ec.set_xlabel("时间 (s)"); ax_ec.set_ylabel("转速 (rpm)")
ax_ec.set_title("(d) 回声窗：撤除 5.9–6.4 s", fontsize=9.4)
ax_ec.grid(alpha=0.22)

fig.savefig("fig_inv_speed_lab.png", dpi=200)
print("ok: fig_inv_speed_lab.png")
