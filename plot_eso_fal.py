# -*- coding: utf-8 -*-
"""plot_eso_fal.py —— 类 fal ESO 增益的四张图（只读 JSON/npz，不重新仿真）

    fig_eso_fal_gain.png    增益形状与小信号斜率
    fig_eso_fal_time.png    线性 vs 类 fal 的时域对照（同种子同噪声）
    fig_eso_fal_pareto.png  12 组参数的（稳态噪声, 回声）散点
    fig_eso_fal_4cfg.png    四档算法 × 两种增益的复算结果
"""
import json
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from eso_gain import FalGain

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({"figure.dpi": 130, "savefig.dpi": 150, "font.size": 10,
                     "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})

T, TW, N_REF = 0.1, 6.0, 600.0
C_LIN, C_FAL, C_ACC, C_MUT = "#1f4e79", "#c0392b", "#e67e22", "#7f8c8d"


def fig_gain():
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    e = np.linspace(-0.6, 0.6, 1201)
    ax[0].plot(e, e, "--", color=C_MUT, lw=1.2, label="线性 $G(e)=e$")
    for (a, d, l), c in zip([(0.75, 0.10, 10), (0.70, 0.10, 10), (0.80, 0.10, 10),
                             (0.90, 0.20, 10)], [C_FAL, C_ACC, "#8e44ad", "#16a085"]):
        g = np.array([FalGain(a, d, l)(x) for x in e])
        ax[0].plot(e, g, color=c, lw=1.8, label=r"$a$=%.2f, $\delta$=%.2f" % (a, d))
    ax[0].set_xlabel("观测误差 $e_1=y-z_1$（标幺）")
    ax[0].set_ylabel("$G(e)$")
    ax[0].set_title("(a) 校正增益：小误差段放大 $1/\\delta^{1-a}$ 倍，随 $|e|$ 增大回落到线性")
    ax[0].legend(fontsize=8.5, loc="upper left")
    ax[0].set_xlim(-0.6, 0.6)

    ds = np.linspace(0.01, 0.5, 300)
    for a, c in zip([0.6, 0.7, 0.75, 0.8, 0.9], ["#f39c12", "#e67e22", C_FAL, "#8e44ad", "#16a085"]):
        ax[1].plot(ds, ds ** (a - 1.0), color=c, lw=1.8, label=r"$a$=%.2f" % a)
    ax[1].axhline(1.0, color=C_MUT, ls="--", lw=1.0)
    for d, lbl in [(0.05, ""), (0.10, "推荐 $\\delta$=0.10"), (0.20, "")]:
        ax[1].axvline(d, color=C_MUT, ls=":", lw=0.8)
    ax[1].annotate("推荐 $\\delta$=0.10\n$a$=0.75 → 1.78$\\times$", xy=(0.10, 0.10 ** -0.25),
                   xytext=(0.17, 3.2), fontsize=8.5,
                   arrowprops=dict(arrowstyle="->", color=C_MUT, lw=0.9))
    ax[1].set_xlabel(r"拐点 $\delta$（标幺；0.10 = 10% 额定转速）")
    ax[1].set_ylabel(r"小信号斜率 $\delta^{a-1}$")
    ax[1].set_title(r"(b) 小信号斜率 = $\delta^{a-1}$（与 $\lambda$ 无关）：噪声增益的唯一旋钮")
    ax[1].set_ylim(0, 6)
    ax[1].legend(fontsize=8.5)
    fig.tight_layout()
    fig.savefig("fig_eso_fal_gain.png", bbox_inches="tight")
    plt.close(fig)


def fig_time():
    d = np.load("_eso_trace.npz")
    t = d["t"]
    e_lin = (d["y_lin"] - 1.0) * N_REF
    e_fal = (d["y_fal"] - 1.0) * N_REF
    step = max(1, len(t) // 8000)          # 只画包络，避免 10 kHz 点糊成一团

    def amp10(e):
        m = (t >= TW) & (t < TW + T)
        return math.hypot(2 * np.mean(e[m] * np.cos(2 * math.pi * t[m] / T)),
                          2 * np.mean(e[m] * np.sin(2 * math.pi * t[m] / T)))
    def dip(e):
        return float(np.min(e[(t >= 1.9) & (t <= 2.4)]))
    def steady(e):
        return float(np.sqrt(np.mean(e[(t >= 7) & (t < 8)] ** 2)))
    M = dict(lin=(amp10(e_lin), dip(e_lin), steady(e_lin)),
             fal=(amp10(e_fal), dip(e_fal), steady(e_fal)))

    def sel(x, y, a, b):
        m = (x >= a) & (x < b)
        return x[m][::step], y[m][::step]

    fig, ax = plt.subplots(2, 3, figsize=(14.5, 7))
    # (a) 全程
    xa, ya = sel(t, e_lin, 0, 8); _, yb = sel(t, e_fal, 0, 8)
    ax[0, 0].plot(xa, ya, color=C_LIN, lw=0.7, label="线性")
    ax[0, 0].plot(xa, yb, color=C_FAL, lw=0.7, alpha=0.85, label="类 fal")
    ax[0, 0].axvline(TW, color=C_MUT, ls="--", lw=1.0)
    ax[0, 0].text(TW + 0.08, np.nanmax(ya) * 0.55, "撤除事件", fontsize=8.5, color=C_MUT)
    ax[0, 0].set_ylabel("转速误差 / rpm"); ax[0, 0].set_xlabel("t / s")
    ax[0, 0].set_title("(a) 全程 0–8 s"); ax[0, 0].legend(fontsize=9, loc="lower left")

    # (b) 回声窗
    xa, ya = sel(t, e_lin, 5.95, 6.9); _, yb = sel(t, e_fal, 5.95, 6.9)
    ax[0, 1].plot(xa, ya, color=C_LIN, lw=1.0, label="线性 %.1f rpm" % M["lin"][0])
    ax[0, 1].plot(xa, yb, color=C_FAL, lw=1.0, label="类 fal %.1f rpm" % M["fal"][0])
    ax[0, 1].axvline(TW, color=C_MUT, ls="--", lw=0.9)
    ax[0, 1].set_ylabel("rpm"); ax[0, 1].set_xlabel("t / s")
    ax[0, 1].set_title("(b) 回声窗放大（首周期 10 Hz 幅值）"); ax[0, 1].legend(fontsize=9)

    # (c) 加载窗
    xa, ya = sel(t, e_lin, 1.9, 2.6); _, yb = sel(t, e_fal, 1.9, 2.6)
    ax[0, 2].plot(xa, ya, color=C_LIN, lw=1.0, label="线性 %.1f" % M["lin"][1])
    ax[0, 2].plot(xa, yb, color=C_FAL, lw=1.0, label="类 fal %.1f" % M["fal"][1])
    ax[0, 2].set_ylabel("rpm"); ax[0, 2].set_xlabel("t / s")
    ax[0, 2].set_title("(c) 加载跌落放大"); ax[0, 2].legend(fontsize=9)

    # (d) 稳态
    xa, ya = sel(t, e_lin, 7.0, 7.6); _, yb = sel(t, e_fal, 7.0, 7.6)
    ax[1, 0].plot(xa, ya, color=C_LIN, lw=0.8, label="线性 %.2f" % M["lin"][2])
    ax[1, 0].plot(xa, yb, color=C_FAL, lw=0.8, label="类 fal %.2f" % M["fal"][2])
    ax[1, 0].set_ylabel("rpm"); ax[1, 0].set_xlabel("t / s")
    ax[1, 0].set_title("(d) 稳态 7.0–7.6 s"); ax[1, 0].legend(fontsize=9)

    # (e) 逐周期 10 Hz
    cyc = np.arange(0, 7)
    def per_cycle(e):
        v = []
        for k in cyc:
            m = (t >= TW + k * T) & (t < TW + (k + 1) * T)
            ee = e[m]; tt = t[m]
            v.append(math.hypot(2 * np.mean(ee * np.cos(2 * math.pi * tt / T)),
                                2 * np.mean(ee * np.sin(2 * math.pi * tt / T))))
        return np.array(v)
    ax[1, 1].plot(cyc, per_cycle(e_lin), "o-", color=C_LIN, lw=1.6, ms=5, label="线性")
    ax[1, 1].plot(cyc, per_cycle(e_fal), "s-", color=C_FAL, lw=1.6, ms=5, label="类 fal")
    ax[1, 1].set_xlabel("撤除事件后的第 k 个周期"); ax[1, 1].set_ylabel("10 Hz 幅值 / rpm")
    ax[1, 1].set_title("(e) 逐周期 10 Hz 衰减"); ax[1, 1].legend(fontsize=9)

    # (f) iq
    xa, ya = sel(t, d["iq_lin"], 4.0, 4.4); _, yb = sel(t, d["iq_fal"], 4.0, 4.4)
    ax[1, 2].plot(xa, ya, color=C_LIN, lw=0.7, alpha=0.85, label="线性")
    ax[1, 2].plot(xa, yb, color=C_FAL, lw=0.7, alpha=0.85, label="类 fal")
    ax[1, 2].set_ylabel("$i_q$ / A"); ax[1, 2].set_xlabel("t / s")
    ax[1, 2].set_title("(f) 持续段 $i_q$（4.0–4.4 s）"); ax[1, 2].legend(fontsize=9)

    fig.suptitle("类 fal ESO 增益 vs 线性 ESO：真实逆变器对象、同种子、同噪声（8 s 工况）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig("fig_eso_fal_time.png", bbox_inches="tight")
    plt.close(fig)


def _load_params():
    pts = {}
    for fn in ("_eso_fal.json", "_eso_fal_sweep2.json"):
        if not os.path.exists(fn):
            continue
        j = json.load(open(fn, encoding="utf-8"))
        for name, rows in j.items():
            if name in pts:
                continue
            pts[name] = (np.mean([r["steady"] for r in rows]),
                         np.mean([r["echo"] for r in rows]),
                         np.mean([r["dip"] for r in rows]))
    return pts


def fig_pareto():
    import re
    pts = _load_params()
    fig, ax = plt.subplots(figsize=(9.2, 5.8))
    rows = []
    for name, (st, ec, dp) in pts.items():
        m = re.search(r"a=([\d.]+) d=([\d.]+) l=([\d.]+)", name)
        a1eq = "a1=a" in name
        rows.append((name, st, ec, m, a1eq))
    # Pareto 前沿（稳态、回声都越小越好）
    fr = []
    best = 1e9
    for r in sorted([x for x in rows if x[1] is not None], key=lambda z: z[1]):
        if r[2] < best:
            best = r[2]; fr.append(r)
    ax.plot([r[1] for r in fr], [r[2] for r in fr], "--", color=C_MUT, lw=1.2, zorder=3,
            label="Pareto 前沿")
    for name, st, ec, m, a1eq in rows:
        if name == "lin":
            ax.scatter(st, ec, s=260, marker="*", color=C_LIN, zorder=6, label="线性档（v4.0 定稿）")
            ax.annotate("线性 $G(e)=e$", (st, ec), textcoords="offset points",
                        xytext=(8, 6), fontsize=9, color=C_LIN)
        elif m and abs(float(m.group(1)) - 0.75) < 1e-6 and abs(float(m.group(2)) - 0.10) < 1e-6 \
                and abs(float(m.group(3)) - 10.0) < 1e-6:
            ax.scatter(st, ec, s=190, marker="D", color=C_FAL, edgecolor="k", zorder=7,
                       label="推荐 $a$=0.75, $\\delta$=0.10, $\\lambda$=10")
        elif a1eq:
            ax.scatter(st, ec, s=110, marker="X", color="#8e44ad", zorder=6,
                       label="z$_1$ 也用 $a$（反例）")
        else:
            ax.scatter(st, ec, s=80, marker="o", color=C_ACC, alpha=0.85, zorder=4,
                       label="其余参数档" if not any("其余" in t for t in ax.get_legend_handles_labels()[1]) else None)
            if m:
                off = (8, -14) if st < 29.5 else (-20, 12)
                ax.annotate("$a$=%s,$\\delta$=%s" % (m.group(1), m.group(2)), (st, ec),
                            textcoords="offset points", xytext=off, fontsize=7.2, color="#7b4b12")
    ax.annotate("", xy=(27.7, 27.2), xytext=(28.05, 39.4),
                arrowprops=dict(arrowstyle="->", color=C_FAL, lw=1.4, ls="--", alpha=0.8))
    ax.text(28.25, 33.5, "线性 → 推荐\n回声 −32.4%\n跌落 +16.7 rpm\n稳态 −2.1%", fontsize=9, color=C_FAL)
    ax.set_xlabel("稳态噪声 $7$–$8$ s / rpm（越小越好）")
    ax.set_ylabel("首周期 10 Hz 回声 / rpm（越小越好）")
    ax.set_title("参数扫描（8 种子）：推荐档落在 Pareto 前沿，且同时优于线性档")
    ax.legend(fontsize=9, loc="upper right")
    ax.set_xlim(21, 33)
    fig.tight_layout()
    fig.savefig("fig_eso_fal_pareto.png", bbox_inches="tight")
    plt.close(fig)


def fig_4cfg():
    j = json.load(open("_eso_fal_4cfg.json", encoding="utf-8"))
    algs = ["Base", "律D", "F-B", "D+F-B"]
    keys = [a + "·" + e for a in algs for e in ("lin", "fal")]
    met = [("echo", "首周期 10 Hz / rpm"), ("dip", "加载跌落 / rpm"), ("steady", "稳态 7–8 s / rpm")]
    fig, ax = plt.subplots(1, 3, figsize=(14.5, 4.4))
    x = np.arange(len(algs)); w = 0.36
    for k, (mk, ml) in enumerate(met):
        mv = [np.mean([r[mk] for r in j[a + "·lin"]]) for a in algs]
        sd = [np.std([r[mk] for r in j[a + "·lin"]], ddof=1) for a in algs]
        mv2 = [np.mean([r[mk] for r in j[a + "·fal"]]) for a in algs]
        sd2 = [np.std([r[mk] for r in j[a + "·fal"]], ddof=1) for a in algs]
        b1 = ax[k].bar(x - w / 2, mv, w, yerr=sd, capsize=3, color=C_LIN, alpha=0.85, label="线性 ESO")
        b2 = ax[k].bar(x + w / 2, mv2, w, yerr=sd2, capsize=3, color=C_FAL, alpha=0.85, label="类 fal ESO")
        for i, a in enumerate(algs):
            ax[k].scatter(np.full(8, x[i] - w / 2) + np.random.default_rng(0).uniform(-0.05, 0.05, 8),
                          [r[mk] for r in j[a + "·lin"]], s=7, color="k", alpha=0.35, zorder=3)
            ax[k].scatter(np.full(8, x[i] + w / 2) + np.random.default_rng(1).uniform(-0.05, 0.05, 8),
                          [r[mk] for r in j[a + "·fal"]], s=7, color="k", alpha=0.35, zorder=3)
        ax[k].set_xticks(x); ax[k].set_xticklabels(algs)
        if k == 2:
            ax[k].set_ylim(20, 32)
        ax[k].set_title("(%s) %s" % ("abc"[k], ml))
        if k == 0:
            ax[k].legend(fontsize=9)
    fig.suptitle("四档算法：类 fal 默认档 vs 线性档（真实逆变器对象，8 种子，标准噪声）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig("fig_eso_fal_4cfg.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_gain()
    print("fig_eso_fal_gain.png ok")
    if os.path.exists("_eso_trace.npz"):
        fig_time()
        print("fig_eso_fal_time.png ok")
    if os.path.exists("_eso_fal.json"):
        fig_pareto()
        print("fig_eso_fal_pareto.png ok")
    if os.path.exists("_eso_fal_4cfg.json"):
        fig_4cfg()
        print("fig_eso_fal_4cfg.png ok")
