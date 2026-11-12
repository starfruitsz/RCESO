# -*- coding: utf-8 -*-
"""plot_lpf_cmp.py —— 无自适应 RCESO：有低通 vs 无低通（三工况，1920×960）"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

N_REF, N_REF2, T_REV = 600.0, 900.0, 5.98361
C_LPF, C_NOL = "#1f4e79", "#c0392b"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 8.6,
    "figure.dpi": 150,
    "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False,
})

D = {}
for case in ("load", "speed", "echo"):
    for cfg in ("lpf", "nolpf"):
        d = np.load("_wave_lpf_%s_%s.npz" % (case, cfg))
        t = np.asarray(d["t"])
        dec = max(1, int(round(1e-3 / (t[1] - t[0]))))
        D[(case, cfg)] = (t[::dec], np.asarray(d["y"])[::dec] * N_REF)
        D[(case, cfg, "full")] = (np.asarray(d["t"]), np.asarray(d["y"]) * N_REF)
ts = D[("load", "lpf")][0]


def spd(case, cfg):
    return D[(case, cfg)][1]


M = {}
for case in ("load", "speed", "echo"):
    for cfg in ("lpf", "nolpf"):
        tt, sfull = D[(case, cfg, "full")]
        e = sfull - N_REF
        if case == "load":
            m = (tt >= 1.9) & (tt <= 2.5)
            M[(case, cfg)] = dict(dip=float(np.min(e[m])),
                                  step_rms=float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))))
        elif case == "speed":
            m = tt >= 5.0
            e2 = sfull - N_REF2
            idx = np.where((np.abs(e2) <= 20.0) & m)[0]
            M[(case, cfg)] = dict(over=float(np.max(e2[m])),
                                  settle=float((tt[idx[0]] - 5.0) * 1e3) if len(idx) else float("nan"))
        else:
            m = (tt >= 6.0) & (tt <= 6.2)
            M[(case, cfg)] = dict(echo_max=float(np.max(np.abs(e[m]))),
                                  echo_rms=float(np.sqrt(np.mean(e[m] ** 2))))

fig = plt.figure(figsize=(12.8, 6.4))
gs = fig.add_gridspec(2, 3, left=0.055, right=0.985, top=0.855, bottom=0.085,
                      wspace=0.26, hspace=0.42)
ax_full = [fig.add_subplot(gs[0, i]) for i in range(3)]
ax_zoom = [fig.add_subplot(gs[1, i]) for i in range(3)]

titles = ["(a) 负载突变（2 s，0.50 额定）", "(b) 参考转速突变（5 s，600→900 rpm）", "(c) 回声重影（5.98 s 反相）"]
for i, case in enumerate(("load", "speed", "echo")):
    ax = ax_full[i]
    ax.plot(ts, spd(case, "nolpf"), color=C_NOL, lw=0.8, alpha=0.85, label="无低通（$\\tau=2\\,\\mu$s）")
    ax.plot(ts, spd(case, "lpf"), color=C_LPF, lw=1.4, label="有低通（$\\tau=20$ ms）")
    ax.set_xlim(0, 8); ax.set_ylim(-6200, 6200)
    ax.set_xlabel("时间 / s"); ax.set_ylabel("转速 / rpm")
    ax.set_title(titles[i], fontsize=8.6)
    if case == "load":
        ax.axvline(2.0, color="#7f8c8d", ls="--", lw=0.8)
    elif case == "speed":
        ax.axvline(5.0, color="#7f8c8d", ls="--", lw=0.8)
        ax.axhline(N_REF2, color="#bdc3c7", ls=":", lw=0.8)
    else:
        ax.axvline(T_REV, color="#7f8c8d", ls="--", lw=0.8)

# (d) 负载窗：|e| 对数
ax = ax_zoom[0]
m = (ts >= 1.9) & (ts <= 2.6)
for cfg, col, lab in (("nolpf", C_NOL, "无低通"), ("lpf", C_LPF, "有低通")):
    ax.semilogy(ts[m], np.maximum(np.abs(spd("load", cfg)[m] - N_REF), 1.0), color=col, lw=1.3, label=lab)
ax.set_xlim(1.9, 2.6); ax.set_ylim(1, 1e4)
ax.set_title("(d) 负载窗 $|e|$（对数）：有低通 %.0f / 无低通 %.0f rpm" % (M[("load","lpf")]["dip"], M[("load","nolpf")]["dip"]), fontsize=8.4)
ax.set_xlabel("时间 / s"); ax.set_ylabel("$|$转速误差$|$ / rpm")

# (e) 换速窗：|e-900|
ax = ax_zoom[1]
m = (ts >= 4.8) & (ts <= 6.0)
for cfg, col, lab in (("nolpf", C_NOL, "无低通"), ("lpf", C_LPF, "有低通")):
    ax.semilogy(ts[m], np.maximum(np.abs(spd("speed", cfg)[m] - N_REF2), 1.0), color=col, lw=1.3, label=lab)
ax.set_xlim(4.8, 6.0); ax.set_ylim(1, 1e4)
ax.set_title("(e) 换速窗 $|e-900|$（对数）：超调 %.0f / %.0f rpm" % (M[("speed","lpf")]["over"], M[("speed","nolpf")]["over"]), fontsize=8.4)
ax.set_xlabel("时间 / s"); ax.set_ylabel("$|$相对 900 rpm 的误差$|$ / rpm")

# (f) 回声窗
ax = ax_zoom[2]
m = (ts >= 5.9) & (ts <= 6.6)
for cfg, col, lab in (("nolpf", C_NOL, "无低通"), ("lpf", C_LPF, "有低通")):
    ax.semilogy(ts[m], np.maximum(np.abs(spd("echo", cfg)[m] - N_REF), 1.0), color=col, lw=1.3, label=lab)
ax.set_xlim(5.9, 6.6); ax.set_ylim(1, 1e4)
ax.set_title("(f) 回声窗 $|e|$（对数）：峰值 %.0f / %.0f rpm" % (M[("echo","lpf")]["echo_max"], M[("echo","nolpf")]["echo_max"]), fontsize=8.4)
ax.set_xlabel("时间 / s"); ax.set_ylabel("$|$转速误差$|$ / rpm")

handles = [Line2D([0], [0], color=C_LPF, lw=1.6, label="有低通 $\\tau=20$ ms"),
           Line2D([0], [0], color=C_NOL, lw=1.2, label="无低通 $\\tau=2\\,\\mu$s（等效取消）")]
fig.legend(handles=handles, loc="upper center", ncol=2, fontsize=8.4, bbox_to_anchor=(0.5, 0.925))
fig.suptitle("无自适应 RCESO：保留低通 vs 去掉低通——负载突变 / 参考转速突变 / 回声重影（600 rpm，8 s）",
             fontsize=10.2, y=0.975)
fig.savefig("fig_lpf_cmp.png", dpi=150, facecolor="white")
try:
    from PIL import Image
    Image.open("fig_lpf_cmp.png").convert("RGB").save("fig_lpf_cmp.png")
except Exception:
    pass

json.dump({f"{c}_{g}": M[(c, g)] for c in ("load", "speed", "echo") for g in ("lpf", "nolpf")},
          open("_lpf_cmp_metrics.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok: fig_lpf_cmp.png")
print(json.dumps({f"{c}_{g}": M[(c, g)] for c in ("load", "speed", "echo") for g in ("lpf", "nolpf")},
                 ensure_ascii=False, indent=1))
