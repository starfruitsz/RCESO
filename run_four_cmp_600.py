# -*- coding: utf-8 -*-
"""run_four_cmp_600.py —— 600 rpm 实验室：四档对比（无自适应 / T / 律D / T+律D）

突变工况 = 负载突变 + 参考转速突变：
  t=2 s  负载 0 → 0.50 额定（并投入圆盘型线 V2 + 5.9 Hz 振动）
  t=15 s 参考转速 600 → 900 rpm
30 s、实验室噪声、fci=500 Hz、β₃=4000、τ₀=20 ms、类 fal ESO、种子 20261018。
T 自适应：δ0=-14.3%、Δ=0.5%、σ=1%、Pd=1.5 s、N=3、t0=3 s、es_ff 前馈重置（换速）；
律 D：kp_boost=8、kb_eso=2（ω_o×3）、kb_b3=0、det_eps=0.01。
输出：_wave_4cmp2_600_<key>.npz
"""
import math
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from tl_profile import disc_unbalance_profile

DT, TEND, TL0, TNREF = 2e-6, 30.0, 2.0, 15.0
N_REF, N_REF2, AMP = 600.0, 900.0, 0.095
F_VIB, VIB1 = 5.9, 0.03
VIB_H = (1.0, 0.2654, 0.0408, 0.2245, 0.0612, 0.1837)

ESC = dict(T_es=True, es_d0=-0.143, es_step=0.01, es_dith=0.005, es_ff=True)
NOESC = dict(T_es=True, es_d0=0.0, es_step=0.0, es_dith=0.0)
LAWD = dict(kp_boost=6.0, kb_eso=3.0, kb_b3=0.0, det_eps=0.01)
CASES = [("base", dict(NOESC)),
         ("T", dict(ESC)),
         ("D", dict(NOESC, **LAWD)),
         ("DT", dict(ESC, **LAWD))]


def build():
    t = np.arange(0.0, TEND, DT)
    vib = np.zeros_like(t)
    for n, a in enumerate(VIB_H, start=1):
        vib += a * np.sin(2.0 * math.pi * F_VIB * n * (t - TL0) * (t >= TL0))
    TL = (0.50 * (t >= TL0)).astype(float) * 0.637 + VIB1 * vib
    return t, TL


def metrics(tt, y, iq, amp):
    spd = np.asarray(y) * N_REF                       # rpm（y 以 600 rpm 归一）
    m = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(spd[m] - N_REF))
    i0 = int(np.where(m)[0][int(np.argmin(spd[m] - N_REF))])
    idx = np.where((np.abs(spd - N_REF) <= 20.0) & (np.arange(len(spd)) > i0) & (tt >= 2.0))[0]
    rec = float(tt[idx[0]] - 2.0) * 1e3 if len(idx) else float("nan")
    m2 = tt >= TNREF
    idx2 = np.where((np.abs(spd - N_REF2) <= 20.0) & m2)[0]
    tset = float(tt[idx2[0]] - TNREF) * 1e3 if len(idx2) else float("nan")
    over = float(np.max(spd[(tt >= TNREF) & (tt <= TNREF + 5.0)] - N_REF2))
    step_rms = float(np.sqrt(np.mean((spd[(tt >= 2.0) & (tt < 2.5)] - N_REF) ** 2)))
    steady = float(np.sqrt(np.mean((spd[(tt >= 25.0)] - N_REF2) ** 2)))
    A = float(np.mean(np.asarray(amp)[tt >= 25.0])) * N_REF   # 基波残余，rpm
    return dict(dip=dip, rec_ms=rec, tset_ms=tset, overshoot=over,
                step_rms=step_rms, steady=steady, amp_res=A,
                iq_max=float(np.max(np.abs(iq))))


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kw = job
    t, TL = build()
    cfg = dict(n_ref=N_REF, n_ref2=N_REF2, t_nref=TNREF,
               T=0.1, T_adapt=True, T_filt=50e-3,
               fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
               tl_ang_start=2.01868, tl_ang_rev=29.9,
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
               es_Pd=1.5, es_N=3, es_dead=1e-5, es_dmax=0.20, es_t0=3.0)
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    amp = np.asarray(Y["amp"]); es = np.asarray(Y["es"])
    mt = metrics(tt, y, iq, amp)
    print("%-4s 跌落 %7.1f  恢复 %5.1f  换速调节 %6.1f ms  超调 %5.1f  突变RMS %5.1f  "
          "基波 %5.2f  稳态 %5.2f  iq %5.2f"
          % (key, mt["dip"], mt["rec_ms"], mt["tset_ms"], mt["overshoot"],
             mt["step_rms"], mt["amp_res"], mt["steady"], mt["iq_max"]), flush=True)
    np.savez("_wave_4cmp2_600_%s.npz" % key, t=tt, y=y, iq=iq, amp=amp, es=es)
    return key


if __name__ == "__main__":
    with Pool(4) as p:
        p.map(one, CASES)
    print("done")
