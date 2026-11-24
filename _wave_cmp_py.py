# -*- coding: utf-8 -*-
"""_wave_cmp_py.py —— 三波（正弦/方波/三角）对比：注入 / 电流 / 转速（带噪声，稳态工况）
用法: python _wave_cmp_py.py [DT] [TEND] [T0]
工况：600 rpm 稳态、恒定负载 0.3 N·m、无故障激励（隔离波形本身的影响）
"""
import sys, json
import numpy as np
import noise_cfg as NC
from pmsm_inv_sim import sim_inv

DT = float(sys.argv[1]) if len(sys.argv) > 1 else 2e-5
TEND = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
T0 = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
t = np.arange(0.0, TEND, DT)
TL = np.full_like(t, 0.30)          # 恒定 0.3 N·m（约 47% 额定）

BASE = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=4000.0,
            Q0=0.98, tau0=20e-3, seed_i=20261018,
            i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
            sig_n=NC.NOISE_LAB["sig_n_rpm"],
            sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
            eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
            rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, J_true=9.95e-5,
            a_ref=1.0, log_eso=True,
            j_recheck=True, j_recheck_period=9999.0, j_recheck_len=0.4,
            j_recheck_amp=0.118, j_recheck_amp_auto=False,
            j_recheck_nmin=2, j_recheck_t0=T0, j_recheck_f=65.0, j_recheck_f_auto=False,
            j_recheck_gate=False, j_recheck_apply=False,
            j_recheck_alpha=1.0, j_recheck_btau=50.0/75.36,
            j_b0_direct=True, j_validate=False, j_b0_new=True, j_b0_onoff=True)

CASES = [('正弦', {}), ('方波', dict(j_dith_sq=True)), ('三角', dict(j_dith_tri=True))]
out = []
print('DT=%.1e TEND=%.1f T0=%.1f  TL=0.30 N·m  噪声 i_peak=%.2fA sig_n=%.1frpm sig_T=%.3fNm'
      % (DT, TEND, T0, NC.NOISE_LAB['i_noise_peak'], NC.NOISE_LAB['sig_n_rpm'], NC.NOISE_LAB['sig_T_nm']))
for name, flags in CASES:
    cfg = dict(BASE); cfg.update(flags)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y['t']); inj = np.asarray(Y['inj']); iq = np.asarray(Y['iq'])
    w = np.asarray(Y['y']) * 600.0
    m = (tt >= T0 - 0.1) & (tt <= T0 + 0.65)
    on = (tt >= T0 + 0.2) & (tt < T0 + 0.4)
    pre = (tt >= T0 - 0.2) & (tt < T0)
    ph = np.exp(-1j * 2 * np.pi * 65.0 * tt[on])
    def amp(x, msk):
        return 2.0 / max(msk.sum(), 1) * abs(np.sum(x[msk] * ph if msk is on else x[msk] * np.exp(-1j*2*np.pi*65.0*tt[msk])))
    d = dict(name=name, t=tt[m].tolist(), inj=inj[m].tolist(), iq=iq[m].tolist(),
             w=w[m].tolist(), t0=T0,
             inj_amp=float(amp(inj, on)), iq_amp=float(amp(iq, on)), w_amp=float(amp(w, on)),
             iq_amp_pre=float(amp(iq, pre)), w_amp_pre=float(amp(w, pre)),
             w_pp=float(w[on].max() - w[on].min()), w_pp_pre=float(w[pre].max() - w[pre].min()),
             iq_pk=float(np.abs(iq[on]).max()))
    out.append(d)
    print('%-3s 注入 %.4f pu | iq 基波 %.3f A（注入前 %.3f）峰值 %.3f A | 转速基波 %.1f rpm（注入前 %.1f）峰峰 %.1f（前 %.1f）'
          % (name, d['inj_amp'], d['iq_amp'], d['iq_amp_pre'], d['iq_pk'], d['w_amp'], d['w_amp_pre'], d['w_pp'], d['w_pp_pre']))
json.dump(out, open('_wave_cmp_py.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('saved _wave_cmp_py.json')
