# -*- coding: utf-8 -*-
"""_es_1d_comp.py —— 额外项处理：符号律（补偿无意义）vs 比例律（补偿恢复对称）。"""
import numpy as np

delta_star, A0, kappa = -0.143, 1.0, 1.0
P_d, N, sigma, Delta = 1.5, 3, 0.01, 0.005
w_d = 2*np.pi/P_d; T_win = N*P_d; dt = 0.005; T_end = 60.0
n = int(T_end/dt); t = np.arange(n)*dt
k_win = int(round(T_win/dt)); r = sigma/(np.pi*N*Delta)
KPROP = 8.0

def run(law="sign", comp=False, d0=-0.10):
    dhat = d0; hist = np.zeros(n); acc = 0.0; out = np.empty(n)
    for k in range(n):
        ph = w_d*t[k]
        d = dhat + Delta*np.sin(ph)
        A = A0*(1+kappa*(d-delta_star)**2)
        val = A*np.sin(ph)*dt
        old = hist[k % k_win]; hist[k % k_win] = val
        acc += val - old
        if k >= k_win:
            I = 2.0/T_win*acc
            Ic = I/(1.0 + r*np.sign(I)) if comp else I
            if law == "sign":
                dhat = max(-0.2, min(0.2, dhat - (sigma/T_win)*np.sign(Ic)*dt))
            else:
                dhat = max(-0.2, min(0.2, dhat - KPROP*Ic*dt))
        out[k] = dhat
    return out

def stats(d):
    dev = np.abs(d - delta_star)
    idx = np.where(dev > 0.01)[0]
    settle = t[idx[-1]] if len(idx) else 0.0
    # 上升段与下降段时间（跨过 δ* 前）
    return d[t > 50].mean(), settle

print("law   comp   final_bias(pp)  settle(s)")
for law in ("sign", "prop"):
    for comp in (False, True):
        d = run(law, comp)
        m, st = stats(d)
        print("%-5s %-5s %8.2f %10.1f" % (law, comp, 100*(m-delta_star), st))
np.savez("_es_1d_comp.npz", t=t, sign_off=run("sign", False), sign_on=run("sign", True),
         prop_off=run("prop", False), prop_on=run("prop", True))
print("r = sigma/(pi N Delta) = %.3f" % r)
