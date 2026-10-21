# -*- coding: utf-8 -*-
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 9.5,
                     "xtick.labelsize": 8.4, "ytick.labelsize": 8.4,
                     "legend.fontsize": 7.0, "axes.titlesize": 9.4,
                     "figure.dpi": 140, "savefig.bbox": "tight", "pdf.fonttype": 42})
D = json.load(open("_phi_sweep.json", encoding="utf-8"))
SER = {"FB": ([0, 20, 40], "律 F-B", "#16a085", "o"), "DFB": ([20, 40], "律 D + F-B", "#2471a3", "s")}
fig, ax = plt.subplots(1, 3, figsize=(11.4, 3.5))
a, b, c_ = ax
for key, (cs, lab, col, mk) in SER.items():
    a.plot(cs, [D["%s_c%d" % (key, k)]["trig_pre"] for k in cs], mk+"-", color=col, lw=1.2, label=lab+" 3–6 s")
    a.plot(cs, [D["%s_c%d" % (key, k)]["trig_post"] for k in cs], mk+"--", color=col, lw=1.1, alpha=0.75, label=lab+" 7–12 s")
a.set_xlabel("软死区宽度 $c$ (rpm)"); a.set_ylabel("触发次数")
a.set_title("(a) 触发次数：随 $c$ 反而上升"); a.legend(fontsize=6.6, ncol=2); a.grid(alpha=0.25)
base = D["Base"]["a_echo"]
for key, (cs, lab, col, mk) in SER.items():
    b.plot(cs, [D["%s_c%d" % (key, k)]["a_echo"] for k in cs], mk+"-", color=col, lw=1.2, label=lab)
b.axhline(base, color="#3a3a3a", ls="--", lw=1.0, label="无自适应")
b.set_xlabel("软死区宽度 $c$ (rpm)"); b.set_ylabel("首周期 10 Hz 回声 (rpm)")
b.set_title("(b) 回声：$c=0$ 反而是最优"); b.legend(fontsize=7.2); b.grid(alpha=0.25)
for key, (cs, lab, col, mk) in SER.items():
    c_.plot(cs, [D["%s_c%d" % (key, k)]["dip"] for k in cs], mk+"-", color=col, lw=1.2, label=lab)
c_.axhline(D["Base"]["dip"], color="#3a3a3a", ls="--", lw=1.0, label="无自适应")
c_.set_xlabel("软死区宽度 $c$ (rpm)"); c_.set_ylabel("加载跌落 (rpm)")
c_.set_title("(c) 阶跃跌落：$\\phi$ 帮不上忙"); c_.legend(fontsize=7.2); c_.grid(alpha=0.25)
fig.tight_layout()
fig.savefig("fig_phi_sweep.png", dpi=200)  # 只存 PNG（2026-10-19 约定）
print("figs done")
