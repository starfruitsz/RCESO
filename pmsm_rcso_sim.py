# -*- coding: utf-8 -*-
"""
PMSM 转速环 + 不对中周期负载转矩（含电流环与电流/负载噪声）
================================================================================
对象侧（本版新增）：
  电流环  : 一阶闭环等效 i_a ← 指令 u，闭环带宽 f_ci（本版主配置 1 kHz，tau_ci = 159.2 us；5 kHz 档仅见于敏感性扫描）
            物理依据：相回路 L/R = 0.57 mH / 0.175 Ω = 3.26 ms；DM807 速度环采样 125 us(8 kHz)，
            数字 PI 电流环按 1/5~1/10 采样率取带宽，5 kHz 取"快环"一档（敏感性见随附扫描）。
  电流噪声: 反馈侧带限白噪声 n_i（sigma_i = 1% 额定电流 = 0.063 A，带宽 2 kHz），
            经同一低通进入实际电流（对应 ADC/传感器噪声 + PWM 纹波折算）。
  负载噪声: 负载转矩带限白噪声 n_T（sigma_T = 5% 额定转矩 = 0.0319 N·m，带宽 200 Hz）。
  随机种子固定 20261016 / 20261017，结果可复现。
标幺口径 : y = w/600rpm，u = iq/I_base (I_base = T_rated/kt = 6.3069 A)，y_dot = b*i_a + d + d_n
控制器   : 与 §3 定稿逐项同参（一项不改）
"""
import math, time
import numpy as np
from adrc_eso_closed import adrc_sim

KT, J_M, T_RATED, I_RATED, N_RATED, I_PEAK = 0.101, 1.89e-5, 0.637, 6.5, 3000.0, 21.0
R_LINE, L_LINE = 0.35, 1.14e-3
R_PHASE, L_PHASE = R_LINE / 2.0, L_LINE / 2.0
TAU_E = L_PHASE / R_PHASE
N_OP = 600.0
W_REF = N_OP * math.pi / 30.0
I_BASE = T_RATED / KT
B_GAIN = KT * I_BASE / (J_M * W_REF)
B0_GAIN = 1.2 * B_GAIN
TAU_S = J_M * W_REF / T_RATED

F_CI_DEF = 1000.0                      # 主配置电流环闭环带宽 (Hz) —— 现实数字 PI 电流环档
TAU_CI_DEF = 1.0 / (2.0 * math.pi * F_CI_DEF)
SIG_I, F_NI = 0.01, 2000.0             # 电流反馈噪声
SIG_T, F_NT = 0.05, 200.0              # 负载转矩噪声
SEED_I, SEED_T = 20261016, 20261017

T, DT, TEND, T_LOAD = 0.1, 1e-5, 12.0, 2.0     # 0-2 s 空载，2 s 起加载
t = np.arange(0.0, TEND, DT); n = len(t)

def band_noise(sigma, f_c, seed):
    rng = np.random.default_rng(seed); x = rng.standard_normal(n)
    a = 1.0 - math.exp(-2.0 * math.pi * f_c * DT)
    nk = max(1, int(math.ceil(6.0 / (2.0 * math.pi * f_c * DT))))
    k = a * np.power(1.0 - a, np.arange(nk))
    y = np.convolve(x, k)[:n]
    return y / y.std() * sigma

NI = band_noise(SIG_I, F_NI, SEED_I)
NT = band_noise(SIG_T, F_NT, SEED_T)

_tau = np.maximum(t - T_LOAD, 0.0)          # 加载后相对时间
_on = (t >= T_LOAD).astype(float)         # 空载段：负载恒为 0（含负载噪声）
step = 0.50 * _on
npc = (0.10 * np.sin(2 * math.pi * 5.9 * _tau) + 0.05 * np.sin(2 * math.pi * 11.8 * _tau)
       + (0.10 / 3.0) * np.sin(2 * math.pi * 17.7 * _tau) + 0.025 * np.sin(2 * math.pi * 23.6 * _tau)) * _on
amp = np.full_like(t, 0.04)
amp = np.where((_tau >= 0.5) & (_tau < 0.6), 0.20, amp)
amp = np.where((_tau >= 1.0) & (_tau < 1.5), 0.20, amp)
amp = np.where(_tau >= 2.0, 0.30, amp)
ph = 2 * math.pi * _tau / T
TL = (step + npc + amp * (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))) * _on
TL_pu = TL
d = -B_GAIN * TL; r = np.full_like(t, 1.0)
DN = -B_GAIN * NT                         # 【2026-10-18】负载噪声全时段（正文 6.1 口径；原 *_on 只加在加载段，与正文不符）

