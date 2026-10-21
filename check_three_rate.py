# -*- coding: utf-8 -*-
"""铁律校验：单速率 vs 三速率（对象 10us / 电流环 50us / 转速环 1ms）"""
import math, numpy as np, os, sys
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")
from rcso_multirate import sim_mr, sim_mr3

KT, J_M, T_RATED = 0.101, 1.89e-5, 0.637
N = 600.0; W_REF = N*math.pi/30.0; I_BASE = T_RATED/KT
B = KT*I_BASE/(J_M*W_REF); B0 = 1.2*B
T, DT, TEND, TL0 = 0.1, 1e-5, 12.0, 2.0
KP, WO, B3, T0 = 75.36, 500.0, 2000.0, 5e-3
TAU_CI = 1.0/(2*math.pi*1000.0)
t = np.arange(0.0, TEND, DT); n = len(t)
def bn(sig, fc, sd):
    rng = np.random.default_rng(sd); x = rng.standard_normal(n)
    a = 1.0 - math.exp(-2.0*math.pi*fc*DT); nk = max(1, int(math.ceil(6.0/(2.0*math.pi*fc*DT))))
    y = np.convolve(x, a*np.power(1.0-a, np.arange(nk)))[:n]; return y/y.std()*sig
NI = bn(0.01, 2000.0, 20261016); NT = bn(0.05, 200.0, 20261017)
tau = np.maximum(t - TL0, 0.0); on = (t >= TL0).astype(float); ph = 2*math.pi*tau/T
npc = 0.06*(np.sin(2*math.pi*5.9*tau) + 0.5*np.sin(2*math.pi*11.8*tau)
            + (1.0/3)*np.sin(2*math.pi*17.7*tau) + 0.25*np.sin(2*math.pi*23.6*tau))*on
amp = np.full_like(t, 0.03)
amp = np.where((tau >= 0.5) & (tau < 0.6), 0.06, amp); amp = np.where((tau >= 1.0) & (tau < 1.5), 0.06, amp)
amp = np.where(tau >= 2.0, 0.08, amp)
TL = (0.50*on + npc + amp*(np.sin(ph) + 0.4*np.sin(3*ph) + 0.2*np.sin(5*ph)))*on
d = -B*TL; r = np.full_like(t, 1.0); DN = -B*NT
W = [(0.5,2.0),(2.0,2.5),(2.5,2.6),(3.0,3.5),(3.5,4.0),(4.0,6.0),(7.0,12.0)]
def rep(Y):
    e = (Y["y"] - 1.0)*N
    return [float(np.sqrt(np.mean(e[(t>=a)&(t<b)]**2))) for a,b in W]
base = dict(b=B, b0=B0, wo=WO, kp=KP, Tper=T, zeta=0.2, beta3=B3, tau0=T0, tau_ci=TAU_CI,
            det_eps=0.01, NI=NI, DN=DN)
for lbl, kw in [
    ("RCESO  single-rate", dict(law="rc", dt_ci=DT, t_ctrl=DT)),
    ("RCESO  10/50us/1ms", dict(law="rc", dt_ci=5e-5, t_ctrl=1e-3)),
    ("RD      single-rate", dict(law="rc", kp_boost=4.0, dt_ci=DT, t_ctrl=DT)),
    ("RD      10/50us/1ms", dict(law="rc", kp_boost=4.0, dt_ci=5e-5, t_ctrl=1e-3)),
]:
    Y = sim_mr3(t, r, d, **base, **kw)
    print("%-20s %s" % (lbl, " ".join("%7.2f" % v for v in rep(Y))), flush=True)
print("DONE")
