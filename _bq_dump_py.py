# -*- coding: utf-8 -*-
"""_bq_dump_py.py —— 跑一次 Python 闭环，导出 1 ms 输入流与逐窗原始估计 bq（bpv）
产物：_bq_dump.mat（t, iq, u, om, e1, v, bpv）供 MATLAB probe_bq.m 逐窗对照
用法: python _bq_dump_py.py [DT] [TEND]
"""
import sys
import numpy as np, scipy.io as sio
import noise_cfg as NC
from pmsm_inv_sim import sim_inv, I_BASE, W_REF

DT = float(sys.argv[1]) if len(sys.argv) > 1 else 2e-5
TEND = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
t = np.arange(0.0, TEND, DT)
TL = np.full_like(t, 0.30)

CFG = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=4000.0,
           Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,   # δ=0.10（历史验证口径）
           rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, J_true=9.95e-5,
           a_ref=1.0, log_eso=True,
           j_recheck=True, j_recheck_period=5.0, j_recheck_len=0.4,
           j_recheck_amp=0.118, j_recheck_amp_auto=False,
           j_recheck_nmin=1, j_recheck_t0=3.0,
           j_recheck_f=65.0, j_recheck_f_auto=False,
           j_recheck_gate=False, j_recheck_apply=False, j_recheck_alpha=1.0,
           j_recheck_btau=50.0/75.36, j_b0_direct=True, j_validate=False,
           j_b0_new=True, j_b0_onoff=True, j_amed=False)

Y = sim_inv(t, TL, CFG)
lg = np.asarray(Y['lg'])
nsp = int(round(1e-3 / DT))
tt = lg[:, 0]; e1 = lg[:, 1]; v = lg[:, 2]
iq = np.asarray(Y['iq'])[::nsp]; u = np.asarray(Y['u'])[::nsp]
om = np.asarray(Y['y'])[::nsp] * 600.0
n = min(len(tt), len(iq), len(u), len(om))
bpv = np.asarray(Y['bpv']) if 'bpv' in Y and np.asarray(Y['bpv']).size else np.zeros((0, 2))
sio.savemat('_bq_dump.mat', dict(t=tt[:n], iq=iq[:n] / I_BASE, u=u[:n], om=om[:n],
                                 e1=e1[:n], v=v[:n], bpv=bpv, dt=1e-3))
print('导出 %d 点（1 ms），逐窗 bq %d 个' % (n, len(bpv)))
if len(bpv):
    print('前 5 个窗: ' + ', '.join('%.2fs %.2f' % (a, b) for a, b in bpv[:5]))
print('saved _bq_dump.mat')
