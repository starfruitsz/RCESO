# -*- coding: utf-8 -*-
"""plot_echo_rev_summary.py —— 反相工况的 10 Hz 包络对比（三转速）

四联图 (d) 面板在原始转速下四条曲线挤在一起，看不出差别；
本图把 e(t) 用 1 个周期窗解调成 10/15/20 Hz 包络，直接显示"残余幅值 vs 时间"。
输出：fig_echo_rev_summary.png
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({"figure.dpi": 130, "savefig.dpi": 150, "font.size": 9.5,
                     "axes.grid": True, "grid.alpha": 0.25, "axes.spines.top": False,
                     "axes.spines.right": False})
CFG = [("Base", "无律", "#3a3a3a"), ("LawD", "律 D", "#c0392b"),
       ("FB.clear", "F-B 清空（反相下不触发）", "#16a085"),
       ("FA.inv", "F-A 反相复位 α=−1", "#8e44ad")]
SPEEDS = [(600, 10.0), (900, 15.0), (1200, 20.0)]
TW = 6.0


def envelope(t, e, T, t0=5.0, t1=6.3, step=0.002):
    ts = np.arange(t0, t1, step)
    out = np.zeros_like(ts)
    for i, tc in enumerate(ts):
        m = (t >= tc - T) & (t < tc)
        ee = e[m]; tt = t[m]
        out[i] = math.hypot(2 * np.mean(ee * np.cos(2 * math.pi * tt / T)),
                            2 * np.mean(ee * np.sin(2 * math.pi * tt / T)))
    return ts, out


def fig():
    fig, ax = plt.subplots(1, 3, figsize=(15.5, 4.3), sharey=False)
    for i, (N, F) in enumerate(SPEEDS):
        T = 1.0 / F
        for k, lab, c in CFG:
            d = np.load("_wave_rev_%d_%s.npz" % (N, k))
            t = d["t"]; e = (d["y"] * N) - N
            ts, env = envelope(t, e, T)
            ax[i].plot(ts, env, color=c, lw=1.5, label=lab)
        ax[i].axvline(TW, color="k", ls="--", lw=0.9, alpha=0.6)
        ax[i].set_title("(%s) %d rpm / %.0f Hz" % ("abc"[i], N, F), fontsize=10.5)
        ax[i].set_xlabel("t / s")
        if i == 0:
            ax[i].set_ylabel("残余 10 Hz 包络 / rpm")
        ax[i].set_xlim(5.0, 6.3)
        ax[i].legend(fontsize=7.6, loc="upper left")
    fig.suptitle("反相工况：一个周期窗解调的残余包络（事件 6.0 s）——首拍回声与 F-A 反相复位的抑制", fontsize=12.5)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig("fig_echo_rev_summary.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig()
    print("fig_echo_rev_summary.png ok")
