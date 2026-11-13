# -*- coding: utf-8 -*-
"""_realj_iqstep_fig.py —— 真实 J 下 iq 峰值的来源分解（原始 / 100us 均值 / 1ms 均值）

读 _wave_realj_check.npz（base/lawd x J_nom/J=4.81e-5，10 us 采样）
iq 原始含 10 kHz PWM/死区纹波；速度环 1 ms 一拍，故同时给出 1 ms 块均值（基波包络）。
输出 fig_realj_iqstep.png、_realj_iqstep.json
"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9,
    "figure.dpi": 150, "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
})

Z = np.load("_wave_realj_check.npz")
t = Z["t"]
CASES = [("base_jnom", "基准 · J_nom", "#1f4e79", "-"),
         ("lawd_jnom", "律D · J_nom", "#c0392b", "-"),
         ("base_j24", "基准 · J=4.81e-5", "#2980b9", "--"),
         ("lawd_j24", "律D · J=4.81e-5", "#e67e22", "--")]
RATED = 6.31
N1MS = 100        # 1 ms / 10 us


def blockmean(x, n):
    m = len(x) // n * n
    return x[:m].reshape(-1, n).mean(axis=1), t[:m:n] + (n / 2) * (t[1] - t[0])


out = {}
fig, ax = plt.subplots(1, 2, figsize=(12.8, 4.4))
fig.subplots_adjust(left=0.07, right=0.985, top=0.87, bottom=0.14, wspace=0.22)
for k, lab, c, ls in CASES:
    iq = Z["iq_" + k].astype(float)
    iqa = np.abs(iq)
    av1, tv1 = blockmean(iq, N1MS)
    av01, _ = blockmean(iq, 10)
    m = (t >= 1.99) & (t <= 2.10)
    m1 = (tv1 >= 1.99) & (tv1 <= 2.10)
    out[k] = dict(iq_max=float(iqa.max()), t_at_max=float(t[int(iqa.argmax())]),
                  iq_step_raw=float(iqa[m].max()),
                  av1ms_max=float(np.abs(av1).max()), t_av1ms=float(tv1[int(np.abs(av1).argmax())]),
                  av1ms_step=float(np.abs(av1[m1]).max()),
                  av01ms_max=float(np.abs(av01).max()),
                  ripple_pp_steady=float(np.percentile(iq[(t >= 7) & (t < 8)], 99)
                                         - np.percentile(iq[(t >= 7) & (t < 8)], 1)))
    ax[0].plot(t, iq, ls, color=c, lw=1.0, label=lab)
    ax[1].plot(tv1, av1, ls, color=c, lw=1.1, label=lab)
    ax[1].plot([out[k]["t_av1ms"]], [out[k]["av1ms_max"]], "v", color=c, ms=6, mfc="none", mew=1.3)
ax[0].axvline(2.0, color="#555", lw=0.8, ls=":")
ax[0].axhline(RATED, color="#8e44ad", lw=0.9, ls="-.")
ax[0].axhline(-RATED, color="#8e44ad", lw=0.9, ls="-.")
ax[0].set_xlim(1.97, 2.12); ax[0].set_xlabel("t / s"); ax[0].set_ylabel("$i_q$ / A（原始 10 us）")
ax[0].set_title("(a) 加载瞬间：原始 i_q（含 10 kHz 纹波）", fontsize=9.5)
ax[0].legend(loc="lower right", fontsize=7.5)
ax[1].axhline(RATED, color="#8e44ad", lw=0.9, ls="-.", label="额定 6.31 A")
ax[1].set_xlim(2.0, 8.0); ax[1].set_ylim(0, 7.2)
ax[1].set_xlabel("t / s"); ax[1].set_ylabel("$i_q$ 1 ms 均值 / A")
ax[1].set_title("(b) 1 ms 块均值（基波包络）", fontsize=9.5)
ax[1].legend(loc="lower right", fontsize=7.5)
fig.suptitle("真实 J（4.81e-5=2.545 J_nom）$i_q$ 峰值分解：阶跃尖峰 vs 稳态纹波 vs PWM 纹波", fontsize=10.5)
fig.savefig("fig_realj_iqstep.png", dpi=150, facecolor="white")
json.dump(out, open("_realj_iqstep.json", "w"), indent=1)
for k, d in out.items():
    print("%-11s raw %.3f@%.4f | 1ms-avg %.3f@%.4f (step %.3f) | 100us-avg %.3f | steady ripple p99-p01 %.2f"
          % (k, d["iq_max"], d["t_at_max"], d["av1ms_max"], d["t_av1ms"],
             d["av1ms_step"], d["av01ms_max"], d["ripple_pp_steady"]))
print("ok")
