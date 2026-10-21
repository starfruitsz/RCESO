# -*- coding: utf-8 -*-
"""电流图（新 F-B，实验室 600 rpm）：第一行 Iq/Iqref，第二行 Id/Idref"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.4,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

D = np.load("_wave_lab_FB.npz")
t = D["t"]
iq, iqr = D["iq"], D["iqr"]
id_, idr = D["id"], D["idr"]
e_q = iq - iqr
e_d = id_ - idr

fig, ax = plt.subplots(2, 1, figsize=(12.0, 6.0), sharex=True,
                       gridspec_kw={"height_ratios": [1.0, 0.8], "hspace": 0.16})

ax[0].plot(t, iq, color="#16a085", lw=0.8, label="实测 $i_q$")
ax[0].plot(t, iqr, "--", color="#111111", lw=0.9, label="给定 $i_q^{\\rm ref}$")
ax[0].axvline(2.0, color="#555", ls=":", lw=0.7)
ax[0].axvline(6.0, color="#555", ls=":", lw=0.7)
ax[0].set_xlim(0, 8); ax[0].set_ylim(-0.3, 7.2)
ax[0].set_ylabel("$i_q$ (A)")
ax[0].set_title("(a) q 轴：实测 $i_q$ 与给定 $i_q^{\\rm ref}$（新 F-B，实验室 600 rpm）",
                fontsize=9.4)
ax[0].legend(fontsize=8.0, loc="upper left")
ax[0].grid(alpha=0.22)
ax[0].text(0.99, 0.95, "跟踪误差 RMS %.2f A" % np.sqrt(np.mean(e_q ** 2)),
           transform=ax[0].transAxes, ha="right", va="top", fontsize=8.0, color="#333")

ax[1].plot(t, id_, color="#2471a3", lw=0.8, label="实测 $i_d$")
ax[1].axhline(0, color="#111111", ls="--", lw=0.9, label="给定 $i_d^{\\rm ref}=0$")
ax[1].axvline(2.0, color="#555", ls=":", lw=0.7)
ax[1].axvline(6.0, color="#555", ls=":", lw=0.7)
ax[1].set_xlim(0, 8); ax[1].set_ylim(-1.0, 1.0)
ax[1].set_xlabel("时间 (s)"); ax[1].set_ylabel("$i_d$ (A)")
ax[1].set_title("(b) d 轴：实测 $i_d$ 与给定 $i_d^{\\rm ref}=0$", fontsize=9.4)
ax[1].legend(fontsize=8.0, loc="upper left")
ax[1].grid(alpha=0.22)
ax[1].text(0.99, 0.95, "误差 RMS %.2f A" % np.sqrt(np.mean(e_d ** 2)),
           transform=ax[1].transAxes, ha="right", va="top", fontsize=8.0, color="#333")

fig.savefig("fig_inv_current.png", dpi=200)
print("ok")
print("iq rms err", round(float(np.sqrt(np.mean(e_q ** 2))), 3),
      "id rms err", round(float(np.sqrt(np.mean(e_d ** 2))), 3))
print("iq max", round(float(iq.max()), 2), "iqr max", round(float(iqr.max()), 2))
