# -*- coding: utf-8 -*-
"""完整转速排版：第一行完整 0–8 s；第二行左突变窗、右回声窗"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

D = {k: np.load("_wave_%s.npz" % k) for k in ["Base", "LawD", "FB", "FA"]}
t = D["Base"]["t"]
N = 600.0
CFG = [("Base", "无律", "#3a3a3a"), ("LawD", "律 D", "#c0392b"),
       ("FB", "新 F-B（D_m+g）", "#16a085"), ("FA", "F-A 立即", "#2471a3")]

fig = plt.figure(figsize=(12.2, 7.2))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0], hspace=0.32, wspace=0.22)
ax_full = fig.add_subplot(gs[0, :])
ax_tr = fig.add_subplot(gs[1, 0])
ax_ec = fig.add_subplot(gs[1, 1])

# (a) 完整 0–8 s
for k, lab, c in CFG:
    ax_full.plot(t, D[k]["y"] * N, color=c, lw=0.7, label=lab)
ax_full.axhline(600, color="#888", lw=0.7, ls=":")
ax_full.axvline(2.0, color="#555", ls="--", lw=0.7)
ax_full.axvline(6.0, color="#555", ls="--", lw=0.7)
ax_full.set_xlim(0, 8); ax_full.set_ylim(200, 780)
ax_full.set_xlabel("时间 (s)"); ax_full.set_ylabel("转速 (rpm)")
ax_full.set_title("(a) 完整转速：0–8 s（600 rpm 给定）", fontsize=9.4)
ax_full.legend(fontsize=7.4, ncol=4); ax_full.grid(alpha=0.22)

# (b) 突变窗
for k, lab, c in CFG:
    m = (t >= 1.9) & (t <= 2.5)
    ax_tr.plot(t[m], D[k]["y"][m] * N, color=c, lw=0.9, label=lab)
ax_tr.axhline(600, color="#888", lw=0.7, ls=":")
ax_tr.axvline(2.0, color="#555", ls="--", lw=0.8)
ax_tr.set_xlim(1.9, 2.5); ax_tr.set_ylim(240, 760)
ax_tr.set_xlabel("时间 (s)"); ax_tr.set_ylabel("转速 (rpm)")
ax_tr.set_title("(b) 突变窗：加载阶跃 1.9–2.5 s", fontsize=9.4)
ax_tr.grid(alpha=0.22)

# (c) 回声窗
for k, lab, c in CFG:
    m = (t >= 5.9) & (t <= 6.4)
    ax_ec.plot(t[m], D[k]["y"][m] * N, color=c, lw=0.9, label=lab)
ax_ec.axhline(600, color="#888", lw=0.7, ls=":")
ax_ec.axvline(6.0, color="#555", ls="--", lw=0.8)
ax_ec.set_xlim(5.9, 6.4); ax_ec.set_ylim(450, 720)
ax_ec.set_xlabel("时间 (s)"); ax_ec.set_ylabel("转速 (rpm)")
ax_ec.set_title("(c) 回声窗：撤除 5.9–6.4 s", fontsize=9.4)
ax_ec.grid(alpha=0.22)

fig.savefig("fig_inv_speed.png", dpi=200)
print("ok: fig_inv_speed.png")

for k in ["Base", "LawD", "FB", "FA"]:
    n = D[k]["y"] * N
    m1 = (t >= 1.9) & (t < 2.6)
    m2 = (t >= 6.0) & (t < 6.2)
    print("%-4s min_step %.1f | echo %.1f..%.1f"
          % (k, n[m1].min(), n[m2].min(), n[m2].max()))
