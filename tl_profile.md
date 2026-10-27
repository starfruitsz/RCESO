# 角度锁相负载型线

## 圆盘质量不对中模式

- 英文标识：disc_mass_misalignment
- 代码入口：tl_profile.py
- 仿真入口：pmsm_inv_sim.sim_inv 的 tl_ang / tl_ang_amp / tl_ang_start
- 用途：模拟圆盘质量不对中引起的转频（1 次）及其 2–6 次谐波转矩脉动。

### 定义

    T(φ) = T(φ + 2π),   dφ/dt = ω
    T_L  = T0 + A · T̃(φ)

    T̃(φ) = Σ_{n=1}^{6} a_n sin(nφ) / max|Σ_{n=1}^{6} a_n sin(nφ)|

    (a1, a2, a3, a4, a5, a6) = (1.00, 0.55, 0.10, 0.45, 0.25, 0.15)

    THD = sqrt(a2² + a3² + a4² + a5² + a6²) / a1
        = 77.46%  （超过上一版 30% 约束）

### 说明

- 1 次转频分量为主；按给定顺序，3 次为 0.10、4 次为 0.45，2–6 次并非逐次递减；7 次及以上为 0。
- 表按峰值归一化（max|T̃| = 1），因此 tl_ang_amp 是峰值转矩（N·m），
  不是基波幅值；基波幅值约为 tl_ang_amp / 1.664 = 0.601 × tl_ang_amp。
- 该模式用于圆盘质量不对中工况；与旧的时间型 1/3/5 次不对中簇不是同一口径，
  数字不可混引。
- **约束冲突**：按给定比值 1.00/0.55/0.10/0.45/0.25/0.15，THD=77.46%，
  不再满足此前“≤30%”的要求。若仍要 ≤30%，保持 1 次为 1.00，
  把 2–6 次整体乘 0.3873，按同一顺序得到 0.2130 / 0.0387 / 0.1743 / 0.0968 / 0.0581。

### 用法

~~~python
from tl_profile import disc_unbalance_profile, MODE_NAME

cfg = dict(
    tl_ang=disc_unbalance_profile(),   # 单位峰值表，长度 4096
    tl_ang_amp=0.1,                    # 峰值转矩，N·m
    tl_ang_start=2.0,                  # 投入时刻，s
)
~~~

### 自检

~~~bash
python tl_profile.py
~~~

输出应为：THD = 77.46%，FFT 只有 1–6 次谐波（7 次及以上接近 0），
峰值归一化后 max|T| = 1。
