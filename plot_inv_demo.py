# -*- coding: utf-8 -*-
"""画真实逆变器模型的 dq/相电流、纹波、频谱：_inv_base.npz → fig_inv_demo.png"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False, "font.size": 9.2,
    "figure.dpi": 140, "savefig.bbox": "tight",
})

d = np.load("_inv_base.npz")
t = d["t"]; y = d["y"]; iq = d["iq"]; idq = d["id"]; ia = d["ia"]; iqr = d["iqr"]
t_old = d["t_old"]; y_old = d["y_old"]; iq_old = d["iq_old"]
N = 600.0
e = (y - 1.0) * N
e_old = (y_old - 1.0) * N

fig, ax = plt.subplots(2, 3, figsize=(12.2, 6.2))

# (a) 转速误差
ax[0, 0].plot(t, e, color="#16a085", lw=0.8, label="新模型（开关级）")
ax[0, 0].plot(t_old, e_old, color="#7f8c8d", lw=0.6, alpha=0.8, label="旧模型（一阶电流环）")
ax[0, 0].set_xlabel("时间 (s)"); ax[0, 0].set_ylabel("转速误差 (rpm)")
ax[0, 0].set_title("(a) 转速误差：新模型含 PWM 纹波与死区畸变", fontsize=9.2)
ax[0, 0].legend(fontsize=7.2, loc="lower right"); ax[0, 0].grid(alpha=0.25)

# (b) 加载瞬态 iq
m = (t >= 2.0) & (t <= 2.2)
ax[0, 1].plot(t[m], iq[m], color="#c0392b", lw=0.8, label="$i_q$ 实际")
ax[0, 1].plot(t[m], iqr[m], color="#2c3e50", lw=0.9, ls="--", label="$i_q^*$")
ax[0, 1].set_xlabel("时间 (s)"); ax[0, 1].set_ylabel("电流 (A)")
ax[0, 1].set_title("(b) 加载瞬态：$i_q$ 跟踪与纹波", fontsize=9.2)
ax[0, 1].legend(fontsize=7.2); ax[0, 1].grid(alpha=0.25)

# (c) 相电流 200 us 放大（取 5.0–5.02 s 内的峰值，纹波最清楚）
_m5 = (t >= 5.0) & (t < 5.02)
_tc = t[_m5][np.argmax(ia[_m5])]
m = (t >= _tc - 1e-4) & (t <= _tc + 1e-4)
ax[0, 2].plot((t[m] - t[m][0]) * 1e6, ia[m], color="#2471a3", lw=1.0)
ax[0, 2].set_xlabel("时间 (us)"); ax[0, 2].set_ylabel("$i_a$ (A)")
ax[0, 2].set_title("(c) 相电流：10 kHz PWM 纹波（2 个周期）", fontsize=9.2)
ax[0, 2].grid(alpha=0.25)

# (d) dq 电流 20 ms 放大
m = (t >= 5.00) & (t <= 5.02)
ax[1, 0].plot(t[m] * 1e3, iq[m], color="#c0392b", lw=0.9, label="$i_q$")
ax[1, 0].plot(t[m] * 1e3, idq[m], color="#2980b9", lw=0.9, label="$i_d$")
ax[1, 0].set_xlabel("时间 (ms)"); ax[1, 0].set_ylabel("电流 (A)")
ax[1, 0].set_title("(d) dq 电流：±0.3 A 采样噪声 + 纹波", fontsize=9.2)
ax[1, 0].legend(fontsize=7.2); ax[1, 0].grid(alpha=0.25)

# (e) iq 频谱（5–6 s）
def spec(x, fs):
    x = x - x.mean()
    w = np.hanning(len(x))
    X = np.fft.rfft(x * w)
    f = np.fft.rfftfreq(len(x), 1 / fs)
    return f, 2 * np.abs(X) / len(x)
m = (t >= 5.0) & (t < 6.0)
f, A = spec(iq[m], 1e5)
ax[1, 1].semilogy(f / 1e3, A, color="#c0392b", lw=0.7)
ax[1, 1].set_xlim(0, 12); ax[1, 1].set_xlabel("频率 (kHz)")
ax[1, 1].set_ylabel("$i_q$ 幅值 (A)")
ax[1, 1].set_title("(e) $i_q$ 频谱：10 kHz 开关峰", fontsize=9.2)
ax[1, 1].grid(alpha=0.25, which="both")

# (f) 相电流频谱
m = (t >= 5.0) & (t < 6.0)
f2, A2 = spec(ia[m], 1e5)
ax[1, 2].semilogy(f2 / 1e3, A2, color="#2471a3", lw=0.7)
ax[1, 2].set_xlim(0, 12); ax[1, 2].set_xlabel("频率 (kHz)")
ax[1, 2].set_ylabel("$i_a$ 幅值 (A)")
ax[1, 2].set_title("(f) 相电流频谱：开关与死区谐波", fontsize=9.2)
ax[1, 2].grid(alpha=0.25, which="both")

fig.tight_layout()
fig.savefig("fig_inv_demo.png", dpi=200)
print("ok: fig_inv_demo.png")
