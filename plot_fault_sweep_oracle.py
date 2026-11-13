# -*- coding: utf-8 -*-
"""plot_fault_sweep_oracle.py —— 故障→转速纹波映射：J 自适应投运前/后（真实 J，附录 B.9 图）

输入 _fault_sweep_j24.json        （J_true=4.81e-5、b0=J_nom，J 自适应未投运）
     _fault_sweep_j24_oracle.json （J_true=4.81e-5、j_oracle=True，b0 按真实 J 归一）
输出 fig_fault_sweep.png（1920×960，附录 B 新增图）
"""
import json
import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter

J_TRUE, J_NOM = 4.81e-5, 1.89e-5
RATIO = J_TRUE / J_NOM
A = json.load(open("_fault_sweep_j24.json", encoding="utf-8"))
B = json.load(open("_fault_sweep_j24_oracle.json", encoding="utf-8"))

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.0,
    "figure.dpi": 150, "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.0,
})
C0, C1 = "#7f8c8d", "#c0392b"      # 未投运 / 已投运
C_BAND = "#8e44ad"


def rows(D, kind, val, filt):
    out = {}
    for k, v in D.items():
        if v["kind"] != kind or not filt(v):
            continue
        out.setdefault(val(v), []).append(v)
    ks = sorted(out)
    return np.array(ks), np.array([out[k][0]["amp10"] for k in ks]), \
        np.array([out[k][0]["rms"] for k in ks]), np.array([out[k][0]["T1"] for k in ks])


unb_f = lambda v: abs(v["e"] - 1e-4) < 1e-12
mis_f = lambda v: abs(v["beta"] - math.radians(1.0)) < 1e-9
ku, au, ru, tu = rows(A, "unb", lambda v: v["kappa"], unb_f)
kbu, abu, rbu, _ = rows(B, "unb", lambda v: v["kappa"], unb_f)
km, am, rm, _ = rows(A, "mis", lambda v: v["kappa"], mis_f)
kbm, abm, rbm, _ = rows(B, "mis", lambda v: v["kappa"], mis_f)

fig, ax = plt.subplots(2, 2, figsize=(12.8, 6.4))
fig.subplots_adjust(left=0.062, right=0.985, top=0.825, bottom=0.095,
                    hspace=0.46, wspace=0.21)

LAB0, LAB1 = "b0=" + "J$_{nom}$（未投运）", "b0=J$_{true}$（已投运）"

# (a) 不平衡：10 Hz 纹波
ax[0, 0].semilogx(ku, au, "o-", color=C0, lw=1.3, ms=4.5, label=LAB0)
ax[0, 0].semilogx(kbu, abu, "s-", color=C1, lw=1.3, ms=4.5, label=LAB1)
for kk, c, dy in ((1.0, "#555", 2.2), (580.0, "#555", 2.2)):
    ax[0, 0].axvline(kk, color=c, ls=":", lw=0.9, alpha=0.6)
i1 = int(np.where(ku == 1.0)[0][0]); i5 = int(np.where(ku == 580.0)[0][0])
ax[0, 0].annotate("κ=1：" + "%.2f→%.2f" % (au[i1], abu[i1]), (1.0, abu[i1]),
                  xytext=(-2, 26), textcoords="offset points", fontsize=7.6, color="#333")
ax[0, 0].annotate("κ=580：" + "%.1f→%.1f" % (au[i5], abu[i5]), (580.0, abu[i5]),
                  xytext=(-64, 18), textcoords="offset points", fontsize=7.6, color="#333")
ax[0, 0].set_xlabel("等效放大系数 κ（e=0.1 mm）")
ax[0, 0].set_ylabel("10 Hz 转速分量 / rpm")
ax[0, 0].set_title("(a) 不平衡：10 Hz 纹波（rpm）", fontsize=9.2, pad=4)
ax[0, 0].legend(loc="upper left")
ax[0, 0].set_ylim(-1.5, 48)

# 顶轴：κ → 1× 转矩幅值 T1（mN·m）
sec = ax[0, 0].twiny()
sec.set_xscale("log")
tick_k = np.array([1.02, 10.2, 102.0, 1020.0])
sec.xaxis.set_major_locator(FixedLocator(tick_k))
sec.xaxis.set_minor_locator(FixedLocator([]))
sec.set_xticklabels(["0.1", "1", "10", "100"])
sec.set_xlabel("1× 转矩幅值 $T_1$ / mN·m（$T_1=9.8\\times10^{-5}\\kappa$）", fontsize=8.0, labelpad=2)
sec.set_xlim(ax[0, 0].get_xlim())
sec.tick_params(labelsize=8.0)

# (b) 不平衡：稳态 RMS
ax[0, 1].semilogx(ku, ru, "o-", color=C0, lw=1.3, ms=4.5, label=LAB0)
ax[0, 1].semilogx(kbu, rbu, "s-", color=C1, lw=1.3, ms=4.5, label=LAB1)
for kk in (1.0, 580.0):
    ax[0, 1].axvline(kk, color="#555", ls=":", lw=0.9, alpha=0.6)