# 【2026-10-18 口径对齐】beta3/tau0 由 1000/10ms 改回 2000/5ms，与 rcso_v3.tex 第 6 节正文一致。
#   判定证据：同一工况下 2000/5ms 的七窗口与正文平均偏差 9.1 rpm，1000/10ms 为 48.7 rpm；
#   且归档 pmsm_rc.npz 的 tau0=0.01，说明第 6 节的图当年用 10ms 档生成（图与表不同源，待重跑）。
# 【自适应通道重整定 2026-10-16】原 tau0=T/80=1.25ms、gamma=3、mu=0.03、sigma2=5 时，
#   PMSM 工况下 tau'/tau0 撞上界 5.000（Q' 最低 0.424）——驱动过猛。按用户要求取 tau0=1/500=2ms，
#   同时压驱动、抬恢复：gamma 3->1、mu 0.03->0.015、sigma2 5->10。实测 tau'/tau0∈[0.515,3.923]、
#   Q'∈[0.877,1.0] 均不触界，且稳态 RMS 由 7.025 改善到 5.117 rpm。
P = dict(wo=500.0, kp=75.36, T=T, zeta=0.2, beta3=2000.0, tau0=5.0e-3, kappa=0.1, Q0=0.98,
         gamma=1.0, sig1=1e5, sig2=10.0, mu=0.015, warm=2.0, taumax=5.0, taumin=0.2,
         law="decupled", qmax=1.8, qmodel_max=1.0, drive_mode="bpw", theta_sign=1.0,
         bpw_fa=5.0, bpw_sa=50.0, bpw_fb=1.0, bpw_sb=10.0, qd_mode=2, qmin=0.2,
         norm_floor=6.5, eo_def="meansq", theta_drive="bnorm", q_drive="bnorm",
         q_rest_tau="none", c1=0.1, c2=0.1, b_filt=1.0, b0_tau=1.0)

def run(adapt, beta3=None, e1src="estimation", tau_ci=TAU_CI_DEF, ni=NI, nt=DN, tau0=None, vstart=0.0):
    Y = adrc_sim(t, r, d, B_GAIN, B0_GAIN, P["wo"], P["kp"], P["T"], P["zeta"],
                 P["beta3"] if beta3 is None else beta3, tau0 or P["tau0"], P["kappa"], P["Q0"],
                 P["gamma"], P["sig1"], P["sig2"], P["mu"], adapt=adapt,
                 warm=P["warm"], taumax=P["taumax"], taumin=P["taumin"], law=P["law"],
                 qmax=P["qmax"], qmodel_max=P["qmodel_max"], drive_mode=P["drive_mode"],
                 theta_sign=P["theta_sign"], bpw_fa=P["bpw_fa"], bpw_sa=P["bpw_sa"],
                 bpw_fb=P["bpw_fb"], bpw_sb=P["bpw_sb"], qd_mode=P["qd_mode"], qmin=P["qmin"],
                 norm_floor=P["norm_floor"], eo_def=P["eo_def"], theta_drive=P["theta_drive"],
                 q_drive=P["q_drive"], q_rest_tau=P["q_rest_tau"], e1src=e1src, c1=P["c1"],
                 c2=P["c2"], b_filt=P["b_filt"], b0_tau=P["b0_tau"], vstart=vstart,
                 cur_tau=tau_ci, cur_noise=ni, d_noise=nt)
    return Y

def metrics(Y):
    m = t >= 7.0; e = (Y["y"] * N_OP - N_OP); ee = e[m]; tt = t[m]
    return (float(np.sqrt(np.mean(ee ** 2))), float(2.0 / len(ee) * abs(np.sum(ee * np.exp(-1j * 2 * np.pi * 10 * tt)))),
            float(np.abs(Y["ia"] * I_BASE).max()))

CASES = [("ideal_rc",   dict(adapt=False, tau_ci=0.0, ni=None, nt=None)),
         ("ideal_rcad", dict(adapt=True,  tau_ci=0.0, ni=None, nt=None)),
         ("eso",        dict(adapt=False, beta3=0.0)),
         ("rc",         dict(adapt=False)),
         ("rcad",       dict(adapt=True)),
         ("tr_rc",      dict(adapt=False, e1src="tracking", vstart=0.5)),
         ("tr_rcad",    dict(adapt=True,  e1src="tracking", vstart=0.5))]

