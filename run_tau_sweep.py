# -*- coding: utf-8 -*-
"""run_tau_sweep.py —— 低通时间常数 tau 的取舍：tau↓ 时按理论值重调周期 delta

口径：600 rpm、8 s、2 s 加载 0.50 额定 + 圆盘 V2 + 5.9 Hz、实验室噪声、
fci=500 Hz、beta3=4000、Q=0.98、类 fal ESO、种子 20261018、T_adapt 开。
每档取 delta = -arctan(2*pi*10*tau)/(2*pi)（相位对齐的理论值）。
输出：_tau_sweep.json
"""
import math
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from run_laws_compare import build_loads, N_REF, AMP, ANG_START, TW
from tl_profile import disc_unbalance_profile

TAUS = [0.020, 0.010, 0.005, 0.002, 0.0005]


def one(tau):
    from pmsm_inv_sim import sim_inv
    t, TL = build_loads()
    d0 = -math.atan(2.0 * math.pi * 10.0 * tau) / (2.0 * math.pi)
    cfg = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=tau, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
               tl_ang_start=ANG_START, tl_ang_rev=29.9,
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               T_es=True, es_d0=d0, es_step=0.0, es_dith=0.0)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * N_REF
    m = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(e[m]))
    step_rms = float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2)))
    ms = (tt >= 7.0) & (tt < 8.0)
    ts = tt[ms]; es = e[ms]
    a = 2.0 * np.mean(es * np.sin(2 * np.pi * 10.0 * ts))
    b = 2.0 * np.mean(es * np.cos(2 * np.pi * 10.0 * ts))
    fund = float(np.hypot(a, b))
    rms = float(np.sqrt(np.mean(es ** 2)))
    iqm = float(np.max(np.abs(iq)))
    print("tau=%.4f d0=%+.3f dip %7.1f stepRMS %5.1f steady %5.2f fund %5.2f iq %5.2f"
          % (tau, d0, dip, step_rms, rms, fund, iqm), flush=True)
    return dict(tau=tau, d0=d0, dip=dip, step_rms=step_rms, steady=rms, fund=fund, iq_max=iqm)


if __name__ == "__main__":
    import json
    with Pool(5) as p:
        res = p.map(one, TAUS)
    json.dump(res, open("_tau_sweep.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("done")
