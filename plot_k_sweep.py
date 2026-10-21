import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 9.5, "figure.dpi": 140,
                     "savefig.bbox": "tight"})
D=json.load(open("_k_sweep.json", encoding="utf-8"))
seeds=[20261018, 20261021]
KS=[1.4,1.6,1.8,2.0,2.4]
fig, ax = plt.subplots(1, 3, figsize=(11.4, 3.4))
a,b,c_=ax
cols={seeds[0]:"#c0392b", seeds[1]:"#2471a3"}
for sd in seeds:
    a.plot(KS, [D["%d_k%.1f"%(sd,k)]["a_echo"] for k in KS], "o-", color=cols[sd], lw=1.3, label="种子 %d"%sd)
a.axhline(78.8, color="#3a3a3a", ls="--", lw=1.0, label="无自适应 78.8")
a.set_xlabel("阈值 $k$"); a.set_ylabel("首周期 10 Hz 回声 (rpm)"); a.set_title("(a) 回声：低 $k$ 好、高 $k$ 失效")
a.legend(fontsize=7.2); a.grid(alpha=0.25)
for sd in seeds:
    b.plot(KS, [D["%d_k%.1f"%(sd,k)]["t36"] for k in KS], "o-", color=cols[sd], lw=1.2, label="3–6 s（带载）")
    b.plot(KS, [D["%d_k%.1f"%(sd,k)]["t712"] for k in KS], "s--", color=cols[sd], lw=1.0, alpha=0.7, label="7–12 s（撤除后）")
b.set_xlabel("阈值 $k$"); b.set_ylabel("误触发次数"); b.set_title("(b) 误触发：$k$ 越大越少")
b.legend(fontsize=6.6, ncol=2); b.grid(alpha=0.25)
for sd in seeds:
    c_.plot(KS, [D["%d_k%.1f"%(sd,k)]["dip"] for k in KS], "o-", color=cols[sd], lw=1.2, label="种子 %d"%sd)
c_.axhline(-273.5, color="#3a3a3a", ls="--", lw=1.0, label="无自适应 −273.5")
c_.set_xlabel("阈值 $k$"); c_.set_ylabel("加载跌落 (rpm)"); c_.set_title("(c) 阶跃：高 $k$ 不误伤")
c_.legend(fontsize=7.2); c_.grid(alpha=0.25)
fig.tight_layout()
fig.savefig("fig_k_sweep.png", dpi=200)
print("ok")
