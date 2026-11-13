# -*- coding: utf-8 -*-
"""plot_base_realj.py —— 真实 J 下基准环 kp x wo 重调的 Pareto 图 + 表

输入 _base_realj.json；输出 fig_base_realj.png、_base_realj_table.txt
"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = json.load(open("_base_realj.json", encoding="utf-8"))
meta = D.pop("_meta")
I_R = meta["i_rated"]
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9,
    "figure.dpi": 150, "axes.grid": True, "grid.alpha": 0.18, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "legend.fontsize": 8,
})

rows = [(k, v) for k, v in D.items()]
fig, ax = plt.subplots(1, 2, figsize=(12.0, 4.6))
fig.subplots_adjust(left=0.07, right=0.985, top=0.86, bottom=0.14, wspace=0.22)
cmap = plt.get_cmap("viridis")
for i, (k, v) in enumerate(sorted(rows, key=lambda kv: (kv[1]["kp"], kv[1]["wo"]))):
    if "lawd" in k:
        continue
    c = cmap(i / max(1, len(rows) - 1))
    ax[0].plot(v["step_rms"], v["iq_global"], "o", color=c, ms=7)
    ax[0].annotate("%g/%g" % (v["kp"], v["wo"]), (v["step_rms"], v["iq_global"]),
                   textcoords="offset points", xytext=(4, 3), fontsize=7, color=c)
    ax[1].plot(v["dip"] * -1, v["rec_ms"], "o", color=c, ms=7)
    ax[1].annotate("%g/%g" % (v["kp"], v["wo"]), (-v["dip"], v["rec_ms"]),
                   textcoords="offset points", xytext=(4, 3), fontsize=7, color=c)
ax[0].axhline(I_R, color="#8e44ad", ls="-.", lw=1.0, label="额定 6.31 A")
ax[0].set_xlabel("突变窗 RMS [2.0,2.5) / rpm"); ax[0].set_ylabel("max|$i_q$| / A")
ax[0].set_title("(a) 电流约束 vs 瞬态（标注 kp/wo）", fontsize=9.5); ax[0].legend(loc="upper right")
ax[1].set_xlabel("跌落 / rpm"); ax[1].set_ylabel("恢复 / ms")
ax[1].set_title("(b) 跌落—恢复", fontsize=9.5)
fig.suptitle("真实 J（4.81e-5）+oracle 下基准环 kp×wo 重调（律D 关，600 rpm、8 s）", fontsize=10.5)
fig.savefig("fig_base_realj.png", dpi=150, facecolor="white")

with open("_base_realj_table.txt", "w", encoding="utf-8") as f:
    hdr = ("key,kp,wo,kp_boost,kb_eso,det_eps,dip_rpm,rec_ms,step_rms,steady_rms,"
           "iq_global,iq_g_t,iq_step,iq1ms,iq100us,ok,ok1ms\n")
    f.write(hdr)
    for k, v in sorted(rows, key=lambda kv: kv[1]["iq_global"]):
        f.write("%s,%g,%g,%g,%g,%g,%.1f,%.1f,%.1f,%.2f,%.2f,%.3f,%.2f,%.2f,%.2f,%d,%d\n"
                % (k, v["kp"], v["wo"], v["kp_boost"], v["kb_eso"], v["det_eps"],
                   v["dip"], v["rec_ms"], v["step_rms"], v["steady"], v["iq_global"],
                   v["iq_g_t"], v["iq_step"], v["iq1ms"], v["iq100us"], v["ok"], v["ok1ms"]))
print(open("_base_realj_table.txt", encoding="utf-8").read())
print("ok")