ax[0, 1].annotate("κ=1：" + "%.1f→%.1f" % (ru[i1], rbu[i1]), (1.0, rbu[i1]),
                  xytext=(8, 30), textcoords="offset points", fontsize=7.6, color="#333")
ax[0, 1].annotate("κ=580：" + "%.1f→%.1f" % (ru[i5], rbu[i5]), (580.0, rbu[i5]),
                  xytext=(-64, 16), textcoords="offset points", fontsize=7.6, color="#333")
ax[0, 1].set_xlabel("κ（e=0.1 mm）"); ax[0, 1].set_ylabel("稳态 7–8 s RMS / rpm")
ax[0, 1].set_title("(b) 不平衡：稳态 RMS（rpm）", fontsize=9.2, pad=4)
ax[0, 1].legend(loc="upper left")
ax[0, 1].set_ylim(4.5, 38)

# (c) 不对中：10 Hz 纹波
ax[1, 0].semilogx(km, am, "o-", color=C0, lw=1.3, ms=4.5, label=LAB0)
ax[1, 0].semilogx(kbm, abm, "s-", color=C1, lw=1.3, ms=4.5, label=LAB1)
ax[1, 0].axvline(67.0, color="#555", ls=":", lw=0.9, alpha=0.6)
j = int(np.where(km == 67.0)[0][0])
ax[1, 0].annotate("κ=67：" + "%.1f→%.1f" % (am[j], abm[j]), (67.0, abm[j]),
                  xytext=(6, 24), textcoords="offset points", fontsize=7.6, color="#333")
ax[1, 0].set_xlabel("κ（β=1°，l=50 mm）"); ax[1, 0].set_ylabel("10 Hz 转速分量 / rpm")
ax[1, 0].set_title("(c) 不对中：10 Hz 纹波（β=1°）", fontsize=9.2, pad=4)
ax[1, 0].legend(loc="upper left")
ax[1, 0].set_ylim(-8, 200)

# (d) 抑制比
ax[1, 1].semilogx(ku, abu / au, "o-", color=C1, lw=1.3, ms=4.0, label="不平衡（e=0.1 mm）")
ax[1, 1].semilogx(km, abm / am, "s--", color=C_BAND, lw=1.3, ms=4.0, label="不对中（β=1°）")
ax[1, 1].axhline(1.0 / RATIO, color="#555", ls=":", lw=1.1,
                 label="1/2.545 = %.3f（若纹波 ∝ 1/J）" % (1.0 / RATIO))
ax[1, 1].set_xlabel("κ"); ax[1, 1].set_ylabel("10 Hz 已投运 / 未投运")
ax[1, 1].set_title("(d) 投运后的纹波抑制比（实测 0.26–0.39，即 2.5–3.8×）", fontsize=9.2, pad=4)
ax[1, 1].legend(loc="upper left")
ax[1, 1].set_ylim(0.20, 0.45)

fig.suptitle("故障→转速纹波映射：J 自适应投运前/后（600 rpm、8 s、RC 开、不加载型线；真实 J="
             + "%.3e=%.3f" % (J_TRUE, RATIO) + " J_nom）", fontsize=10.2, y=0.962)
fig.savefig("fig_fault_sweep.png", dpi=150, facecolor="white")
try:
    from PIL import Image
    Image.open("fig_fault_sweep.png").convert("RGB").save("fig_fault_sweep.png")
except Exception:
    pass

json.dump(dict(
    unb=dict(kappa=ku.tolist(), amp10_nonoracle=au.tolist(), amp10_oracle=abu.tolist(),
             rms_nonoracle=ru.tolist(), rms_oracle=rbu.tolist(), T1=tu.tolist()),
    mis=dict(kappa=km.tolist(), amp10_nonoracle=am.tolist(), amp10_oracle=abm.tolist(),
             rms_nonoracle=rm.tolist(), rms_oracle=rbm.tolist()),
    ratio_range=[float((abu / au).min()), float((abu / au).max()),
                 float((abm / am).min()), float((abm / am).max())],
    J_true=J_TRUE, J_ratio=RATIO),
    open("_fig_fault_sweep_numbers.json", "w", encoding="utf-8"), indent=1)
print("ok: fig_fault_sweep.png")
for tag, kk, Aa, Ab, Ar, Br in (("unb", ku, au, abu, ru, rbu), ("mis", km, am, abm, rm, rbm)):
    for k0 in ((1.0, 580.0) if tag == "unb" else (67.0,)):
        i = int(np.where(kk == k0)[0][0])
        print("  %s kappa=%g  T1=%.5f N·m  10Hz %6.2f -> %6.2f rpm  RMS %6.2f -> %6.2f rpm  ratio %.3f"
              % (tag, k0, (tu[i] if tag == "unb" else 0.0), Aa[i], Ab[i], Ar[i], Br[i], Ab[i] / Aa[i]))
print("  unb ratio %.3f-%.3f  mis ratio %.3f-%.3f"
      % ((abu / au).min(), (abu / au).max(), (abm / am).min(), (abm / am).max()))
