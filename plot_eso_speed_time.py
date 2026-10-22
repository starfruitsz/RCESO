# -*- coding: utf-8 -*-
"""plot_eso_speed_time.py —— 600/900/1200 rpm 的转速波形（只读 _eso_speed_trace.npz）

    fig_eso_fal_speed_time.png
      左列：转速误差全程 0–8 s（Base 档，线性 vs 类 fal）
      右列：撤除窗放大 5.90–6.55 s（Base / F-B × 线性 / 类 fal；竖线=F-B 实际复位时刻）
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({"figure.dpi": 130, "savefig.dpi": 150, "font.size": 9.5,
                     "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
C_LIN, C_FAL, C_FLIN, C_FFAL = "#1f4e79", "#c0392b", "#5d6d7e", "#e67e22"
TW = 6.0
SPEEDS = [(600, 10.0, 380), (900, 15.0, 380), (1200, 20.0, 300)]


def dec(t, y, a, b, step):
    m = (t >= a) & (t < b)
    return t[m][::step], y[m][::step]


def fig():
    d = np.load("_eso_speed_trace.npz")
    t = d["t"]
    fig, ax = plt.subplots(3, 2, figsize=(14.5, 10.0),
                           gridspec_kw=dict(width_ratios=[1.3, 1.0]))
    for i, (n, f, yl) in enumerate(SPEEDS):
        k = "%d" % n
        e_lin = d[k + "_Base_lin"] - n
        e_fal = d[k + "_Base_fal"] - n
        # 左：全程误差
        xa, ya = dec(t, e_lin, 0, 8, 40)
        _, yb = dec(t, e_fal, 0, 8, 40)
        ax[i, 0].plot(xa, ya, color=C_LIN, lw=0.75, label="线性 ESO")
        ax[i, 0].plot(xa, yb, color=C_FAL, lw=0.75, alpha=0.9, label="类 fal ESO")
        ax[i, 0].axvline(TW, color="k", ls="--", lw=0.9, alpha=0.55)
        ax[i, 0].axhline(0, color="k", ls=":", lw=0.8, alpha=0.5)
        ax[i, 0].set_ylim(-yl, yl * 0.75)
        ax[i, 0].set_ylabel("转速误差 / rpm")
        ax[i, 0].set_title("(%s1) %d rpm（%.0f Hz）全程轨迹：Base 档" % ("abc"[i], n, f), fontsize=10.5)
        ax[i, 0].text(TW + 0.06, yl * 0.6, "撤除", fontsize=8.5, color="k", alpha=0.7)
        if i == 2:
            ax[i, 0].set_xlabel("t / s")
        ax[i, 0].set_xlim(0, 8)
        ax[i, 0].legend(fontsize=8.5, loc="lower left")
        # 右：撤除窗误差
        for key, c, ls, lab in ((k + "_Base_lin", C_LIN, "-", "Base·线性"),
                                (k + "_Base_fal", C_FAL, "-", "Base·类 fal"),
                                (k + "_FB_lin", C_FLIN, "--", "F-B·线性"),
                                (k + "_FB_fal", C_FFAL, "--", "F-B·类 fal")):
            xx, yy = dec(t, d[key] - n, 5.90, 6.55, 2)
            ax[i, 1].plot(xx, yy, color=c, ls=ls, lw=1.0, label=lab)
        for key, c in ((k + "_FB_lin_trig", C_FLIN), (k + "_FB_fal_trig", C_FFAL)):
            tr = d[key]
            sel = tr[(tr >= 5.95) & (tr <= 6.55)]
            ax[i, 1].vlines(sel, -18, 12, color=c, lw=1.6, alpha=0.95)
        ax[i, 1].axvline(TW, color="k", ls="--", lw=0.9, alpha=0.55)
        ax[i, 1].axhline(0, color="k", ls=":", lw=0.8, alpha=0.5)
        ax[i, 1].set_title("(%s2) 撤除窗 5.90–6.55 s（竖线 = F-B 复位时刻）" % "abc"[i], fontsize=10.5)
        ax[i, 1].set_ylim(-150, 120)
        if i == 2:
            ax[i, 1].set_xlabel("t / s")
        ax[i, 1].set_xlim(5.90, 6.55)
        if i == 0:
            ax[i, 1].legend(fontsize=7.6, loc="upper right", ncol=2)
    fig.suptitle("三个额定转速（600/900/1200 rpm）的转速误差：线性 ESO vs 类 fal ESO（实验室噪声，种子 20261018）",
                 fontsize=12.5)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig("fig_eso_fal_speed_time.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig()
    print("fig_eso_fal_speed_time.png ok")
