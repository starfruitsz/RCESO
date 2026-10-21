# -*- coding: utf-8 -*-
r"""
一阶 ADRC（灰箱重构自适应 ESO）：被控对象  y_dot = b*u + d

【顶层结构】"先观测总扰动，再前馈抵消" —— 与"控制器内部追参考"是两回事。

  被控对象    y_dot = b*u + d(t)
  扰动分解    d = d_step(阶跃负载) + d_np(非周期) + d_p(周期，含突变)
               d_np 取 0.7 Hz —— 不是基波 5 Hz 的整数倍，故重复控制律无法抵消它，
               必须靠 ESO 把它当"未知扰动"估出来（这才叫非周期扰动）
               d_p  = 5 Hz + 3/5 次谐波，周期 T；在 [tsw, tsw+dur] 内幅值或延时突变

  灰箱 ESO（已知周期模型内嵌，只把残余划为总扰动）
     周期分量估计 v 由 PPT 的低通重复控制律产生：
         tau*v_dot + v = Q*v(t-T) + beta3*tanh(e1/zeta) = chi
         e1 = y - z1（ESO 观测误差）—— 与 PPT 第5页有界性证明的驱动量口径一致，本版默认
         旧实现（e1 = y - r 跟踪误差驱动）保留开关：--e1-src tracking（供回归对账）
         e_f = chi - v = tau*v_dot        <- 滤波误差，自适应律的驱动源
     残余总扰动 z2 由线性 ESO 估计：
         z1_dot = z2 + b0*u + v + beta1*(y - z1)
         z2_dot = beta2*(y - z1)
     beta1 = 2*wo ,  beta2 = wo^2 （按观测器带宽 wo 参数化）

  控制律      u = (u0 - z2 - v)/b0 ,   u0 = kp*(r - y)
              （v 前馈抵消周期扰动，z2 抵消残余总扰动，u0 做跟踪）

  自适应律（--law signed，【默认】= PPT 现行律）
      E_o       = (1/T)*Integral_{t-T}^{t} |e_f| dt    （滑动窗：一个周期内 |e_f| 的均值；--eo-def meanabs）
                  E_o^2 = E_o**2
      （旧口径 --eo-def meansq：E_o^2 = (1/T)*Integral_{t-T}^{t} e_f^2 dt，即均方 = RMS^2，供回归对账）
              theta_dot = gamma/(2*kappa*tau^2)*(e_f^2 - E_o^2) - sigma1*(tau - tau0^2/tau)
                          （= -2*sigma1*tau0*sinh(kappa*theta)，即 PPT 的 -sigma1_ppt*sinh(kappa*theta)）
              Q_dot     = -(mu/(2*tau))*[1-(1-Q)^2]*(|e_f| - E_o)^2 + sigma2*tau*atanh(1-Q)   （--q-drive devsq，默认）
              tau       = tau0*exp(kappa*theta)
  自适应律（--law new，θ 驱动项取 |e_f^2 - E_o^2|：非负，但稳态被单向泵高 -> tau 偏置）
              theta_dot = gamma/(2*kappa*tau^2)*|e_f^2 - E_o^2| - sigma1*(tau - tau0)
  自适应律（--law ppt，旧律，保留用于回归对账）
              theta_dot = gamma/(2*kappa*tau^2)*e_f^2 - sigma1*(tau - tau0)
              Q_dot     = -(kappa*mu/(2*gamma))*[1-(1-Q)^2]*tau*theta_dot - sigma2*atanh(Q-1)
  对照组：tau ≡ tau0, Q ≡ Q0 固定

积分：v 用指数积分（chi 冻结下精确、对 tau 刚性无条件稳定）；其余显式欧拉。

用法：
    python adrc_eso_closed.py                    # 自适应 vs 无自适应对比
    python adrc_eso_closed.py --dist-mode delay  # 周期扰动改用延时突变
    python adrc_eso_closed.py --wo 80 --kp 20    # 调观测器带宽/控制器增益
"""
import argparse
import math
import sys
import warnings
from datetime import datetime
import numpy as np

try:                                   # 控制台若是 GBK，打印 θ? / ? / ? 这类字符会直接抛
    sys.stdout.reconfigure(errors="replace")   # UnicodeEncodeError 把整个脚本搞崩（已踩过一次）
except Exception:
    pass

warnings.filterwarnings("ignore",
                        message="This figure includes Axes that are not compatible with tight_layout")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    _AV = {f.name for f in font_manager.fontManager.ttflist}
    for _f in ["Microsoft YaHei", "SimHei", "SimSun", "DengXian"]:
        if _f in _AV:
            plt.rcParams["font.sans-serif"] = [_f]
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["mathtext.fontset"] = "stix"
    _HAS_MPL = True
except ImportError:
    plt = None
    _HAS_MPL = False


# ---------------------------------------------------------------- 默认参数
B_DEF = 1.0            # 被控对象真实输入增益
B0_DEF = 1.2           # ESO/控制律用的标称增益（故意留 20% 失配，才需要总扰动观测）
WO_DEF = 300.0          # ESO 带宽 = eso_ratio * wc（脚本内按 --wc/--eso-ratio 计算）          # 观测器带宽 (rad/s) -> beta1=2*wo, beta2=wo^2
KP_DEF = 50.0          # 控制器比例增益
T_DEF = 0.1            # 周期扰动基波周期（5 Hz）
ZETA_DEF = 0.2
BETA3_DEF = 16000.0     # [2026-10-11 放大效果] 重复通道增益。实测"三档差距"随 beta3 单调放大：
                       # 4000 -> 最小窗间距 6.9%；8000 -> 21.5%；16000 -> 35.4%；30000 -> 47.7%。
                       # 取 16000：间距够大且 tau 不漂（tau/tau0∈[1.0,1.24]、末 1.0047）、
                       # 对 b0 失配 ±50%、事件时刻、wo、kp 都稳。代价：|u|max 1046 -> 2501。
                       # 且单调有效：beta3=3000/4000/5000 的 (3)vs(2) 最小窗间距 = 4.2% / 6.6% / 10.5%。
                       # 上限不在 beta3 本身而在 tau 分支：beta3>=12000 时 tau 被压到数值地板，
                       # 低通退化成纯重复控制，数值虚好不可信 -> 取 4000 留约 3 倍余量。
                       # 注: 曾按线性化估出上界 beta3<(1-Q0)*wc/b=1，已被实测推翻（tanh 饱和压住有效增益）。
TAU0_DEF = 1.0 / 800.0
KAPPA_DEF = 0.1
Q0_DEF = 0.98          # [扫描后] 原 0.98。Q0=0.9 时 恢复+79.7% 与 长期+24.8% 同时为正
GAMMA_DEF = 1e-7       # [2026-10-11 定稿] θ 通道速率。1e-9 会把 τ 稳态偏置抬到 1.5 以上（整流效应），
                       # 偏置 ∝ gamma/sigma1。gamma=5e-10 时 τ 末值冲到 1.47（长期窗 -48%）；
                       # 1e-10 + sigma1=1e5 时 τ∈[1.0,1.064]、末 1.005，长期回到 -0.5%。
SIG1_DEF = 8.5e6      # 长期窗掉到 -288%；1e-10 + 本值 时 τ 末 1.0047、长期 +29%。
                       # 本组合 tau 末 1.006、长期窗 -0.5%（同口径最好）。原 5000。
                       # 靠 sigma1 把 τ 拉回，故 sigma1 同时决定"稳态偏置"与"回拉快慢"，提高到 1e5。
SIG2_DEF = 10000          # [2026-10-11 定稿] Q 的恢复增益。原 5/10 时 Q 只降不回升（实测末值掉到 0.42），
                       # 长期窗 (3)vs(2) 被拖到 -12%；300 让 Q 在稳态回到 0.99 附近，长期窗转为 0%~+5%。
MU_DEF = 3e-2
Q_ABS = False

# [2026-10-13] ★ 以上 *_DEF 已整体对齐【终稿配置 = PPT 第6页现行律】：
#   law=signed(θ 驱动取 e_f^2-E_o^2) + q_drive=abs(Q 驱动取绝对值) + eo_def=meanabs(E_o=mean|e_f| 再平方)
#   参数 kp=50 wo=300 beta3=16000 zeta=0.2 gamma=1e-7 sig1=8.5e6 sig2=1e4 mu=3e-2
#        qmin=0.2 qmax=2.0 taumin=0.5 taumax=2.0
#   => 裸跑 `python adrc_eso_closed.py` 即终稿控制器配置（工况 tend/dist-mode 仍由 CLI 控制）。
#   改动前的旧档（回归对账用）由 --preset mem_suppress 完整锁定，不再依赖 CLI 默认值。
#   上一个状态留档：_bode/adrc_eso_closed_pre_align_20261013.py
DT_DEF = 1e-5


def disturbances(t, T, tsw=6.0, dur=2.0, dist_mode="amp",
                 step_t=0.2, step_amp=0.5, np_amp=0.3, np_f=0.7,
                 p_amp=1.0, p_amp_after=300.0, p_dly2=0.25, np_amp_after=None,
                 tsw2=0.0, dur2=0.1, dsust=0.0, tsust=1.0, sust_dur=0.0):
    """返回 (d_total, d_step, d_np, d_p)；d_p 在 [tsw, tsw+dur] 内突变，且 t>=tsust 时叠加持续周期扰动"""
    d_step = np.where(t >= step_t, step_amp, 0.0)
    d_np = np_amp * np.sin(2.0 * np.pi * np_f * t)          # 0.7 Hz：非 T 的整数倍 -> 重复控制律无能为力
    if np_amp_after is not None:                            # 非周期扰动与周期扰动【一起】突变
        d_np = np.where((t >= tsw) & (t < tsw + dur),
                        np_amp_after * np.sin(2.0 * np.pi * np_f * t), d_np)
    dly = np.zeros_like(t)
    amp = np.full_like(t, p_amp)
    m = (t >= tsw) & (t < tsw + dur)
    if tsw2 > 0.0:                                   # 第二段突变窗口
        m = m | ((t >= tsw2) & (t < tsw2 + dur2))
    if dist_mode == "amp":
        d_step = np.where(m, d_step * (p_amp_after / max(p_amp, 1e-12)), d_step)
        amp = np.where(m, p_amp_after, amp)
    elif dist_mode == "delay":
        dly = np.where(m, p_dly2 * T, 0.0)
    elif dist_mode == "amp_step":                    # 【错误记忆工况】持续性幅值突变：
        amp = np.where(t >= tsw, p_amp_after, p_amp)  # 此后旧记忆的【幅值】永远是错的
    elif dist_mode == "dly_step":                    # 【错误记忆工况】持续性相位突变：
        dly = np.where(t >= tsw, p_dly2 * T, 0.0)     # 此后旧记忆的【相位】永远是错的
    d_sust = np.zeros_like(t)
    if dsust > 0.0:                                  # 从 tsust 起叠加的持续扰动 —— 它本身是周期量
        # [sust-dur 2026-10-15] sust_dur>0 时持续扰动只持续 sust_dur 秒（默认 0 = 到结束，回归不变）
        _m3 = (t >= tsust) & ((t < tsust + sust_dur) if sust_dur > 0.0 else True)
        _ph2 = 2.0 * np.pi * (t - tsust) / T         # 图上把 1 s 后的周期波形画成了"阶跃型负载"；
        _ds = dsust * (np.sin(_ph2) + 0.4 * np.sin(3.0 * _ph2) + 0.2 * np.sin(5.0 * _ph2))
        d_sust = np.where(_m3, _ds, 0.0)             # 合计量不变，只是分项归属改对
    ph = 2.0 * np.pi * (t - dly) / T
    d_p = amp * (np.sin(ph) + 0.4 * np.sin(3.0 * ph) + 0.2 * np.sin(5.0 * ph)) + d_sust
    return d_step + d_np + d_p, d_step, d_np, d_p
    d_p = amp * (np.sin(ph) + 0.4 * np.sin(3.0 * ph) + 0.2 * np.sin(5.0 * ph))
    return d_step + d_np + d_p, d_step, d_np, d_p


