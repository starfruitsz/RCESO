# -*- coding: utf-8 -*-
"""plot_fb_retune.py —— 类 fal 默认档下律 F-B 的重标定证据图（只读 JSON）

    fig_fb_retune.png
      (a) oracle 复位时刻扫描：线性最优 20 ms / 类 fal 最优 30 ms
      (b) 检测器实际首次触发时刻（8 种子）：线性 / fal 对称 .20 / fal 对称 .30 / fal 方向 .30
      (c1..c3) 回声、加载跌落、稳态：三组配置的绝对量与逐种子散点
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({"figure.dpi": 130, "savefig.dpi": 150, "font.size": 10,
                     "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
C_LIN, C_FAL, C_OK, C_MUT, C_MID = "#1f4e79", "#c0392b", "#27ae60", "#7f8c8d", "#e67e22"
TW = 6.0


def load(fn):
    return json.load(open(fn, encoding="utf-8"))


def fig():
    orc = load("_fb_oracle.json")
    cfg4 = load("_eso_fal_4cfg.json")
    cur = load("_fb_retune3.json")["D_m=.20 cool=.30 (现状)"]
    mid = load("_fb_retune3.json")["D_m=.30 cool=.30"]
    new = load("_fb_retune5.json")["方向 D_m=.30"]
    lin = cfg4["F-B·lin"]

    fig = plt.figure(figsize=(15.5, 7.6))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.15, 1.0], hspace=0.42, wspace=0.30)
    ax0 = fig.add_subplot(gs[0, :2])
    ax1 = fig.add_subplot(gs[0, 2])
    axb = [fig.add_subplot(gs[1, i]) for i in range(3)]

    # ---------- (a) oracle ----------
    for tag, c, lab in (("fal", C_FAL, "类 fal（新默认）"), ("lin", C_LIN, "线性（v4.0）")):
        pts = []
        for k, rows in orc.items():
            if k.startswith(tag):
                tau = float(k.split("tau=")[1].split(" ")[0])
                if tau >= 0:
                    pts.append((tau, np.mean([r["echo"] for r in rows])))
        pts.sort()
        x = [p[0] for p in pts]; y = [p[1] for p in pts]
        ax0.plot(x, y, "o-", color=c, lw=2.0, ms=7, label=lab)
        base = np.mean([r["echo"] for r in cfg4["Base·" + ("fal" if tag == "fal" else "lin")]])
        ax0.axhline(base, color=c, ls=":", lw=1.1, alpha=0.75)
        ax0.text(61, base + 0.9, "无复位 %.1f" % base, color=c, fontsize=8.5, ha="right")
        i = int(np.argmin(y))
        ax0.annotate("最优 %.2f rpm @ %g ms" % (y[i], x[i]), (x[i], y[i]),
                     textcoords="offset points", xytext=(6, -14), fontsize=8.5, color=c)
    ax0.set_xlabel("复位滞后 $\\tau$ / ms（事件 6.0 s 之后的延时）")
    ax0.set_ylabel("首周期 10 Hz 回声 / rpm")
    ax0.set_title("(a) oracle：复位时刻的能力曲线——线性最优 20 ms、类 fal 最优 30 ms（非单调）")
    ax0.set_xlim(-2, 62); ax0.set_ylim(0, 42); ax0.legend(fontsize=9)

    # ---------- (b) 触发时刻 ----------
    def taus_of(rows):
        return np.array([(r["first"] - TW) * 1000 for r in rows if r.get("first") and r["first"] > 5.9])
    groups = [(lin, C_LIN, "线性 F-B"), (cur, C_MUT, "fal 对称 .20"),
              (mid, C_MID, "fal 对称 .30"), (new, C_OK, "fal 方向 .30")]
    ax1.axvspan(15, 25, color=C_LIN, alpha=0.10)
    ax1.axvspan(25, 35, color=C_FAL, alpha=0.12)
    for i, (rr, c, lab) in enumerate(groups):
        v = np.clip(taus_of(rr), 0, 90)
        y = np.full(len(v), i) + np.random.default_rng(i).uniform(-0.10, 0.10, len(v))
        ax1.scatter(v, y, s=55, color=c, alpha=0.9, zorder=3)
        ax1.plot([np.median(v)] * 2, [i - 0.22, i + 0.22], color=c, lw=2.4)
    ax1.set_yticks(range(len(groups)))
    ax1.set_yticklabels([g[2] for g in groups], fontsize=8.5)
    ax1.set_xlabel("事件后首次触发 / ms（>90 已截断）")
    ax1.set_title("(b) 触发时刻分布\n（蓝带=线性最优窗，红带=fal 最优窗）", fontsize=10)
    ax1.set_xlim(-3, 92)

    # ---------- (c) 指标 ----------
    sets = [("线性 F-B", lin, C_LIN), ("fal 对称 .20", cur, C_MUT),
            ("fal 对称 .30", mid, C_MID), ("fal 方向 .30", new, C_OK)]
    metas = [("echo", "首周期 10 Hz / rpm"), ("dip", "加载跌落 / rpm"), ("steady", "稳态 7–8 s / rpm")]
    for j, (fld, ylab) in enumerate(metas):
        a = axb[j]
        for i, (name, rr, c) in enumerate(sets):
            vals = np.array([r[fld] for r in rr], dtype=float)
            a.bar(i, abs(vals.mean()), 0.66, color=c, alpha=0.85,
                  yerr=vals.std(ddof=1), capsize=4, error_kw=dict(lw=1.1))
            a.scatter(np.full(len(vals), i) + np.random.default_rng(i).uniform(-0.10, 0.10, len(vals)),
                      np.abs(vals), s=9, color="k", alpha=0.30, zorder=3)
            a.text(i, abs(vals.mean()) + vals.std(ddof=1) + (0.35 if j else 0.25),
                   "%.1f" % vals.mean(), ha="center", fontsize=8)
        a.set_xticks(range(len(sets)))
        a.set_xticklabels(["线性", "对称.20", "对称.30", "方向.30"], fontsize=8.5)
        a.set_title(("(c%d) " % (j + 1)) + ylab, fontsize=10)
        if j == 2:
            a.set_ylim(20, 30)

    fig.suptitle("律 F-B 在类 fal 默认档下的重标定：唯一变量是触发时刻，方向限定消除事件前误复位",
                 fontsize=12.5)
    fig.savefig("fig_fb_retune.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig()
    print("fig_fb_retune.png ok")
