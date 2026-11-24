# -*- coding: utf-8 -*-
"""run_tj_cont.py —— 9 s 快跑版：律T 连续滑动窗 ESC + 律J α=1（一步到位）+ b0 低通带宽 kp/10 + 校验关。

用法: python run_tj_cont.py <tag> <mode> [TEND] [cont] [tau_div]
  mode    : base | t | j | fusion
  TEND    : 仿真时长 / s（默认 9）
  cont    : 1 = 连续滑动窗解调（δ̂ 每 1 ms 更新，默认）；0 = 事件式 hold（对照）
  tau_div : b0 低通带宽 = kp/tau_div（默认 10，即 τ = 10/kp ≈ 0.133 s）
  period  : 律J burst 周期 / s（默认 10；9 s 内只跑 1 次，设 5 则 2 次）

场景：600 rpm、组合故障（2 s 起）、2 s 加载 0.50 额定、J_true=9.95e-5=5.26 J_nom。
"""
import numpy as np, json, sys, time, os
import noise_cfg as NC
from pmsm_inv_sim import sim_inv

D0 = float(os.environ.get("ES_D0", -0.143))      # 律T 初始 δ̂
ESTEP = float(os.environ.get("ES_STEP", 0.01))   # 律T 步长 σ（0 = 冻结 δ̂，做定点扫描）
RCSRC = os.environ.get("RC_SRC", "e1")           # 律T 幅值来源：e1（ESO 新息）或 et（跟踪误差）
DLAW = os.environ.get("DLAW", "0") == "1"         # 律D：瞬态抬 kp 与 ESO 带宽
ESPD = float(os.environ.get("ES_PD", 1.5))       # 律T 抖动周期 P_d / s（f_d = 1/P_d）
ESN = int(os.environ.get("ES_N", 3))             # 每步抖动周期数 N（窗长 = N·P_d）

tag = sys.argv[1]; mode = sys.argv[2]
TEND = float(sys.argv[3]) if len(sys.argv) > 3 else 9.0
CONT = (len(sys.argv) <= 4) or (sys.argv[4] == "1")
TAU_DIV = float(sys.argv[5]) if len(sys.argv) > 5 else 10.0

KP = 75.36                       # 速度环比例增益（与 pmsm_inv_sim.py 默认 kp 一致）
_B3 = float(os.environ.get("B3", "4000.0"))    # 内模注入增益（线性化 = B3/ZETA）
_ZE = float(os.environ.get("ZETA", "0.2"))     # 注入 tanh 线性区宽度
_LAM = float(os.environ.get("ESOLAM", "10.0"))  # 类fal 拐点位置：越小越线性（斜率不变）
BTAU = TAU_DIV / KP              # 带宽 = kp/tau_div  ⇒  τ = tau_div/kp
PERIOD = float(sys.argv[6]) if len(sys.argv) > 6 else 10.0   # burst 周期 / s
T0 = float(os.environ.get("T0J", "1.0"))   # 律J 首个 burst 时刻 / s
SS = 3.0                         # 稳态窗 = 末 3 s
DT = 2e-6

FAULT = dict(start=2.0,
             unbalance=dict(M=0.1, e=1e-4, kappa=580.0),
             misalign=dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0),
             parallel=dict(e=1e-4, dk=1.0e5, kappa=100.0))
t = np.arange(0.0, TEND, DT)
TL = (0.50 * (t >= 2.0)).astype(float) * 0.637

cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=_B3, zeta_inj=_ZE,
           Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
           sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=_LAM,
           b0_scale=float(os.environ.get("B0SCALE", "1.0")),
           rc_bp=5.0, b3_min=_B3, b3_max=_B3,
           tl_fault=FAULT, J_true=9.95e-5)

use_t = mode in ("t", "fusion")
use_j = mode in ("j", "fusion")
if DLAW:
    cfg.update(kp_boost=6.0, det_eps=0.01, kb_eso=3.0, kb_b3=0.0)
if use_j:
    cfg.update(j_amed_d2=float(os.environ.get("AMED_D2", "0.08")),
               j_amed_dmax=float(os.environ.get("AMED_DMAX", "0.30")),
               j_amed_d1=float(os.environ.get("AMED_D1", "0.10")),
               j_amed_warm=int(os.environ.get("AMED_WARM", "3")),
               j_amed_abase=float(os.environ.get("AMED_AB", "0.30")))

if use_t:
    cfg.update(T_es=True, es_d0=D0, es_step=ESTEP, es_dith=0.005, es_Pd=ESPD, es_N=ESN,
               es_dead=2e-6, es_dmax=0.20, es_t0=3.0, T_dft=2.0, a_ref=0.2,
               es_cont=CONT, es_nofreeze=True, rc_src=RCSRC)