out, t0 = {}, time.time()
for nm, kw in CASES:
    t1 = time.time(); out[nm] = run(**kw); print("run %-11s %.1f s" % (nm, time.time() - t1))

for nm, _ in CASES:
    Y = out[nm]
    np.savez_compressed("pmsm_%s.npz" % nm, t=t, r=r, d=d, TL_pu=TL, TL_Nm=(TL + NT) * T_RATED,
        NI=NI, NT=NT, rpm=Y["y"] * N_OP, iq=Y["u"] * I_BASE, iq_act=Y["ia"] * I_BASE,
        y=Y["y"], z1=Y["z1"], z2=Y["z2"], v=Y["v"], u=Y["u"], ia=Y["ia"], e1=Y["e1"],
        ef=Y["ef"], th=Y["th"], tau=Y["tau"], Q=Y["Q"], E0=Y["E0"], D=Y["D"], B=Y["B"],
        tau_state=Y["tau_state"], Q_state=Y["Q_state"], _dth=Y["_dth"], _drv=Y["_drv"],
        B_GAIN=B_GAIN, B0_GAIN=B0_GAIN, KT=KT, J_M=J_M, W_REF=W_REF, I_BASE=I_BASE,
        TAU_S=TAU_S, T_RATED=T_RATED, N_OP=N_OP, I_PEAK=I_PEAK, dt=DT, T=T,
        tau0=P["tau0"], kappa=P["kappa"], gamma=P["gamma"], sig1=P["sig1"], sig2=P["sig2"],
        mu=P["mu"], norm_floor=P["norm_floor"], TAU_CI=TAU_CI_DEF, F_CI=F_CI_DEF,
        SIG_I=SIG_I, SIG_T=SIG_T, F_NI=F_NI, F_NT=F_NT, SEED_I=SEED_I, SEED_T=SEED_T)

# ---------------- 汇总 1：主配置（含电流环与噪声）----------------
WINS = [("空载稳态", 0.5, 2.0), ("加载瞬态", 2.0, 2.5), ("事件1", 2.5, 2.6), ("事件2", 3.0, 3.5),
        ("事件后", 3.5, 4.0), ("持续段", 4.0, 6.0), ("稳态段", 7.0, 12.0)]
Wb = lambda a, b: (t >= a) & (t < b)
def rms_of(nm, a, b):
    e = (out[nm]["y"] * N_OP - N_OP)[Wb(a, b)]
    return float(np.sqrt(np.mean(e ** 2)))
def hz_of(nm, f0):
    e = (out[nm]["y"] * N_OP - N_OP)[t >= 7.0]; tt = t[t >= 7.0]
    return float(2.0 / len(e) * abs(np.sum(e * np.exp(-1j * 2 * np.pi * f0 * tt))))

print("\n" + "=" * 100)
print("【主配置】电流环 f_ci=%.0f Hz (tau_ci=%.1f us) + 电流噪声 sigma_i=%.3f p.u.(%.3f A) + 负载噪声 sigma_T=%.3f p.u.(%.4f N·m)"
      % (F_CI_DEF, TAU_CI_DEF * 1e6, SIG_I, SIG_I * I_BASE, SIG_T, SIG_T * T_RATED))
print("=" * 100)
print("%-9s %14s %14s %14s %14s %14s" % ("窗口 RMS", "理想RC", "理想RC+自适", "纯ESO", "RC(含环+噪)", "RC+自适应(含环+噪)"))
for nmw, a, b in WINS:
    print("%-9s %14.5f %14.5f %14.5f %14.5f %14.5f" % (nmw, rms_of("ideal_rc", a, b), rms_of("ideal_rcad", a, b),
          rms_of("eso", a, b), rms_of("rc", a, b), rms_of("rcad", a, b)))
print("-" * 100)
print("%-14s %10s %10s %10s %12s %12s" % ("档", "10Hz", "30Hz", "50Hz", "max|iq指令|", "max|iq实际|"))
for c, _ in CASES:
    print("%-14s %10.4f %10.4f %10.4f %12.3f %12.3f" % (c, hz_of(c, 10), hz_of(c, 30), hz_of(c, 50),
          float(np.max(np.abs(out[c]["u"] * I_BASE))), float(np.max(np.abs(out[c]["ia"] * I_BASE)))))

