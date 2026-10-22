# -*- coding: utf-8 -*-
"""plot_echo_reversal.py —— 为什么要把回声工况从"撤除"换成"反相"（只读 JSON/npz）

    fig_echo_case.png
      (a) 两种事件的负载：撤除 vs 反相（5.5–6.5 s）
      (b) 转速误差 5.90–6.40 s：四组（事件 × ESO）
      (c) 逐周期 10 Hz 幅值：k = -1（事件前）到 3
      (d) 可辨识度：首周期 / 事件前（>1 才看得见）
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({"figure.dpi": 130, "savefig.dpi": 150, "font.size": 9.5,
                     "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
T, TW = 0.1, 6.0
CL = {"removal_lin": ("#5d6d7e", "-", "撤除·线性"),
      "removal_fal": ("#1f4e79", "-", "撤除·类 fal"),
      "reversal_lin": ("#e67e22", "-", "反相·线性"),
      "reversal_fal": ("#c0392b", "-", "反相·类 fal")}


def fig():
    j = json.load(open("_echo_reversal.json", encoding="utf-8"))
    d = np.load("_echo_reversal_trace.npz")
    t = d["t"]
    fig, ax = plt.subplots(2, 2, figsize=(12.6, 7.6))

    m = (t >= 5.5) & (t <= 6.6)
    ax[0, 0].plot(t[m][::5], d["TL_removal"][m][::5], color="#5d6d7e", lw=1.0, label="撤除")
    ax[0, 0].plot(t[m][::5], d["TL_reversal"][m][::5], color="#c0392b", lw=1.0, label="反相")
    ax[0, 0].axvline(TW, color="k", ls="--", lw=0.9, alpha=0.6)
    ax[0, 0].set_xlabel("t / s"); ax[0, 0].set_ylabel("$T_L$ / N·m")
    ax[0, 0].set_title("(a) 两种事件的负载：撤除（→0）与反相（→−c）", fontsize=10)
    ax[0, 0].legend(fontsize=8.5)

    m = (t >= 5.90) & (t <= 6.40)
    for k in ("removal_lin", "removal_fal", "reversal_lin", "reversal_fal"):
        c, ls, lab = CL[k]
        ax[0, 1].plot(t[m][::2], d[k][m][::2], color=c, ls=ls, lw=1.0, label=lab)
    ax[0, 1].axvline(TW, color="k", ls="--", lw=0.9, alpha=0.6)
    ax[0, 1].axhline(0, color="k", ls=":", lw=0.8, alpha=0.5)
    ax[0, 1].set_xlabel("t / s"); ax[0, 1].set_ylabel("转速误差 / rpm")
    ax[0, 1].set_title("(b) 事件窗：反相后的 10 Hz 回声明显更高", fontsize=10)
    ax[0, 1].legend(fontsize=8, ncol=2)

    ks = [-1, 0, 1, 2, 3]
    for k in ("removal_lin", "removal_fal", "reversal_lin", "reversal_fal"):
        rr = j[k.replace("_", "·")]
        pre = np.mean([x["pre"] for x in rr])
        post = [np.mean([x["post"][i] for x in rr]) for i in range(4)]
        c, ls, lab = CL[k]
        ax[1, 0].plot(ks, [pre] + post, "o-", color=c, lw=1.6, ms=5, label=lab)
    ax[1, 0].axvline(-0.5, color="k", ls="--", lw=0.9, alpha=0.5)
    ax[1, 0].set_yscale("log")
    ax[1, 0].set_xlabel("事件后的第 k 个周期（k=−1 为事件前）")
    ax[1, 0].set_ylabel("10 Hz 幅值 / rpm（对数）")
    ax[1, 0].set_title("(c) 逐周期衰减：撤除的首周期低于事件前，反相高于事件前", fontsize=10)
    ax[1, 0].legend(fontsize=8.5)

    labels = ["撤除·线性", "撤除·类 fal", "反相·线性", "反相·类 fal"]
    keys = ["removal_lin", "removal_fal", "reversal_lin", "reversal_fal"]
    ratios = [np.mean([x["ratio"] for x in j[k.replace("_", "·")]]) for k in keys]
    cols = [CL[k][0] for k in keys]
    b = ax[1, 1].bar(range(4), ratios, 0.6, color=cols, alpha=0.9)
    ax[1, 1].axhline(1.0, color="k", ls="--", lw=1.0)
    ax[1, 1].text(3.42, 1.03, "=1：回声与稳态残余同量级\n（低于此线即图上不可辨）", fontsize=8, ha="right")
    for i, v in enumerate(ratios):
        ax[1, 1].text(i, v + 0.04, "%.2f" % v, ha="center", fontsize=9)
    ax[1, 1].set_xticks(range(4)); ax[1, 1].set_xticklabels(labels, fontsize=8.5)
    ax[1, 1].set_ylim(0, max(ratios) * 1.35)
    ax[1, 1].set_ylabel("首周期 / 事件前")
    ax[1, 1].set_title("(d) 可辨识度：撤除 0.44–0.60（不可辨）→ 反相 1.26–1.54（可辨）", fontsize=9.6)

    fig.suptitle("回声工况换型：撤除 → 反相（600 rpm / 10 Hz，实验室噪声，8 种子）", fontsize=12.5)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig("fig_echo_case.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig()
    print("fig_echo_case.png ok")
