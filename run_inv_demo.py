# -*- coding: utf-8 -*-
"""真实逆变器 + 电机模型演示：三相 PWM、死区、器件压降、反电动势、±0.3 A dq 采样噪声

工况：0–2 s 空载，2 s 加载 0.50 额定；2–6 s 叠加 10 Hz 不对中簇（A=0.30）；
6 s 零交越撤除。8 s 轨迹。
对比：旧 pmsm_dq_sim（一阶电流环等效） vs 新 pmsm_inv_sim（开关级逆变器）。
输出：_inv_base.npz；指标打印。
"""
import math
import numpy as np

from pmsm_inv_sim import sim_inv, N_REF as N_INV
from pmsm_dq_sim import sim_dq, N_REF as N_DQ
import noise_cfg as NC

T, DT, TEND, TL0, TW = 0.1, 1e-6, 8.0, 2.0, 6.0
t = np.arange(0.0, TEND, DT)
tau = np.maximum(t - TL0, 0.0)
ph = 2 * math.pi * tau / T
on = (t >= TL0).astype(float)
onp = ((t >= TL0) & (t < TW)).astype(float)
TL = (0.50 * on + 0.30 * onp *
      (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))) * 0.637

# 新模型（默认：fci=1 kHz、beta3=2000、tau0=20 ms，针对开关级对象重整定）
Y = sim_inv(t, TL, dict(i_noise_peak=NC.NOISE["i_noise_peak"],
                        fci=2000.0, beta3=4000.0, tau0=20e-3))

# 旧模型（同一负载，一阶电流环；用 10 us 步长以控制内存）
t_old = np.arange(0.0, TEND, 1e-5)
tau_o = np.maximum(t_old - TL0, 0.0); ph_o = 2 * math.pi * tau_o / T
on_o = (t_old >= TL0).astype(float)
onp_o = ((t_old >= TL0) & (t_old < TW)).astype(float)
TL_o = (0.50 * on_o + 0.30 * onp_o *
        (np.sin(ph_o) + 0.4 * np.sin(3 * ph_o) + 0.2 * np.sin(5 * ph_o))) * 0.637
TL_o = TL_o + NC.load_noise(len(t_old), 1e-5)
Y_old = sim_dq(t_old, TL_o, dict(**NC.sim_kwargs(), beta3=2000.0, tau0=5e-3,
                                 fci=1000.0))

np.savez("_inv_base.npz",
         t=Y["t"], y=Y["y"], id=Y["id"], iq=Y["iq"], ia=Y["ia"],
         iqr=Y["iqr"], vq=Y["vq"], fl=Y["fl"],
         t_old=t_old, y_old=Y_old["y"], iq_old=Y_old["iq"], id_old=Y_old["id"])

tt = Y["t"]; e = (Y["y"] - 1.0) * N_INV
m_load = (tt >= 4.0) & (tt < 6.0)
m_aft = (tt >= 7.0) & (tt < 8.0)
# dq 采样噪声：1 kHz 以上高频分量（去趋势）
def hp(x, fs, fc=1000.0):
    a = math.exp(-2 * math.pi * fc / fs)
    y = np.empty_like(x); s = x[0]
    for i, v in enumerate(x):
        s = a * s + (1 - a) * v
        y[i] = v - s
    return y
iq_hf = hp(Y["iq"], 1e5)
id_hf = hp(Y["id"], 1e5)
print("NEW: speed RMS with-load %.2f rpm, after %.2f rpm" %
      (np.sqrt(np.mean(e[m_load] ** 2)), np.sqrt(np.mean(e[m_aft] ** 2))))
print("NEW: iq mean %.2f A, std %.2f A, HF std %.2f A (id HF %.2f)" %
      (Y["iq"][m_load].mean(), Y["iq"][m_load].std(),
       iq_hf[m_load].std(), id_hf[m_load].std()))
print("OLD: speed RMS with-load %.2f rpm, after %.2f rpm" %
      (np.sqrt(np.mean(((Y_old["y"] - 1.0) * N_DQ)[(t_old >= 4) & (t_old < 6)] ** 2)),
       np.sqrt(np.mean(((Y_old["y"] - 1.0) * N_DQ)[(t_old >= 7) & (t_old < 8)] ** 2))))
print("saved _inv_base.npz")
