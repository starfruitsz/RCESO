# -*- coding: utf-8 -*-
"""_plot_col_cmp.py —— 旧版比值法 vs 新版代数法+电流差分（撞频对比）"""
import numpy as np, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False})
B = 101.89
CASES = [("d_oldau", "d_newau", "65 Hz（选频器输出，清洁）"),
         ("d_old20", "d_new20", "20 Hz（强制 2× 撞频）")]
fig, ax = plt.subplots(2, 2, figsize=(9.6, 5.4))
for i, (to, tn, ttl) in enumerate(CASES):
    a = ax[i, 0]
    for tag, lab, c, ls in ((to, "旧·比值法", "#7f8c8d", "--"), (tn, "新·代数+电流差分", "#c0392b", "-")):
        if not os.path.exists(tag + ".npz"): continue
        d = np.load(tag + ".npz"); lg = np.asarray(d["lg"])
        a.plot(lg[:, 0], lg[:, 5], color=c, ls=ls, lw=1.5, label=lab)
    a.axhline(B, color="#1f4e79", ls=":", lw=1.1, label=r"真值 $b$=101.9")
    a.set_ylim(80, 150); a.set_xlim(1, 8); a.set_xlabel("t / s"); a.set_ylabel(r"$\hat b_0$")
    a.set_title("(%s) %s" % ("ab"[i], ttl), fontsize=9)
    a.legend(fontsize=7, loc="lower left", framealpha=0.92)
    b = ax[i, 1]
    for tag, lab, c, mk in ((tn, "新·电流差分", "#c0392b", "o"),):
        if not os.path.exists(tag + ".npz"): continue
        j = np.asarray(np.load(tag + ".npz")["jnew"]); j = j[j[:, 3] > 0]
        v = np.array([r[5] for r in j]); v = v[v > 0]
        b.plot(np.arange(len(v)) * 0.2 + 3.2, v, mk, ms=3.6, lw=0.9, color=c, label=lab)
        s = np.array([r[2] for r in j])
        b.plot(np.arange(len(s)) * 0.2 + 3.2, s, color="#7f8c8d", lw=0.9, ls="--", label="单窗（含 T）")
    b.axhline(B, color="#1f4e79", ls=":", lw=1.1, label=r"真值 $b$=101.9")
    b.set_ylim(20, 130); b.set_xlim(3, 7.4); b.set_xlabel("t / s"); b.set_ylabel(r"单次估计 $\hat b_0$")
    b.set_title("(%s) %s 逐窗估计" % ("cd"[i], ttl.split("（")[0]), fontsize=9)
    b.legend(fontsize=6.8, ncol=2, loc="lower right", framealpha=0.92)
plt.tight_layout()
plt.savefig("fig_collision_cmp.png", bbox_inches="tight")
print("saved fig_collision_cmp.png")
