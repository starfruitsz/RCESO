# -*- coding: utf-8 -*-
"""run_lawd_cmp_600.py —— 600 rpm 实验室：律 D（带宽自适应）对加载的改善

场景与 run_lawd_new.py 一致（TEND=8 s、2 s 加载 0.5 额定、圆盘型线 V2 + 5.9 Hz 振动、
实验室噪声、fci=500 Hz、类 fal ESO、种子 20261018）。
两档：Base（无自适应）与 律D 新（kp_boost=6、kb_eso=3、kb_b3=0、det_eps=0.01）。
输出：_wave_lawd_cmp_600.npz（t、y_base、y_lawd、iq_base、iq_lawd、tl）
指标：跌落、恢复到 ±20 rpm 的时间、突变窗 RMS [2.0,2.5)、max|iq|、稳态 [7,8) RMS
"""
import numpy as np

import noise_cfg as NC
from run_laws_compare import build_loads, N_REF, AMP, ANG_START, TW
from pmsm_inv_sim import sim_inv
from tl_profile import disc_unbalance_profile

CASES = [("base", dict(det_eps=0.0)),
         ("lawd", dict(kp_boost=6.0, det_eps=0.01, kb_eso=3.0, kb_b3=0.0))]


def metrics(tt, y, iq):
    e = (np.asarray(y) - 1.0) * N_REF
    m_dip = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(e[m_dip]))
    i_dip = int(np.where(m_dip)[0][int(np.argmin(e[m_dip]))])
    ok = (np.abs(e) <= 20.0) & (np.arange(len(e)) > i_dip) & (tt >= 2.0)
    rec = None
    idx = np.where(ok)[0]
    if len(idx):
        rec = float(tt[idx[0]] - 2.0) * 1e3
    step_rms = float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2)))
    steady = float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2)))
    return dict(dip=dip, rec_ms=rec, step_rms=step_rms, iq_max=float(np.max(np.abs(iq))),
                steady=steady)


if __name__ == "__main__":
    t, TL = build_loads()
    out = {}
    for key, kw in CASES:
        cfg = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
                   rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
                   fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3,
                   seed_i=20261018,
                   i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
                   sig_n=NC.NOISE_LAB["sig_n_rpm"],
                   sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
                   tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
                   tl_ang_start=ANG_START, tl_ang_rev=29.9,
                   eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
        cfg.update(kw)
        Y = sim_inv(t, TL, cfg)
        tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
        mt = metrics(tt, y, iq)
        print("%-4s 跌落 %7.1f rpm  恢复 %5.1f ms  突变RMS %5.1f  稳态 %5.2f  iqmax %5.2f"
              % (key, mt["dip"], mt["rec_ms"], mt["step_rms"], mt["steady"], mt["iq_max"]), flush=True)
        out["y_" + key] = y; out["iq_" + key] = iq
        out.setdefault("tl", np.asarray(Y["tl"]))
    np.savez("_wave_lawd_cmp_600.npz", t=tt, **out)
    print("saved _wave_lawd_cmp_600.npz")
