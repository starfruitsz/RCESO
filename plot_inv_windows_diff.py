# -*- coding: utf-8 -*-
"""仅 Δ转速误差（相对无律）：突变窗 + 回声窗。
dq 电流不做差值，直接看 fig_inv_windows.png 的绝对值。
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

D = {k: np.load("_wave_%s.npz" % k) for k in ["Base", "LawD", "FB", "FA"]}
t = D["Base"]["t"]
N = 600.0
CFG = [("LawD", "律 D", "#c0392b"), ("FB", "新 F-B（D_m+g）", "#16a085"),
       ("FA", "F-A 立即", "#2471a3")]
WIN = [("突变窗（加载阶跃）", 1.90, 2.50, 2.0),
       ("回声窗（撤除）", 5.90, 6.40, 6.0)]

fig, ax = plt.subplots(1, 2, figsize=(12.0, 3.5))
for col, (wtitle, lo, hi, mark) in enumerate(WIN):
    m = (t >= lo) & (t <= hi)
    base = (D["Base"]["y"][m] - 1.0) * N
    for k, lab, c in CFG:
        de = (D[k]["y"][m] - 1.0) * N - base
        ax[col].plot(t[m], de, color=c, lw=0.9, label=lab)
        print("%s %-4s dErr rms %.2f" % (wtitle, k, np.sqrt(np.mean(de ** 2))))
    ax[col].axvline(mark, color="#555", ls="--", lw=0.8)
    ax[col].axhline(0, color="#888", lw=0.6)
    ax[col].set_xlabel("时间 (s)"); ax[col].set_ylabel("Δ转速误差 (rpm)")
    ax[col].set_title("(%s) %s：Δ转速误差（相对无律）" % ("ab"[col], wtitle), fontsize=9.2)
    ax[col].legend(fontsize=7.0); ax[col].grid(alpha=0.22)

fig.text(0.5, 0.01, "Δ 是相对无律的动作量，不是性能；dq 电流不做差值，见 fig_inv_windows.png 的绝对值",
         ha="center", fontsize=7.6, color="#555")
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("fig_inv_windows_diff.png", dpi=200)
print("ok: fig_inv_windows_diff.png")
