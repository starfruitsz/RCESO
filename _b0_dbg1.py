# -*- coding: utf-8 -*-
"""_b0_dbg1.py —— 单波（正弦）60 s，打印逐 burst 的 btm/bq/B0e，定位更新环问题"""
import numpy as np
import noise_cfg as NC
from pmsm_inv_sim import sim_inv, W_REF

DT = 5e-5; TEND = 60.0
t = np.arange(0.0, TEND, DT); TL = np.full_like(t, 0.30)
B_TRUE = 0.101 * 6.3069 / (9.95e-5 * W_REF)
cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=4000.0,
           Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="linear", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
           rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, J_true=9.95e-5,
           a_ref=1.0, log_eso=True,
           j_recheck=True, j_recheck_period=5.0, j_recheck_len=0.4,
           j_recheck_amp=0.118, j_recheck_amp_auto=False,
           j_recheck_nmin=1, j_recheck_t0=3.0,
           j_recheck_f=65.0, j_recheck_f_auto=False,
           j_recheck_gate=False, j_recheck_apply=True, j_recheck_alpha=1.0,
           j_recheck_btau=50.0/75.36, j_b0_direct=True, j_validate=False,
           j_b0_new=True, j_b0_onoff=True, j_amed=False, j_b0_final=True,
           j_b0_lo=10.0, j_b0_hi=5000.0, b0_scale=0.16)
Y = sim_inv(t, TL, cfg)
jn = np.asarray(Y['jnew']); bpv = np.asarray(Y['bpv'])
print('b_true=%.1f   逐 burst（t, 更新前B0e, 本窗原始估计）：' % B_TRUE)
for r in jn[:14]:
    print('  t=%6.2f  B0e=%8.2f  btm=%8.2f' % (r[0], r[1], r[2]))
print('逐窗 bpv（前 14）：', ' '.join('%.1f' % x[1] for x in bpv[:14]))
