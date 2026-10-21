# -*- coding: utf-8 -*-
"""律 F-B 的官方配置（2026-10-19 定稿）

用法：
    from fb_cfg import FB_NEW, FB_OLD
    Y = sim_dq(t, TL, dict(FB_NEW, **noise_cfg.sim_kwargs()))

FB_NEW：撤除事件的推荐配置（跟踪误差检测 + g 门控 + 绝对下限 + |v| 门控）。
        8 种子：首周期 10 Hz 51.7±5.7 rpm（无自适应 78.8±0.8），t=-13.5；
        跌落/稳态/峰值电流不劣化；代价：加载瞬态窗 +6.3 rpm。
FB_OLD：旧的 e1 残差检测（仅用于回归对账/历史复现），不要用于新结果。
"""
FB_NEW = dict(
    ff_flush=1.8, ff_tau_f=4e-3, ff_tau_s=0.5, ff_cool=0.3, det_eps=0.01,
    ff_src="et",      # 检测量 = 跟踪误差 1-y（旧版为 e1=y-z1）
    ff_gmax=0.05,     # 非周期能量门控（挡加载阶跃）
    ff_amin=0.09,     # 快包络绝对下限
    ff_vmax=20.0,     # 补偿 |v| 上限：只在补偿已塌陷时复位
)

FB_OLD = dict(
    ff_flush=1.8, ff_tau_f=4e-3, ff_tau_s=0.5, ff_cool=0.3, det_eps=0.01,
)

FB_OFF = dict(ff_flush=0.0)