else:
    cfg.update(T_es=False, a_ref=1.0)

if use_j:
    cfg.update(j_recheck=True, j_recheck_period=PERIOD,
               j_recheck_len=float(os.environ.get("DLEN", "0.6")),
               j_recheck_amp=float(os.environ.get("AMP", "0.157")),
               j_recheck_nmin=2, j_recheck_t0=T0, j_recheck_f_auto=True, j_recheck_f_q=6.0,
               j_recheck_f_alpha=0.35, j_recheck_f_min=50.0, j_recheck_f_max=110.0,
               j_recheck_amp_auto=True, j_recheck_gate=True, j_recheck_gate_ac=10.0,
               j_recheck_gate_step=10.0, j_recheck_alpha=1.0,
               j_recheck_apply=(os.environ.get("APPLY", "1") == "1"),
               j_recheck_btau=BTAU, j_b0_direct=True, j_validate=False,
               j_amed=(os.environ.get("AMED", "1") == "1"),
               j_b0_onoff=(os.environ.get("ONOFF", "0") == "1"),
               j_dith_sq=(os.environ.get("SQ", "0") == "1"),
               j_dith_tri=(os.environ.get("TRI", "0") == "1"),
               j_b0_batch=(os.environ.get("BATCH", "0") == "1"),
               j_period_switch_t=float(os.environ.get("PTSW", "1e9")),
               j_period_after=float(os.environ.get("PAFT", "0")),
               j_batch_n=int(os.environ.get("BN", "12")),
               j_batch_mad=float(os.environ.get("BMAD", "0.15")),
               j_b0_new=(os.environ.get("JB0NEW", "0") == "1"),
               j_b0_alg=(os.environ.get("JB0ALG", "0") == "1"),
               j_b0_alt=(os.environ.get("JB0ALT", "0") == "1"),
               j_b0_tcorr=(os.environ.get("TCORR", "0") == "1"),
               j_b0_final=(os.environ.get("B0FINAL", "0") == "1"),
               j_b0_lo=float(os.environ.get("B0LO", "10")),
               j_b0_hi=float(os.environ.get("B0HI", "5000")))

t0 = time.time()
Y = sim_inv(t, TL, cfg)
el = time.time() - t0
tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
es = np.asarray(Y["es"]); jh = np.asarray(Y["jhat"]); b0 = np.asarray(Y["b0e"])
np.savez("_tjc_%s.npz" % tag, t=tt, y=y, iq=iq, tl=np.asarray(Y["tl"]), b0e=b0,
         amp=np.asarray(Y["amp"]), es=es, jhat=jh, t_j=np.asarray(Y["t_j"]),
         jnew=np.asarray(Y["jnew"]))

e = (y - 1.0) * 600.0
m = tt >= (TEND - SS)
rms = float(np.sqrt(np.mean(e[m] ** 2)))
w = m & (tt < TEND + 1e-12)
x = e[w] - e[w].mean()
X = np.fft.rfft(x * np.hanning(len(x)))
fr = np.fft.rfftfreq(len(x), d=float(tt[1] - tt[0]))
k10 = int(np.argmin(np.abs(fr - 10.0)))
a10 = float(2.0 * np.abs(X[k10]) / np.sum(np.hanning(len(x))))

n1 = int(round(1e-3 / (tt[1] - tt[0])))
iq1 = np.abs(iq[:len(iq)//n1*n1].reshape(-1, n1).mean(axis=1))
t1 = tt[:len(iq1)*n1:n1]
miq = t1 >= 2.0
iq1ms = float(iq1[miq].max())
iq_raw = float(np.abs(iq[tt >= 2.0]).max())

d = dict(tag=tag, mode=mode, TEND=TEND, cont=int(CONT), tau_div=TAU_DIV, btau=BTAU,
         J_true=9.95e-5, period=PERIOD, t0=T0, b0d=True, valid=0, alpha=1.0,
         b0e=float(b0[-1]), b0_err_pct=float(100.0 * (b0[-1] / 122.3 - 1.0)),
         jfin=float(jh[-1]) if jh.size else 0.0,
         es_end=float(es[-1] if es.size else 0.0),
         es_mean=float(np.mean(es[m])) if es.size else 0.0,
         rms=rms, amp10=a10, iq1ms=iq1ms, iq_raw=iq_raw, runtime_s=el)
json.dump(d, open("_tjc_%s.json" % tag, "w"), indent=1)
print("%-8s T=%d J=%d cont=%d | RMS %6.2f  10Hz %6.2f  iq1ms %5.2f  b0e %6.1f (%+5.1f%%)  es %7.4f  (%.0fs)" % (
    tag, use_t, use_j, CONT, rms, a10, iq1ms, d["b0e"], d["b0_err_pct"], d["es_mean"], el), flush=True)
