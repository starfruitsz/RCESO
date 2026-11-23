# -*- coding: utf-8 -*-
"""_plot_cases_three.py —— 一张图三个子图：负载突变 / b0 纯失配 / T 漂移 各自 vs 对照组（三合一故障）。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
})

C_CTRL = "#7f8c8d"
PANELS = [
    dict(key="loadd", color="#e67e22", tag="(a) 负载突变 vs 对照组",
         name="负载突变（2 s 0→0.5 额定）", mark=(2.0, "2 s 加载"), ylim=(100, 760), zoom=True),
    dict(key="b0pd", color="#c0392b", tag="(b) b0 严重失配 vs 对照组",
         name="b0 失配（控制器 b0 估大 5.26×）", mark=(2.0, "2 s 故障"), ylim=(-900, 900), zoom=False),
    dict(key="td15", color="#1f4e79", tag="(c) T 漂移 vs 对照组",
         name="T 漂移（δ 偏理论最优 15%）", mark=(2.0, "2 s 故障"), ylim=(100, 760), zoom=False),
]

def load(c):
    z = np.load("_c4_%s.npz" % c)
    t = np.asarray(z["t"]); dec = max(1, int(round(1e-4 / (t[1] - t[0]))))
    return dict(t=t[::dec], y=np.asarray(z["y"])[::dec] * 600.0)

def amp10(t, e, a=5.0, b=6.0):
    m = (t >= a) & (t < b); tt = t[m]; ee = e[m]; w = 2 * np.pi * 10
    return float(np.hypot(2 * np.mean(ee * np.cos(w * tt)), 2 * np.mean(ee * np.sin(w * tt))))

def met(d):
    t = d["t"]; e = d["y"] - 600.0
    m = (t >= 5.0) & (t <= 6.0)
    m2 = (t >= 1.9) & (t <= 2.5)
    return float(np.sqrt(np.mean(e[m] ** 2))), amp10(t, e), float(e[m2].min())

ctrl = load("ctrld")
cR, cA, cD = met(ctrl)

fig, ax = plt.subplots(1, 3, figsize=(12.8, 4.4))
fig.subplots_adjust(left=0.055, right=0.995, top=0.80, bottom=0.22, wspace=0.17)

for a, p in zip(ax, PANELS):
    d = load(p["key"]); r, a10, dip = met(d)
    if p["key"] == "loadd":
        note = "跌落 %.0f rpm（对照组 %.0f）" % (dip, cD)
    else:
        note = "10 Hz %.0f vs %.0f rpm\nRMS %.0f vs %.0f rpm" % (a10, cA, r, cR)
    a.plot(ctrl["t"], ctrl["y"], color=C_CTRL, lw=0.9)
    a.plot(d["t"], d["y"], color=p["color"], lw=0.9)
    a.axhline(600, color="#999", ls=":", lw=0.7)
    a.axvline(p["mark"][0], color="#888", ls="--", lw=0.7, alpha=0.7)
    a.text(p["mark"][0] + 0.08, p["ylim"][1] - 22, p["mark"][1], fontsize=6.6,
           color="#555", va="top")
    a.set_xlim(0, 8); a.set_ylim(*p["ylim"])
    a.set_xlabel("时间 / s"); a.set_ylabel("转速 / rpm")
    a.set_title(p["tag"], fontsize=9.2)
    a.text(0.02, 0.05, note, transform=a.transAxes, fontsize=6.8,
           color=p["color"], va="bottom", ha="left")
    if p["zoom"]:
        zi = a.inset_axes([0.56, 0.10, 0.40, 0.40])
        m = (ctrl["t"] >= 1.9) & (ctrl["t"] <= 2.5)
        zi.plot(ctrl["t"][m], ctrl["y"][m] - 600, color=C_CTRL, lw=0.9)
        mm = (d["t"] >= 1.9) & (d["t"] <= 2.5)
        zi.plot(d["t"][mm], d["y"][mm] - 600, color=p["color"], lw=0.9)
        zi.set_xlim(1.9, 2.5); zi.set_ylim(-520, 80)
        zi.tick_params(labelsize=5.2); zi.grid(alpha=0.15, lw=0.4)
        zi.set_title("放大 1.9–2.5 s", fontsize=5.8, pad=2)
        for s in ("top", "right"):
            zi.spines[s].set_visible(False)

handles = [Line2D([0], [0], color=C_CTRL, lw=1.4, label="对照组（仅故障；b0、T 均准确）")]
for p in PANELS:
    handles.append(Line2D([0], [0], color=p["color"], lw=1.4, label=p["name"]))
fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=7.4, frameon=False,
           bbox_to_anchor=(0.5, 0.005))

fig.suptitle("三种工况与对照组对比（600 rpm；圆盘不平衡 + 角不对中 β=1° + 平行不对中）",
             fontsize=9.6, y=0.955)
fig.savefig("fig_cases_three.png", dpi=150, bbox_inches=None, facecolor="white")
print("saved fig_cases_three.png")
