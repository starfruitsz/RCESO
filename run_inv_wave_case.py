# -*- coding: utf-8 -*-
"""指定额定转速/负载频率的四配置时序（实验室噪声）

用法：python run_inv_wave_case.py 900 15
输出 _wave_900_{Base,LawD,FB,D+FB}.npz
"""
import math
import sys
import numpy as np

from pmsm_inv_sim import sim_inv, band_noise
import noise_cfg as NC

N_REF = float(sys.argv[1]) if len(sys.argv) > 1 else 600.0
F_LOAD = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
T = 1.0 / F_LOAD
DT, TEND, TL0, TW = 2e-6, 8.0, 2.0, 6.0
SEED = 20261018
t = np.arange(0.0, TEND, DT)
tau = np.maximum(t - TL0, 0.0); ph = 2 * math.pi * tau / T
on = (t >= TL0).astype(float)
onp = ((t >= TL0) & (t < TW)).astype(float)
TLdet = (0.50 * on + 0.30 * onp *
         (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))) * 0.637
nT = int(round(t[-1] / 1e-4)) + 2
TLn = band_noise(nT, NC.NOISE_LAB["sig_T_nm"], 200.0, 1e-4, 20261017)

base_kw = dict(n_ref=N_REF, T=T,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=SEED)
CFG = [
    ("Base", dict(det_eps=0.0)),
    ("LawD", dict(kp_boost=4.0, det_eps=0.01)),
    ("FB", dict(ff_mism=0.2, ff_mism_eps=1e-6, ff_cool=0.3, ff_flush=0.0, ff_gmax=0.05)),
    ("D+FB", dict(kp_boost=4.0, det_eps=0.01, ff_mism=0.2, ff_mism_eps=1e-6,
                  ff_cool=0.3, ff_flush=0.0, ff_gmax=0.05)),
]
DEC = max(1, int(round(1e-5 / DT)))
for name, kw in CFG:
    Y = sim_inv(t, TLdet, dict(base_kw, **kw))
    tt = Y["t"]; n = len(tt)
    TLplot = TLdet[::DEC][:n] + TLn[np.minimum((tt / 1e-4).astype(int), nT - 1)]
    np.savez("_wave_%d_%s.npz" % (int(N_REF), name),
             t=tt, TL=TLplot, y=Y["y"], iq=Y["iq"], id=Y["id"])
    e = (Y["y"] - 1.0) * N_REF
    print(name, int(N_REF), "dip", round(float(np.min(e[(tt >= 1.9) & (tt <= 2.4)])), 1),
          "steady", round(float(np.sqrt(np.mean(e[(tt >= 7) & (tt < 8)] ** 2))), 2))
print("done")