# ---------------------------------------------------------------- 仿真内核
def adrc_sim(t, r, d, b, b0, wo, kp, T, zeta, beta3, tau0, kappa, Q0,
             gamma, sig1, sig2, mu, adapt=True, warm=0.0, taumax=0.0, vstart=0.0,
             e0norm=False, eref2=1.0, s2tau=False, s2pow=0.0, taumin=-1.0, law="new",
             e1src="estimation", memflush=None, drv_dbz=0.0, ret_mult=1.0, qmax=0.0, tau_lock_from=0.0,
             q_drive="devsq", qmin=1e-4, eo_def="meanabs", theta_drive="auto", q_rest_tau="tau", rest_d=False, norm_floor=1e-6,
             c1=1e-3, c2=1e-3, tau_theta=5e-4, tau_q=5e-3, qmodel_max=0.0,drive_mode="phi",theta_sign=1.0,
             bpw_fa=1.0, bpw_sa=10.0, bpw_fb=1.0, bpw_sb=10.0, qd_lpf=0.0, qd_abs=0, qd_mode=0, qd_hp=0.0,dbias_tau=0.0,
             lpf_fast=5.0, lpf_slow=50.0, lpf_k=1.0, b_filt=1.0, ac_base=0.5103, b0_tau=1.0, tau2_mode="live", hpma_win=1.0, tau_B=0.0, tau_f=0.0, tau_l=0.0, theta_gain="tau2",
             cur_tau=0.0, cur_noise=None, d_noise=None, spd_noise=None, aj_gate=0.0, eso_sched=0.0,
             pr_gain=0.0, pr_tau=0.5, p_boost=0.0, det_eps=0.05, det_phi=0.0, theta_dz=0.0, pi_ki=0.0, q_src="ef", q_mism=0.0, q_mism_eps=1e-9, q_mism_c=0.0, q_mism_mode="energy", q_mism_latch=0.0, q_mism_dur=2.0,
             ff_flush=0.0, ff_tau_f=0.01, ff_tau_s=0.5, ff_cool=0.3, ff_q=0.0, ff_b3=0.0, ff_b3_dur=1.0, ff_scale=0.0, ff_rel=0.0, ff_tau_rs=2.0, ff_period=0.0, ff_phase=0.0, mm_det=0.0, mm_tau=2e-4, mm_win=20, mm_ratio=0.6, mm2=0.0, mm2_win=50, mm2_ratio=2.0,
             ff_src="e1", ff_amin=0.0, ff_gmax=-1.0, ff_vmax=-1.0):
    # 【PI 对照档 2026-10-17】pi_ki>0 时在比例项上叠加积分项（u0 = kp(r-y) + ki*int(r-y)dt），
    #   配合 beta1=beta2=0（无 ESO）、beta3=0（无重复通道）即得纯 PI 控制器。pi_ki=0 时逐位退化。
    # 【检测器前置 phi 压缩 2026-10-17】e1bar = (1/T)*int_{t-T}^{t} phi(e1,c) dtau，
    #   phi(x,c)=x-c*tanh(x/c)（与 §3 的 phi 同定义）。奇函数 => 谐波簇的周期积分为 0 的性质不变，
    #   但噪声小样本被压掉，避免"检测器被噪声持续点亮"。det_phi=0 时 phi(x,0)=x，逐位退化。
    # 【突变检测器共用阈值 det_eps】fire = 1 - 1/(1+(e1bar/det_eps)^2)；det_eps<=0 时 fire≡0。
    # aj_gate 为泵浦门控【增益】(0=关，1=按 fire 全门)；p_boost 为 P 增益提升【倍数】。
    # 三者全 0 时 fire≡0 => 全部退化，与改动前逐位一致。
    # 【突变期 P 增益提升 2026-10-17】kp_eff = kp*(1 + p_boost*fire)，fire = 1 - 1/(1+(e1bar/aj_gate)^2)。
    #   动机：阶跃峰值误差的主因是"ESO 估计到位之前"的比例项不足；抬 kp 直接顶住跌落。
    #   噪声安全性：触发窗口 ≈0.2 s（稳态 fire≡0），且 kp 只在比例通道放大，不改观测器噪声增益。
    #   p_boost=0 时与改动前逐位一致。
    # 【谐波谐振辅助 PR-assist 2026-10-17】以 1/T 谐波解调 e1，按【对象在 omega1 处的逆】直接算出
    #   所需的补偿增量并合成回 chi —— 绕过重复通道"必须等一个周期"的固有时延。
    #   X_e1 = 2(h_c + j h_s)（使 e1 = Im[X e^{j wt}]），H(jw)=(b/b0)/(jw+b*kp/b0)，
    #   dX = -X_e1/H(jw) => dv(t) = Im[dX e^{j wt}]；pr_gain∈(0,1] 为安全系数，pr_tau 为解调低通（×T）。
    #   稳态 X_e1->0 故辅助项自动归零；pr_gain=0 时与改动前逐位一致。
    # 【ESO 带宽调度 2026-10-17】eso_sched>0 时，观测器带宽随突变检测器放大：
    #   omega_o^eff = omega_o * (1 + eso_sched*fire),  fire = 1 - 1/(1+(e1bar/aj_gate)^2) ∈ [0,1)
    #   => 突变期观测器变快（削减阶跃引起的转速跌落），稳态回到标称（不放大噪声）。
    #   eso_sched=0 时 b1e,b2e 与改动前逐位一致。
    # 【突变期泵浦门控 2026-10-17】aj_gate>0 时启用新律：
    #   chi = Q*v(t-T) + g*beta3*tanh(e1/zeta),  g = 1/(1+(e1bar/aj_gate)^2)
    #   e1bar = 一周期 T 内 e1 的均值（周期信号恒为 0，阶跃/非周期分量不为 0 => 突变判别器）。
    #   记忆项 Q*v(t-T) 不动 => 保留周期与相位信息（清记忆实测劣化 249%）。
    #   aj_gate=0 时不进入该分支，chi 与改动前逐位一致。
    # 【PMSM 电流环 2026-10-16】可选的对象侧强化（默认关，逐位保持原行为）：
    #   cur_tau   : 电流环闭环等效时间常数（s）。>0 时实际电流 i_a 以一阶滞后跟踪指令 u，
    #               cur_noise[k] 从【反馈侧】注入、经同一低通进入实际电流。
    #   cur_noise : 电流反馈噪声数组（与 t 等长，单位同 u）；None = 无噪声。
    #   d_noise   : 叠加在总扰动 d 上的噪声数组（负载转矩噪声），None = 无噪声。
    #   R["ia"] 记录实际进入对象的电流（cur_tau<=0 时 = u - cur_noise）。
    # s2tau: 恢复项乘 (tau/tau0) —— 使 Q 的平衡方程中 tau 被提到括号外，平衡点不随带宽漂移
    # e0norm: 恢复项按 E0^2/Eref^2 归一化（E0^2 = 一个周期内 e_f^2 的均值）
    #         E0^2 与驱动项的 e_f^2 同量纲 -> 使 Q 的平衡点不随扰动幅值漂移
    # vstart: 重复通道投入时刻 —— 此前 v 恒为 0，使阶跃跟踪段与纯 ESO 完全一致（共模对比）
    # warm  : 前 warm 个周期【冻结】自适应（theta/Q 不动），避开启动学习暂态
    # taumax: tau/tau0 硬上界（限在 theta 上，保持 tau=tau0*exp(kappa*theta) 关系）
    # law   : 自适应律形式。new = PPT 新图（驱动项 e_f^2-E_o^2；Q 律自带 tau 因子与
    #         atanh(1-Q) 恢复项）；ppt = 原律（驱动项只有 e_f^2；Q 由 theta_dot 耦合驱动）
    # eo_def: E_o 的定义口径（PPT 第6页；2026-10-13 用户定稿 —— 本次改动的主要落点）。
    #         "meanabs" =【PPT 现行定义】E_o = (1/T)*Integral[t-T, t] |e_f| dt，E_o^2 = E_o**2
    #         "meansq"  =【旧口径，供回归对账】E_o^2 = (1/T)*Integral[t-T, t] e_f^2 dt（均方 = RMS^2）
    #         两者不等价（Jensen 不等式），且差在结构上：
    #           · meansq  : mean(e_f^2 - E_o^2) ≡ 0  -> theta_dot 无偏置，tau 不漂移
    #                       （这正是 ADRC_工作汇总 §11.4 的核心结论，长期窗 -939.8% -> -3.0%）
    #           · meanabs : mean(e_f^2 - E_o^2) ≈ (1-2/pi)*sigma^2 ≈ 0.363*sigma^2 > 0
    #                       -> theta_dot 存在常值正偏置 -> tau 被单向抬高；
    #                       稳定偏移由 -sigma1*sinh(kappa*theta) 平衡，
    #                       故 tau 的稳态偏移 ∝ gamma/(2*kappa*tau^2)/sigma1，sigma1 越大越可忽略。
    #         正弦下具体差多少：mean(e_f^2)=A^2/2=0.500A^2，(mean|e_f|)^2=(2A/pi)^2≈0.405A^2。
    # e1src : 学习律驱动量来源。"estimation" = e1 = y - z1（ESO 观测误差，与 PPT 第5页
    #         证明口径一致，默认）；"tracking" = e1 = y - r（旧实现，供回归对账）
    # taumin: tau/tau0 下界（自动 -1 = 不限，只留 1e-6 纯数值防除零下界）。
    #         1) 图注语义"误差小时带宽拉回初始值"由 ODE 自身实现：实测 tau 末值 0.9997*tau0；
    #         2) 钳到 1.0 反而有害：theta 被顶在 0 上形成半波整流，tau 均值 +0.7%，
    #            长期窗 (3)vs(2) 由 -0.2% 掉到 -1.0%；
    #         3) 只有 gamma 放大到 1e-7 量级才会 tau→0 发散，界时汇总会报"tau 触底"
    n = len(t); dt = float(t[1] - t[0]); nd = max(1, int(round(T / dt)))
    if (q_drive == "devsq" or theta_drive in ("dev2", "devsq")) and eo_def != "meanabs" and law != "decupled":
        raise ValueError('q_drive="devsq" 或 theta_drive in (dev2,devsq) 需要 eo_def="meanabs"'
                         '（都用 E_o 本身）；当前 eo_def=%r。请改用 --eo-def meanabs。' % (eo_def,))
    keys = ("y", "z1", "z2", "v", "u", "e1", "ef", "th", "tau", "Q", "E0", "D", "B", "tau_state", "Q_state", "_dth", "_drv", "ia", "_fl", "_mm")
    R = {k: np.zeros(n) for k in keys}
    R["tau"][:] = tau0; R["Q"][:] = Q0
    R["tau_state"][:] = tau0; R["Q_state"][:] = Q0
    R["_dth"][:] = 0.0; R["_drv"][:] = 0.0
    _Qsh = float(Q0); _thsh = 0.0      # 【影子状态】投影前（未限幅）的演化，仅用于对比
    vbuf = np.zeros(nd); ip = 0
    axbuf = np.zeros(nd)              # 【q_drive=acd】|x|(t-T) 的延迟缓冲（与 vbuf 共用 ip 指针）
    dbuf = np.zeros(nd); accD = 0.0        # D = ∫(|e_f|-E_o)²dt 的周期累加器（--rest-d 用）
    e2buf = np.zeros(nd); acc2 = 0.0        # 周期累加器：窗内元素 = |e_f|*dt（meanabs）或 e_f^2*dt（meansq）
    e1sbuf = np.zeros(nd); _acc1s = 0.0      # 【q_src=e1】e1^2 的周期窗累加器（与 e2buf 共用指针 ip）
    vm_buf = np.zeros(nd); vm_old = np.zeros(nd)   # 【q_mism】v^2*dt 的滑动窗（当前/上一周期）
    _vm_now = 0.0; _vm_prev = 0.0
    # 【q_mism=harm】只取 k/T 谐波分量的滑动相量（k=1,3,5）：5.9 Hz 等非 T 整数倍内容被结构剔除
    qh_buf = np.zeros(nd); _qc = [0j, 0j, 0j]
    _qml_t = 0; _qml_force = None      # 【q_mism_latch】事件触发的一次性遗忘计时
    _efs = 0.0; _efl = 0.0; _fft = 0.0; _fb_flush = False   # 【ff_flush】快/慢包络 + 冷却
    _ffg_buf = np.zeros(nd); _ffg_acc = 0.0; _ffg_p = 0      # 【ff_gmax】e1 的 T 窗均值（独立缓冲）
    _frs = 0.0                                              # 【ff_rel】比值 E_f/E_s 的慢基线
    _fp_t = 0.0                                             # 【ff_period】无条件周期刷新计时
    # 【mm_det】MMAE 三假设残差（保持 v / 清空 0 / 反相 -v）
    _mm_e = [0.0, 0.0, 0.0]; _mm_n = 0; _mm_flip = False; _mm_trig = False
    _z1h = [0.0, 0.0, 0.0]; _z2h = [0.0, 0.0, 0.0]; _iah = [0.0, 0.0, 0.0]
    _mm2e = [0.0, 0.0, 0.0]; _mm2n = 0; _mm2_ok = False; _pred3 = [0.0, 0.0, 0.0]
    if ff_period > 0.0:
        _fp_t = ff_phase * ff_period                          # 【ff_phase】首拍相位偏移（0~1）
    _fb3_t = 0                                               # 【ff_b3】清空后泵浦限速计时（步）
    _ph = [np.exp(-2j * np.pi * _kk * np.arange(nd) / nd) for _kk in (1, 3, 5)] if q_mism_mode == "harm" else None
    e1buf = np.zeros(nd); acc1 = 0.0        # 【aj_gate】周期累加器：窗内元素 = e1*dt（突变判别用）
    _hs = 0.0; _hc = 0.0                    # 【PR-assist】1/T 谐波解调状态（同相/正交）
    # 【PPT 重构 2026-10-15】PPT 给的是三个【独立的】滤波器时间常数：
    #   B_k + tau_B*B_k_dot = e_f^2 ; A_f + tau_f*A_f_dot = e_f^2 ; A_l + tau_l*A_l_dot = e_f^2
    #   取 0 表示沿用旧口径（B_k 用 lpf_slow*T、A_f/A_l 用 lpf_fast/lpf_slow*T），保证回归逐位不变。
    _tauB = (tau_B * T) if tau_B > 0 else (lpf_slow * T)
    _tauF = (tau_f * T) if tau_f > 0 else (lpf_fast * T)
    _tauL = (tau_l * T) if tau_l > 0 else (lpf_slow * T)
    _ndh = max(1, int(round(hpma_win * T / dt)))   # 【hpma 分母窗口】= hpma_win 个周期 T
    hpbuf = np.zeros(_ndh); acch = 0.0      # 【theta_drive=hpma】窗内元素 = |高通输出|*dt
    b1, b2 = 2.0 * wo, wo * wo
    nwarm = int(round(warm * T / dt))
    nvst = int(round(vstart / dt))
    dbz = float(drv_dbz)            # 自适应驱动死区（0=关闭；见循环内注释）
    rml = float(ret_mult)           # 死区内回复项倍数（>1 = 稳态强制把 tau 拉回 tau0）
    # Q 上界（内模稳定域 |Q|<=1）：qmax<=0 -> 1-1e-9（默认，与改动前逐位一致）；
    #   qmax>=1 直通（保留域保护）；qmax<0 = 实验室模式（连域保护一并去除）（>1 即【故意放开内模稳定域】，用于检验 Q>1 时 v 是否失控）；qmax=1e9 视作无上界。
    # qmax>0: Q 上界（>=1 即放开内模稳定域，但仍受域保护 Q<2-1e-6）；
    # qmax==0（默认）: 1-1e-9；qmax<0: 【实验室模式】连域保护一并去除，用于复现"完全放开"的行为。
    _qhard = (qmax >= 0.0)
    qmx = (1.0 - 1e-9) if qmax == 0.0 else (1e9 if qmax < 0.0 else float(qmax))
    if qmodel_max > 0.0:                 # 【修复 2026-10-16】模型侧上界此前从未被引用（死参数）
        qmx = min(qmx, float(qmodel_max))
    qn_floor = float(qmin) if qmin > 0.0 else 1e-4   # Q 下界（防止大扰动期把记忆压死）
    thmax = (math.log(taumax) / kappa) if taumax > 0 else float('inf')
    if taumin < 0.0:                                   # -1 = 自动 = 不限
        taumin = 0.0                                   # 实证：物理钳位会引入 +0.7% 的 tau 偏置，
    if taumin <= 0.0:                                  #       长期窗代价 0.8%；E0^2 修好后本无需钳位
        taumin = 1e-6                                  # 纯数值下界，防止 τ→0 除零
    thmin = (math.log(taumin) / kappa) if taumin > 0 else float('-inf')
    # 理想遗忘 oracle：在给定时刻把记忆缓冲 vbuf(=v(t-T)) 清零。
    # 用途：突变瞬间旧记忆已被污染，清零点即为"立刻忘掉错误记忆"的上界对照组，
    #       于是  错误记忆造成的损失 = (2)无自适应 - (4)理想遗忘 ，
    #             自适应律挽回的比例 = ((2)-(3)) / ((2)-(4)) 。
    flush_steps = set()
    if memflush is not None:
        for _tf in np.atleast_1d(memflush):
            _k = int(round(float(_tf) / dt))
            if 1 <= _k < n:
                flush_steps.add(_k)
    yk = z1k = z2k = vk = uk = thk = 0.0; tk = tau0; Qk = Q0; Bk = 0.0; B0k = 0.0
    _pi_int = 0.0                          # 【PI 档】积分器状态
    _rth = 0.0; _rq = 0.0                    # 【decupled 新律】两条通道各自的滤波器状态
    _lpf_f = 0.0; _lpf_s = 0.0        # 【q_drive=lpf】快/慢两路 η2 低通状态
    _ac_s = 0.0                        # 【q_drive=ac/acp】|x| 的慢基线（去整流用），时间常数 = lpf_slow*T
    _bp_f = 0.0; _bp_s = 0.0
    _wfa = _wsa = _wfb = _wsb = 0.0
    _dql = 0.0                        # 【bpw】Q 驱动的时间平均状态
    _rqh = 0.0                        # 【bpw】Q 通道高通状态
    _dbm = 0.0                        # 【bpw】驱动的慢均值估计（去直流用）   # 【bpw】phi 之后的两路带通状态（θ/Q 各一组）          # 【q_drive/theta_drive=bpbn】对 e_f^2 的快/慢低通（带通两路）
    _hp_s = 0.0                        # 【theta_drive=hp/hpn】LPF_slow(e_f^2)，原高通用
    _iast = 0.0                                        # 【电流环】实际电流状态（cur_tau>0 时启用）
    for k in range(1, n):
        rk = r[k - 1]; dk = d[k - 1]
        # 学习律驱动量 e1：estimation = y - z1（PPT 第5页证明口径，默认）
        #                  tracking   = y - r （旧实现，供回归对账）
        # 注：y 与 z1 都是上一步的值，与下方 ESO 校正用的 eo = y - z1 同源同值
        # 【测量噪声 2026-10-18】转速采样噪声：只进入控制器，不改对象真值
        ymk = yk + (spd_noise[k] if spd_noise is not None else 0.0)
        e1k = (ymk - z1k) if e1src == "estimation" else (ymk - rk)
        _fb_flush = False
        _mm_trig = False; _mm_flip = False
        if mm2 > 0.0:
            # 【三并行观测器 MMAE】每个假设自带 ESO 与电流环副本，用各自 z2 反推扰动做一步预测
            _vh3 = (vk, 0.0, -vk)
            _b1 = 2.0 * wo; _b2 = wo * wo
            _a2 = 1.0 - math.exp(-dt / max(mm_tau, 1e-9))
            if not _mm2_ok:
                _z1h = [ymk, ymk, ymk]; _z2h = [0.0, 0.0, 0.0]; _iah = [_iast, _iast, _iast]
                _pred3 = [ymk, ymk, ymk]
            for _i in range(3):
                _mm2e[_i] += _a2 * (abs(ymk - _pred3[_i]) - _mm2e[_i])   # 上一拍预测 vs 本拍实测
                _eh = ymk - _z1h[_i]
                _uh = (kp * (rk - ymk) - _z2h[_i] - _vh3[_i]) / b0
                _ia_new = (_iah[_i] + (dt / cur_tau) * (_uh - _iah[_i])) if cur_tau > 0.0 else _uh
                _z1h[_i] += dt * (_z2h[_i] + b0 * _uh + _vh3[_i] + _b1 * _eh)
                _z2h[_i] += dt * (_b2 * _eh)
                _iah[_i] = _ia_new
                _dh = _z2h[_i] - (b - b0) * _uh
                _pred3[_i] = ymk + dt * (b * _ia_new + _dh)
        if mm_det > 0.0:
            # 三个假设对应的控制量（同一时刻、同一状态，只有 v 不同）
            # 预测器：y[n+1] = y[n] + dt*(b*i_a[n+1] + a_res)，a_res 由上一拍实测反推，
            #   i_a[n+1] 由电流环一阶滞后给出（cur_tau>0 时必须建模，否则"保持"假设永不成立）
            _yprev = R["y"][k - 1]; _iaprev = R["ia"][k - 1]
            _a_res = (ymk - _yprev) / dt - b * _iaprev
            _pred = []
            for _vh in (vk, 0.0, -vk):
                _uh = (kp * (rk - ymk) - z2k - _vh) / b0
                _ia_h = (_iast + (dt / cur_tau) * (_uh - _iast)) if cur_tau > 0.0 else _uh
                _pred.append(ymk + dt * (b * _ia_h + _a_res))
        if ff_period > 0.0:
            _fp_t += dt
            if _fp_t >= ff_period:
                _fp_t = 0.0
                _fb_flush = True
        if ff_flush > 0.0:
            # 【快速事件检测 + 状态级清记忆】快包络(10ms) 超过 慢包络(0.5s) 的 k 倍 -> 判定"记忆已失效"，
            #   立即清空重复通道状态（而不是改 Q 这种参数级遗忘）。冷却 ff_cool 防连发。
            # 【ff_src】检测量：e1（ESO 残差，旧默认）或 et（跟踪误差 y-r）。
            #   回声进 y 不进 e1（ESO 吸收），dq 口径实测旧检测量对撤除事件结构性失聪。
            _esrc = (ymk - rk) if ff_src == "et" else e1k
            _efs += (1.0 - math.exp(-dt / max(ff_tau_f, 1e-9))) * (abs(_esrc) - _efs)
            _efl += (1.0 - math.exp(-dt / max(ff_tau_s, 1e-9))) * (abs(_esrc) - _efl)
            # 【ff_gmax】非周期能量门控：e1 的 T 窗均值（与律 D 检测器同式，独立缓冲）
            _ffg_acc += e1k * dt - _ffg_buf[_ffg_p]
            _ffg_buf[_ffg_p] = e1k * dt
            _ffg_p = (_ffg_p + 1) % nd
            _e1m_ff = _ffg_acc / T
            _ffg_eps = det_eps if det_eps > 0.0 else 0.01
            _gg = (_e1m_ff * _e1m_ff) / (_e1m_ff * _e1m_ff + _ffg_eps * _ffg_eps)
            _okg = (ff_gmax < 0.0) or (_gg < ff_gmax)
            _okv = (ff_vmax < 0.0) or (abs(vk) < ff_vmax)
            _oka = abs(_esrc) > ff_amin
            if _fft > 0.0:
                _fft -= dt
            _rt = _efs / max(_efl, 1e-9)
            _frs += (1.0 - math.exp(-dt / max(ff_tau_rs, 1e-9))) * (_rt - _frs)
            if ff_rel > 0.0:
                _fire_now = (_rt > ff_rel * max(_frs, 1e-9))
            else:
                _fire_now = (_efs > ff_flush * max(_efl, 1e-9))
            if _fire_now and _okg and _okv and _oka and _fft <= 0.0 and k > nvst + 50:
                _fb_flush = True
                _fft = ff_cool
                if ff_b3 > 0.0:
                    _fb3_t = int(round(ff_b3_dur * T / dt))   # 清空后立即进入泵浦限速窗口
        vd = vbuf[ip]                                   # v(t-T)
        if k in flush_steps:                            # 理想遗忘 oracle：清空被污染的记忆
            vbuf[:] = 0.0
            vd = 0.0
        e2old = e2buf[ip]                               # 窗内元素(t-T)：|e_f|*dt 或 e_f^2*dt
        if (aj_gate > 0.0) or (p_boost > 0.0) or (eso_sched > 0.0) or (det_eps > 0.0):
            _e1old = e1buf[ip]                           # 【突变检测器】周期信号在 T 上均值为 0，阶跃不为 0
            # 与 §3 的 phi 同式：phi(x,c)=x-c*tanh(x/c)；内联以免依赖后文定义的 _phi
            _e1c = (e1k - det_phi * math.tanh(e1k / det_phi)) if det_phi > 0.0 else e1k
            e1buf[ip] = _e1c * dt
            acc1 += _e1c * dt - _e1old
            _e1m = acc1 / T
            # fire = e1bar^2/(e1bar^2+eps^2)：等价于 1/(1+(eps/e1bar)^2)，但无除法、无上溢
            _fire = (_e1m * _e1m) / (_e1m * _e1m + det_eps * det_eps) if det_eps > 0.0 else 0.0
        else:
            _fire = 0.0
        _gate = 1.0 - aj_gate * _fire                    # aj_gate=0 → 恒为 1（不门控）
        if eso_sched > 0.0:                              # 【ESO 带宽调度】
            _wk = 1.0 + eso_sched * _fire
            _b1e = b1 * _wk; _b2e = b2 * _wk * _wk
        else:
            _b1e = b1; _b2e = b2
        if pr_gain > 0.0:                               # 【PR-assist】谐波解调 + 对象逆 + 波形合成
            _w1 = 2.0 * math.pi / T
            _s1 = math.sin(_w1 * k * dt); _c1 = math.cos(_w1 * k * dt)
            _a1 = 1.0 - math.exp(-dt / max(pr_tau * T, 1e-12))
            _hs += _a1 * (e1k * _s1 - _hs)
            _hc += _a1 * (e1k * _c1 - _hc)
            _wr = 2.0 * _hc; _wi = 2.0 * _hs
            _ga = b * kp / b0; _gb = _w1 * (b0 / b)
            _dr = -(_wr * _ga - _wi * _gb); _di = -(_wr * _gb + _wi * _ga)
            _chi_pr = pr_gain * (_dr * _s1 + _di * _c1)
        else:
            _chi_pr = 0.0
        # 【ff_b3】清空后短暂降低泵浦增益：限制"把暂态写入记忆"的速度（Q 管不了这件事）
        _b3eff = beta3 if (_fb3_t <= 0 or ff_b3 <= 0.0) else beta3 * ff_b3
        if _fb3_t > 0:
            _fb3_t -= 1
        chi = Qk * vd + _gate * _b3eff * math.tanh(e1k / zeta) + _chi_pr
        # 低通重复控制律：tau*v_dot + v = chi（指数积分，精确且无条件稳定）
        if k < nvst:                                    # 通道未投入：v 恒 0，控制律退化为纯 ESO
            vnew = 0.0
            efk = 0.0
        else:
            vnew = chi + (vk - chi) * math.exp(-dt / tk)
            efk = chi - vnew                            # 滤波误差 = tau*v_dot
        if _fb_flush:
            # 【ff_scale】触发时的记忆处理：v <- alpha*v
            #   alpha=0 -> 清空（默认）；0<alpha<1 -> 部分保留；alpha=-1 -> 反相复位
            vnew = vnew * ff_scale
            vbuf *= ff_scale
        # 【B 状态 · PPT 2026-10-14 新版律】B + tau*B_dot = e_f^2
        #   一阶低通状态，时间常数 = tau/b_filt（b_filt=1 = 逐字实现式(1)的定义式）。
        #   PPT 中式(1) 的 B 无下标、式(2)~(5) 写作 B_kappa —— 两种读法都保留：
        #   默认 b_filt=1 取定义式；--b-filt <数值> 可试 B + (tau/k)*B_dot = e_f^2。
        #   它替代 E_o^2（一个周期滑动均值）作为零点与分母：
        #   稳态下 B 的周期漂移 = (tau/T)*DeltaB -> 0（tau<<T），故 (e_f^2-B) 近似零均值；
        #   而分母 B 是"近期能量尺度"，不再需要等满一个周期才补上（修 E_o 口径的滞后放大）。
        _bfk = (1.0 if b_filt <= 0.0 else float(b_filt))
        _ubf = efk * efk
        _bn = _ubf + (Bk - _ubf) * math.exp(-dt * _bfk / tk)
        # 【K.9 修法对照 2026-10-15】B0：时间常数与自适应 tau 【解耦】，固定用 tau0。
        #   仅供 --theta-drive bdecu 使用；默认路径不读它，回归逐位不变。
        _b0n = _ubf + (B0k - _ubf) * math.exp(-dt / max(1e-12, tau0 * b0_tau))
        # 【E_o 定义 2026-10-13】窗内元素：meanabs -> |e_f|*dt（取窗内均值后再平方）；
        #   meansq -> e_f^2*dt（窗内均方 = RMS^2）。定义与等价性见函数头 eo_def 注释。
        e2new = (abs(efk) * dt) if eo_def == "meanabs" else (efk * efk * dt)                          # 本步写入窗内的"能量元"
        acc2 += e2new - e2old                           # 【单位修正】累加器必须与窗内元素同量纲：
        e2buf[ip] = e2new                               # 旧的 (ef^2 - e2old)*dt 把"速率"与"量"相减，
                                                        # 只减掉 1/dt 分之一个旧元素 -> 衰减时间常数
                                                        # 变成 1/dt≈1e5 步(1 s) 而不是 T(0.1 s)
        # 【E_o 定义 2026-10-13】以下尾部旧注释仅适用于 meansq 口径；
        #   meanabs 口径下 E0sq = (窗内 |e_f| 的均值)^2，即 PPT 第6页 E_o^2 = E_o**2。
        _emean = (acc2 / T) if T > 0 else 0.0
        E0sq = (max(_emean, 0.0) ** 2) if eo_def == "meanabs" else max(_emean, 0.0)
        # 【新 Q 律 2026-10-13】η2=(|e_f|-E_o)^2 需要 E_o 本身，不只是 E_o^2：
        E0abs = max(_emean, 0.0) if eo_def == "meanabs" else math.sqrt(max(_emean, 0.0))
        # 【D 2026-10-13】D = ∫[t-T,t](|e_f|-E_o)^2 dt（PPT 第6页；注意是积分不是方差，差一个 /T）
        _dnew = (abs(efk) - E0abs) ** 2 * dt
        accD += _dnew - dbuf[ip]
        dbuf[ip] = _dnew
        Dval = max(accD, 0.0)
        _dfac = Dval if rest_d else 1.0        # 回复力倍率：--rest-d 关闭时恒为 1（逐位不变）      # E0^2 = 一个周期内 e_f^2 的均值
        eo = ymk - z1k                                   # 观测误差
        z1n = z1k + dt * (z2k + b0 * uk + vnew + _b1e * eo)
        z2n = z2k + dt * (_b2e * eo)
        if pi_ki > 0.0:                                  # 【PI 档】比例 + 积分
            _pi_int += (rk - ymk) * dt
            u0 = kp * (rk - ymk) + pi_ki * _pi_int
        else:
            _pi_int = 0.0
            u0 = (kp * (1.0 + p_boost * _fire)) * (rk - ymk) if p_boost > 0.0 else kp * (rk - ymk)
        un = (u0 - z2n - vnew) / b0                     # 控制律：抵消残余总扰动 + 周期分量
        _inoise = cur_noise[k] if cur_noise is not None else 0.0
        if cur_tau > 0.0:                               # 一阶闭环电流环：指令 -> 实际电流
            _iast += (1.0 - math.exp(-dt / cur_tau)) * ((un - _inoise) - _iast)
            _uef = _iast
        else:                                           # 理想电流源（原行为）
            _uef = un - _inoise
        _dnoise = d_noise[k] if d_noise is not None else 0.0
        yn = yk + dt * (b * _uef + dk + _dnoise)        # 被控对象 y_dot = b*i_a + d + d_noise
        _g2t = (E0sq / eref2) if (e0norm and eref2 > 0) else 1.0
        # 驱动项：新律用 e_f^2 - E_o^2（滑动窗均值），旧律只用 e_f^2
        # 驱动项：new 的 θ 通道用 |e_f^2 - E_o^2|（恒非负 -> τ 只会被推高、由 σ1 拉回 τ0，
        # 结构上就没有 τ→0 的退化分支）；signed 的 θ 通道用带符号的 e_f^2 - E_o^2。
        # 【2026-10-13 更正】旧注释「Q 通道仍用带符号的 e_f^2-E_o^2（图里未改）」已过期：
        #   PPT 第6页现行律为 Q_dot = -(mu/(2*tau))*[1-(1-Q)^2]*|e_f^2-E_o^2| + sigma2*tau*atanh(1-Q)，
        #   即 --q-drive abs（现为默认）；配合 V_dot_3 <= (1/4*tau)e_f^2 + (1/4*tau)E_o^2 - ...，
        #   该上界正是由三角不等式 |e_f^2-E_o^2| <= e_f^2+E_o^2 给出的。
        _dev = efk * efk - E0sq
        _ax_now = abs((efk * efk - Bk) / (Bk + norm_floor))   # 【q_drive=acd】延迟缓冲写入用
        # 【两通道统一驱动 2026-10-15】对 e_f^2 先带通（LPF_fast - LPF_slow）再归一化：
        #   _bp_drv = (LPF_fast(e_f^2) - LPF_slow(e_f^2)) / (B0 + eps)
        #   带通 H(0)=0  =>  稳态均值为零  =>  两通道都不会被假直流顶偏（对照 K.9/K.11）。
        _bp_f += (1.0 - math.exp(-dt / max(_tauF, 1e-12))) * (efk * efk - _bp_f)   # A_f（tau_f）
        _bp_s += (1.0 - math.exp(-dt / max(_tauL, 1e-12))) * (efk * efk - _bp_s)   # A_l（tau_l）
        _bp_drv = (_bp_f - _bp_s) / (B0k + norm_floor)
        # 【theta_drive=hp 2026-10-15】对 e_f^2 的【原高通】：D = e_f^2 - LPF_slow(e_f^2)。
        #   与带通的区别：高通在 10 Hz 的增益约 1，带通只有 0.105（上截止 1/tau_f）。
        #   H(0)=0 => 同样去直流；但保留 tau 最需要的 10 Hz 驱动源（K.12 的失败点）。
        _hp_s += (1.0 - math.exp(-dt / max(_tauB, 1e-12))) * (efk * efk - _hp_s)   # B_k（tau_B）
        _hp_drv = efk * efk - _hp_s
        # 【归一化因子 2026-10-15 · 用户口径】分母 = 【分子绝对值在周期 T 内的均值】：
        #   mean_T(|n|) 直接对齐分子自身的尺度；正弦下约 (2/pi)*峰值，
        #   而低通 B 对正弦给 RMS^2 = A^2/2（比 (E|e_f|)^2 大 23%），且突变期跟不上。
        _ih = ip % _ndh
        _hn = abs(_hp_drv) * dt; _ho = hpbuf[_ih]
        acch += _hn - _ho; hpbuf[_ih] = _hn
        _hp_ma = (acch / (_ndh * dt)) if _ndh > 0 else 0.0   # 窗均值（= hpma_win 个 T 的平均）
        # θ 通道驱动量的三种口径：
        #   new    : |e_f^2 - E_o^2|  —— 恒非负。E_o 只去掉直流，取绝对值后均值仍严格为正
        #            => θ 被单向泵高，稳态平衡点必然停在 τ>τ0（τ 回不去，只能靠 σ1 压住偏移）
        #   signed :   e_f^2 - E_o^2   —— 保留 E_o 的零均值性质：瞬态 e_f^2≫E_o^2 推高 τ，
        #            瞬态过后 e_f^2≲E_o^2 把 τ 拉回 τ0（τ→0 由 taumin/thmin + σ1 兜住）
        #   ppt    :   e_f^2           —— 原始律
        # 【theta 驱动 2026-10-13】--theta-drive 独立覆盖：
        #   signed = e_f^2-E_o^2（恒零均值 -> tau 不漂移，PPT 现行）
        #   abs    = |e_f^2-E_o^2|（恒非负 -> theta 单向泵高）
        #   dev2   = (e_f-E_o)^2   （恒非负：= Var(e_f)+(mean(e_f)-E_o)^2 > 0）
        #   devsq  = (|e_f|-E_o)^2 （恒非负 = eta2）
        #   auto   = 跟随 --law（原行为，逐位不变）
        if theta_drive == "signed":
            _drv = _dev
        elif theta_drive == "norm":
            # 【θ 驱动归一化 2026-10-14】PPT 第6页新版： (e_f²-E_o²)/(E_o²+ε)
            #   保留 e_f²-E_o² 的零均值性质，同时去掉量纲尺度 ⇒ θ 平衡点不随扰动幅值漂移。
            _drv = _dev / (E0sq + norm_floor)
        elif theta_drive == "bnorm":
            # 【θ 驱动 · PPT 2026-10-14 新版律 B_κ】(e_f² − B_κ)/(B_κ + ε)
            #   与 norm 的区别：归一化基准由"一个周期滑动均值 E_o²"换成"一阶低通状态 B"。
            #   ⇒ 不再需要等满一个周期才建立分母（E_o 口径实测有 24 万倍放大尖峰，见口径说明
            #     2026-10-14「问题 1」）；ε 仍必须是真实尺度，取值同 norm_floor 口径。
            _drv = (efk * efk - Bk) / (Bk + norm_floor)
        elif theta_drive == "bdiff":
            # 【去归一化对照 2026-10-15】删掉分母 (B+eps)、保留 B：x = e_f^2 - B。
            #   用于回答「把归一化删掉会怎样」：分子偏置 E[e_f^2-B] 是否仍在。
            _drv = efk * efk - Bk
        elif theta_drive == "hpma":
            # 高通 + 周期均值归一化（不删归一化，只换分母口径）
            _drv = _hp_drv / (_hp_ma + norm_floor)
        elif theta_drive == "hp":
            # 原高通【不归一化】（用户 2026-10-15 指定）
            _drv = _hp_drv
        elif theta_drive == "hpn":
            # 原高通 + 归一化（对照组）
            _drv = _hp_drv / (B0k + norm_floor)
        elif theta_drive == "bpbn":
            # 【带通+归一化 2026-10-15】x = (LPF_fast(e_f^2) - LPF_slow(e_f^2))/(B0+eps)
            #   H(0)=0 => 稳态零均值 => 从源头消掉 K.9 的假直流，无需解耦 B。
            _drv = _bp_drv
        elif theta_drive == "bdecu":
            # 【K.9 修法验证 2026-10-15】B0 的时间常数与自适应 tau 解耦（固定 tau0）：
            #   x = (e_f^2 - B0)/(B0 + eps)。预期 E[x] -> 0，theta 通道假直流消失。
            _drv = (efk * efk - B0k) / (B0k + norm_floor)
        elif theta_drive == "abs":
            _drv = abs(_dev)
        elif theta_drive == "dev2":
            _drv = (efk - E0abs) ** 2
        elif theta_drive == "devsq":
            _drv = (abs(efk) - E0abs) ** 2
        elif law == "new":
            _drv = abs(_dev)
        elif law == "signed":
            _drv = _dev
        else:
            _drv = efk * efk
        # 【Q 驱动来源 2026-10-12 / 默认值 2026-10-13】q_drive="abs" = PPT 现行律：|e_f^2-E_o^2|
        #   （驱动恒<=0，稳态 Q 停在 1 以下）—— 现为【默认】；
        #   "signed" = 原律（供回归对账，与改动前逐位一致）
        # 【q_drive 三档 2026-10-13】devsq=(|e_f|-E_o)^2 = η2（PPT 最新律，默认）；
        #   abs=|e_f^2-E_o^2|（PPT 2026-10-12 版，用 --q-drive abs 可复现旧图）；
        #   signed=(e_f^2-E_o^2) 原律（仅回归对账，与改动前逐位一致）。
        if law in ("new", "signed"):
            if q_drive == "devsq":
                _drvq = (abs(efk) - E0abs) ** 2
            elif q_drive == "norm":
                # 【归一化驱动 2026-10-13】η2/(E_o²+floor)：把驱动的量纲尺度去掉，
                #   使 Q 的平衡点不再随误差幅值漂移（口径说明 §六 ★★★）。
                #   本配置 η2 均值≈715、E_o²≈713 ⇒ 比值≈1，与回复项 σ2*tau*atanh≈13.7 同量级。
                _drvq = (abs(efk) - E0abs) ** 2 / (E0sq + norm_floor)
            elif q_drive == "norm0":
                # 【零均值归一化驱动 2026-10-13】η₂ 减掉窗内均值（=D/T），使稳态驱动→0
                #   ⇒ 回复项自由把 Q 爬回 Q0（"缓慢恢复"）；突变时 η₂≫⟨η₂⟩ ⇒ 驱动>0 ⇒ Q 迅速下降。
                #   与 θ 通道的 e_f^2-E_o^2 完全对称（那个天然零均值）——这是两通道唯一的非对称之处。
                _drvq = ((abs(efk) - E0abs) ** 2 - Dval / max(T, 1e-12)) / (E0sq + norm_floor)
            elif q_drive == "lpf":
                # 【双时间尺度低通驱动 2026-10-13】drive = max(0, LPF_fast(η2) - k*LPF_slow(η2))
                #   稳态两路汇合 ⇒ drive≈0 ⇒ 回复项自由把 Q 爬回（"缓慢恢复"）；
                #   突变时 fast 先起 ⇒ drive>0 ⇒ Q 迅速下降。取正部保证单边（Q 不会越 1）。
                _eta2 = (abs(efk) - E0abs) ** 2
                _lpf_f += (1.0 - math.exp(-dt / max(lpf_fast * T, 1e-12))) * (_eta2 - _lpf_f)
                _lpf_s += (1.0 - math.exp(-dt / max(lpf_slow * T, 1e-12))) * (_eta2 - _lpf_s)
                _drvq = max(0.0, _lpf_f - lpf_k * _lpf_s)
            elif q_drive == "bnorm":
                # 【Q 驱动 · PPT 2026-10-14 新版律 B_κ】|e_f² − B_κ|/(B_κ + ε)
                #   绝对值保持单边 ⇒ Q 只被往下推（Q<2 域内），回复项 sigma2*atanh(1-Q) 负责爬回。
                #   分母用近期能量尺度 B（而非 E_o²）—— Q 的平衡点因此不再随误差幅值漂移。
                _drvq = abs(efk * efk - Bk) / (Bk + norm_floor)
            elif q_drive in ("ac", "acp"):
                # 【去整流 AC 驱动 2026-10-14】D = |x| − LPF_slow(|x|)，x = (e_f²−B)/(B+ε)
                #   病灶：Q 通道用 |x| 而 θ 通道用 x —— |x| 是零均值信号的【整流】，
                #         整流偏置 = 实测 0.5103（θ 侧只有 0.0015）⇒ 稳态恒正 ⇒ Q 被压死。
                #   本驱动把整流偏置减掉：稳态 |x|≈基线 ⇒ D≈0 ⇒ 回复项自由把 Q 拉回；
                #   突变期 |x| 远高于慢基线 ⇒ D>0 ⇒ Q 迅速下降（快速遗忘错误记忆）。
                #   ac  = 有符号（Q 可越过 1，需 qmax 兜住）
                #   acp = max(0,·)（保持单边 ⇒ PPT 的 V_dot_3 上界推导原样成立，代价是残余整流偏置）
                #   慢基线时间常数 = --lpf-slow 个周期 T。
                _dx = (efk * efk - Bk) / (Bk + norm_floor)
                _ax = abs(_dx)
                _ac_s += (1.0 - math.exp(-dt / max(lpf_slow * T, 1e-12))) * (_ax - _ac_s)
                _drvq = (_ax - _ac_s) if q_drive == "ac" else max(0.0, _ax - _ac_s)
            elif q_drive == "ac0":
                # 【常数基线 2026-10-15】D = |x| − c（**零滤波器**）—— 判定实验：
                #   若「去偏置」只需一个常数，则滤波器非必需；若跨工况失效，则滤波器是必需的。
                #   c 由 --ac-base 给定（默认 0.5103 = CLR 稳态实测均值）。
                _dx = (efk * efk - Bk) / (Bk + norm_floor)
                _drvq = abs(_dx) - ac_base
            elif q_drive == "acd":
                # 【周期延迟梳状陷波 2026-10-15】D = |x|(t) − |x|(t−T)
                #   动机：带通版 acb 的上截止 = 1/(2π·σ_f·T)；σ_f=1 时只有 1.59 Hz，
                #         对【真正的短事件】（如 dur2=0.1 s 的突变）会把它的能量滤掉 ⇒ 漏检。
                #   本式是【延迟线差分】，不是低通：
                #         H(s) = 1 − e^{−sT}  ⇒  在 s = j·2πk/T（含 k=0 的直流）处【精确置零】，
                #         其余频率全通（增益 ≤ 2）。
                #   而本系统的周期扰动恰是 T 的谐波（基波 1/T = 10 Hz 及 3、5 次）⇒
                #         **纹波被精确陷掉，直流（整流偏置）也被陷掉，任何非 k/T 频率的
                #           真实事件（含高频）一律通过** ⇒ 同时解决"抖动"和"漏检高频"。
                #   代价：依赖周期 T 的准确性（与 PPT 引入 LPF 的初衷相反，需实测权衡）。
                _dx = (efk * efk - Bk) / (Bk + norm_floor)
                _drvq = abs(_dx) - axbuf[ip]
            elif q_drive == "acb":
                # 【带通瞬态检测驱动 2026-10-14】D = LPF_fast(|x|) − LPF_slow(|x|)
                #   与 ac 的唯一区别：快路先低通一次。ac 直接把 |x| 的高频全灌进 Q 通道，
                #   实测 μ=10 时 Q 在两个夹点间以 293 次/s 抖动（ΔQ_rms=0.0176）——
                #   那是数值开关，不是慢变工作点，论文里站不住（Lyapunov 推导假设光滑）。
                #   快路时间常数 = --lpf-fast 个周期 T（默认 5）；慢路 = --lpf-slow 个周期 T。
                #   两路在稳态汇合 ⇒ D→0 ⇒ Q 回 1；突变期快路先起 ⇒ D>0 ⇒ Q 下降。
                _dx = (efk * efk - Bk) / (Bk + norm_floor)
                _ax = abs(_dx)
                _lpf_f += (1.0 - math.exp(-dt / max(lpf_fast * T, 1e-12))) * (_ax - _lpf_f)
                _ac_s += (1.0 - math.exp(-dt / max(lpf_slow * T, 1e-12))) * (_ax - _ac_s)
                _drvq = _lpf_f - _ac_s
            elif q_drive == "bpbn":
                # 【带通+归一化 2026-10-15】与 theta 通道共用同一驱动（有符号带通）。
                _drvq = _bp_drv
            elif q_drive == "bpq":
                # 【PPT 原式 2026-10-15】Q_dot 的驱动 = A_f - A_l，A_f/A_l 是 e_f^2 的快/慢低通。
                #   与 acb 的关键区别：acb 建在 |(e_f^2-B)/(B+eps)| 上，PPT 要求建在 e_f^2 上。
                _drvq = _bp_f - _bp_s
            elif q_drive == "abs":
                _drvq = abs(_dev)
            else:
                _drvq = _dev
        else:
            _drvq = efk * efk
        # 【驱动死区 2026-10-12】稳态下 |e_f²−E_o²| 是不大但恒在的纹波，会让 θ/Q 一直微调
        #   => 长期窗出现残留纹波（实测 (3)vs(2) 长期 0.30×，即劣化 3.3 倍）。
        #   死区：|e_f²−E_o²| < dbz 时两个通道的驱动都置 0（自适应只在"真突变"时动作）。
        #   dbz=0（默认）= 关闭死区，行为与改动前逐位一致。
        # ================= 【decupled 新律 2026-10-16】Q 与 theta 驱动完全解耦 =================
        #   phi(x,c) = x - c*tanh(x/c);  E_o 用上面的周期累加器值（新定义：窗内 e_f^2 均值）
        #   r_th + tau_th*r_th_dot = phi(e_f^2/(E_o+eps), c1)   ->  D_th = phi(...,c1) - r_th
        #   r_Q  + tau_Q *r_Q_dot  = phi(e_f^2/(E_o+eps), c2)   ->  D_Q  = phi(...,c2) - r_Q
        #   死区：|D| < c 时该通道驱动置零（两通道的 c 相互独立）
        if law == "decupled":
            _arg = (efk * efk) / (E0sq + norm_floor)          # 原实参（保旧口径）
            _arg0 = (efk * efk - E0sq) / (E0sq + norm_floor)   # 零均值实参（本版对照用）
            def _phi(x, c):
                return x - c * math.tanh(x / c) if c > 0.0 else x
            _pt = _phi(_arg0, c1); _pq = _pt          # 三档统一用零均值实参，唯一差别=滤波器
            _rth = _pt + (_rth - _pt) * math.exp(-dt / max(tau_theta, 1e-12))
            _rq  = _pq + (_rq  - _pq) * math.exp(-dt / max(tau_q, 1e-12))
            _Dth = _pt - _rth; _Dq = _pq - _rq
            if c1 > 0.0 and abs(_Dth) < c1: _Dth = 0.0
            if c2 > 0.0 and abs(_Dq)  < c2: _Dq  = 0.0
            if drive_mode in ("bp", "bpn"):
                # === B 方案：驱动 = A_f - A_l（快慢低通之差，稳态趋零）===
                #   与 phi-r 的区别：这不是"两次滤波相减"，而是"两个不同时间常数的低通之差"，
                #   在突变期有值、稳态严格趋零 ⇒ theta/Q 只在事件期被泵浦，事后由回复项缓慢拉回。
                _Dth = _bp_f - _bp_s; _Dq = _bp_f - _bp_s
                if drive_mode == "bpn":
                    _Dth = _Dth / (B0k + norm_floor); _Dq = _Dq / (B0k + norm_floor)
                if c1 > 0.0 and abs(_Dth) < c1: _Dth = 0.0
                if c2 > 0.0 and abs(_Dq)  < c2: _Dq  = 0.0
            if drive_mode in ("hp", "bpe"):
                # === 最优候选：归一到 E_o（离线统计：稳态均值 ~1e-2，唯一接近零均值的口径）===
                #   hp  = (e_f^2 - MA_T(e_f^2)) / (E_o + eps)   —— 高通 + 归一化（E_o）
                #   bpe = (A_f - A_l) / (E_o + eps)             —— 带通 + 归一化（E_o）
                #   MA_T 用与 E_o 同一个周期累加器 e2buf 实现（窗内 e_f^2 的算术均值）
                if drive_mode == "hp":
                    _ma = e2buf.sum() / len(e2buf)
                    _Dth = (efk * efk - _ma) / (E0sq + norm_floor)
                else:
                    _Dth = (_bp_f - _bp_s) / (E0sq + norm_floor)
                _Dq = _Dth
                if c1 > 0.0 and abs(_Dth) < c1: _Dth = 0.0
                if c2 > 0.0 and abs(_Dq)  < c2: _Dq  = 0.0
            if drive_mode == "direct":
                # 【无滤波】D = w = phi((e_f^2-E_o)/(E_o+eps), c) 直接用，不过任何低通
                _w0 = _phi((efk * efk - E0sq) / (E0sq + norm_floor), c1)
                _Dth = _w0; _Dq = _w0
            if drive_mode == "bpw":
                # === 本次方案：原律基础上把【高通】换成【带通】，保留归一化与死区 ===
                #   w = phi(e_f^2/(E_o+eps), c)  —— 归一化 + phi 压缩（与原律一致）
                #   两路低通：w_f (快, bpw_f*T)、w_l (慢, bpw_s*T)
                #   D = w_f - w_l                —— 带通，稳态严格趋零
                #   死区：|D| < c 时置零（θ 用 c1、Q 用 c2，各自独立）
                _pt0 = _phi((efk * efk - E0sq) / (E0sq + norm_floor), c1)   # 零均值实参
                if q_src == "e1":
                    # 【q_src=e1】Q 通道改由 e1 驱动：实参与归一化基准都换成 e1 自己的一套
                    #   （E1_o = 窗内 mean(e1^2)），下游带通/死区/回复项不变。
                    _e1o = e1sbuf[ip]
                    _e1n = e1k * e1k * dt
                    e1sbuf[ip] = _e1n
                    _acc1s += _e1n - _e1o
                    _E1sq = (_acc1s / T) if T > 0 else 0.0
                    _pq0 = _phi((e1k * e1k - _E1sq) / (_E1sq + norm_floor), c2)
                else:
                    _pq0 = _pt0
                _wfa += (1.0 - math.exp(-dt / max(bpw_fa * T, 1e-12))) * (_pt0 - _wfa)
                _wsa += (1.0 - math.exp(-dt / max(bpw_sa * T, 1e-12))) * (_pt0 - _wsa)
                _wfb += (1.0 - math.exp(-dt / max(bpw_fb * T, 1e-12))) * (_pq0 - _wfb)
                _wsb += (1.0 - math.exp(-dt / max(bpw_sb * T, 1e-12))) * (_pq0 - _wsb)
                _Dth = _wfa - _wsa; _Dq = _wfb - _wsb
                if qd_mode == 1 or qd_abs == 1:           # Q 驱动取绝对值
                    _Dq = abs(_Dq)
                elif qd_mode == 2:                         # Q 驱动单边死区 max(0,D)：只保留正向
                    _Dq = _Dq if _Dq > 0.0 else 0.0
                if qd_hp > 0.0:                           # Q 驱动改用高通 phi-r_Q
                    _rqh += (_pq0 - _rqh) * (1.0 - math.exp(-dt / max(qd_hp, 1e-12)))
                    _Dq = _pq0 - _rqh
                if qd_lpf > 0.0:                          # Q 驱动时间平均：消掉周期内变号
                    _dql += (1.0 - math.exp(-dt / max(qd_lpf * T, 1e-12))) * ((_wfb - _wsb) - _dql)
                    _Dq = _dql
                if dbias_tau > 0.0:                      # 驱动去均值（消直流偏置）
                    _dbm += (1.0 - math.exp(-dt / max(dbias_tau * T, 1e-12))) * ((_wfa - _wsa) - _dbm)
                    _Dth = _Dth - _dbm; _Dq = _Dq - _dbm
                if c1 > 0.0 and abs(_Dth) < c1: _Dth = 0.0
                if c2 > 0.0 and abs(_Dq)  < c2: _Dq  = 0.0
            _Dth = theta_sign * _Dth       # 符号开关：-1 = 事件期提带宽（在所有 drive 分支之后统一应用）
            # 【θ 单向死区 2026-10-17】theta_dz>0：Dθ=max(0,D)（负向截断、驱动恒正，与 Q 同构）；
            #   theta_dz<0：Dθ=min(0,D)（只留负向，作对照）。theta_dz=0 逐位退化。
            if theta_dz > 0.0:
                _Dth = max(0.0, _Dth)
            elif theta_dz < 0.0:
                _Dth = min(0.0, _Dth)
            _drv = _Dth; _drvq = _Dq
            if q_mism > 0.0:
                # 【q_mism 记忆失配驱动】D_Q = |E_v(t) - E_v(t-T)| / (E_v(t-T) + eps)
                #   E_v = v^2 的 T 窗均值（滑动窗，不要求事件与窗边界对齐）。
                #   为什么用它替代 e_f / e1：e_f 只反映"能量变大"，e1 被 ESO 吸收后失聪；
                #   而"旧记忆 vs 当前需求"的失配才是回声重影的因果量，且天然双向（升/降都响应）。
                _v2d = vnew * vnew * dt
                _leave = vm_buf[ip]
                _drop = vm_old[ip]
                _vm_now += _v2d - _leave
                _vm_prev += _leave - _drop
                vm_buf[ip] = _v2d
                vm_old[ip] = _leave
                if q_mism_mode == "harm":
                    # 【谐波投影】A_k(t)=2|c_k|/N，c_k 为 v 在 k/T 上的滑动单周期相量；
                    #   H=sum A_k^2/2 即"周期分量能量"，再与一个周期前的 H 比。
                    _dv = vnew - vbuf[ip]
                    _hh = 0.0
                    for _k in range(3):
                        _qc[_k] += _dv * _ph[_k][ip]
                        _ak = 2.0 * abs(_qc[_k]) / nd
                        _hh += 0.5 * _ak * _ak
                    _old = qh_buf[ip]
                    qh_buf[ip] = _hh
                    _raw = abs(_hh - _old) / (_old + q_mism_eps)
                else:
                    _raw = abs(_vm_now - _vm_prev) / (_vm_prev + q_mism_eps)
                if q_mism_latch > 0.0:
                    # 【事件触发一次性遗忘】驱动过阈 -> 置位，Q 直接压到 latch 值并保持 q_mism_dur 个周期；
                    #   稳态低于阈值则完全不动作（不累积、不需要大 mu）。
                    if _raw > q_mism_c and _qml_t <= 0:
                        _qml_t = int(round(q_mism_dur * T / dt))
                    if _qml_t > 0:
                        _qml_t -= 1
                        _qml_force = q_mism_latch
                    else:
                        _qml_force = None
                    _drvq = 0.0
                else:
                    if q_mism_c > 0.0:
                        # 【死区+压缩】phi(x,c)=x-c*tanh(x/c)：稳态小偏差被压到 ~0，
                        # 事件期大偏差按 x-c 通过（与 §3.2 的 phi 同一函数）。
                        _raw = _raw - q_mism_c * math.tanh(_raw / q_mism_c)
                    _drvq = _raw
            _in_dz_new = (abs(_Dth) == 0.0)
        _in_dz = (dbz > 0.0 and abs(_dev) < dbz) and law != "decupled"
        if _in_dz:
            _drv = 0.0
            _drvq = 0.0
        # 回复项（PPT 第6页口径）：θ̇ 的回复项 = -σ1·sinh(κθ)，而 sinh(κθ) = τ/τ0 - τ0/τ。
        #   本文件把 σ1 定义在【秒】量纲上，故等价写法为  σ1·(τ - τ0²/τ)：
        #   一阶展开与 σ1(τ-τ0) 相同（既有调参不失效），但【对数对称】——
        #   τ>τ0 与 τ<τ0 的对数距离等权重，消掉线性版固有的向上偏置。
        #   signed 律（=PPT 律）用 sinh 版；其余律保持原线性版，回归对账不受影响。
        #   【与 PPT 的系数对应】PPT: θ̇ = γ/(2κτ²)(e_f²-E_o²) - σ1_ppt·sinh(κθ)，
        #   而 sinh(κθ) = ½(τ/τ₀ - τ₀/τ)（标准定义，注意 PPT 上写漏了 ½）。
        #   代码: -σ1_code·(τ - τ₀²/τ) = -2σ1_code·τ₀·sinh(κθ)
        #   ⇒ σ1_ppt = 2·σ1_code·τ₀ 。本 preset: σ1_code=8.5e6, τ₀=0.00125 ⇒ σ1_ppt=21250。
        _rest = (tk - tau0 * tau0 / tk) if law == "signed" else (tk - tau0)
        _sg = sig1 * (rml if (_in_dz and rml > 1.0) else 1.0)
        # [PPT 新版 2026-10-15] theta_dot 增益二选一：
        #   tau2 (旧) : gamma/(2*kappa*tau^2)               —— theta 越负增益越大（1/tau^2 放大）
        #   cosh2(PPT): gamma/(4*kappa*cosh^2(kappa*theta)) —— theta 越负增益越小
        _tk2 = (tk * tk) if tau2_mode == "live" else (tau0 * tau0)
        if theta_gain == "cosh2":
            _ch = math.cosh(kappa * thk)
            _gain = 1.0 / (2.0 * kappa * tau0 * _ch * _ch)
        else:
            _gain = 1.0 / (2.0 * kappa * _tk2)
        # [tau2-mode 2026-10-15] 1/tau^2 是个整流器：hp>0 时 tau 大 -> 权重被压缩、
        #   hp<0 时 tau 小 -> 权重被放大 => 负半周赢 => tau 被单向压到限幅下界。
        #   实测 E[hp]=+389 但 E[hp/tau^2]=-8.43e9（反号），corr(hp,1/tau^2)=-0.67。
        #   tau2_mode=tau0 把加权固定成 1/tau0^2，消掉该整流器。
        if law == "decupled":
            _chu = math.cosh(kappa * thk)
            # PPT 新律原式：gamma/(2*kappa*tau0*cosh^2) * D_th - sigma1*sinh(kappa*theta)
            dth = (gamma / (2.0 * kappa * tau0 * _chu * _chu)) * _drv - 2.0 * sig1 * tau0 * math.sinh(kappa * thk)
        else:
            dth = gamma * _gain * _drv - _sg * _g2t * _rest * _dfac
        if not adapt:
            thk = 0.0; tkn = tau0; Qkn = Q0
        elif k <= nwarm:
            tkn = tau0 * math.exp(kappa * thk); Qkn = Qk          # 冻结：保持不变
        else:
            thk = min(thmax, max(thmin, thk + dt * dth))                      # 限幅在 theta 上
            tkn = tau0 * math.exp(kappa * thk)
            if law == "decupled":
                # 【新律】Q_dot = -(mu/(2*tau0*cosh(kappa*theta)))*[1-(1-Q)^2]*D_Q + sigma2*atanh(1-Q)
                #   严格按原式：分母为 2*tau0*cosh(kappa*theta)（不含 eps、不含 tau 的时变值）
                _rtau = 1.0 if q_rest_tau == "none" else tau0
                dQ = (-(mu / (2.0 * tau0 * math.cosh(kappa * thk))) * (1.0 - (1.0 - Qk) ** 2) * _drvq
                      + sig2 * _rtau * 0.5 * math.log(max(2.0 - Qk, 1e-12) / max(Qk, 1e-12)))
            elif law in ("new", "signed"):
                # 【PPT 律】Q_dot = -(mu/(2*tau))*[1-(1-Q)^2]*(e_f^2 - E_o^2) + sigma2*tau*atanh(1-Q)
                # atanh(1-Q) = 0.5*ln((2-Q)/Q)：误差被拉大 -> Q 掉；误差归零 -> Q 缓慢拉回 1
                # 【2026-10-12 修正】此前 law="signed" 会掉进下面的旧律分支（θ 律换了、Q 律没换），
                #   与 PPT 不一致；现统一：new 与 signed 都走 PPT 的 Q 律。
                # 【2026-10-13】Q 回复项 tau 因子开关：tau≈tau0=1.25e-3，删掉 tau 等于回复力放大 ~800 倍。
                _rtau = 1.0 if q_rest_tau == "none" else tk
                dQ = (-(mu / (2.0 * tk)) * (1.0 - (1.0 - Qk) ** 2) * _drvq
                      + sig2 * _rtau * _dfac * 0.5 * math.log(max(2.0 - Qk, 1e-12) / max(Qk, 1e-12)))
            else:
                # 旧律：Q_dot = -(kappa*mu/(2*gamma))*[1-(1-Q)^2]*tau*theta_dot - sigma2*atanh(Q-1)
                _d = abs(dth) if Q_ABS else dth
                _g2 = (E0sq / eref2) if (e0norm and eref2 > 0) else 1.0
                if s2tau and tau0 > 0:
                    _g2 = _g2 * (tk / tau0)
                if s2pow > 0 and tau0 > 0:
                    _g2 = _g2 * (tk / tau0) ** s2pow
                dQ = (-(kappa * mu / (2.0 * gamma)) * (1.0 - (1.0 - Qk) ** 2) * tk * _d
                      - sig2 * _g2 * 0.5 * math.log(max(Qk, 1e-12) / max(2.0 - Qk, 1e-12)))
            # 【域保护 2026-10-12】atanh(1-Q) 在 Q→2 处发散（|1-Q|→1），故 Q 必须在
            #   求值前就被约束在 (1e-4, 2-1e-6)。注意：绝不能像早前那样去截断 log 的实参
            #   （max(2-Q,1e-12)）—— 那会把无穷回复力变成有限值，使 Q 越过 2 后驱动项系数
            #   Q(2-Q) 反号形成正反馈而失控（实测 |y|max=4.5e156）。钳 Q 则结构上不可能越界。
            if tau_lock_from > 0.0 and t[k - 1] >= tau_lock_from:
                thk = 0.0; tkn = tau0          # 【诊断】tau 硬锁在 tau0
            Qkn = min(qmx, (2.0 - 1e-6) if _qhard else float("inf"), max(qn_floor, Qk + dt * dQ))
            if q_mism_latch > 0.0 and _qml_force is not None:
                Qkn = min(Qkn, _qml_force)      # 【latch】事件置位期强制压低
            if ff_q > 0.0 and _fb_flush:
                Qkn = min(Qkn, ff_q)            # 【ff_q】清记忆同时把 Q 拉低，之后由回复项缓慢回升
            # 【影子状态】同样的动力学，但不做任何投影（qn_floor / qmx / thmax）
            R["_dth"][k] = dth                             # 【诊断】真实 dth
            R["_drv"][k] = _drv                            # 【诊断】真实驱动
            # 【影子状态】真正的不限幅演化：回复项用【自己的 theta_sh】计算
            _sh_ch = math.cosh(kappa * _thsh)
            _dthsh = ((gamma / (2.0 * kappa * tau0 * _sh_ch * _sh_ch)) * _drv
                      - 2.0 * sig1 * tau0 * math.sinh(kappa * _thsh))
            _thsh = _thsh + dt * _dthsh
            try:
                _Qsh = min(2.0 - 1e-6, max(1e-4, _Qsh + dt * dQ))   # 状态侧 Q：仅限 (0,2)
            except NameError:
                pass
        if mm_det > 0.0 and k > nvst + 200:
            _a = 1.0 - math.exp(-dt / max(mm_tau, 1e-9))
            for _i in range(3):
                _mm_e[_i] += _a * (abs(yn - _pred[_i]) - _mm_e[_i])
            _ratio = _mm_e[0] / max(min(_mm_e[1], _mm_e[2]), 1e-12)
            if _ratio > 1.0 / mm_ratio:
                _mm_n += 1
            else:
                _mm_n = 0
            if _mm_n >= mm_win:
                _mm_trig = True
                _mm_flip = (_mm_e[2] < _mm_e[1])
                _mm_n = 0
        if mm2 > 0.0 and k > nvst + 300:
            _mm2_ok = True
            _lo = min(_mm2e[1], _mm2e[2])
            if _mm2e[0] > mm2_ratio * max(_lo, 1e-15):
                _mm2n += 1
            else:
                _mm2n = 0
            if _mm2n >= mm2_win:
                _mm_trig = True
                _mm_flip = (_mm2e[2] < _mm2e[1])
                _mm2n = 0
        if _mm_trig:
            if _mm_flip:
                vnew = -vnew; vbuf *= -1.0          # 【MMAE】判为反相 -> 反相复位
            else:
                vnew = 0.0; vbuf[:] = 0.0           # 【MMAE】判为撤除 -> 清空
        R["_mm"][k] = 1.0 if _mm_trig else 0.0
        R["_fl"][k] = 1.0 if _fb_flush else 0.0
        R["y"][k] = yn; R["z1"][k] = z1n; R["z2"][k] = z2n; R["v"][k] = vnew
        R["u"][k] = un; R["e1"][k] = e1k; R["ef"][k] = efk; R["ia"][k] = _uef
        R["E0"][k] = E0sq; R["D"][k] = Dval
        R["th"][k] = thk; R["tau"][k] = tkn; R["Q"][k] = Qkn; R["B"][k] = Bk
        R["tau_state"][k] = tau0 * math.exp(kappa * _thsh)   # 状态侧 tau【不限幅】
        R["Q_state"][k] = _Qsh                               # 状态侧 Q【仅限 (0,2)】
        vbuf[ip] = vnew; axbuf[ip] = _ax_now; ip += 1
        if ip == nd:
            ip = 0
        yk, z1k, z2k, vk, uk, tk, Qk, Bk = yn, z1n, z2n, vnew, un, tkn, Qkn, _bn; B0k = _b0n
    return R


