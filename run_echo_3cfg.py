# -*- coding: utf-8 -*-
"""回声 + 加载突变：律 D / F-B / D+F-B 三组仿真"""
import math, os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from adrc_eso_closed import adrc_sim
os.chdir(r"C:\Users\Administrator\Desktop\2026.10汇报")

KT, J_M, T_RATED = 0.101, 1.89e-5, 0.637
N = 600.0; W_REF = N*math.pi/30.0; I_BASE = T_RATED/KT
B = KT*I_BASE/(J_M*W_REF); B0 = 1.2*B
T, DT, TEND, TL0 = 0.1, 1e-5, 12.0, 2.0
TW = 6.0                      # 撤除时刻（10 Hz 零交越）
KP, WO, FCI, B3, T0 = 75.36, 500.0, 1000.0, 2000.0, 5e-3
t = np.arange(0.0, TEND, DT); n = len(t)

def bn(sig, fc, sd):
    rng = np.random.default_rng(sd); x = rng.standard_normal(n)
    a = 1.0 - math.exp(-2.0*math.pi*fc*DT); nk = max(1, int(math.ceil(6.0/(2.0*math.pi*fc*DT))))
    y = np.convolve(x, a*np.power(1.0-a, np.arange(nk)))[:n]; return y/y.std()*sig
NI = bn(0.01, 2000.0, 20261016); NT = bn(0.05, 200.0, 20261017)

tau = np.maximum(t - TL0, 0.0); ph = 2*math.pi*tau/T
A = 0.30                                  # 不对中幅值（额定倍数）
on_step = (t >= TL0).astype(float)
on_per  = ((t >= TL0) & (t < TW)).astype(float)   # 6 s 零交越处撤除
TL = 0.50*on_step + A*on_per*(np.sin(ph) + 0.4*np.sin(3*ph) + 0.2*np.sin(5*ph))
d = -B*TL; r = np.full_like(t, 1.0); DN = -B*NT

common = dict(b=B, b0=B0, wo=WO, kp=KP, T=T, zeta=0.2, beta3=B3, tau0=T0, kappa=0.1, Q0=0.98,
              gamma=1.0, sig1=1e5, sig2=5.0, mu=0.0, adapt=0, warm=2.0, taumax=5.0, taumin=0.2,
              law="decupled", qmax=1.8, qmodel_max=1.0, drive_mode="bpw", theta_sign=1.0,
              bpw_fa=5.0, bpw_sa=50.0, bpw_fb=1.0, bpw_sb=10.0, qd_mode=2, qmin=0.2,
              norm_floor=6.5, eo_def="meansq", theta_drive="bnorm", q_drive="bnorm",
              q_rest_tau="none", e1src="estimation", c1=0.1, c2=0.1, b_filt=1.0, b0_tau=1.0,
              cur_tau=1.0/(2*math.pi*FCI), cur_noise=NI, d_noise=DN, det_eps=0.01)
CFG = [
    ("LawD",   dict(p_boost=4.0)),
    ("FB",     dict(ff_flush=1.8, ff_tau_f=4e-3, ff_tau_s=0.5, ff_cool=0.3)),
    ("D+FB",   dict(p_boost=4.0, ff_flush=1.8, ff_tau_f=4e-3, ff_tau_s=0.5, ff_cool=0.3)),
]
res = {}
for name, kw in CFG:
    Y = adrc_sim(t, r, d, **common, **kw)
    y = np.asarray(Y["y"]); ia = np.asarray(Y["ia"])
    np.savez("_echo_%s.npz" % name, t=t, y=y, ia=ia, TL=TL, u=np.asarray(Y.get("u", ia)))
    e = (y - 1.0)*N
    seg = (t >= 1.9) & (t <= 2.4)
    dip = float(np.min(e[seg]))
    m1 = (t >= TW) & (t < TW + T)
    rms1 = float(np.sqrt(np.mean(e[m1]**2)))
    # 10 Hz 幅值（滑窗 1 个周期）
    def amp(t0s, t1s):
        m = (t >= t0s) & (t < t1s)
        tt = t[m]; ee = e[m]
        c = 2*np.mean(ee*np.cos(2*math.pi*tt/T)); s_ = 2*np.mean(ee*np.sin(2*math.pi*tt/T))
        return float(math.hypot(c, s_))
    res[name] = dict(dip=dip, rms1=rms1, a_pre=amp(5.0, 5.9), a_echo=amp(TW, TW+T),
                     steady=float(np.sqrt(np.mean(e[(t >= 8.0) & (t < 10.0)]**2))),
                     maxia=float(np.max(np.abs(ia))*I_BASE))
    print("W7 %-5s dip=%.1f rms1=%.1f a_pre=%.1f a_echo=%.1f steady=%.2f maxia=%.2f"
          % (name, dip, rms1, res[name]["a_pre"], res[name]["a_echo"], res[name]["steady"], res[name]["maxia"]), flush=True)
json.dump(res, open("_echo_metrics.json", "w"), ensure_ascii=False, indent=1)
print("DONE")
