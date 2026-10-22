# -*- coding: utf-8 -*-
"""plot_eso_fal_speed.py —— 600/900/1200 rpm 下线性 vs 类 fal 的性能（只读 JSON）

    fig_eso_fal_speed.png
      上排：首周期 10/15/20 Hz 回声    下排：加载跌落
      每根柱一个配置；颜色=算法，填充=ESO 增益档（实心=线性，斜线=fal，交叉=fal+方向限定 F-B）
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({"figure.dpi": 130, "savefig.dpi": 150, "font.size": 10,
                     "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})

CFG = ["Base·lin", "Base·fal", "律D·lin", "律D·fal", "F-B·lin", "F-B·fal", "F-B·fal方向",
       "D+F-B·lin", "D+F-B·fal方向"]
COL = {"Base": "#1f4e79", "律D": "#e67e22", "F-B": "#c0392b", "D+F-B": "#27ae60"}
HATCH = {"lin": "", "fal": "//", "fal方向": "xx"}


def style(name):
    algo, eso = name.split("·")
    return COL[algo], HATCH[eso]


def fig():
    j = json.load(open("_eso_fal_speed.json", encoding="utf-8"))
    speeds = list(j.keys())
    fig, ax = plt.subplots(2, 3, figsize=(15.5, 7.4), sharey="row")
    for col, sp in enumerate(speeds):
        d = j[sp]
        for row, (fld, ylab, tag) in enumerate([("echo", "首周期回声 / rpm", "a"), ("dip", "加载跌落 / rpm", "b")]):
            a = ax[row, col]
            for i, name in enumerate(CFG):
                vals = np.array([r[fld] for r in d[name]], dtype=float)
                c, h = style(name)
                a.bar(i, abs(vals.mean()), 0.78, color=c, hatch=h, alpha=0.85,
                      edgecolor="k", linewidth=0.4,
                      yerr=vals.std(ddof=1), capsize=3, error_kw=dict(lw=0.9))
                a.scatter(np.full(len(vals), i) + np.random.default_rng(i).uniform(-0.11, 0.11, len(vals)),
                          np.abs(vals), s=7, color="k", alpha=0.28, zorder=3)
            a.set_xticks(range(len(CFG)))
            a.set_xticklabels([n.replace("·", "\n") for n in CFG], fontsize=7.2, rotation=0)
            a.set_title("(%s%d) %s" % (tag, col + 1, sp), fontsize=11)
            if col == 0:
                a.set_ylabel(ylab)
            if fld == "echo" and sp.startswith("600"):
                a.set_ylim(0, 45)
            if fld == "dip":
                a.set_ylim(300, 520)
    handles = [Patch(facecolor=COL[k], label=k) for k in ("Base", "律D", "F-B", "D+F-B")]
    handles += [Patch(facecolor="0.75", hatch="", edgecolor="k", label="线性 ESO"),
                Patch(facecolor="0.75", hatch="//", edgecolor="k", label="类 fal ESO"),
                Patch(facecolor="0.75", hatch="xx", edgecolor="k", label="类 fal + 方向限定 F-B")]
    fig.legend(handles=handles, loc="lower center", ncol=7, fontsize=9, frameon=False,
               bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("600 / 900 / 1200 rpm（10 / 15 / 20 Hz）：线性 ESO vs 类 fal ESO（实验室噪声，8 种子）", fontsize=13)
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    fig.savefig("fig_eso_fal_speed.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig()
    print("fig_eso_fal_speed.png ok")