def phases(t, tsw=2.0, dur=1.0, t_step=0.0, ton=0.0, tsw2=0.0, dur2=0.1,
           tsust=0.0, dsust=0.0):

    """相位窗口【全部】相对 t_step / tsw 计算，不写死任何绝对时刻。
    教训：曾把 "阶跃后" 写死成 (2.3, tsw-0.2)，tsw 改小后窗口为空；
         又把 "稳态" 写死成 (0.75, ...)，时间轴压到 1 s 后同样为空 —— 故此处一律参数化，
         并在返回前检查空窗口，直接抛错而不是让 RMS 静默变成 nan。"""
    t_end = float(t[-1])
    w = [("阶跃暂态", (t > t_step) & (t < min(t_step + 0.05, tsw))),
         ("扰动初段", (t > max(t_step + 0.05, ton + 0.02)) & (t < tsw - 0.01)),
         ("突变中", (t > tsw + 0.01) & (t < tsw + dur)),
         ("恢复中", (t > tsw + dur + 0.01) & (t < min(tsw + dur + 0.2, t_end)))]
    _tmax = tsw + dur
    if tsw2 > 0.0:                      # 仅在启用第二段突变时才生成这两个窗口
        w += [("突变中2", (t > tsw2 + 0.01) & (t < tsw2 + dur2)),
              ("恢复中2", (t > tsw2 + dur2 + 0.01) & (t < min(tsw2 + dur2 + 0.3, t_end)))]
        _tmax = max(_tmax, tsw2 + dur2)
    w += [("长期", (t > max(t_end - 0.5, _tmax + 0.5)) & (t <= t_end))]
    for nm, m in w:
        if int(np.sum(m)) < 10:
            _tmax = max(tsw + dur, (tsw2 + dur2) if tsw2 > 0 else 0.0,
                         tsust if dsust > 0 else 0.0, ton)
            raise ValueError(
                "相位窗口为空或过窄: %s\n"
                "  -> 最晚的事件在 %.4g s，长期窗还需其后 0.5 s，故 tend 至少要 %.4g s\n"
                "  -> 当前 tend = %.4g s。请把 --tend 调到 >= %.4g，或把 --tsw2/--tsust 等事件时间提前"
                % (nm, _tmax, _tmax + 1.0, t_end, _tmax + 1.0))
    return w


