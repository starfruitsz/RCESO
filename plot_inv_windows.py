# -*- coding: utf-8 -*-
"""突变窗 + 回声窗：转速误差 / iq / id（四配置）→ fig_inv_windows.png"""
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
t = D["Base"]["t"]
N = 600.0
CFG = [("Base", "无律", "#3a3a3a"), ("LawD", "律 D", "#c0392b"),
       ("FB", "新 F-B（D_m+g）", "#16a085"), ("FA", "F-A 立即", "#2471a3")]
WIN = [("突变窗（加载阶跃）", 1.90, 2.50, 2.0),
       ("回声窗（撤除）", 5.90, 6.40, 6.0)]

fig, ax = plt.subplots(3, 2, figsize=(12.0, 8.6))

for col, (wtitle, lo, hi, mark) in enumerate(WIN):
    m = (t >= lo) & (t <= hi)
    # 转速误差
    for k, lab, c in CFG:
        ax[0, col].plot(t[m], (D[k]["y"][m] - 1.0) * N, color=c, lw=0.9, label=lab)
    ax[0, col].axvline(mark, color="#555", ls="--", lw=0.8)
    ax[0, col].set_xlabel("时间 (s)"); ax[0, col].set_ylabel("转速误差 (rpm)")
    ax[0, col].set_title("(%s) %s：转速误差" % ("ab"[col], wtitle), fontsize=9.2)
    ax[0, col].legend(fontsize=6.8, ncol=2); ax[0, col].grid(alpha=0.22)

    # iq
    for k, lab, c in CFG:
        ax[1, col].plot(t[m], D[k]["iq"][m], color=c, lw=0.9, label=lab)
    ax[1, col].axvline(mark, color="#555", ls="--", lw=0.8)
    ax[1, col].set_xlabel("时间 (s)"); ax[1, col].set_ylabel("$i_q$ (A)")
    ax[1, col].set_title("(%s) %s：$i_q$" % ("cd"[col], wtitle), fontsize=9.2)
    ax[1, col].legend(fontsize=6.8, ncol=2); ax[1, col].grid(alpha=0.22)

    # id
    for k, lab, c in CFG:
        ax[2, col].plot(t[m], D[k]["id"][m], color=c, lw=0.9, label=lab)
    ax[2, col].axvline(mark, color="#555", ls="--", lw=0.8)
    ax[2, col].set_xlabel("时间 (s)"); ax[2, col].set_ylabel("$i_d$ (A)")
    ax[2, col].set_title("(%s) %s：$i_d$" % ("ef"[col], wtitle), fontsize=9.2)
    ax[2, col].legend(fontsize=6.8, ncol=2); ax[2, col].grid(alpha=0.22)

    # 窗口指标
    for k, lab, c in CFG:
        e = (D[k]["y"][m] - 1.0) * N
        print("%s %-4s %s: err rms %.1f min %.1f | iq rms %.2f max %.2f"
              % (wtitle, k, "%.2f-%.2f" % (lo, hi),
                 np.sqrt(np.mean(e ** 2)), e.min(),
                 np.sqrt(np.mean(D[k]["iq"][m] ** 2)), D[k]["iq"][m].max()))

fig.tight_layout()
fig.savefig("fig_inv_windows.png", dpi=200)
print("ok: fig_inv_windows.png")