# ---------------- 触界自检（状态侧硬钳位）----------------
print("-" * 100)
print("【触界自检】状态侧硬钳位：|theta|<=ln5/kappa=16.0944（等价 tau'/tau0<=5）、Q'<=1.0、下界 0.2/0.2")
for c in ("rcad", "tr_rcad"):
    Y = out[c]; th = Y["th"]; tp = Y["tau"] / P["tau0"]
    nth = int(np.sum(np.abs(np.abs(th) - 16.0944) < 1e-9))
    nthmin = int(np.sum(np.abs(np.abs(th) + 16.0944) < 1e-9))
    nq = int(np.sum(Y["Q"] >= 1.0 - 1e-9))
    print("  %-9s theta∈[%.4f,%.4f]  tau'/tau0∈[%.4f,%.4f]  Q'∈[%.6f,%.6f]  上界贴界=%d 下界贴界=%d  Q'>=1=%d"
          % (c, th.min(), th.max(), tp.min(), tp.max(), Y["Q"].min(), Y["Q"].max(), nth, nthmin, nq))

# ---------------- 噪声->D 通路自检 ----------------
print("-" * 100)
print("【噪声->D 通路】phi 压缩尺度/死区 c1=c2=%.2f（0=关闭）" % P["c1"])
for c in ("ideal_rcad", "rcad"):
    Y = out[c]; drv = np.abs(Y["_drv"]); mm = t >= 7.0
    print("  %-11s 稳态 |D| 均值=%.5f 中位=%.5f  p95=%.5f  事件窗 |D| 最大=%.3f"
          % (c, float(drv[mm].mean()), float(np.median(drv[mm])), float(np.percentile(drv[mm], 95)),
             float(drv[(t >= 0.5) & (t < 2.0)].max())))

# ---------------- 汇总 2：电流环带宽扫描（RC 档，无噪声）----------------
print("\n" + "=" * 100)
print("【敏感性 A】电流环闭环带宽 f_ci（RC 档，无自适、无噪声，beta3=16000）")
print("%12s %14s %12s %12s" % ("f_ci (Hz)", "稳态 RMS rpm", "10Hz rpm", "max|ia| A"))
band = []
for f in [15900.0, 8000.0, 5300.0, 4000.0, 3200.0, 2000.0, 1000.0]:
    Y = run(False, tau_ci=0.0 if f > 1e5 else 1.0 / (2 * math.pi * f), ni=None, nt=None)
    r1, a1, m1 = metrics(Y); band.append((f, r1, a1, m1))
    print("%12.0f %14.4f %12.4f %12.2f" % (f, r1, a1, m1))
np.savez_compressed("pmsm_band.npz", f=np.array([b[0] for b in band]), rms=np.array([b[1] for b in band]),
                    hz10=np.array([b[2] for b in band]), imax=np.array([b[3] for b in band]))

# ---------------- 汇总 3：噪声扫描（理想电流环，隔离噪声效应）----------------
print("\n" + "=" * 100)
print("【敏感性 B】噪声（理想电流环，隔离电流环本身的影响）")
print("%-10s %14s %14s %14s %14s" % ("配置", "RC RMS", "RC 10Hz", "RC+自适 RMS", "RC+自适 10Hz"))
rows = []
for lbl, si, st in [("无噪声", 0.0, 0.0), ("仅电流噪声0.2%", 0.2 * SIG_I, 0.0), ("仅电流噪声0.5%", 0.5 * SIG_I, 0.0),
                    ("仅电流噪声1%", SIG_I, 0.0), ("仅电流噪声3%", 3 * SIG_I, 0.0),
                    ("仅负载噪声5%", 0.0, SIG_T), ("仅负载噪声10%", 0.0, 2 * SIG_T),
                    ("两者同时", SIG_I, SIG_T)]:
    ni = band_noise(si, F_NI, SEED_I) if si > 0 else None
    nt = (-B_GAIN * band_noise(st, F_NT, SEED_T)) if st > 0 else None
    y1 = run(False, tau_ci=0.0, ni=ni, nt=nt); y2 = run(True, tau_ci=0.0, ni=ni, nt=nt)
    m1 = metrics(y1); m2 = metrics(y2); rows.append((lbl, m1, m2))
    print("%-10s %14.4f %14.4f %14.4f %14.4f" % (lbl, m1[0], m1[1], m2[0], m2[1]))
np.savez_compressed("pmsm_noise.npz", lbl=np.array([r[0] for r in rows]),
                    rc_rms=np.array([r[1][0] for r in rows]), rc_hz=np.array([r[1][1] for r in rows]),
                    rcad_rms=np.array([r[2][0] for r in rows]), rcad_hz=np.array([r[2][1] for r in rows]))
print("总耗时 %.1f s" % (time.time() - t0))
print("=" * 100)
