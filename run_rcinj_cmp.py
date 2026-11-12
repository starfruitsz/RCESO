# -*- coding: utf-8 -*-
"""run_rcinj_cmp.py —— 重复通道注入非线性：tanh vs 类 fal

工况：600 rpm、8 s、2 s 加载 0.50 额定 + 圆盘 V2 + 5.9 Hz、实验室噪声、
fci=500 Hz、Q=0.98、tau=20 ms、类 fal ESO、种子 20261018。
四档：tanh(β3=4000) / fal(β3=4000) / fal(β3=11247，小信号增益匹配) / fal+无低通。
"""
import math
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from run_laws_compare import build_loads, N_REF, AMP, ANG_START, TW
from tl_profile import disc_unbalance_profile

CASES = [
    ("tanh", dict(rc_inj="tanh", beta3=4000.0, tau0=20e-3)),
    ("fal", dict(rc_inj="fal", beta3=4000.0, tau0=20e-3)),
    ("fal_b3m", dict(rc_inj="fal", beta3=11247.0, tau0=20e-3)),
    ("fal_nolpf", dict(rc_inj="fal", beta3=4000.0, tau0=0.0)),
]


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kw = job
    t, TL = build_loads()
    cfg = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
               tl_ang_start=ANG_START, tl_ang_rev=TW,
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * N_REF
    fin = bool(np.all(np.isfinite(y)) and np.all(np.isfinite(iq)))
    m = (tt >= 1.9) & (tt <= 2.5)
    ms = tt >= 7.0
    print("%-9s dip %10.1f  stepRMS %9.1f  steady %9.1f  iq %9.2f  max|spd| %10.1f  finite=%s"
          % (key, float(np.min(e[m])), float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))),
             float(np.sqrt(np.mean(e[ms] ** 2))), float(np.nanmax(np.abs(iq))),
             float(np.nanmax(np.abs(y)) * N_REF), fin), flush=True)
    np.savez("_wave_rcinj_%s.npz" % key, t=tt, y=y, iq=iq)
    return key


if __name__ == "__main__":
    with Pool(4) as p:
        p.map(one, CASES)
    print("done")
