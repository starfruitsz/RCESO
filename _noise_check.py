# -*- coding: utf-8 -*-
"""单个噪声源的贡献分解（串行，避免 Windows spawn 的顶层 Pool 问题）"""
import numpy as np
from pmsm_inv_sim import sim_inv
from tl_profile import disc_unbalance_profile
import noise_cfg as NC

print("NOISE_LAB =", NC.NOISE_LAB, flush=True)
t = np.arange(0.0, 8.0, 2e-6)
TL = (0.50 * (t >= 2.0)).astype(float) * 0.637
base = dict(n_ref=600.0, T=0.1, fci=500.0, beta3=0.0, tau0=20e-3, seed_i=20261018,
            tl_ang=disc_unbalance_profile(), tl_ang_amp=0.1, tl_ang_start=2.0,
            eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
cases = [("全部实验室噪声", dict(i_noise_peak=0.1, sig_n=3.0, sig_T_nm=0.01)),
         ("无噪声", dict(i_noise_peak=0.0, sig_n=0.0, sig_T_nm=0.0)),
         ("仅电流噪声", dict(i_noise_peak=0.1, sig_n=0.0, sig_T_nm=0.0)),
         ("仅转速噪声", dict(i_noise_peak=0.0, sig_n=3.0, sig_T_nm=0.0)),
         ("仅负载噪声", dict(i_noise_peak=0.0, sig_n=0.0, sig_T_nm=0.01))]
print("%-14s %10s %10s %10s %10s" % ("配置", "空载n_rms", "空载iq_std", "故障n_rms", "iq_std"), flush=True)
for name, nk in cases:
    Y = sim_inv(t, TL, dict(base, **nk))
    tt = Y["t"]; e = (Y["y"] - 1.0) * 600.0
    m0 = (tt >= 1.0) & (tt < 2.0)
    m1 = (tt >= 5.0) & (tt < 6.0)
    print("%-14s %10.2f %10.3f %10.1f %10.3f" % (
        name, float(np.sqrt(np.mean(e[m0] ** 2))), float(np.std(Y["iq"][m0])),
        float(np.sqrt(np.mean(e[m1] ** 2))), float(np.std(Y["iq"][m1]))), flush=True)
print("DONE", flush=True)
