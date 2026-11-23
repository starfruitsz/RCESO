# b0 辨识移植到 MATLAB 2018b Simulink（无 C 编译器）

## 为什么必须换实现

| 约束 | 后果 |
|---|---|
| **C Caller 模块 R2019b 才引入** | R2018b 里没有这个块，现有 `b0_foc2.slx` 无法搬 |
| **Simulink 不向下兼容** | R2023b 保存的 .slx 在 R2018b 打不开 |
| **目标机无 C 编译器** | 无法构建 MEX / 仿真目标 DLL |

改为 **MATLAB Function 块**：纯 .m，正常仿真由 Stateflow 解释执行，**不需要编译器**。

## 已验证等价

| 实现 | 平台 | b0 | 误差 |
|---|---|---|---|
| C Caller (`b0_ident_res`) | R2023b + MinGW | **531.55** | −0.90% |
| **MATLAB Function (`b0_ident_m`)** | R2023b | **531.84** | −0.85% |

真值 536.40；转速 600.00 rpm、注入 0.1180 两者一致。

## 迁移步骤

1. 把 `b0_ident_m.m` 和 `build_foc_m.m` 拷到目标机
2. 在 R2018b 里执行 `build_foc_m`，生成 `b0_foc_m.slx` 并自动跑 130 s
3. 或只取 `b0_ident_m.m`，粘进自己的 MATLAB Function 块

## 端口（采样时间 1 ms）

| 端口 | 方向 | 单位 | 说明 |
|---|---|---|---|
| iq | in | pu | 实测 q 轴电流（A ÷ 6.3069） |
| u | in | pu | 控制量，**延迟一拍**与 iq 对齐 |
| omega | in | rpm | 转速，仅诊断 |
| e1 | in | pu | 观测器误差 y − z1 |
| v | in | pu/s | 重复内模状态 |
| b0 | out | 标幺 | 初值 400 |
| du | out | pu | 注入量，内部生成 |

## R2018b 兼容性

全部使用的块（Sum / Gain / Product / Divide / Discrete-Time Integrator / Unit Delay /
Discrete Transfer Fcn / Trigonometric Function / Subsystem / Inport / Outport /
To Workspace / MATLAB Function）在 R2018b 中均存在。

**不需要**：C Caller、SimCustomHeaderCode、SimUserSources、Simulink.Bus、任何编译器。

## 关键实现点

1. 相位累加 `ph = ph + 0.065`，跨段不重置（保证两段同一绝对时钟）
2. 两段式：前 200 拍不注入、后 200 拍注入，各自单频复解调
3. 反演 `D = V + pd*E1`，pd = Sd + β1 + β2/Sd，β1=2ωo、β2=ωo²（δ=1）
4. **差分取模长** `bq = abs(num/den)` 而非实部——对相位误差免疫
5. 门控：平台 + 软底，d>dmax 时保持 dmax 处的权重
6. 低通 τ = kp/50 = 0.663 s
7. 冻结：24 个 burst（120 s）后取最近 4 次均值

## 定标点

| 参数 | 位置 | 说明 |
|---|---|---|
| 注入频率 | `cyc = 65*1e-3` | 须使 cyc*200 为整数（5 Hz 整数倍） |
| 注入幅值 | `amp = 0.118` | |
| 初始 b0 | `b0v = 400` | 改成你的标称值 |
| 限幅 | `b0lo/b0hi = 200/800` | |
| 观测器带宽 | `wo = 500` | 必须与模型 ESO 一致 |
| 转速环 kp | `kp = 75.36` | 决定低通时间常数 |

## 注意

- R2018b 的 MATLAB Function 块**正常仿真不需要编译器**；只有勾选加速/代码生成模式时才需要。
- 若要上 DSP，仍需在**有编译器的机器**上用 Embedded Coder 生成代码，或用已经验证的 C 版（`b0_ident.c`）。
