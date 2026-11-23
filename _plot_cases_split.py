# -*- coding: utf-8 -*-
"""_plot_cases_split.py —— 三张独立对照图：每个工况 vs 对照组（不四合一）。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 7.4,
})

C_CTRL = "#7f8c8d"
CASES = [
    dict(key="load", color="#e67e22", name="负载突变（2 s 0→0.5 额定）",
         title="负载突变 vs 对照组（600 rpm；不对中 β=1° + 圆盘不平衡）",
         out="fig_case_load_vs_ctrl.png"),
    dict(key="b0", color="#c0392b", name="b0 严重失配（J=5.26J$_{nom}$）",
         title="b0 严重失配 vs 对照组（600 rpm；不对中 β=1° + 圆盘不平衡）",
         out="fig_case_b0_vs_ctrl.png"),
    dict(key="tm", color="#1f4e79", name="T 失配（6 s 换速 600→300）",
         title="T 失配 vs 对照组（600 rpm→300 rpm；不对中 β=1° + 圆盘不平衡）",
         out="fig_case_tm_vs_ctrl.png"),
]

def load(c):
    z = np.load("_c4_%s.npz" % c)
    t = np.asarray(z["t"]); dec = max(1, int(round(1e-5 / (t[1] - t[0]))))
    return dict(t=t[::dec], y=np.asarray(z["y"])[::dec] * 600.0, tl=np.asarray(z["tl"])[::dec])

ctrl = load("ctrl")
for cs in CASES:
    d = load(cs["key"])
    fig, ax = plt.subplots(2, 2, figsize=(12.8, 6.4))
    fig.subplots_adjust(left=0.07, right=0.99, top=0.86, bottom=0.10, wspace=0.22, hspace=0.40)
    lab_c = "对照组（恒载、恒 600）"
    ax[0, 0].plot(ctrl["t"], ctrl["tl"], color=C_CTRL, lw=1.2, label=lab_c)
    ax[0, 0].plot(d["t"], d["tl"], color=cs["color"], lw=1.0, label=cs["name"])
    ax[0, 0].set_xlim(0, 8); ax[0, 0].set_ylim(-0.03, 0.62)
    ax[0, 0].set_ylabel("$T_L$ / N·m"); ax[0, 0].set_title("(a) 两组负载", fontsize=8.8)
    ax[0, 0].legend(fontsize=6.8, loc="upper left")

    ax[0, 1].plot(ctrl["t"], ctrl["y"], color=C_CTRL, lw=0.7, label=lab_c)
    ax[0, 1].plot(d["t"], d["y"], color=cs["color"], lw=0.7, label=cs["name"])
    ax[0, 1].axhline(600, color="#888", ls=":", lw=0.8)
    ax[0, 1].axvline(2.0, color="#888", ls="--", lw=0.7, alpha=0.7)
    ax[0, 1].text(2.05, 748, "2 s 加载", fontsize=6.4, color="#555")
    if cs["key"] == "tm":
        ax[0, 1].axvline(6.0, color="#888", ls="--", lw=0.7, alpha=0.7)
        ax[0, 1].text(6.05, 748, "6 s 换速", fontsize=6.4, color="#555")
    ax[0, 1].set_xlim(0, 8); ax[0, 1].set_ylim(150, 760)
    ax[0, 1].set_ylabel("转速 / rpm"); ax[0, 1].set_title("(b) 全程转速", fontsize=8.8)
    ax[0, 1].legend(fontsize=6.8, loc="lower left")
    if cs["key"] == "b0":
        ax[0, 1].text(4.2, 175, "b0 真值 122.3 / 标称 643.7（5.26×）\niq1ms 4.9 vs 6.0 A（失配→出力偏小）",
                      fontsize=6.4, color="#7b241c", va="bottom")

    m = (ctrl["t"] >= 1.9) & (ctrl["t"] <= 2.5)
    ax[1, 0].plot(ctrl["t"][m], ctrl["y"][m] - 600.0, color=C_CTRL, lw=0.9, label="对照组")
    mm = (d["t"] >= 1.9) & (d["t"] <= 2.5)
    ax[1, 0].plot(d["t"][mm], d["y"][mm] - 600.0, color=cs["color"], lw=0.9, label=cs["name"])
    dip = float((d["y"][mm] - 600.0).min())
    ax[1, 0].set_xlim(1.9, 2.5); ax[1, 0].set_ylim(min(-520, dip * 1.15), 160)
    ax[1, 0].set_ylabel("转速误差 / rpm"); ax[1, 0].set_title("(c) 加载窗 1.9–2.5 s", fontsize=8.8)
    ax[1, 0].legend(fontsize=6.8, loc="lower right")
    ax[1, 0].text(1.905, dip * 1.12, "跌至 %.0f rpm" % dip, fontsize=6.6, color=cs["color"], va="bottom")

    m = (ctrl["t"] >= 5.8) & (ctrl["t"] <= 6.4)
    ax[1, 1].plot(ctrl["t"][m], ctrl["y"][m], color=C_CTRL, lw=0.9, label="对照组")
    mm = (d["t"] >= 5.8) & (d["t"] <= 6.4)
    ax[1, 1].plot(d["t"][mm], d["y"][mm], color=cs["color"], lw=0.9, label=cs["name"])
    if cs["key"] == "tm":
        ax[1, 1].set_ylim(150, 760); ttl = "(d) 换速窗 5.8–6.4 s"
    else:
        ax[1, 1].set_ylim(480, 720); ttl = "(d) 稳态窗 5.8–6.4 s"
    ax[1, 1].set_xlim(5.8, 6.4)
    ax[1, 1].set_ylabel("转速 / rpm"); ax[1, 1].set_title(ttl, fontsize=8.8)
    ax[1, 1].legend(fontsize=6.8, loc="lower left")

    fig.suptitle(cs["title"], fontsize=9.8, y=0.965)
    fig.savefig(cs["out"], dpi=150, bbox_inches=None, facecolor="white")
    plt.close(fig)
    print("saved", cs["out"])
