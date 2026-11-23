# -*- coding: utf-8 -*-
"""_run_cases4.py — 四工况对照（无自适应律，与 s8 同配置）。
用法: python _run_cases4.py <ctrl|load|b0|tm>
"""
import numpy as np, sys, time
import noise_cfg as NC
from pmsm_inv_sim import sim_inv

case = sys.argv[1]
DT = 2e-6; TEND = 8.0
FAULT = dict(start=2.0,
             unbalance=dict(M=0.1, e=1e-4, kappa=580.0),
             misalign=dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0),
             parallel=dict(e=1e-4, dk=1.0e5, kappa=100.0))
t = np.arange(0.0, TEND, DT)
TL_RATED = 0.637
cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3,
           fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
           rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
           tl_fault=FAULT)

if case == "ctrl":          # 对照组：恒载 0.5 额定、恒 600、J=J_nom
    TL = 0.5 * TL_RATED * np.ones_like(t)
elif case == "load":        # 负载突变：2 s 0 -> 0.5 额定
    TL = (0.5 * (t >= 2.0)).astype(float) * TL_RATED
elif case == "b0":          # b0 严重失配：J=5.26 J_nom（b0 真值 122.3 vs 标称 643.7）
    TL = (0.5 * (t >= 2.0)).astype(float) * TL_RATED
    cfg.update(J_true=9.95e-5)
elif case == "b0p":        # 纯 b0 失配：对象不变（J=J_nom），控制器 b0 估大 5.26 倍
    TL = 0.5 * TL_RATED * np.ones_like(t)
    cfg.update(b0_scale=5.26)
elif case in ("td", "td05", "td10"):   # T 漂移（相对理论最优 −14.3% 的偏移）
    TL = 0.5 * TL_RATED * np.ones_like(t)
    off = {"td": 0.02, "td05": 0.05, "td10": 0.10}[case]
    cfg.update(T_es=True, es_d0=-0.143 + off, es_step=0.0, es_dith=0.0)
elif case in ("b0pd", "b0s2", "b0s3"):   # 纯 b0 失配（δ=δ*）
    TL = 0.5 * TL_RATED * np.ones_like(t)
    sc = {"b0pd": 5.26, "b0s2": 2.0, "b0s3": 3.0}[case]
    cfg.update(T_es=True, es_d0=-0.143, es_step=0.0, es_dith=0.0, b0_scale=sc)
elif case == "td15":       # T 漂移 15%（δ=+0.007，近似补偿丢失）
    TL = 0.5 * TL_RATED * np.ones_like(t)
    cfg.update(T_es=True, es_d0=0.007, es_step=0.0, es_dith=0.0)
elif case == "ctrld":       # T 准确（δ=δ*）的对照组
    TL = 0.5 * TL_RATED * np.ones_like(t)
    cfg.update(T_es=True, es_d0=-0.143, es_step=0.0, es_dith=0.0)
elif case == "loadd":       # 负载突变（δ=δ*）
    TL = (0.5 * (t >= 2.0)).astype(float) * TL_RATED
    cfg.update(T_es=True, es_d0=-0.143, es_step=0.0, es_dith=0.0)
elif case == "b0c":        # b0 严重失配（恒载，不引入负载突变）
    TL = 0.5 * TL_RATED * np.ones_like(t)
    cfg.update(J_true=9.95e-5)
elif case == "tmc":         # T 失配（恒载，6 s 换速）
    TL = 0.5 * TL_RATED * np.ones_like(t)
    cfg.update(n_ref2=300.0, t_nref=6.0)
elif case == "tm":          # T 失配：6 s 换速 600->300
    TL = (0.5 * (t >= 2.0)).astype(float) * TL_RATED
    cfg.update(n_ref2=300.0, t_nref=6.0)
else:
    raise SystemExit("unknown case")

t0 = time.time()
Y = sim_inv(t, TL, cfg)
el = time.time() - t0
np.savez("_c4_%s.npz" % case, t=Y["t"], y=Y["y"], iq=Y["iq"], tl=Y["tl"])
print("%-5s done (%.0fs)" % (case, el), flush=True)
