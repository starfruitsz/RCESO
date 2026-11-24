import numpy as np
import noise_cfg as NC
from pmsm_inv_sim import sim_inv, W_REF
DT = 5e-5; TEND = 12.0
t = np.arange(0.0, TEND, DT); TL = np.full_like(t, 0.30)
base = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=4000.0,
            Q0=0.98, tau0=20e-3, seed_i=20261018,
            i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
            sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
            eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
            rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, J_true=9.95e-5,
            a_ref=1.0, log_eso=True,
            j_recheck=True, j_recheck_period=5.0, j_recheck_len=0.4,
            j_recheck_amp=0.118, j_recheck_amp_auto=False,
            j_recheck_nmin=1, j_recheck_t0=3.0,
            j_recheck_f=65.0, j_recheck_f_auto=False,
            j_recheck_gate=False, j_recheck_apply=False, j_recheck_alpha=1.0,
            j_recheck_btau=50.0/75.36, j_b0_direct=True, j_validate=False,
            j_b0_new=True, j_b0_onoff=True, j_amed=False)
for law in ('fal', 'linear'):
    cfg = dict(base); cfg['eso_law'] = law
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y['t']); om = np.asarray(Y['y'])*600.0; u = np.asarray(Y['u'])
    m = tt > 8.0
    print('%-7s  8s后转速均值=%.1f rpm  范围 %.0f..%.0f   |u|max=%.2f' % (law, om[m].mean(), om[m].min(), om[m].max(), np.abs(u[m]).max()))
