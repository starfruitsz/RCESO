# -*- coding: utf-8 -*-
"""_es_1d_study.py —— 律T 极值搜索 1D 对照（逐样本模拟，窗口按真实历史累积）：
   (A) 事件式（窗内 δ̂ 保持不变，当前实现）
   (B) 连续滑动窗（δ̂ 每步都变，无 hold）
   A(δ)=A0[1+κ(δ−δ*)²]，δ=δ̂+Δ sin(ω_d t)。"""
import numpy as np

delta_star, A0, kappa = -0.143, 1.0, 1.0
P_d, N, sigma, Delta = 1.5, 3, 0.01, 0.005
w_d = 2 * np.pi / P_d
T_win = N * P_d
dt = 0.005
T_end = 90.0
n = int(T_end / dt)
t = np.arange(n) * dt

def run(mode, d0=-0.10, dead=0.0):
    dhat = d0
    hist = np.zeros(n)      # A*sin 的窗口缓冲
    acc = 0.0
    k_win = int(round(T_win / dt))
    out = np.empty(n)
    next_upd = T_win
    for k in range(n):
        ph = w_d * t[k]
        d = dhat + Delta * np.sin(ph)
        A = A0 * (1 + kappa * (d - delta_star) ** 2)
        val = A * np.sin(ph) * dt
        old = hist[k % k_win]
        hist[k % k_win] = val
        acc += val - old
        if k >= k_win:
            I = 2.0 / T_win * acc
            if mode == "event":
                if t[k] >= next_upd:
                    if abs(I) > dead:
                        dhat = max(-0.2, min(0.2, dhat - sigma * np.sign(I)))
                    next_upd += T_win
            else:
                if abs(I) > dead:
                    dhat = max(-0.2, min(0.2, dhat - (sigma / T_win) * np.sign(I) * dt))
        out[k] = dhat
    return out

dA = run("event")
dB = run("cont")
def metrics(d):
    tail = d[t > 70]
    dev = np.abs(d - delta_star)
    idx = np.where(dev > 0.01)[0]
    settle = t[idx[-1]] if len(idx) else 0.0
    return tail.mean(), tail.mean() - delta_star, settle, tail.std()
for name, d in (("事件式(hold)", dA), ("连续滑动窗", dB)):
    m, e, s, sd = metrics(d)
    print("%s：末段均值 %.4f  偏差 %+.4f  进入±1%%时刻 %.1f s  末段抖动 %.4f" % (name, m, e, s, sd))
print("理论额外项系数 2σ/(N P_d ω_d Δ) = %.3f" % (2 * sigma / (T_win * w_d * Delta)))
np.savez("_es_1d.npz", t=t, dA=dA, dB=dB)
print("saved _es_1d.npz")
