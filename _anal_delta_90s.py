# -*- coding: utf-8 -*-
"""_anal_delta_90s.py — 90 s 收敛检查：delta_hat 轨迹、慢振荡周期/幅值、滚动 10 Hz 残余。"""
import numpy as np, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TAGS = [("f90c", "融合", "#1e8449"), ("t90c", "仅律T", "#e67e22")]
T_D0, P_D, DITH = 3.0, 1.5, 0.005

def load(tag):
    z = np.load("_tjc_%s.npz" % tag)
    return (np.asarray(z["t"]), np.asarray(z["y"]), np.asarray(z["es"]),
            np.asarray(z["b0e"]), np.asarray(z["t_j"]))

def dh_of(t, es):
    d = np.array(es, dtype=float)
    d[0] = d[1]                      # 首个采样是 0 初始化，跳过
    m = t >= T_D0
    d[m] -= DITH * np.sin(2 * np.pi * (t[m] - T_D0) / P_D)
    return d

def rolling(t, y, tq, w=2.0):
    e = (y - 1.0) * 600.0
    i0 = np.searchsorted(t, tq); i1 = np.searchsorted(t, tq + w)
    xs = e[i0:i1]; ts = t[i0:i1]
    if len(xs) < 100:
        return np.nan, np.nan
    rms = float(np.sqrt(np.mean(xs ** 2)))
    c = 2 * np.mean(xs * np.cos(2 * np.pi * 10 * ts)); s = 2 * np.mean(xs * np.sin(2 * np.pi * 10 * ts))
    return rms, float(np.hypot(c, s))

plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "font.size": 8.6, "figure.dpi": 150,
                     "axes.grid": True, "grid.alpha": 0.17, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False})
fig, ax = plt.subplots(3, 1, figsize=(12.8, 7.2), sharex=True,
                       gridspec_kw=dict(height_ratios=[1.6, 1, 1], hspace=0.16))
out = {}
for tag, name, col in TAGS:
    t, y, es, b0, tj = load(tag)
    dh = dh_of(t, es)
    dec = 200
    ts = t[::dec]; ds = dh[::dec]
    n = max(3, int(round(1.5 / (ts[1] - ts[0]))))   # 1 个 dither 周期的滑动平均
    pad = n // 2
    dsp = np.concatenate([np.full(pad, ds[0]), ds, np.full(pad, ds[-1])])
    sm = np.convolve(dsp, np.ones(n) / n, mode="valid")[:len(ds)]   # 无零填充边缘效应
    ax[0].plot(ts, 100 * ds, color=col, lw=0.3, alpha=0.3)
    ax[0].plot(ts, 100 * sm, color=col, lw=1.5, label=name)
    vals = []
    for tv in range(10, 91, 10):
        i = min(int(round(tv / (ts[1] - ts[0]))), len(ds) - 1)
        vals.append(round(100 * float(ds[i]), 2))   # 用原始（已扣 dither）采样，避免平滑边缘
    seg_m = (ts >= 30) & (ts <= 90)
    seg = sm[seg_m]; tseg = ts[seg_m]
    dsm = np.diff(seg)
    ipk = np.where((np.sign(dsm[:-1]) > 0) & (np.sign(dsm[1:]) <= 0))[0] + 1
    itr = np.where((np.sign(dsm[:-1]) < 0) & (np.sign(dsm[1:]) >= 0))[0] + 1
    pk = tseg[ipk]; tr = tseg[itr]
    qs = np.arange(4.0, 88.0, 2.0)
    rr = np.array([rolling(t, y, q) for q in qs])
    ax[1].plot(qs + 1.0, rr[:, 1], color=col, lw=1.0, label=name)
    ax[2].plot(qs + 1.0, rr[:, 0], color=col, lw=1.0, label=name)
    def st(a, b):
        m = (ts >= a) & (ts <= b); return float(np.mean(sm[m])), float(np.std(sm[m]))
    out[tag] = dict(name=name, every10s=vals,
                    mean_std_30_50=st(30, 50), mean_std_50_70=st(50, 70), mean_std_70_90=st(70, 90),
                    peaks=[round(float(x), 1) for x in pk], troughs=[round(float(x), 1) for x in tr],
                    b0_end=float(b0[-1]),
                    rms_last10=float(np.nanmean(rr[qs >= 78, 0])), a10_last10=float(np.nanmean(rr[qs >= 78, 1])))
ax[0].axhline(-14.3, color="#2c3e50", ls=":", lw=0.9)
ax[0].text(88, -14.45, "理论 δ*=−14.3%", fontsize=6.4, color="#2c3e50", ha="right", va="top")
for k in range(1, 9):
    ax[0].axvline(1 + 10 * k, color="#888", ls="--", lw=0.6, alpha=0.7)
ax[0].set_ylabel("$\\hat{\\delta}$ / %"); ax[0].set_xlim(0, 90); ax[0].set_ylim(-15.6, -10.4)
ax[0].legend(fontsize=7, ncol=2, loc="upper right")
ax[0].set_title("(a) 律T 的 $\\hat{\\delta}$（0–90 s；虚线 = 律J burst 时刻）", fontsize=9)
ax[1].set_ylabel("10 Hz / rpm"); ax[1].legend(fontsize=7, ncol=2, loc="upper right")
ax[1].set_title("(b) 滚动 10 Hz 残余（2 s 窗）", fontsize=9)
ax[2].set_ylabel("RMS / rpm"); ax[2].set_xlabel("时间 / s"); ax[2].legend(fontsize=7, ncol=2, loc="upper right")
ax[2].set_title("(c) 滚动 RMS（2 s 窗）", fontsize=9)
fig.suptitle("90 s 收敛检查：连续滑动窗律T + 律J（α=1、b0 低通 kp/10）", fontsize=9.6, y=0.965)
fig.savefig("fig_delta_90s.png", dpi=150, facecolor="white")
json.dump(out, open("_delta_90s.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
