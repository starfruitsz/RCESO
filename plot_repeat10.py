import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 9.5, "figure.dpi": 140,
                     "savefig.bbox": "tight", "pdf.fonttype": 42})
D = json.load(open("_repeat10.json", encoding="utf-8"))
seeds = [r["seed"] for r in D["Base"]]
base = [r["a_echo"] for r in D["Base"]]
fb = [r["a_echo"] for r in D["FB"]]
x = np.arange(len(seeds)); w = 0.36
fig, ax = plt.subplots(1, 1, figsize=(7.2, 3.4))
ax.bar(x-w/2, base, w, color="#3a3a3a", label="无自适应（基准）")
ax.bar(x+w/2, fb, w, color="#16a085", label="律 F-B")
for i,(b_,f_) in enumerate(zip(base, fb)):
    ax.text(i-w/2, b_+1.2, "%.1f" % b_, ha="center", fontsize=8)
    ax.text(i+w/2, f_+1.2, "%.1f" % f_, ha="center", fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(["种子 %d" % s_ for s_ in seeds])
ax.set_ylabel("首周期 10 Hz 回声 (rpm)")
ax.axhline(np.mean(base), color="#3a3a3a", ls=":", lw=1.0)
ax.axhline(np.mean(fb), color="#16a085", ls=":", lw=1.0)
ax.set_title("10 rpm 转速噪声下的事件重复性（3 个种子）：F-B 均值下降但方差极大", fontsize=9.6)
ax.legend(fontsize=8); ax.grid(alpha=0.25, axis="y")
fig.tight_layout()
fig.savefig("fig_repeat10.png", dpi=200)  # 只存 PNG（2026-10-19 约定）
print("ok")
