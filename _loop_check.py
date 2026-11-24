# -*- coding: utf-8 -*-
"""_loop_check.py —— b0=标称(643.7) vs b0=真值附近(103) 时闭环对同一注入的响应"""
import numpy as np
import noise_cfg as NC
from pmsm_inv_sim import sim_inv, W_REF

DT = 5e-5; TEND = 25.0
t = np.arange(0.0, TEND, DT); TL = np.full_like(t, 0.30)
B_TRUE = 0.101 * 6.3069 / (9.95e-5 * W_REF)
base = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=4000.0,
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
            j_recheck_gate=False, j_recheck_apply=False, j_recheck_alpha=1.0,
            j_recheck_btau=50.0/75.36, j_b0_direct=True, j_validate=False,
            j_b0_new=True, j_b0_onoff=True, j_amed=False, j_b0_lo=10.0, j_b0_hi=5000.0)
print('b_true = %.1f' % B_TRUE)
for scale, name in ((1.0, 'b0=643.7（原标称，控制器整定值）'), (0.16, 'b0=103（真值附近）')):
    cfg = dict(base); cfg['b0_scale'] = scale
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y['t']); u = np.asarray(Y['u']); iq = np.asarray(Y['iq'])
    om = np.asarray(Y['y']) * 600.0
    on = (tt >= 3.2) & (tt < 3.4)
    ph = np.exp(-1j*2*np.pi*65.0*tt[on])
    au = 2.0/on.sum()*abs(np.sum(u[on]*ph)); aq = 2.0/on.sum()*abs(np.sum(iq[on]/6.3069*ph))
    print('%-28s |u65|=%.4f pu  |iq65|=%.4f pu  转速峰峰=%.1f rpm  转速均值=%.1f'
          % (name, au, aq, om[on].max()-om[on].min(), om[(tt>4)&(tt<5)].mean()))