# ---------------------------------------------------------------- 图
def fig_adrc(t, r, dd, dstep, dnp, dp, A, Bn, par, out, tsw, dur, C=None, inset_win="", inset_ymin=0.0):
    """四栏 2x2 主图：① r/y 跟踪  ② 扰动分解  ③ v/z2 观测  ④ Q 与 tau/tau0 自适应量"""
    fig, axs = plt.subplots(2, 2, figsize=(15.6, 8.8), sharex=True,
                            gridspec_kw=dict(hspace=0.26, wspace=0.22))
    a0, a1, a2, a3 = axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]
    axall = list(axs.ravel())

    # ---- ① 输出响应 ----
    a0.plot(t, r, lw=1.3, color="#444", label=r"$r$ 阶跃指令")
    a0.plot(t, C["y"], lw=1.1, color="#16a085", alpha=0.9, label="普通 ESO（无重复控制）$y$")
    a0.plot(t, Bn["y"], lw=1.1, color="#1f6feb", alpha=0.85, label="无自适应 $y$")
    a0.plot(t, A["y"], lw=1.4, color="#c0392b", label="自适应 $y$")
    a0.set_ylabel(r"$r$ / $y$", fontsize=11)
    a0.legend(fontsize=8.6, loc="lower right", ncol=2)
    a0.set_title("一阶 ADRC  被控对象 $\\dot y = b u + d$",
                 fontsize=12, fontweight="bold")

    # 【内嵌放大】本栏纵轴被普通 ESO 的 ±4 撑满，(2)(3) 的差别只占 ~2% 高度，肉眼看不见 ——
    # 就在同栏左下角嵌一个只画 (2)(3) 的放大窗。
    # 【2026-10-11 修正】原来 xlim 取全程、ylim 取全程极值 => 只缩了时间没缩幅度，等于没放大。
    #   现在：窗口收到 [突变时刻 tsw, tsw+0.5 s]（可用 --inset-win a,b 覆盖），
    #         纵轴只按该窗内 (2)(3) 的数据定标 => 红蓝的差距才真正被放大出来。
    _iw = None
    if inset_win:
        try:
            _p = [float(x) for x in str(inset_win).replace("，", ",").split(",")]
            if len(_p) == 2 and _p[1] > _p[0]:
                _iw = (_p[0], _p[1])
        except ValueError:
            _iw = None
    if _iw is None:
        # 【2026-10-16 修正·定稿】默认窗取【末端收敛段】，而不是 (tsw, tsw+0.5)。
        #   为什么不再做「自适应找收敛点」：试过 min/max、稳健分位数、按跟踪偏差定标、
        #   后 40% 定标、末周期中位判收敛共 5 版，每版只挪一点点 —— 那是原地打转。
        #   本质问题是：慢系统（如 wo=40）在突变后很久才收敛，任何「包含突变又要看清细节」
        #   的窗都是自相矛盾的。inset 的职责是【放大看跟踪细节】，末端必然收敛、必然好看；
        #   突变响应由主图承担。要指定别的窗，用 --inset-win 起,止。
        _w = min(0.5, 0.25 * float(t[-1]))
        _iw = (float(t[-1]) - _w, float(t[-1]))
    _mk = (t >= _iw[0]) & (t <= _iw[1])
    if not np.any(_mk):
        _mk = np.ones_like(t, dtype=bool); _iw = (float(t[0]), float(t[-1]))
    # 【2026-10-16 修正】内嵌放大窗：恢复为「指令 r vs 三种 y」四条线对比（图二效果）
    #   旧改法（画 |y-1| 误差、框放大到 [0.28,0.12,0.58,0.60]）有两个毛病：
    #     (1) _lim 只取 e1/e2，没算 e3（普通 ESO）=> 青线尖峰被裁平；
    #     (2) 框太大且居中，与主图曲线打架、灰底压住内容。
    _C = C if C is not None else Bn
    # 【2026-10-16】内嵌窗：只画【自适应 vs 无自适应】两条线（去掉普通 ESO），
    #   并按两条线的实际量级定标 => 纵轴自动放大，红蓝分离可见。
    #   --inset-ymin 只作为【下界】：实际半幅 = max(该值, 两条线最大值 × 1.08)。
    axi = a0.inset_axes([0.28, 0.12, 0.58, 0.60])
    _e2 = np.abs(Bn["y"][_mk] - 1.0); _e1 = np.abs(A["y"][_mk] - 1.0)
    axi.plot(t[_mk], _e2, lw=1.0, color="#1f6feb", ls="--", label="无自适应 $y$")
    axi.plot(t[_mk], _e1, lw=1.3, color="#c0392b", label="自适应 $y$")
    axi.legend(fontsize=6.8, loc="upper right", framealpha=0.9)
    axi.set_ylabel(r"$|y-1|$", fontsize=7.5)
    _lim = max(float(_e1.max()), float(_e2.max())) * 1.08
    if inset_ymin > 0.0:
        _lim = max(_lim, float(inset_ymin))
    axi.set_ylim(-_lim, _lim)
    axi.axhline(0.0, color="k", lw=0.7, ls=":")
    axi.set_xlim(_iw[0], _iw[1])
    axi.axvspan(tsw, min(tsw + dur, _iw[1]), color="0.90", zorder=0)
    axi.axhline(1.0, color="0.55", lw=0.6, ls="-.")      # 终值参考线
    axi.grid(True, ls="--", lw=0.35, alpha=0.5)
    axi.tick_params(labelsize=5.8, length=2.0, pad=1.5)
    axi.set_ylabel("")
    for _sp in ("top", "right"):
        axi.spines[_sp].set_linewidth(0.7)
    axi.legend(fontsize=5.0, loc="lower right", framealpha=0.92, borderpad=0.28,
               labelspacing=0.24, handlelength=1.5, handletextpad=0.5)

    # ---- ② 扰动分解 ----
    a1.plot(t, dd, lw=0.9, color="#7f8c8d", label=r"$d$ 总扰动")
    a1.plot(t, dstep, lw=0.9, ls="--", color="#e67e22", label=r"$d_{step}$ 阶跃")
    a1.plot(t, dnp, lw=0.9, ls="--", color="#16a085", label=r"$d_{np}$ 非周期(0.7 Hz)")
    a1.plot(t, dp, lw=0.9, ls="--", color="#8e44ad", label=r"$d_p$ 周期(含突变)")
    a1.set_ylabel(r"扰动 $d$", fontsize=11)
    a1.legend(fontsize=8.2, loc="upper right", ncol=2)

    # ---- ③ v / z2 ----
    a2.plot(t, A["v"], lw=1.2, color="#8e44ad", label=r"$v$ 周期分量估计（自适应）")
    a2.plot(t, dp, lw=0.9, ls="--", color="#b3b3b3", label=r"$d_p$ 真值")
    a2b = a2.twinx()
    a2b.plot(t, A["z2"], lw=1.0, color="#e67e22", label=r"$z_2$ 残余总扰动")
    a2.set_ylabel(r"$v$", fontsize=11, color="#8e44ad")
    a2b.set_ylabel(r"$z_2$", fontsize=11, color="#e67e22")
    a2.legend(fontsize=8.4, loc="lower left")
    a2b.legend(fontsize=8.4, loc="upper right")

    # ---- ④ Q / tau ----
    _dt = float(t[1] - t[0])

    def sm(x):
        n = max(1, int(round(par["T"] / _dt))); h = n // 2
        xp = np.concatenate((np.full(h, x[0]), x, np.full(n - 1 - h, x[-1])))
        return np.convolve(xp, np.ones(n) / n, mode="valid")[:len(x)]

    # 【2026-10-16】右下栏：状态量与模型侧量同框
    #   Q（状态）与 Q'（模型侧，=clip(Q,[qmin,qmodel_max])）
    #   tau（状态）与 tau'（模型侧，=clip(tau,[taumin,taumax])*tau0）
    _qs = A["Q_state"] if "Q_state" in A else A["Q"]
    _ts = (A["tau_state"] if "tau_state" in A else A["tau"]) / par["tau0"]
    _qlo = float(par.get("qmin", 0.2)) if par.get("qmin", 0.0) > 0 else 1e-4
    _qhi = float(par.get("qmodel_max", 0.0))
    if _qhi <= 0.0:
        _qhi = float(par.get("qmax", 2.0))
        if _qhi <= 0.0: _qhi = 1.0 - 1e-9
    _qhi = min(_qhi, 2.0 - 1e-6)
    _qs_clip = np.clip(_qs, _qlo, _qhi)
    _tlo = float(par.get("taumin", 0.2)) if par.get("taumin", 0.0) > 0 else 0.0
    _thi = float(par.get("taumax", 5.0)) if par.get("taumax", 0.0) > 0 else 1e9
    _ts_clip = np.clip(_ts, _tlo, _thi)
    a3.plot(t, sm(_qs), lw=1.0, color="#1f6feb", ls="--", label=r"$Q$（状态）")
    a3.plot(t, sm(_qs_clip), lw=1.7, color="#1f6feb", label=r"$Q'$（模型侧）")
    a3b = a3.twinx()
    a3b.plot(t, sm(_ts), lw=1.0, color="#27ae60", ls="--", label=r"$\tau/\tau_0$（状态）")
    a3b.plot(t, sm(_ts_clip), lw=1.7, color="#27ae60", label=r"$\tau'/\tau_0$（模型侧）")
    a3.set_ylabel(r"$Q$ / $Q'$", fontsize=10, color="#1f6feb")
    a3b.set_ylabel(r"$\tau/\tau_0$ / $\tau'/\tau_0$", fontsize=10, color="#27ae60")
    a3.legend(fontsize=7.4, loc="lower left")
    a3b.legend(fontsize=7.4, loc="upper right")
    a3.set_ylim(0.30, 1.05)                              # Q/Q' 的量程
    a3b.set_ylim(0.10, 8.0)                              # tau/tau' 量程（覆盖状态侧峰值）
    a3.set_xlabel("时间 (s)", fontsize=11)

    for ax in axall:
        ax.grid(True, ls="--", lw=0.5, alpha=0.6)
        ax.set_xlim(0, t[-1])
        ax.axvspan(tsw, tsw + dur, color="0.92", zorder=0)
        ax.axvline(tsw, color="k", lw=0.9, alpha=0.6)
        ax.axvline(tsw + dur, color="k", lw=0.9, alpha=0.6)
    _xs = par.get("xstart", 0.0)
    _xl = par.get("xlim", 0.0)
    if _xl > 0.0:                                   # 【x 轴显示上限】只裁显示范围，不改数据
        for ax in axall:
            ax.set_xlim(_xs, _xl)
    if _xs > 0:
        _m = t >= _xs
        for ax in axall:
            ax.set_xlim(_xs, (_xl if _xl > 0.0 else t[-1]))
            _ymin, _ymax = 1e30, -1e30
            for _ln in ax.get_lines():
                _yy = _ln.get_ydata()
                if len(_yy) == len(t):
                    _v = _yy[_m]
                    _v = _v[np.isfinite(_v)]
                    if len(_v):
                        _ymin = min(_ymin, float(np.min(_v))); _ymax = max(_ymax, float(np.max(_v)))
            if _ymin < _ymax:
                _pad = 0.08 * (_ymax - _ymin) if _ymax > _ymin else 1.0
                ax.set_ylim(_ymin - _pad, _ymax + _pad)
    fig.subplots_adjust(bottom=0.135)
    # 【2026-10-13 修】参数框自证：Q 下界必须打真实 qmin，不能写死 1e-4。
    #   原写法与同一行里的 "Qmin=%.3g" 自相矛盾 —— 终稿图上会同时出现 Qmin=0.2 与 Q in [1e-4, ...]，
    #   违反《错误记忆抑制_口径说明.md》第四节口径纪律第 4 条（参数框必须自证被改动的参数）。
    #   口径与 L182 的 qn_floor 保持一致：qmin>0 用 qmin，否则退回 1e-4。
    _qlo = float(par.get("qmin", 1e-4))
    if not (_qlo > 0.0):
        _qlo = 1e-4
    txt = (r"$b$=%.4g  $b_0$=%.4g（失配 %+.1f%%）  $\omega_o$=%g rad/s  $k_p$=%g   $T$=%g s (基波 %g Hz)"
           % (par["b"], par["b0"], 100 * (par["b0"] / par["b"] - 1), par["wo"], par["kp"],
              par["T"], 1.0 / par["T"]) + "\n"
           + r"$\beta_3$=%g  $\zeta$=%g  $\tau_0$=%.6g s  $Q_0$=%g  $\kappa$=%g  $\gamma$=%g  $\sigma_1$=%g  $\sigma_2$=%g  $\mu$=%g  q_drive=%s  Eo_def=%s  theta_drv=%s  Qrest=%s  restD=%s  Qmin=%.3g  Bfilt=%.3g  norm_floor=%.3g  lpfF=%.3g  lpfS=%.3g"
             % (par["beta3"], par.get("zeta", 0.0), par["tau0"], par["Q0"], par["kappa"], par["gamma"],
                par["sig1"], par["sig2"], par["mu"], par.get("q_drive","signed"), par.get("eo_def","meanabs"), par.get("theta_drive","auto"), par.get("q_rest_tau","tau"), ("on" if par.get("rest_d") else "off"), par.get("qmin", 1e-4), par.get("b_filt", 1.0), par.get("norm_floor", 1e-6), par.get("lpf_fast", 5.0), par.get("lpf_slow", 50.0)) + "\n"
           + "dt=%g s   tend=%g s   law=%s   tau/tau0 in [%s, %s]   Q in [%.3g, %s]（即 Q<2）"
             % (par["dt"], t[-1], par.get("law", "?"),
                ("%.3g" % par["taumin"]) if par.get("taumin", -1.0) > 0 else "auto",
                ("%.3g" % par["taumax"]) if par.get("taumax", 0.0) > 0 else "不限",
                _qlo,
                 ("2-1e-6" if par.get("qmax_eff", 0.0) > 1.99999 else "%.6g" % par.get("qmax_eff", 1.0 - 1e-9))))
    fig.text(0.5, 0.010, txt, ha="center", va="bottom", fontsize=8.2, linespacing=1.35,
             bbox=dict(fc="white", ec="0.75", alpha=0.95, pad=3.0))
    fig.text(0.998, 0.003, "生成时间 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             ha="right", va="bottom", fontsize=7.4, color="0.42")
    import time as _t
    for i in range(5):
        try:
            fig.savefig(out, dpi=165, bbox_inches="tight")
            # 只存 PNG（2026-10-19 约定）：不再生成 PDF
            break
        except OSError:
            if i == 4: raise
            _t.sleep(1.0)
    plt.close(fig)


# ---------------------------------------------------------------- 主程序
def main():
    ap = argparse.ArgumentParser(description="一阶ADRC重复控制RCESO对比图")
    ap.add_argument("--b", type=float, default=B_DEF)
    ap.add_argument("--b0", type=float, default=B0_DEF)
    ap.add_argument("--wo", type=float, default=WO_DEF,
                    help="ESO 带宽 (rad/s)。0 = 用 eso-ratio*wc；>0 则直接指定（此前该参数被覆盖、未接线）")
    ap.add_argument("--kp", type=float, default=KP_DEF,
                    help="控制增益。0 = 跟随 wc（一阶对象+纯P 下 kp=wc）；>0 则直接指定，"
                         "与 wc 解耦（ESO 带宽仍按 eso-ratio*wc 计算）。"
                         "【按用户要求默认已改为 10】注意：kp=10 会使重复通道环路增益 beta3/(1-Q)*b/kp "
                         "比 kp=50 时大 5 倍，实测长期改善为负（-177%% / -121%%），需同步缩小 beta3")
    ap.add_argument("--T", type=float, default=T_DEF)
    ap.add_argument("--zeta", type=float, default=ZETA_DEF)
    ap.add_argument("--beta3", type=float, default=BETA3_DEF)
    ap.add_argument("--tau", type=float, default=TAU0_DEF)
    ap.add_argument("--kappa", type=float, default=KAPPA_DEF)
    ap.add_argument("--Q0", type=float, default=Q0_DEF)
    ap.add_argument("--gamma", type=float, default=GAMMA_DEF)
    ap.add_argument("--sig1", type=float, default=SIG1_DEF)
    ap.add_argument("--sig2", type=float, default=SIG2_DEF)
    ap.add_argument("--mu", type=float, default=MU_DEF)
    ap.add_argument("--dt", type=float, default=DT_DEF)
    ap.add_argument("--tend", type=float, default=2.0, help="时间轴长度（默认 2.0s，容纳三段突变）")
    ap.add_argument("--tstep", type=float, default=0.0, help="参考阶跃时刻")
    ap.add_argument("--rstep", type=float, default=1.0, help="阶跃参考幅值 r（默认 1.0）")
    ap.add_argument("--tsw2", type=float, default=0.5, help="第二段突变起始时刻，0=不启用（默认 0.5s）")
    ap.add_argument("--dur2", type=float, default=0.1, help="第二段突变持续时间")
    ap.add_argument("--dsust", type=float, default=300.0, help="从 tsust 起叠加的持续周期扰动幅值，0=不加（默认 300）")
    ap.add_argument("--tsust", type=float, default=1.0, help="持续扰动起始时刻")
    ap.add_argument("--sust-dur", dest="sust_dur", type=float, default=0.0,
                    help="t>=tsust 起的持续扰动只持续多少秒；0（默认）=一直持续到 tend。")
    ap.add_argument("--xstart", type=float, default=0.0,
                    help="出图起点（秒）。用于剔除阶跃跟踪段，只显示稳态，例如 --xstart 0.1")
    ap.add_argument("--ton", type=float, default=0.0,
                    help="扰动引入时刻：t<ton 时扰动分量全为 0（默认 0 = 从 0 就有扰动）")
    ap.add_argument("--dscale", type=float, default=1.0,
                    help="扰动整体缩放倍数（对 d_step/d_np/d_p 同时生效，保持各分量比例）")
    ap.add_argument("--tsw", type=float, default=0.2, help="周期扰动突变起始时刻")
    ap.add_argument("--dur", type=float, default=0.05, help="突变持续时间")
    ap.add_argument("--dist-mode", choices=["amp", "delay", "amp_step", "dly_step"], default="amp",
                    help="amp/delay = 0.05 s 窗口内的瞬时突变（原工况）；"
                         "amp_step/dly_step = 【持续性】幅值/相位突变 —— 旧记忆从此永久错误，"
                         "才是检验『错误记忆抑制』的工况")
    ap.add_argument("--p-dly", type=float, default=0.25,
                    help="delay 模式下周期扰动的相位后移量（单位 T）。0.5=反相：旧记忆变成反向补偿，"
                         "是检验『错误记忆抑制』最狠的工况；0.25=四分之一周期（旧记忆仍约 70%% 同相）")
    ap.add_argument("--dist-amp", type=float, default=1.0, help="周期扰动基准幅值")
    ap.add_argument("--np-amp", type=float, default=0.3, help="非周期扰动(0.7Hz)基准幅值；突变时同倍数放大")
    ap.add_argument("--jump-mult", type=float, default=300.0,
                    help="周期扰动突变倍数（突变后幅值 = 基准幅值 x 该倍数，默认 300 倍）")
    ap.add_argument("--wc", type=float, default=50.0,
                    help="系统闭环带宽 (rad/s)，取 50~100。一阶对象+纯P 下 wc 即 kp")
    ap.add_argument("--warm", type=float, default=2.0,
                    help="前 N 个周期冻结自适应（默认 2）。作用：① 阶跃/初段两窗里 (2)(3) 完全一致，"
                         "对比更干净；② 避开启动大误差把 tau 推向退化分支（warm=0 + gamma>=1e-9 实测触底）。"
                         "实测 warm>=4 会盖住第一段突变窗，排序反被破坏")
    ap.add_argument("--s2pow", type=float, default=0.0,
                    help="恢复项乘 (tau/tau0)^s2pow。0=原律, 1=tau, 2=tau^2")
    ap.add_argument("--s2tau", action="store_true",
                    help="恢复项乘 tau/tau0（使 Q 平衡点不随带宽漂移）。注意：需把 sig2 按标定工况折半" )
    ap.add_argument("--e0norm", action="store_true",
                    help="恢复项按 E0^2/Eref^2 归一化（E0^2 = 一个周期内 e_f^2 的均值）")
    ap.add_argument("--eref2", type=float, default=1.0,
                    help="E0^2 的标定参考值（标定工况下使因子=1，保证回归零风险）")
    ap.add_argument("--law", choices=["new", "ppt", "signed", "decupled"], default="signed",
                    help="自适应律形式。signed=【默认·= PPT 现行律】θ 通道驱动项取 e_f^2-E_o^2（带符号，"
                         "保留零均值性质 -> τ 不漂移），回复项用 sinh(κθ)（对数对称）："
                         "theta_dot=gamma/(2*kappa*tau^2)*(e_f^2-E_o^2)-sigma1*sinh(kappa*theta)；"
                         "Q 通道驱动项由 --q-drive 决定（默认 devsq）。"
                         "new=θ 通道驱动项取 |e_f^2-E_o^2|（非负，τ 不会跑向 0，但稳态被单向泵高）；"
                         "ppt=原律：驱动项仅 e_f^2，Q_dot 由 theta_dot 耦合驱动（仅用于回归对账）")
    ap.add_argument("--e1-src", choices=["estimation", "tracking"], default="estimation",
                    help="学习律驱动量 e1：estimation = y - z1（ESO 观测误差，与 PPT 第5页证明口径一致，默认）；"
                         "tracking = y - r（跟踪误差，旧实现，仅用于回归对账）")
    ap.add_argument("--mem-flush-auto", action="store_true",
                    help="在每个突变时刻(tsw/tsw2)清空重复通道记忆 v(t-T)，作为【理想遗忘】上界对照组，"
                         "并在汇总里给出『错误记忆抑制率』")
    ap.add_argument("--inset-ymin", dest="inset_ymin", type=float, default=0.0, help="inset y half-range; 0 = auto from data")
    ap.add_argument("--xlim", type=float, default=0.0, help="x 轴显示上限（0=自动取 t[-1]）")
    ap.add_argument("--inset-win", type=str, default="",
                    help="panel(a) 内嵌放大窗的时间范围 \"a,b\"（秒），例如 0.2,0.7。"
                         "默认 = 突变时刻 tsw 起 0.5 s；纵轴只按该窗数据定标（全程定标会把 (2)(3) 差别压没）")
    ap.add_argument("--tau-lock-from", type=float, default=0.0,
                    help="诊断用：从该时刻起把 tau 硬锁在 tau0（theta:=0），用于判定长期残差是否来自 tau 偏移。0=关")
    ap.add_argument("--q-drive", type=str, default="devsq",
                    choices=("signed", "abs", "devsq", "norm", "norm0", "lpf", "bnorm", "ac", "acp", "acb", "ac0", "acd", "bpbn", "bpq"),
                    help="Q 律驱动项。devsq=(|e_f|-E_o)^2 = η2（【默认·= PPT 第6页 2026-10-13 版】，"
                         "恒非负；配 V_dot_3 <= (1/4*tau)e_f^2 + (1/4*tau)E_o^2 的上界）；"
                         "abs=|e_f^2-E_o^2|（PPT 2026-10-12 版，供复现旧图）；"
                         "bnorm=|e_f^2-B_kappa|/(B_kappa+eps)（【PPT 2026-10-14 新版律】，"
                         "B 为 B+tau*B_dot=e_f^2 的一阶低通状态；分母换 B 后 Q 平衡点不随误差幅值漂移）；"
                         "ac=|x|-LPF_slow(|x|)（【去整流驱动 2026-10-14】，x=(e_f^2-B)/(B+eps)；"
                         "把 |x| 的整流偏置减掉 ⇒ 稳态驱动≈0 ⇒ Q 能爬回；突变期 |x| 高于慢基线 ⇒ Q 迅速下降。"
                         "慢基线时间常数用 --lpf-slow 个周期 T。acp = max(0,·) 版（保单边 ⇒ V_dot_3 上界原样成立）；"
                         "acb=LPF_fast(|x|)-LPF_slow(|x|)（【带通瞬态检测】，快路 --lpf-fast 个 T、慢路 --lpf-slow 个 T；先低通再做差 ⇒ 不把 |x| 的高频灌进 Q，消除夹点间抖动）；"
                         "signed=(e_f^2-E_o^2)（原律，供回归对账，与改动前逐位一致）")
    for _nm, _ds, _hl in (("--tau-B", "tau_B", "PPT: B_k + tau_B*B_k_dot = e_f^2 的时间常数，单位=周期 T（0=沿用 lpf_slow）"),
                          ("--tau-f", "tau_f", "PPT: A_f + tau_f*A_f_dot = e_f^2 的时间常数，单位=T（0=沿用 lpf_fast）"),
                          ("--tau-l", "tau_l", "PPT: A_l + tau_l*A_l_dot = e_f^2 的时间常数，单位=T（0=沿用 lpf_slow）")):
        ap.add_argument(_nm, dest=_ds, type=float, default=0.0, help=_hl)
    ap.add_argument("--theta-gain", dest="theta_gain", type=str, default="tau2", choices=("tau2", "cosh2"),
                    help="theta_dot 增益口径。tau2=gamma/(2*kappa*tau^2)（旧，theta 越负增益越大）；cosh2=gamma/(4*kappa*cosh^2(kappa*theta))（PPT 新版，theta 越负增益越小）")
    ap.add_argument("--hpma-win", dest="hpma_win", type=float, default=1.0,
                    help="[hpma] 归一化分母的窗口长度，单位=周期 T（默认 1.0）。1.0 与扰动同周期、仍相关；取 10~50 让分母远慢于分子。")
    ap.add_argument("--tau2-mode", dest="tau2_mode", type=str, default="live", choices=("live", "tau0"),
                    help="theta_dot 的 1/tau^2 加权口径（2026-10-15）。live=PPT 原式（默认，回归逐位不变）；tau0=固定 1/tau0^2，消掉整流偏置。")
    ap.add_argument("--b0-tau", dest="b0_tau", type=float, default=1.0,
                    help="【K.9 解耦修法 2026-10-15】B0 的时间常数 = b0_tau * tau0（固定，与自适应 tau 解耦）。"
                         "仅 --theta-drive bdecu 使用；默认 1.0。1.0 表示 B0 用标称带宽做低通。")
    ap.add_argument("--theta-drive", dest="theta_drive", type=str, default="auto",
                    choices=("auto", "signed", "abs", "dev2", "devsq", "norm", "bnorm", "bdiff", "bdecu", "bpbn", "hp", "hpn", "hpma"),
                    help="theta 通道驱动项（独立于 --law）。auto=跟随 --law（原行为，逐位不变）；"
                         "signed=e_f^2-E_o^2（【PPT 现行】恒零均值 -> tau 不漂移）；"
                         "abs=|e_f^2-E_o^2|；dev2=(e_f-E_o)^2；devsq=(|e_f|-E_o)^2；"
                         "norm=(e_f^2-E_o^2)/(E_o^2+norm_floor)（【PPT 2026-10-14 版】保持零均值的同时去尺度）；"
                         "bnorm=(e_f^2-B_kappa)/(B_kappa+norm_floor)（【PPT 2026-10-14 新版律 B】"
                         "用一阶低通状态 B 替代窗口均值 E_o，见 --preset blaw）。"
                         "后三者恒非负 -> theta 被单向泵高 -> tau 出现稳态偏置。"
                         "注意：换成非零均值驱动后，PPT 的 V_dot_2 精确式不再成立，须改写推导")
    ap.add_argument("--eo-def", dest="eo_def", type=str, default="meanabs", choices=("meanabs", "meansq"),
                    help="E_o（驱动能量的归一化基准）的定义口径，PPT 第6页。"
                         "meanabs=【默认·= PPT 现行定义】E_o=(1/T)*Integral[t-T,t]|e_f|dt，E_o^2=E_o**2；"
                         "meansq=【旧口径，供回归对账】E_o^2=(1/T)*Integral[t-T,t]e_f^2 dt（均方=RMS^2）。"
                         "两者由 Jensen 不等式分开，且 meanabs 会给 theta_dot 留下常值正偏置（tau 被抬高）")
    ap.add_argument("--q-rest-tau", dest="q_rest_tau", type=str, default="tau", choices=("tau", "none"),
                    help="Q 律回复项是否带 tau 因子。tau=+sigma2*tau*atanh(1-Q)（原行为，逐位不变）；"
                         "none=+sigma2*atanh(1-Q)（2026-10-13 用户要求：删掉 tau）。"
                         "注意：tau≈1.25e-3，删掉 tau 等于回复力放大 ~800 倍，Q 平衡点会被抬离限幅底，"
                         "需重新配合 --sig2 使用（原 sigma2=1e4 会过强）")
    ap.add_argument("--rest-d", dest="rest_d", action="store_true",
                    help="回复项乘以 D = ∫[t-T,t](|e_f|-E_o)^2 dt（PPT 第6页 2026-10-13 版）。"
                         "关闭（默认）= 回复项不乘 D，逐位不变。注意 D 是积分不是方差（T=0.1 时 D≈26*η2），"
                         "开启后回复力整体放大约 D 倍，且随误差离散度时变；需重标定 sigma1/sigma2")
    ap.add_argument("--lpf-fast", dest="lpf_fast", type=float, default=5.0,
                    help="q_drive=lpf 的快路低通时间常数（单位：个周期 T）。默认 5"
                         "（稳态与慢路汇合；突变时先起）")
    ap.add_argument("--lpf-slow", dest="lpf_slow", type=float, default=50.0,
                    help="q_drive=lpf 的慢路低通时间常数（单位：个周期 T）。默认 50 = 基线参考")
    ap.add_argument("--lpf-k", dest="lpf_k", type=float, default=1.0,
                    help="q_drive=lpf 的门限系数 k：drive=max(0, LPF_fast - k*LPF_slow)。"
                         "k>1 可压掉整流偏置（稳态 drive 的均值不再恒正）")
    ap.add_argument("--ac-base", dest="ac_base", type=float, default=0.5103,
                    help="q_drive=ac0 的常数基线 c（D=|x|-c，零滤波器）。默认 0.5103 = CLR 稳态实测 E|x|。"
                         "用于判定『去偏置是否只需一个常数』——跨工况测试会给出答案")
    ap.add_argument("--b-filt", dest="b_filt", type=float, default=1.0,
                    help="B 状态 (B+tau*B_dot=e_f^2) 的时间常数口径：B_dot=(e_f^2-B)/(tau/b_filt)。"
                         "1（默认）= 逐字实现 PPT 式(1)；取 --kappa 的值 = 试 B+(tau/kappa)*B_dot=e_f^2"
                         "（PPT 式(2) 写作 B_kappa 的下标读法）。仅 bnorm 驱动使用")
    ap.add_argument("--norm-floor", dest="norm_floor", type=float, default=1e-6,
                    help="归一化驱动 η2/(E_o²+floor) 的分母数值下限（防除零）。默认 1e-6"
                         "相对本配置的 E_o²≈713 可忽略；仅用于启动段 E_o²→0 时兜底")
    ap.add_argument("--qmin", type=float, default=0.2,
                    help="Q 的下界（默认 0.2 = 终稿口径；--preset mem_suppress 会锁回旧值 1e-4）。律在 |dev| 大时会把 Q 压死，故设下界保证记忆不被关闭")
    ap.add_argument("--theta-sign", dest="theta_sign", type=float, default=1.0,
                    help="【decupled 新律】theta 通道驱动符号：+1 原式（事件期 tau 升=降带宽）；-1 翻转（事件期 tau 降=提带宽）")
    ap.add_argument("--qd-mode", dest="qd_mode", type=int, default=0,
                    help="【bpw】Q 驱动口径：0=带符号(原) 1=|D|(绝对值) 2=max(0,D)(单边死区)")
    ap.add_argument("--qd-abs", dest="qd_abs", type=int, default=0,
                    help="【bpw】Q 驱动取绝对值（1=是）。|D|>=0，去符号来回，Q 只被""误差大""驱动")
    ap.add_argument("--qd-hp", dest="qd_hp", type=float, default=0.0,
                    help="【bpw】Q 驱动改用高通 phi-r_Q 的时间常数（s；0=用带通 D）。配合 --qd-mode 2 即【先高通再单向死区】")
    ap.add_argument("--qd-lpf", dest="qd_lpf", type=float, default=0.0,
                    help="【bpw】Q 驱动的时间平均时间常数（单位 T；0=不平均）。把周期内反复变号的 D_Q 平滑成活""动""的低频量")
    ap.add_argument("--dbias-tau", dest="dbias_tau", type=float, default=0.0,
                    help="【bpw】驱动去均值的时间常数（单位 T；0=不去均值）。把 D 减去其慢均值，消除直流偏置")
    ap.add_argument("--bpw-fast-a", dest="bpw_fa", type=float, default=1.0, help="【bpw】theta 通道带通快路时间常数（单位 T）")
    ap.add_argument("--bpw-slow-a", dest="bpw_sa", type=float, default=10.0, help="【bpw】theta 通道带通慢路时间常数（单位 T）")
    ap.add_argument("--bpw-fast-b", dest="bpw_fb", type=float, default=1.0, help="【bpw】Q 通道带通快路时间常数（单位 T）")
    ap.add_argument("--bpw-slow-b", dest="bpw_sb", type=float, default=10.0, help="【bpw】Q 通道带通慢路时间常数（单位 T）")
    ap.add_argument("--drive-mode", dest="drive_mode", type=str, default="phi",
                    choices=("phi", "bp", "bpn", "hp", "bpe", "bpw", "bpwd", "direct"), help="【decupled 新律】驱动口径：phi=phi(x,c)-r（原式）；bp=A_f-A_l（快慢低通之差，稳态趋零）；bpn=(A_f-A_l)/(B0+eps)")
    ap.add_argument("--c1", type=float, default=0.0, help="【decupled 新律】phi 的压缩尺度 c（同时是 theta 通道死区界；0=无死区，本版默认）")
    ap.add_argument("--c2", type=float, default=0.0, help="【decupled 新律】Q 通道死区界（0=无死区，本版默认）")
    ap.add_argument("--tau-theta", dest="tau_theta", type=float, default=5e-4, help="【decupled 新律】r_theta 滤波器时间常数（秒）")
    ap.add_argument("--tau-q", dest="tau_q", type=float, default=5e-3, help="【decupled 新律】r_Q 滤波器时间常数（秒）")
    ap.add_argument("--qmodel-max", dest="qmodel_max", type=float, default=0.0, help="【decupled 新律】模型侧 Q 上界（0=不限）")
    ap.add_argument("--qmax", type=float, default=2.0,
                    help="Q 的上界。<=0（默认）= 1-1e-9（与改动前逐位一致）；工程推荐 0.99；"
                         ">=1 = 放开内模稳定域（1e9 = 无上界），用于检验 Q>1 时 v 是否失控")
    ap.add_argument("--ret-mult", type=float, default=1.0,
                    help="死区内回复项倍数（需配合 --drv-dbz>0）：1=不变；>1 = 稳态把 tau 强制拉回 tau0")
    ap.add_argument("--drv-dbz", type=float, default=0.0,
                    help="自适应驱动死区 epsilon：|e_f^2-E_o^2| < epsilon 时 theta/Q 驱动置 0，"
                         "只让真突变驱动自适应。0（默认）= 关闭，行为不变")
    ap.add_argument("--taumax", type=float, default=2.0,
                    help="tau/tau0 硬上界（限在 theta 上），0=不限。实测 2 全场最优："
                         "突变中 -58.1%%->-24.2%%，长期 +43.7%%->+54.6%%")
    ap.add_argument("--taumin", type=float, default=0.5,
                    help="tau/tau0 下界（限在 theta 上）。-1 = 自动：新律取 1.0（带宽只降不升，"
                         "误差小时拉回初始值），原律取 0 = 不限；显式 0 = 关掉物理下界，"
                         "只留 1e-6 数值防除零（复现 tau→0 的退化分支用）。")
    ap.add_argument("--eso-ratio", type=float, default=4.0,
                    help="ESO 带宽 / 系统带宽 倍数，推荐 3~5")
    ap.add_argument("--dump-trace", dest="dump_trace", action="store_true",
                    help="额外写出 <prefix>_trace.npz（t/r/ef/B/tau/Q/th/y/u/v/E0/D 轨迹）。"
                         "默认关（行为不变）；供推导界 V_dot_2/V_dot_3 的逐点数值校验与事后诊断")
    ap.add_argument("--no-fig", action="store_true",
                    help="只算并写 *_summary.txt，不出图（调参扫描用，省掉 matplotlib 开销）")
    ap.add_argument("--prefix", type=str, default="adrc_eso")
    ap.add_argument("--preset", type=str, default="", choices=["", "mem_suppress", "final", "newlaw", "blaw"],
                    help="参数预设。final=【终稿配置】口径(law=signed / q_drive=abs / eo_def=meanabs) + 参数 + 工况(amp_step, dist-amp=300, jump-mult=0.0033, tend=4) 全部钉死，一条命令复现 PPT 第16页那张图，不会因默认值漂移而静默变口径；"
                         "mem_suppress=『错误记忆抑制』演示配置(2026-10-11 定稿，【已锁定旧口径 eo_def=meansq / q_drive=signed / qmin=1e-4 / qmax=0】，供回归对账)："
                         "kp=50 wo=300 beta3=16000 zeta=1 mu=1e-2 sig2=30 gamma=1e-10 sig1=1e6 tend=2 "
                         "e1src=estimation 并自动开 --mem-flush-auto。"
                         "只对本条命令生效；命令行里显式给出的同名参数会覆盖预设值。默认值一律不变")
    a = ap.parse_args()

    # ---- 预设应用：仅当 --preset 打开；命令行显式给出的参数优先（不动任何默认值）----
    _PRESETS = {
        "mem_suppress": {
            "kp": 50.0, "wo": 300.0, "beta3": 16000.0, "zeta": 0.2,
            "mu": 1e-2, "sig2": 30.0, "gamma": 1e-7, "sig1": 8.5e6,
            "tend": 2.0, "e1_src": "estimation",
            "law": "signed", "taumin": 0.5, "taumax": 2.0,
            "q_drive": "signed", "eo_def": "meansq", "qmin": 1e-4, "qmax": 0.0,
        },
        "final": {
            # 【2026-10-13】= PPT 第16页那张图的完整配置：口径 + 参数 + 工况 全钉死。
            #   用法：python adrc_eso_closed.py --preset final   （一条命令复现上图）
            "kp": 50.0, "wo": 300.0, "beta3": 16000.0, "zeta": 0.2,
            "mu": 3e-2, "sig2": 10000.0, "gamma": 1e-7, "sig1": 8.5e6,
            "tend": 4.0, "e1_src": "estimation",
            "law": "signed", "taumin": 0.5, "taumax": 2.0,
            "q_drive": "devsq", "eo_def": "meanabs", "qmin": 0.2, "qmax": 2.0,
            "dist_mode": "amp_step", "dist_amp": 300.0, "jump_mult": 0.0033,
        },
        "newlaw": {
            # 【2026-10-14 定稿】PPT 新版自适应律：
            #   θ 驱动归一化 (e_f^2-E_o^2)/(E_o^2+eps)、Q 回复项去掉 tau、回复力不乘 D  —— 全部采纳；
            #   【唯一保留的旧式】Q 的驱动不归一化（用 eta2 而非 eta2/(E_o^2+eps)）。
            #   实测依据：Q 驱动归一化会把 Q 的工作点从 0.33 抬到 0.99，"突变后忘记错误记忆"
            #   的能力消失 => 突变/恢复窗的 +82.2%/+79.2% 全部归零（四窗几何 2.86e-4 -> 6.76e-4）。
            #   本配置与旧终稿：CLR 四突变窗 (3)vs(2) 逐位相同、Q 轨迹完全相同，且修掉 tau 撞限幅。
            #   注意 sig2=12.5（不是 1e4）：Q 回复项去掉 tau 后量纲变了，sigma2_new = sigma2_old * tau0。
            #   用法：python adrc_eso_closed.py --preset newlaw
            "kp": 50.0, "wo": 300.0, "beta3": 16000.0, "zeta": 0.2,
            "mu": 3e-2, "sig2": 12.5, "gamma": 1e-7, "sig1": 8.5e6,
            "tend": 4.0, "e1_src": "estimation",
            "law": "signed", "taumin": 0.5, "taumax": 2.0,
            "q_drive": "devsq", "eo_def": "meanabs", "qmin": 0.2, "qmax": 2.0,
            "theta_drive": "norm", "q_rest_tau": "none", "norm_floor": 6.5,
            "dist_mode": "amp_step", "dist_amp": 300.0, "jump_mult": 0.0033,
        },
        "blaw": {
            # 【2026-10-14 新版律 · 用户 PPT 第6页新式】B + tau*B_dot = e_f^2 归一化。
            #   式(1)  B + tau*B_dot = e_f^2
            #   式(2)  theta_dot = gamma/(2*kappa*tau^2) * (e_f^2 - B_k)/(B_k + eps) - sigma1*sinh(kappa*theta)
            #   式(4)  Q_dot = -(mu/(2*tau))*[1-(1-Q)^2]*|e_f^2 - B_k|/(B_k + eps) + sigma2*atanh(1-Q)
            #   ⇒ 全部落为 --theta-drive bnorm --q-drive bnorm --q-rest-tau none。
            #   sig2=12.5（非 1e4）：式(4) 的回复项不带 tau，量纲变了 => sigma2_new = sigma2_old * tau0。
            #   eps = norm_floor = 6.5（≈1% × 典型 e_f^2 尺度；口径纪律见 --norm-floor）。
            #   用法：python adrc_eso_closed.py --preset blaw
            "kp": 50.0, "wo": 300.0, "beta3": 16000.0, "zeta": 0.2,
            "mu": 3e-2, "sig2": 12.5, "gamma": 1e-7, "sig1": 8.5e6,
            "tend": 4.0, "e1_src": "estimation",
            "law": "signed", "taumin": 0.5, "taumax": 2.0,
            "q_drive": "bnorm", "eo_def": "meanabs", "qmin": 0.2, "qmax": 2.0,
            "theta_drive": "bnorm", "q_rest_tau": "none", "norm_floor": 6.5,
            "b_filt": 1.0,
            "dist_mode": "amp_step", "dist_amp": 300.0, "jump_mult": 0.0033,
        },
    }
    if a.preset:
        _flag = {"kp": "--kp", "wo": "--wo", "beta3": "--beta3", "zeta": "--zeta",
                 "mu": "--mu", "sig2": "--sig2", "gamma": "--gamma", "sig1": "--sig1",
                 "tend": "--tend", "e1_src": "--e1-src",
                 "law": "--law", "taumin": "--taumin", "taumax": "--taumax",
                 "q_drive": "--q-drive", "eo_def": "--eo-def", "qmin": "--qmin", "qmax": "--qmax",
                 "dist_mode": "--dist-mode", "dist_amp": "--dist-amp", "jump_mult": "--jump-mult",
                 "theta_drive": "--theta-drive", "q_rest_tau": "--q-rest-tau", "norm_floor": "--norm-floor",
                 "b_filt": "--b-filt"}
        _argv = [x.replace("-", "") for x in sys.argv]
        _applied = []
        for _k, _v in _PRESETS[a.preset].items():
            if _flag[_k].replace("-", "") not in _argv:
                setattr(a, _k, _v); _applied.append(_k)
        if "--mem-flush-auto" not in sys.argv:
            a.mem_flush_auto = True; _applied.append("mem_flush_auto")
        print("[preset %s] 已应用：%s（命令行显式给出的参数不受影响）"
              % (a.preset, ", ".join(_applied)))

    # ---- 按带宽口径定参：一阶对象+纯P => 闭环带宽 = kp；ESO 带宽 = ratio * 系统带宽 ----
    if a.kp > 0:
        pass                      # 直接指定 kp（与 wc 解耦）
    else:
        a.kp = a.wc               # 一阶对象 + 纯 P：闭环带宽 = kp
    if a.wo > 0:
        pass                      # 直接指定 ESO 带宽
    else:
        a.wo = a.eso_ratio * a.wc
    # 周期通道环路增益上界：谐振增益 beta3/(1-Q) 乘 v->y 增益(≈ b/wc) 必须 < 1
    b3_bound = (1.0 - a.Q0) * a.wc / max(1e-12, a.b)
    par = dict(xstart=a.xstart, xlim=a.xlim, b=a.b, b0=a.b0, wo=a.wo, kp=a.kp,
               wc=a.wc, eso_ratio=a.eso_ratio, b3_bound=b3_bound, T=a.T, tau0=a.tau, Q0=a.Q0, kappa=a.kappa,
               gamma=a.gamma, sig1=a.sig1, sig2=a.sig2, mu=a.mu, beta3=a.beta3, 
               zeta=a.zeta,dt=a.dt, law=a.law, drv_dbz=a.drv_dbz, ret_mult=a.ret_mult, qmax=a.qmax, tau_lock_from=a.tau_lock_from, q_drive=a.q_drive, c1=a.c1, c2=a.c2, tau_theta=a.tau_theta, tau_q=a.tau_q, qmodel_max=a.qmodel_max, drive_mode=a.drive_mode, theta_sign=a.theta_sign, bpw_fa=a.bpw_fa, bpw_sa=a.bpw_sa, bpw_fb=a.bpw_fb, bpw_sb=a.bpw_sb, dbias_tau=a.dbias_tau, qd_lpf=a.qd_lpf, qd_abs=a.qd_abs, qd_mode=a.qd_mode, qd_hp=a.qd_hp, qmin=a.qmin, eo_def=a.eo_def, theta_drive=a.theta_drive, q_rest_tau=a.q_rest_tau, rest_d=a.rest_d, norm_floor=a.norm_floor, lpf_fast=a.lpf_fast, lpf_slow=a.lpf_slow, lpf_k=a.lpf_k, b_filt=a.b_filt, b0_tau=a.b0_tau, tau2_mode=a.tau2_mode, hpma_win=a.hpma_win, tau_B=a.tau_B, tau_f=a.tau_f, tau_l=a.tau_l, theta_gain=a.theta_gain, ac_base=a.ac_base,
               taumin=a.taumin, taumax=a.taumax,
               qmax_eff=((1.0-1e-9) if a.qmax==0.0 else (1e9 if a.qmax<0.0 else min(float(a.qmax), 2.0-1e-6))))
    t = np.arange(0.0, a.tend, a.dt)
    r = np.where(t >= a.tstep, a.rstep, 0.0)               # 阶跃输入（幅值 --rstep）
    _dsc = a.dscale
    _p_after = a.dist_amp * a.jump_mult
    dd, dstep, dnp, dp = disturbances(t, a.T, a.tsw, a.dur, a.dist_mode,
                                      step_t=a.tstep, p_amp=a.dist_amp, p_amp_after=_p_after,
                                      np_amp_after=a.np_amp * a.jump_mult, p_dly2=a.p_dly,
                                      tsw2=a.tsw2, dur2=a.dur2,
                                      dsust=a.dsust, tsust=a.tsust, sust_dur=a.sust_dur)

    if _dsc != 1.0:
        dd = dd * _dsc; dstep = dstep * _dsc; dnp = dnp * _dsc; dp = dp * _dsc
    if a.ton > 0.0:                       # t<ton 完全不引入扰动
        _m0 = (t >= a.ton)
        dd = np.where(_m0, dd, 0.0)
        dstep = np.where(_m0, dstep, 0.0)
        dnp = np.where(_m0, dnp, 0.0)
        dp = np.where(_m0, dp, 0.0)
    A = adrc_sim(t, r, dd, a.b, a.b0, a.wo, a.kp, a.T, a.zeta, a.beta3, a.tau,
                 a.kappa, a.Q0, a.gamma, a.sig1, a.sig2, a.mu, adapt=True,
                  warm=a.warm, taumax=a.taumax, vstart=a.ton, e0norm=a.e0norm, eref2=a.eref2, s2tau=a.s2tau, s2pow=a.s2pow, taumin=a.taumin, law=a.law, drv_dbz=a.drv_dbz, ret_mult=a.ret_mult, qmax=a.qmax, tau_lock_from=a.tau_lock_from, q_drive=a.q_drive, c1=a.c1, c2=a.c2, tau_theta=a.tau_theta, tau_q=a.tau_q, qmodel_max=a.qmodel_max, drive_mode=a.drive_mode, theta_sign=a.theta_sign, bpw_fa=a.bpw_fa, bpw_sa=a.bpw_sa, bpw_fb=a.bpw_fb, bpw_sb=a.bpw_sb, dbias_tau=a.dbias_tau, qd_lpf=a.qd_lpf, qd_abs=a.qd_abs, qd_mode=a.qd_mode, qd_hp=a.qd_hp, qmin=a.qmin, e1src=a.e1_src, eo_def=a.eo_def, theta_drive=a.theta_drive, q_rest_tau=a.q_rest_tau, rest_d=a.rest_d, norm_floor=a.norm_floor, lpf_fast=a.lpf_fast, lpf_slow=a.lpf_slow, lpf_k=a.lpf_k, b_filt=a.b_filt, b0_tau=a.b0_tau, tau2_mode=a.tau2_mode, hpma_win=a.hpma_win, tau_B=a.tau_B, tau_f=a.tau_f, tau_l=a.tau_l, theta_gain=a.theta_gain, ac_base=a.ac_base)
    Bn = adrc_sim(t, r, dd, a.b, a.b0, a.wo, a.kp, a.T, a.zeta, a.beta3, a.tau,
                  a.kappa, a.Q0, a.gamma, a.sig1, a.sig2, a.mu, adapt=False,
                  warm=a.warm, taumax=a.taumax, vstart=a.ton, e0norm=a.e0norm, eref2=a.eref2, s2tau=a.s2tau, s2pow=a.s2pow, taumin=a.taumin, law=a.law, drv_dbz=a.drv_dbz, ret_mult=a.ret_mult, qmax=a.qmax, tau_lock_from=a.tau_lock_from, q_drive=a.q_drive, c1=a.c1, c2=a.c2, tau_theta=a.tau_theta, tau_q=a.tau_q, qmodel_max=a.qmodel_max, drive_mode=a.drive_mode, theta_sign=a.theta_sign, bpw_fa=a.bpw_fa, bpw_sa=a.bpw_sa, bpw_fb=a.bpw_fb, bpw_sb=a.bpw_sb, dbias_tau=a.dbias_tau, qd_lpf=a.qd_lpf, qd_abs=a.qd_abs, qd_mode=a.qd_mode, qd_hp=a.qd_hp, qmin=a.qmin, e1src=a.e1_src, eo_def=a.eo_def, theta_drive=a.theta_drive, q_rest_tau=a.q_rest_tau, rest_d=a.rest_d, norm_floor=a.norm_floor, lpf_fast=a.lpf_fast, lpf_slow=a.lpf_slow, lpf_k=a.lpf_k, b_filt=a.b_filt, b0_tau=a.b0_tau, tau2_mode=a.tau2_mode, hpma_win=a.hpma_win, tau_B=a.tau_B, tau_f=a.tau_f, tau_l=a.tau_l, theta_gain=a.theta_gain, ac_base=a.ac_base)
    # 第三组：纯 ESO（beta3=0 => 周期通道 v 恒为 0，即不加重复控制的普通一阶 ADRC）
    C = adrc_sim(t, r, dd, a.b, a.b0, a.wo, a.kp, a.T, a.zeta, 0.0, a.tau,
                 a.kappa, a.Q0, a.gamma, a.sig1, a.sig2, a.mu, adapt=False,
                 warm=a.warm, taumax=a.taumax, vstart=a.ton, e0norm=a.e0norm, eref2=a.eref2, s2tau=a.s2tau, s2pow=a.s2pow, taumin=a.taumin, law=a.law, drv_dbz=a.drv_dbz, ret_mult=a.ret_mult, qmax=a.qmax, tau_lock_from=a.tau_lock_from, q_drive=a.q_drive, c1=a.c1, c2=a.c2, tau_theta=a.tau_theta, tau_q=a.tau_q, qmodel_max=a.qmodel_max, drive_mode=a.drive_mode, theta_sign=a.theta_sign, bpw_fa=a.bpw_fa, bpw_sa=a.bpw_sa, bpw_fb=a.bpw_fb, bpw_sb=a.bpw_sb, dbias_tau=a.dbias_tau, qd_lpf=a.qd_lpf, qd_abs=a.qd_abs, qd_mode=a.qd_mode, qd_hp=a.qd_hp, qmin=a.qmin, e1src=a.e1_src, eo_def=a.eo_def, theta_drive=a.theta_drive, q_rest_tau=a.q_rest_tau, rest_d=a.rest_d, norm_floor=a.norm_floor, lpf_fast=a.lpf_fast, lpf_slow=a.lpf_slow, lpf_k=a.lpf_k, b_filt=a.b_filt, b0_tau=a.b0_tau, tau2_mode=a.tau2_mode, hpma_win=a.hpma_win, tau_B=a.tau_B, tau_f=a.tau_f, tau_l=a.tau_l, theta_gain=a.theta_gain, ac_base=a.ac_base)
    # 第四组：理想遗忘 oracle —— 突变瞬间把记忆 v(t-T) 清零（自适应律要逼近的上界）
    _flush = [x for x in (a.tsw, a.tsw2) if x > 0] if a.mem_flush_auto else None
    D = None
    if _flush:
        D = adrc_sim(t, r, dd, a.b, a.b0, a.wo, a.kp, a.T, a.zeta, a.beta3, a.tau,
                     a.kappa, a.Q0, a.gamma, a.sig1, a.sig2, a.mu, adapt=False,
                     warm=a.warm, taumax=a.taumax, vstart=a.ton, e0norm=a.e0norm, eref2=a.eref2, s2tau=a.s2tau, s2pow=a.s2pow, taumin=a.taumin, law=a.law, drv_dbz=a.drv_dbz, ret_mult=a.ret_mult, qmax=a.qmax, tau_lock_from=a.tau_lock_from, q_drive=a.q_drive, c1=a.c1, c2=a.c2, tau_theta=a.tau_theta, tau_q=a.tau_q, qmodel_max=a.qmodel_max, drive_mode=a.drive_mode, theta_sign=a.theta_sign, bpw_fa=a.bpw_fa, bpw_sa=a.bpw_sa, bpw_fb=a.bpw_fb, bpw_sb=a.bpw_sb, dbias_tau=a.dbias_tau, qd_lpf=a.qd_lpf, qd_abs=a.qd_abs, qd_mode=a.qd_mode, qd_hp=a.qd_hp, qmin=a.qmin, e1src=a.e1_src, eo_def=a.eo_def, theta_drive=a.theta_drive, q_rest_tau=a.q_rest_tau, rest_d=a.rest_d, norm_floor=a.norm_floor, lpf_fast=a.lpf_fast, lpf_slow=a.lpf_slow, lpf_k=a.lpf_k,
                     memflush=_flush)

    # 【--dump-trace】把状态量落盘，用于推导上界 V_dot_2 / V_dot_3 的逐点校验（默认关）。
    if a.dump_trace:
        _tp = a.prefix + "_trace.npz"
        np.savez_compressed(_tp, t=t, r=r, dd=dd,
                            ef=A["ef"], B=A["B"], tau=A["tau"], Q=A["Q"], th=A["th"],
                            y=A["y"], u=A["u"], v=A["v"], E0=A["E0"], D=A["D"], z1=A["z1"], z2=A["z2"],
                            tau_state=A["tau_state"], Q_state=A["Q_state"], _dth=A["_dth"], _drv=A["_drv"],
                            tau0=a.tau, kappa=a.kappa, gamma=a.gamma, sig1=a.sig1,
                            sig2=a.sig2, mu=a.mu, norm_floor=a.norm_floor,
                            b_filt=a.b_filt, b0_tau=a.b0_tau, tau2_mode=a.tau2_mode, hpma_win=a.hpma_win, tau_B=a.tau_B, tau_f=a.tau_f, tau_l=a.tau_l, qmin=a.qmin, theta_drive=a.theta_drive,
                            q_drive=a.q_drive, c1=a.c1, c2=a.c2, tau_theta=a.tau_theta, tau_q=a.tau_q, qmodel_max=a.qmodel_max, drive_mode=a.drive_mode, theta_sign=a.theta_sign, bpw_fa=a.bpw_fa, bpw_sa=a.bpw_sa, bpw_fb=a.bpw_fb, bpw_sb=a.bpw_sb, dbias_tau=a.dbias_tau, qd_lpf=a.qd_lpf, qd_abs=a.qd_abs, qd_mode=a.qd_mode, qd_hp=a.qd_hp, q_rest_tau=a.q_rest_tau, dt=a.dt)
        print("OK -> %s （轨迹转储）" % _tp)
        np.savez_compressed(a.prefix + "_trace_no.npz", t=t, y=Bn["y"], tau=Bn["tau"], Q=Bn["Q"], ef=Bn["ef"],
                            v=Bn["v"], E0=Bn["E0"], th=Bn["th"], tau0=a.tau, dt=a.dt)
        print("OK -> %s_trace_no.npz （无自适应对照组）" % a.prefix)

    L = []
    L.append("=" * 92)
    L.append("一阶 ADRC 自适应 vs 无自适应     生成时间 %s"
             % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    L.append("=" * 92)
    L.append("命令行： %s" % (" ".join(sys.argv[1:]) if len(sys.argv) > 1 else "(无参数，全部使用默认值)"))
    L.append("被控对象： y_dot = b*u + d,   b=%.4g      时间轴 0~%g s，阶跃 @ t=%g s"
             % (a.b, a.tend, a.tstep))
    L.append("扰动构成： [整体 x%g]  d = d_step(0.5 @ t=%gs) + d_np(%.3g @ 0.7Hz) + d_p(周期 %gs, %s)"
             % (a.dscale, a.tstep, a.np_amp, a.T, ("[%g,%g]s 幅值由 %.4g 跳到 %.4g（%.0f 倍）" % (a.tsw, a.tsw + a.dur, a.dist_amp, _p_after, a.jump_mult)) if a.dist_mode == "amp" else ("[%g,%g]s 延时跳到 0.25T" % (a.tsw, a.tsw + a.dur))))

    L.append("  注1：d_np 取 0.7 Hz —— 非基波整数倍，重复控制律无法抵消，只能靠 ESO 观测")
    L.append("  注2：突变时 d_np 与 d_p 【一起】按同倍数跳变（窗口 %.3g s）" % a.dur)
    L.append("  注3：扰动引入时刻 ton = %g s —— 此前【完全不引入扰动】" % a.ton)
    L.append("  注8：三段突变事件 —— ① [%g,%g]s  ② [%g,%g]s  ③ %g s 起持续扰动(幅值 %.4g)"
             % (a.tsw, a.tsw + a.dur, a.tsw2, a.tsw2 + a.dur2, a.tsust, a.dsust))
    if a.dsust > 0:
        L.append("  注7：持续扰动 [%g s 起，幅值 %.4g × 周期分量] —— 考察稳态下的永久性扰动变化"
                 % (a.tsust, a.dsust))
    if a.tsw2 > 0:
        L.append("  注6：第二段突变窗口 [%g, %g] s（持续 %g s）—— 用于考察稳态后再遇突变"
                 % (a.tsw2, a.tsw2 + a.dur2, a.dur2))
    L.append("  注5：重复通道投入时刻 vstart = %g s —— 此前 v 恒为 0，阶跃跟踪段三组完全一致" % a.ton)
    L.append("  注4：相位窗口径 —— '扰动初段' 仅 %g s（受 ton/tsw 间距限制，测的是通道建起瞬态）；"
             "'长期' 窗长 %.2f s = %.1f 个周期，才是真稳态口径"
             % (max(0.0, a.tsw - a.ton - 0.03), max(0.0, a.tend - max(a.tend - 0.5, a.tsw + a.dur + 0.5)),
                max(0.0, a.tend - max(a.tend - 0.5, a.tsw + a.dur + 0.5)) / a.T))
    L.append("控制器：【纯比例】u = (kp*(r-y) - z2 - v)/b0,  b0=%.4g（失配 %+.1f%%）"
             % (a.b0, 100 * (a.b0 / a.b - 1)))
    L.append("带宽设计：系统闭环带宽 wc = %g rad/s；kp = %g%s"
             % (a.wc, a.kp, "（与 wc 解耦，单独指定）" if abs(a.kp - a.wc) > 1e-12 else "（= wc）"))
    L.append("          ESO 带宽 wo = %g rad/s (= %.2f x wc) -> beta1=2*wo=%g, beta2=wo^2=%g"
             % (a.wo, a.wo / max(1e-12, a.wc), 2 * a.wo, a.wo * a.wo))
    L.append("          周期通道增益 beta3 = %g" % a.beta3)
    L.append("          [更正] 线性化估出的上界 (1-Q0)*wc/b = %.4g 已被实测【推翻】：tanh 饱和压住了" % b3_bound)
    L.append("                 有效增益。该上界仅作量级参考，不是硬约束（当前 beta3=%.4g）。" % a.beta3)
    L.append("自适应律：%s" % {"signed": "PPT 现行律（θ 驱动取 e_f^2-E_o^2；Q 驱动由 q_drive 决定）",
                              "new": "PPT 新图（θ 驱动取 |e_f^2-E_o^2|）",
                              "ppt": "PPT 原律（仅用于回归对账）"}.get(a.law, a.law))
    L.append("          学习律驱动量 e1 = %s"
             % ("y - z1（ESO 观测误差；与 PPT 第5页证明口径一致）" if a.e1_src == "estimation"
                else "y - r（跟踪误差；旧实现，仅用于回归对账）"))
    if a.law in ("new", "signed"):
        if a.eo_def == "meanabs":
            L.append("          E_o   = (1/T)*Integral[t-T, t] |e_f| dt（滑动窗长 = 一个周期 T = %g s）" % a.T)
            L.append("          E_o^2 = E_o**2   【PPT 现行定义】")
        else:
            L.append("          E_o^2 = (1/T)*Integral[t-T, t] e_f^2 dt（滑动窗长 = 一个周期 T = %g s）" % a.T)
            L.append("          （均方 = RMS^2 【旧口径，供回归对账】）")
        if a.law == "new":
            L.append("          theta_dot = gamma/(2*kappa*tau^2)*|e_f^2 - E_o^2| - sigma1*(tau - tau0)")
        else:
            L.append("          theta_dot = gamma/(2*kappa*tau^2)*(e_f^2 - E_o^2) - sigma1*(tau - tau0^2/tau)")
            L.append("                      = gamma/(2*kappa*tau^2)*(e_f^2 - E_o^2) - 2*sigma1*tau0*sinh(kappa*theta)"
                     "  【= PPT 的 -sigma1_ppt*sinh(kappa*theta)，sigma1_ppt = 2*sigma1_code*tau0】")
        L.append("          Q_dot     = -(mu/(2*tau))*[1-(1-Q)^2]*%s + sigma2*tau*atanh(1-Q)"
                 % {"devsq": "(|e_f| - E_o)^2", "abs": "|e_f^2 - E_o^2|",
                    "norm": "(|e_f| - E_o)^2 / (E_o^2 + %.3g)" % a.norm_floor,
                    "norm0": "((|e_f| - E_o)^2 - D/T) / (E_o^2 + %.3g)" % a.norm_floor,
                    "lpf": "max(0, LPF_{%gT}(eta2) - %g*LPF_{%gT}(eta2))" % (a.lpf_fast, a.lpf_k, a.lpf_slow)}.get(a.q_drive, "(e_f^2 - E_o^2)"))
    else:
        L.append("          theta_dot = gamma/(2*kappa*tau^2)*e_f^2 - sigma1*(tau - tau0)")
        L.append("          Q_dot     = -(kappa*mu/(2*gamma))*[1-(1-Q)^2]*tau*theta_dot - sigma2*atanh(Q-1)")
    L.append("          Q 律驱动项 q_drive = %s" % a.q_drive)
    L.append("          theta 驱动项 --theta-drive = %s（auto=跟随 law）" % a.theta_drive)
    L.append("          Q 回复项 tau 因子 --q-rest-tau = %s" % a.q_rest_tau)
    if a.rest_d and "D" in A:
        L.append("          回复力倍率 D（--rest-d on）= 均值 %.6g  最大 %.6g  末 %.6g"
                 % (float(A["D"].mean()), float(A["D"].max()), float(A["D"][-1])))
    L.append("          自适应参数： tau0 = %.6g s   kappa = %g   gamma = %g   sigma1 = %g   sigma2 = %g   mu = %g   Q0 = %g"
             % (a.tau, a.kappa, a.gamma, a.sig1, a.sig2, a.mu, a.Q0))
    _tmn_s = ("%.4g" % a.taumin) if a.taumin > 0 else "不限（自动，仅留 1e-6 数值下界）"
    L.append("          warm = %g 个周期（冻结自适应，避开启动暂态）；tau/tau0 上界 = %s，下界 = %s"
             % (a.warm, ("%.4g" % a.taumax) if a.taumax > 0 else "不限", _tmn_s))
    if a.law == "ppt":
        L.append("          旧律附加开关： e0norm=%s (eref2=%g)  s2tau=%s  s2pow=%g  Q_ABS=%s"
                 % (a.e0norm, a.eref2, a.s2tau, a.s2pow, Q_ABS))
    L.append("")
    L.append("【1】被控对象输出 y 的跟踪表现（r 为 0->%g 阶跃 @ t=%g s）" % (a.rstep, a.tstep))
    L.append("     组别        相位      误差RMS      误差峰值     稳态偏差     超调(最大y)")
    ph = phases(t, a.tsw, a.dur, a.tstep, a.ton, a.tsw2, a.dur2, a.tsust, a.dsust)
    res = {}
    for nm, R in (("(1)普通ESO", C), ("(2)无自适应", Bn), ("(3)自适应", A)):
        e = r - R["y"]
        res[nm] = {}
        for pn, m in ph:
            res[nm][pn] = (float(np.sqrt(np.mean(e[m] ** 2))), float(np.max(np.abs(e[m]))))
        L.append("     %-10s %-9s %-12.4g %-12.4g %-12.4g %.4f" % (
            nm, "阶跃暂态", res[nm]["阶跃暂态"][0], res[nm]["阶跃暂态"][1],
            float(np.mean((r - R["y"])[(t > max(a.tstep + 0.05, a.ton + 0.02)) & (t < a.tsw - 0.01)])),
            float(np.max(R["y"]))))
        for pn in [nm for nm, _ in ph if nm not in ("阶跃暂态",)]:
            L.append("     %-10s %-9s %-12.4g %-12.4g" % (nm, pn, res[nm][pn][0], res[nm][pn][1]))
    L.append("")
    L.append("【2】三组归因（相对 (1)普通ESO 的误差 RMS 改善，正=更好）")
    L.append("     相位      (1)普通ESO      (2)无自适应    (2)vs(1)     (3)自适应     (3)vs(1)     (3)vs(2)")
    for pn, _ in ph:
        r1 = res["(1)普通ESO"][pn][0]; r2 = res["(2)无自适应"][pn][0]; r3 = res["(3)自适应"][pn][0]
        L.append("     %-9s %-14.5g %-14.5g %-11s %-12.5g %-11s %s"
                 % (pn, r1, r2, "%+.1f%%" % (100 * (r1 - r2) / max(1e-15, r1)),
                    r3, "%+.1f%%" % (100 * (r1 - r3) / max(1e-15, r1)),
                    "%+.1f%%" % (100 * (r2 - r3) / max(1e-15, r2))))
    L.append("     说明：(2)vs(1) = 重复通道本身的贡献；(3)vs(2) = 自适应在重复通道之上额外贡献的")
    L.append("           (3)vs(1) = 相对纯 ESO 的总改善")
    L.append("")
    if D is not None:
        # 突变相关窗口（记忆被污染的那几段）
        _jw = [pn for pn, _ in ph if pn in ("突变中", "恢复中", "突变中2", "恢复中2")]
        def _mask(names):
            mk = np.zeros_like(t, dtype=bool)
            for pn, m in ph:
                if pn in names:
                    mk |= m
            return mk
        mk = _mask(set(_jw))
        J2 = float(np.sqrt(np.mean((r - Bn["y"])[mk] ** 2)))     # 无自适应：旧记忆直接污染
        J3 = float(np.sqrt(np.mean((r - A["y"])[mk] ** 2)))      # 自适应：Q/τ 抑制错误记忆
        J4 = float(np.sqrt(np.mean((r - D["y"])[mk] ** 2)))      # 理想遗忘 oracle：突变即清零
        L.append("【4】错误记忆抑制（设计初衷口径；统计窗 = 突变中/恢复中/突变中2/恢复中2 的并集）")
        L.append("     【口径说明】重复通道把上一周期学到的 v(t-T) 当补偿发出去；突变后这段记忆是【错的】，")
        L.append("       它的代价 = (2)无自适应 相对 (4)理想遗忘 的额外误差；(3)自适应要把它压回去。")
        L.append("     (2)无自适应 (旧记忆直通)   突变窗 RMS = %.5g" % J2)
        L.append("     (3)自适应   (Q/τ 抑制)      突变窗 RMS = %.5g   相对(2) 改善 %+.1f%%"
                 % (J3, 100 * (J2 - J3) / max(1e-15, J2)))
        L.append("     (4)理想遗忘 (突变即清零记忆) 突变窗 RMS = %.5g   相对(2) 改善 %+.1f%%  <- 上界"
                 % (J4, 100 * (J2 - J4) / max(1e-15, J2)))
        _ach = 100 * (J2 - J3) / max(1e-15, J2 - J4)
        L.append("     ⇒ 错误记忆抑制率 = [(2)-(3)]/[(2)-(4)] = %.1f%%   （100%% = 达到理想遗忘；≤0 = 自适应没帮上）"
                 % _ach)
        L.append("     逐窗明细（错误记忆只在前 1~2 个周期起作用，聚合会被长窗稀释）：")
        L.append("       窗口        (2)无自适应   (3)自适应     (4)理想遗忘   (3)vs(2)   (4)vs(2)[上界]")
        for _pn in ("突变中", "恢复中", "突变中2", "恢复中2"):
            _mk = dict(ph)[_pn]
            _a = float(np.sqrt(np.mean((r - Bn["y"])[_mk] ** 2)))
            _b = float(np.sqrt(np.mean((r - A["y"])[_mk] ** 2)))
            _c = float(np.sqrt(np.mean((r - D["y"])[_mk] ** 2)))
            L.append("       %-10s %-13.5g %-13.5g %-13.5g %+8.1f%% %+12.1f%%"
                     % (_pn, _a, _b, _c, 100 * (_a - _b) / max(1e-15, _a), 100 * (_a - _c) / max(1e-15, _a)))
        L.append("     参考：Q 轨迹 [%.3g, %.3g] 末 %.3g ；tau/tau0 轨迹 [%.4g, %.4g] 末 %.4g"
                 % (float(np.min(A["Q"])), float(np.max(A["Q"])), float(A["Q"][-1]),
                    float(np.min(A["tau"])) / a.tau, float(np.max(A["tau"])) / a.tau,
                    float(A["tau"][-1]) / a.tau))
    else:
        L.append("【4】错误记忆抑制：未启用 oracle（加 --mem-flush-auto 可给出抑制率）")
    L.append("")
    L.append("【3】观测与补偿")
    _va = float(np.sqrt(np.mean(A["v"] ** 2))); _da = float(np.sqrt(np.mean(dp ** 2)))
    L.append("     v 幅值 %.4g ，d_p 幅值 %.4g ，比值 %.2f" % (_va, _da, _va / max(1e-12, _da)))
    L.append("     【口径说明】v 需经 控制器->被控对象 才能作用到 y（该通道衰减约 %.1f 倍），"
             % (_va / max(1e-12, _da)))
    L.append("       故 v 幅值约为 d_p 的该倍数才是【正确量级】，不能把 v 与 d_p 直接相减当残差。")
    L.append("       周期扰动是否被抵消，要看 y 的残差（见【1】），不是看 v 本身。")
    L.append("     z2 峰值 %.4g（含 d_np 与建模失配）" % float(np.max(np.abs(A["z2"]))))
    L.append("")
    L.append("【3b】E0^2 统计（用于标定 --eref2；当前 E_o 口径 = %s）" % a.eo_def)
    _e = A["E0"][t > max(a.tend - 0.5, a.tsw + a.dur + 0.5)]
    L.append("     E0^2 稳态均值 = %.6g   （当前 eref2 = %g，归一化%s）"
             % (float(np.mean(_e)) if len(_e) else 0.0, a.eref2,
                "开启" if a.e0norm else "关闭"))
    L.append("")
    L.append("【4】自适应量")
    L.append("     Q: [%.6f, %.6f] 末 %.6f      tau/tau0: [%.5f, %.5f] 末 %.5f"
             % (A["Q"].min(), A["Q"].max(), A["Q"][-1],
                (A["tau"] / a.tau).min(), (A["tau"] / a.tau).max(), A["tau"][-1] / a.tau))
    # 【B 状态 · PPT 2026-10-14 新版律】B + tau*B_dot = e_f^2 的一阶低通状态。
    #   只有 theta_drive/q_drive 取 bnorm 时它才参与律；否则恒为 e_f^2 的低通跟踪值。
    _bw = (t > max(a.tend - 0.5, a.tsw + a.dur + 0.5))
    L.append("     B (B+tau*B_dot=e_f^2, b_filt=%.4g): [%.5g, %.5g] 末 %.5g   稳态均值 %.5g"
             % (a.b_filt, float(A["B"].min()), float(A["B"].max()), float(A["B"][-1]),
                float(np.mean(A["B"][_bw])) if _bw.any() else 0.0))
    _bm = (t > a.tsw)
    L.append("     归一化驱动 (e_f^2-B)/(B+norm_floor=%.4g) 统计：均值 %.4g  最大值 %.4g"
             % (a.norm_floor,
                float(np.mean((A["ef"][_bm] ** 2 - A["B"][_bm]) / (A["B"][_bm] + a.norm_floor))) if _bm.any() else 0.0,
                float(np.max((A["ef"][_bm] ** 2 - A["B"][_bm]) / (A["B"][_bm] + a.norm_floor))) if _bm.any() else 0.0))
    L.append("")
    # 【口径纪律 7 · 2026-10-13】必须披露"Q 贴限幅底"的时长占比：
    #   只报 Q<0.01 占比只能证明"没被静音"，不能证明"自适应真的在工作"。
    #   实测终稿配置该占比 ≈81% —— 即驱动项形式此时根本不参与运算。
    _qfl = float(a.qmin) if float(a.qmin) > 0.0 else 1e-4
    _qm = (t > a.tsw)
    _qfrac = float((A["Q"][_qm] <= _qfl * (1.0 + 1e-9)).mean() * 100.0)
    L.append("     Q 贴限幅底占比 = %.1f%%（qmin=%.4g，统计窗 t>%.3g s）  【口径纪律 7：必须披露】"
             % (_qfrac, _qfl, a.tsw))
    L.append("     Q 自由区占比   = %.1f%%   （该窗 Q 均值 %.6f，Q0=%.4g）"
             % (100.0 - _qfrac, float(A["Q"][_qm].mean()), a.Q0))
    L.append("")
    L.append("【5】数值健康检查")
    ok = all(np.isfinite(A[k]).all() and np.isfinite(Bn[k]).all() for k in ("y", "z2", "v", "Q", "tau"))
    L.append("     全部状态量有限：%s" % ("是（稳定）" if ok else "否（发散）"))
    _tmn = float((A["tau"] / a.tau).min())
    L.append("     tau 下界检查：tau/tau0 最小 = %.5f -> %s"
             % (_tmn, ("正常（新律取 |e_f^2-E_o^2|，驱动项恒非负，τ 不会跌破 τ0）"
                       if (a.law == "new" and _tmn > 0.99) else
                       ("正常" if _tmn > 0.01 else "[警告] 已触底：请减小 --gamma 或加 --taumin 1"))))
    L.append("     |y|max = %.5g   |u|max = %.5g   |z2|max = %.5g"
             % (max(float(np.max(np.abs(A["y"]))), float(np.max(np.abs(Bn["y"])))),
                float(np.max(np.abs(A["u"]))), float(np.max(np.abs(A["z2"])))))
    open(a.prefix + "_summary.txt", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    if _HAS_MPL and not a.no_fig:
        fig_adrc(t, r, dd, dstep, dnp, dp, A, Bn, par, a.prefix + "_response.png", a.tsw, a.dur, C, a.inset_win, a.inset_ymin)
        print("\nOK -> %s_response.png / %s_summary.txt" % (a.prefix, a.prefix))
        # 额外产出"三种扰动独立图"：直接传入本脚本已算出的扰动数组，避免两处逻辑不一致
        try:
            import plot_dist3 as _d3
            if _d3.HAS_MPL and _d3.figure(t, dd, dstep, dnp, dp, a.prefix + "_dist3.png",
                                          a.T, a.dscale, a.jump_mult, a.tsw, a.dur,
                                          a.tsw2, a.dur2, a.ton):
                _m = np.max(np.abs(dd))
                print("OK -> %s_dist3.png（三种扰动独立图；d_step 峰值 %.4g / d_np %.4g / d_p %.4g / 合计 %.4g）"
                      % (a.prefix, float(np.max(np.abs(dstep))), float(np.max(np.abs(dnp))),
                         float(np.max(np.abs(dp))), float(_m)))
        except Exception as _e:
            print("  （三扰动独立图生成失败：%s）" % _e)


if __name__ == "__main__":
    main()