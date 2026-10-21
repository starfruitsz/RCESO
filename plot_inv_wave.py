# -*- coding: utf-8 -*-
"""三张图：负载转矩、转速误差、dq 电流（四配置）→ fig_inv_wave.png

数据：_wave_{Base,LawD,FB,FA}.npz（每配置自己的 Y["t"]，避免对齐问题）。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.0,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

NAMES = ["Base", "LawD", "FB", "FA"]
D = {k: np.load("_wave_%s.npz" % k) for k in NAMES}
t = D["Base"]["t"]; TL = D["Base"]["TL"]
N = 600.0
CFG = [("Base", "无律", "#3a3a3a"), ("LawD", "律 D", "#c0392b"),
       ("FB", "新 F-B（D_m+g）", "#16a085"), ("FA", "F-A 立即", "#2471a3")]

fig, ax = plt.subplots(3, 2, figsize=(12.4, 9.0))

# (a) 负载转矩
ax[0, 0].plot(t, TL, color="#8e44ad", lw=0.7)
ax[0, 0].axvspan(2.0, 6.0, color="#8e44ad", alpha=0.06)
ax[0, 0].axvline(6.0, color="#555", ls="--", lw=0.8)
ax[0, 0].set_xlabel("时间 (s)"); ax[0, 0].set_ylabel("$T_L$ (N·m)")
ax[0, 0].set_title("(a) 负载转矩：2 s 阶跃 + 2–6 s 10 Hz 簇，6 s 撤除", fontsize=9.3)
ax[0, 0].grid(alpha=0.22)

# (b) 转速误差全景
for k, lab, c in CFG:
    ax[0, 1].plot(t, (D[k]["y"] - 1.0) * N, color=c, lw=0.6, label=lab)
ax[0, 1].set_xlabel("时间 (s)"); ax[0, 1].set_ylabel("转速误差 (rpm)")
ax[0, 1].set_title("(b) 转速误差（8 s）", fontsize=9.3)
ax[0, 1].legend(fontsize=7.0, ncol=2); ax[0, 1].grid(alpha=0.22)

# (c) 转速误差回声窗放大
for k, lab, c in CFG:
    m = (t >= 5.85) & (t <= 6.45)
    ax[1, 0].plot(t[m], (D[k]["y"][m] - 1.0) * N, color=c, lw=0.8, label=lab)
ax[1, 0].axvline(6.0, color="#555", ls="--", lw=0.8)
ax[1, 0].set_xlabel("时间 (s)"); ax[1, 0].set_ylabel("转速误差 (rpm)")
ax[1, 0].set_title("(c) 回声窗放大（5.85–6.45 s）", fontsize=9.3)
ax[1, 0].legend(fontsize=7.0); ax[1, 0].grid(alpha=0.22)

# (d) iq 全景
for k, lab, c in CFG:
    ax[1, 1].plot(t, D[k]["iq"], color=c, lw=0.5, label=lab)
ax[1, 1].set_xlabel("时间 (s)"); ax[1, 1].set_ylabel("$i_q$ (A)")
ax[1, 1].set_title("(d) q 轴电流 $i_q$（8 s）", fontsize=9.3)
ax[1, 1].legend(fontsize=7.0, ncol=2); ax[1, 1].grid(alpha=0.22)

# (e) iq 回声窗
for k, lab, c in CFG:
    m = (t >= 5.95) & (t <= 6.20)
    ax[2, 0].plot(t[m], D[k]["iq"][m], color=c, lw=0.9, label=lab)
ax[2, 0].axvline(6.0, color="#555", ls="--", lw=0.8)
ax[2, 0].set_xlabel("时间 (s)"); ax[2, 0].set_ylabel("$i_q$ (A)")
ax[2, 0].set_title("(e) $i_q$ 回声窗（5.95–6.20 s）", fontsize=9.3)
ax[2, 0].legend(fontsize=7.0); ax[2, 0].grid(alpha=0.22)

# (f) id 回声窗
for k, lab, c in CFG:
    m = (t >= 5.95) & (t <= 6.20)
    ax[2, 1].plot(t[m], D[k]["id"][m], color=c, lw=0.9, label=lab)
ax[2, 1].axvline(6.0, color="#555", ls="--", lw=0.8)
ax[2, 1].set_xlabel("时间 (s)"); ax[2, 1].set_ylabel("$i_d$ (A)")
ax[2, 1].set_title("(f) $i_d$ 回声窗（5.95–6.20 s）", fontsize=9.3)
ax[2, 1].legend(fontsize=7.0); ax[2, 1].grid(alpha=0.22)

fig.tight_layout()
fig.savefig("fig_inv_wave.png", dpi=200)
print("ok: fig_inv_wave.png")
