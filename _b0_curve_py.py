# -*- coding: utf-8 -*-
"""_b0_curve_py.py —— Python 带噪声闭环里，三种注入波形的 b0 辨识曲线
用法: python _b0_curve_py.py [DT] [TEND]
默认 DT=1e-3（与 Simulink 同步）、TEND=130；period=5 s、24 个 burst 量级
"""
import sys, json
import numpy as np
import noise_cfg as NC
from pmsm_inv_sim import sim_inv, J_M, I_BASE, W_REF

DT = float(sys.argv[1]) if len(sys.argv) > 1 else 2e-5
TEND = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
t = np.arange(0.0, TEND, DT)
TL = np.full_like(t, 0.30)

B_TRUE = 0.101 * I_BASE / (9.95e-5 * W_REF)      # 物理增益 kt*IBASE/(J*w_ref) = 101.89
BTAU = 50.0 / 75.36

BASE = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=4000.0,
            Q0=0.98, tau0=20e-3, seed_i=20261018,
            i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
            sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
            eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
            rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, J_true=9.95e-5,
            a_ref=1.0, log_eso=True,
            j_recheck=True, j_recheck_period=5.0, j_recheck_len=0.4,
            j_recheck_amp=0.118, j_recheck_amp_auto=False,
            j_recheck_nmin=2, j_recheck_t0=3.0,
            j_recheck_f=65.0, j_recheck_f_auto=False,
            j_recheck_gate=False, j_recheck_apply=True, j_recheck_alpha=1.0,
            j_recheck_btau=BTAU, j_b0_direct=True, j_validate=False,
            j_b0_new=True, j_b0_onoff=True, j_amed=False)

CASES = [('正弦', {}), ('方波', dict(j_dith_sq=True)), ('三角', dict(j_dith_tri=True))]
out = []
print('DT=%.1e TEND=%.0f  真值 b=%.2f  period=5 s' % (DT, TEND, B_TRUE))
for name, flags in CASES:
    cfg = dict(BASE); cfg.update(flags)
    Y = sim_inv(t, TL, cfg)
    b = np.asarray(Y['b0e']); nb = len(b)
    tb = np.linspace(0.0, TEND, nb)
    rel = np.abs(b - B_TRUE) / B_TRUE
    t3 = next((float(tb[i]) for i in range(nb) if rel[i] <= 0.03 and np.max(rel[i:]) <= 0.05), float('nan'))
    t1 = next((float(tb[i]) for i in range(nb) if rel[i] <= 0.01 and np.max(rel[i:]) <= 0.02), float('nan'))
    d = dict(name=name, t=tb.tolist(), b0=b.tolist(), b_true=float(B_TRUE),
             final=float(b[-1]), err=float(100 * (b[-1] / B_TRUE - 1)),
             t3=t3, t1=t1, n=int(len(np.asarray(Y['jnew']))))
    out.append(d)
    print('%-3s 终值 %.3f  误差 %+.3f%%  3%% %s  1%% %s  辨识窗数 %d'
          % (name, d['final'], d['err'], ('%.1f s' % t3) if t3 == t3 else '未达',
             ('%.1f s' % t1) if t1 == t1 else '未达', d['n']))
json.dump(out, open('_b0_curve_py.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('saved _b0_curve_py.json')
