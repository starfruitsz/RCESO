# -*- coding: utf-8 -*-
"""_probe_im_ident.py —— RCESO 内模传递函数核验 + 反演自标定（2026-11-18）

环境变量：FD（不设=自动选频≈65Hz；设则强制该频率，用于撞频试验）
          TAG / TEND / T0B
核验：
  1) V/X == beta3_code/D(jw)，X = tanh(e1/zeta)   -> 反解 T
  2) d^ = V + P(jw)E1/(jw) == delta_b * U         -> 反解 b0
场景：三合一故障 t>=2 s；律J 单次 burst 在 T0B（故障已生效）；
      j_recheck_apply=False => burst 内 b0 冻结，delta_b 已知恒定。
"""
import numpy as np, math, os, json
import noise_cfg as NC
from pmsm_inv_sim import sim_inv, J_M, I_BASE, W_REF

DT = 2e-6
TEND = float(os.environ.get("TEND", "8.0"))
T0B = float(os.environ.get("T0B", "3.0"))
BLEN = 0.6
FD = os.environ.get("FD", "")
TAG = os.environ.get("TAG", "auto" if not FD else FD)
FAULT = dict(start=2.0,
             unbalance=dict(M=0.1, e=1e-4, kappa=580.0),
             misalign=dict(M=0.1, beta=0.01745, l=0.05, kappa=67.0),
             parallel=dict(e=1e-4, dk=1.0e5, kappa=100.0))
t = np.arange(0.0, TEND, DT)
TL = (0.50 * (t >= 2.0)).astype(float) * 0.637
cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0, beta3=4000.0,
           Q0=0.98, tau0=20e-3, seed_i=20261018,
           i_noise_peak=NC.NOISE_LAB["i_noise_peak"], sig_n=NC.NOISE_LAB["sig_n_rpm"],
           sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
           eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
           rc_bp=5.0, b3_min=4000.0, b3_max=4000.0,
           tl_fault=FAULT, J_true=9.95e-5, a_ref=1.0, log_eso=True,
           j_recheck=True, j_recheck_period=9999.0, j_recheck_len=BLEN,
           j_recheck_amp=0.157, j_recheck_nmin=2, j_recheck_t0=T0B,
           j_recheck_f_auto=(FD == ""), j_recheck_f=float(FD) if FD else 100.0,
           j_recheck_f_q=6.0, j_recheck_f_alpha=0.35,
           j_recheck_f_min=50.0, j_recheck_f_max=110.0, j_recheck_amp_auto=True,
           j_recheck_gate=False, j_recheck_apply=False, j_recheck_alpha=1.0,
           j_recheck_btau=0.0, j_b0_direct=True, j_validate=False)
Y = sim_inv(t, TL, cfg)
lg = np.asarray(Y["lg"])
np.savez("_probe_im_%s.npz" % TAG, lg=lg, fd=np.asarray(Y["fd"]), b0e=np.asarray(Y["b0e"]))

tk, e1, v, z2, u, B0e, woe = (lg[:, i] for i in range(7))
fd = float(Y["fd"][-1][1]); w = 2 * math.pi * fd
zeta = 0.2; kap = 0.10 ** (0.75 - 1.0)
b1 = 2.0 * 500.0 * 1.0
b2 = 500.0 ** 2 * kap
Q, tau = 0.98, 0.020
b3c = 4000.0                 # 以 X=tanh(e1/zeta) 为输入时的实际增益
b3l = b3c / zeta             # 以 e1 为输入时的线性化增益 = 20000
B0 = 1.2 * 0.101 * I_BASE / (J_M * W_REF)
b_true = B0 * J_M / 9.95e-5
dB = b_true - B0e[-1]
print("\n############  TAG=%s   fd=%.2f Hz  b_true=%.2f  B0e=%.2f  delta_b=%+.2f  ############"
      % (TAG, fd, b_true, B0e[-1], dB))

def Pj(ww): return complex(b2 - ww * ww, b1 * ww)
def Dj(ww, T): return 1.0 + tau * 1j * ww - Q * np.exp(-1j * ww * T)
def amp(xx, ph):
    n = len(xx)
    return (2.0 / n) * (np.sum(xx * np.cos(ph)) - 1j * np.sum(xx * np.sin(ph)))

x = np.tanh(e1 / zeta)
res = []
for i in range(3):
    ta = T0B + 0.2 * i + 0.02; tb = T0B + 0.2 * (i + 1)
    m = (tk >= ta) & (tk < tb); ph = w * tk[m]
    X, V, E, U = (amp(a[m], ph) for a in (x, v, e1, u))
    R = V / X
    Ts = np.linspace(0.070, 0.140, 14001)
    Th = Ts[int(np.argmin([abs(R - b3c / Dj(w, Tt)) for Tt in Ts]))]
    dA = V + Pj(w) / (1j * w) * E
    dP = Pj(w) / (1j * w) * E
    dF = E * (b3l / Dj(w, 0.100)) + dP
    est = lambda dd: (dd / U).real
    res.append((est(dA), est(dP), est(dF), Th, abs(U)))
    print("--- 窗%d [%.2f,%.2f)  X=%6.3f@%+7.1f  |U|=%6.3f  V/X=%7.1f@%+7.1f 理论%7.1f@%+7.1f"
          % (i + 1, ta, tb, abs(X), math.degrees(np.angle(X)), abs(U),
             abs(R), math.degrees(np.angle(R)),
             abs(b3c / Dj(w, .1)), math.degrees(np.angle(b3c / Dj(w, .1)))))
    print("      T_hat=%.4f s (%+.1f%%)   db: 自标定 %+8.2f (%+6.2f%%) | 无内模 %+8.2f (%+6.2f%%) | 解析G %+8.2f (%+6.2f%%)"
          % (Th, 100 * (Th / .1 - 1), est(dA), 100 * (est(dA) / dB - 1),
             est(dP), 100 * (est(dP) / dB - 1), est(dF), 100 * (est(dF) / dB - 1)))
a = np.array([r[:1] + r[1:2] + r[2:3] for r in res])
print("== 三窗均值：自标定 %+8.2f (%+6.2f%%) | 无内模 %+8.2f (%+6.2f%%) | 解析G %+8.2f (%+6.2f%%) | T_hat=%.4f"
      % (a[:, 0].mean(), 100 * (a[:, 0].mean() / dB - 1), a[:, 1].mean(), 100 * (a[:, 1].mean() / dB - 1),
         a[:, 2].mean(), 100 * (a[:, 2].mean() / dB - 1), np.mean([r[3] for r in res])))
json.dump(dict(tag=TAG, fd=fd, b_true=b_true, B0e=float(B0e[-1]), dB=dB,
               dA=[float(v) for v in a[:, 0]], dP=[float(v) for v in a[:, 1]],
               dF=[float(v) for v in a[:, 2]], That=[float(r[3]) for r in res]),
          open("_probe_im_%s.json" % TAG, "w"), indent=1)
