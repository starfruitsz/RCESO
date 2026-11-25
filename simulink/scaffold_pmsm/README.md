# 厂家模块 FOC + b0 辨识

## 当前基线配置（pmsm_foc.slx）

| 项 | 值 |
|---|---|
| 注入幅值 amp | **0.05 pu**（原 0.118，burst 冲击太大） |
| b0 初值 / 限幅 | 536.4 / 300–900 |
| 起跑延时 t_start | 8 s |
| 速度环 kp | 0.4（1 kHz） |
| 电流环 | 20 kHz，θe = p·θm + π/2 |
| 求解步长 | 1e-5 |
| 负载 | 0.5 N·m（`TLf` 幅值 0 → 故障关闭） |
| b0 辨识输出 | 仅 `[b0, du]`（诊断输出已移除） |

基线实测（130 s）：转速 **599.8 rpm**、b̂₀ **545.1（+1.63%）**，仿真 20 s。

## 开关（用于实验）

| 目的 | 怎么改 |
|---|---|
| 开 10 Hz 故障扰动 | `TLf` 幅值 0 → **0.1**（= 0.5+0.1sin(2π·10t) N·m） |
| 严重 b0 失配 | `dB0` 初值 536.4 → **800**（并同步 `b0_ident_m` 的 `b0_init`） |
| 关闭辨识 | `b0_ident_m` 的 `upd_on` 1 → **0** |
| 换注入波形 | `wave` 0/1/2（正弦/方波/三角） |

## 已记录的坑

1. SPS PMSM 块名含换行：`...Permanent Magnet<newline>Synchronous Machine`
2. 物理端口必须用 PortHandles 连线
3. Bus Selector 信号名带空格括号（先读 InputSignals）
4. To Workspace 接总线 → `out.x.signals.values`（N×13，列 11=wm）
5. `Controlled Voltage Source` 是受控 AC 源（Frequency=0 才是直流）
6. **PMSM 的 Mechanical 参数必须显式设**（默认 J=0.0027，是 1.89e-5 的 143 倍；
   不设会让辨识"测出" b0≈3.75，其实辨识是对的）
7. MATLAB Function 块采样时间要用 `ch.ChartUpdate/ch.SampleTime`，`set_param` 无效
8. ESO 的 u 必须用注入后的 `u_act = u + du`
9. Park 约定：θe = p·θm + π/2（静止注入标定得出）
