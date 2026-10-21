# -*- coding: utf-8 -*-
"""Light-load seven-window RMS for RCESO + Law D only (Q channel removed)."""
import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from adrc_eso_closed import adrc_sim
KT, J_M, T_RATED = 0.101, 1.89e-5, 0.637
N = 600.0; W_REF = N*math.pi/30.0; I_BASE = T_RATED/KT
B = KT*I_BASE/(J_M*W_REF); B0 = 1.2*B
T, DT, TEND, TL0 = 0.1, 1e-5, 12.0, 2.0
KP, WO, FCI, B3, T0 = 75.36, 500.0, 1000.0, 2000.0, 5e-3
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
def go(pi=0.0, eso=True, rc=True, q=0, b=0, dd=0):
    return adrc_sim(t, r, d, B, B0, (WO if eso else 0.0), KP, T, 0.2, (B3 if rc else 0.0), T0, 0.1, 0.98,
                    0.0 if q else 1.0, 1e5, 5.0, (0.06 if q else 0.0), adapt=q, warm=2.0, taumax=5.0, taumin=0.2,
                    law="decupled", qmax=1.8, qmodel_max=1.0, drive_mode="bpw", theta_sign=1.0,
                    bpw_fa=5.0, bpw_sa=50.0, bpw_fb=1.0, bpw_sb=10.0, qd_mode=2, qmin=0.2,
                    norm_floor=6.5, eo_def="meansq", theta_drive="bnorm", q_drive="bnorm",
                    q_rest_tau="none", e1src="estimation", c1=0.1, c2=0.1, b_filt=1.0, b0_tau=1.0,
                    cur_tau=1.0/(2*math.pi*FCI), cur_noise=NI, d_noise=DN,
                    p_boost=(4.0 if dd else 0.0), eso_sched=(3.0 if b else 0.0), det_eps=0.01, pi_ki=pi)
W = [(0.5,2.0),(2.0,2.5),(2.5,2.6),(3.0,3.5),(3.5,4.0),(4.0,6.0),(7.0,12.0)]
for nm, kw in [("RCESO", dict()), ("RCESO+LawD", dict(dd=1)), ("RCESO+BD", dict(dd=1, b=1))]:
    Y = go(**kw); e = (Y["y"]-1.0)*N
    rms = [float(np.sqrt(np.mean(e[(t>=a)&(t<b)]**2))) for a,b in W]
    print("W7 %-12s %s  maxia=%.2f" % (nm, " ".join("%.2f" % v for v in rms), float(np.abs(Y["ia"]).max()*I_BASE)), flush=True)
print("DONE")
