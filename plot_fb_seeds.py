import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 9.5, "figure.dpi": 140,
                     "savefig.bbox": "tight"})
a = json.load(open("_repeat25.json", encoding="utf-8"))
b = json.load(open("_repeat_more.json", encoding="utf-8"))
rows = []
for d in (a, b):
    for i in range(len(d["Base"])):
        rows.append((d["Base"][i]["seed"], d["Base"][i]["a_echo"], d["FB"][i]["a_echo"]))
rows.sort(key=lambda r: r[2])
labels = [str(r[0])[-2:] for r in rows]
base = [r[1] for r in rows]; fb = [r[2] for r in rows]
x = np.arange(len(rows)); w = 0.38
fig, ax = plt.subplots(figsize=(9.0, 3.6))
ax.bar(x-w/2, base, w, color="#3a3a3a", label="无自适应（基准）")
ax.bar(x+w/2, fb, w, color="#16a085", label="律 F-B")
for i,(b_,f_) in enumerate(zip(base, fb)):
    ax.text(i+w/2, f_+1.5, "%.0f" % f_, ha="center", fontsize=7.4)
ax.axhline(np.mean(base), color="#3a3a3a", ls=":", lw=1)
ax.axhline(np.mean(fb), color="#16a085", ls=":", lw=1)
ax.set_xticks(x); ax.set_xticklabels(["种子 " + l for l in labels], fontsize=8)
ax.set_ylabel("首周期 10 Hz 回声 (rpm)")
ax.set_title("8 个种子：F-B 5/8 明显改善、3/8 无效或略差（均值 47.6 vs 78.8，t=−2.29）", fontsize=9.6)
ax.legend(fontsize=8); ax.grid(alpha=0.25, axis="y")
fig.tight_layout()
fig.savefig("fig_fb_seeds.png", dpi=200)
print("ok")
