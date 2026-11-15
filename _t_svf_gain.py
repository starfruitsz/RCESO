# -*- coding: utf-8 -*-
"""校验 SVF 带通在中心频率的增益（与 pmsm_inv_sim 的实现逐行一致）。"""
import numpy as np, math
fs = 1000.0; f0 = 10.0; Q = 5.0
N = 20000
t = np.arange(N)/fs
for amp in (1.0,):
    x = amp*np.cos(2*np.pi*f0*t)
    f = 2.0*math.sin(math.pi*f0/fs)
    low=0.0; band=0.0; out=np.zeros(N)
    for k in range(N):
        low += f*band
        high = x[k] - low - (1.0/Q)*band
        band += f*high
        out[k] = band
    ss = out[N//2:]
    # 用同一周期的均方根（项目口径 A = sqrt(mean(band^2)) over 1 period）
    nT = int(round((1.0/f0)*fs))
    A = np.sqrt(np.mean(ss[:nT]**2))
    # 幅值
    X = np.fft.rfft(ss); fr = np.fft.rfftfreq(len(ss), 1/fs)
    k10 = np.argmin(abs(fr-f0)); amp_out = 2*abs(X[k10])/len(ss)
    print("输入幅值 %.2f -> 带通输出幅值 %.3f（gain %.2f）; A=%.3f; 输入 RMS=%.3f" % (
        amp, amp_out, amp_out/amp, A, amp/np.sqrt(2)))
# 纯 1x 的 DFT 估计：A_dft = sqrt(2)/N |sum x e^{-j theta}|
th = 2*np.pi*f0*t
Nw = 200
for start in (5000, 8000):
    seg = x[start:start+Nw]; ths = th[start:start+Nw]
    c = np.sum(seg*np.cos(ths)); s = np.sum(seg*np.sin(ths))
    print("DFT 估计 A = %.4f（真值 RMS %.4f）" % (math.sqrt(2)*math.hypot(c,s)/Nw, amp/np.sqrt(2)))
