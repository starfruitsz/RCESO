# -*- coding: utf-8 -*-
"""噪声口径的单一入口：负载 / 电流 / 转速三路噪声都可调（后续优化用）
用法：
    from noise_cfg import NOISE, load_noise, sim_kwargs
    TL = base_TL + load_noise(n, dt, NOISE)          # 负载噪声（N·m）
    Y  = sim_dq(t, TL, dict(kw, **sim_kwargs(NOISE))) # 电流/转速噪声
"""
import math
import numpy as np

T_RATED = 0.637      # 额定转矩 (N·m)

# —— 三个可调旋钮（改这里即可，全项目统一口径）——
NOISE = dict(
    sig_i_A   = 0.2,    # 电流采样噪声 RMS (A)，d/q 各一路（旧 dq 模型用）
    i_noise_peak = 0.2, # dq 采样噪声峰值 (A，均匀分布)，真实逆变器模型 pmsm_inv_sim 用
    sig_n_rpm = 6.0,    # 转速采样噪声 RMS (rpm)：1% × 600 rpm
    sig_T_nm = 0.025,   # 负载转矩噪声 RMS (N·m)，真实对象默认口径
    sig_T_pct = 2.5,    # 旧口径：负载噪声 (% 额定)，仅旧模型/兼容保留
    fc_i   = 2000.0,    # 电流噪声带宽 (Hz)
    fc_n   = 200.0,     # 转速噪声带宽 (Hz)
    fc_T   = 200.0,     # 负载噪声带宽 (Hz)
    seed_i = 20261016,
    seed_q = 20261017,
    seed_n = 20261018,
    seed_T = 20261017,
)

# —— 三档噪声工况（2026-10-20 定义）——
# 实验室：转速 ≤0.5%（3 rpm）、电流 ≤0.1 A、转矩 ≤0.01 N·m
# 标准：  转速 =1%（6 rpm）、电流 0.2 A、转矩 0.025 N·m
# 恶劣：  转速 >2%（取 2.5%=15 rpm）、电流 >0.3 A（取 0.4）、转矩 >0.05 N·m（取 0.06）
NOISE_LAB = dict(i_noise_peak=0.1, sig_n_rpm=3.0, sig_T_nm=0.01)
NOISE_STD = dict(i_noise_peak=0.2, sig_n_rpm=6.0, sig_T_nm=0.025)
NOISE_HARSH = dict(i_noise_peak=0.4, sig_n_rpm=15.0, sig_T_nm=0.06)
PROFILES = {"lab": NOISE_LAB, "std": NOISE_STD, "harsh": NOISE_HARSH}

def band_noise(n, sigma, fc, dt, seed):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    a = 1.0 - math.exp(-2*math.pi*fc*dt)
    nk = max(1, int(math.ceil(6.0/(2*math.pi*fc*dt))))
    y = np.convolve(x, a*np.power(1.0-a, np.arange(nk)))[:n]
    return y/y.std()*sigma

def load_noise(n, dt, cfg=None):
    """负载转矩噪声，返回 N·m 数组（优先 sig_T_nm，兼容旧 sig_T_pct）"""
    c = dict(NOISE, **(cfg or {}))
    sig = c.get("sig_T_nm")
    if sig is None:
        sig = c["sig_T_pct"] / 100.0 * T_RATED
    return band_noise(n, float(sig), c["fc_T"], dt, c["seed_T"])

def sim_kwargs(cfg=None):
    """传给 sim_dq 的电流/转速噪声参数"""
    c = dict(NOISE, **(cfg or {}))
    return dict(sig_i=c["sig_i_A"], sig_n=c["sig_n_rpm"],
                seed_i=c["seed_i"], seed_q=c["seed_q"], seed_w=c["seed_n"])
