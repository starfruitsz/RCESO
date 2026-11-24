# 厂家模块 FOC + b0 辨识（已跑通 ✅）

## 最终结果（130 s，厂家 PMSM + 平均逆变器）

| 指标 | 值 |
|---|---|
| 转速 | **599.4 rpm**（稳态） |
| b̂₀ 终值 | **545.1**（真值 536.4，**+1.63%**） |
| bq 逐窗 | 中位 545.1（121603 样本，极稳定） |
| 仿真耗时 | **20.1 s / 130 s 物理时间**（1e-5 步长） |

## 根因链（按发现顺序）

1. **MATLAB Function 块跑在基速率**：必须 `ch.ChartUpdate='DISCRETE'; ch.SampleTime`，
   `set_param` 不支持 → 之前 burst 周期只有 0.25 s（应 5 s）
2. **ESO 的 u 要用注入后的 u_act = u + du**（幅频特性看输入 u）
3. **PMSM 块的 Mechanical 参数没设**：默认 J=0.0027，是我们的 143 倍！
   → 辨识测出 b0≈3.75 = 536.4/143，**辨识其实一直是对的**
   → 设 J=1.89e-5 后 b0 立刻回到 545.1

## 其余踩坑

- SPS PMSM 块名含换行：`...Permanent Magnet<newline>Synchronous Machine`
- 物理端口必须用 PortHandles 连线
- Bus Selector 信号名带空格括号（先读 InputSignals）
- To Workspace 接总线：`out.x.signals.values`（N×13，列 11=wm）
- `Controlled Voltage Source` 是受控 AC 源（Frequency=0 才是直流）
- Park 约定：**θe = p·θm + π/2**
- 速度环 kp=0.4（配 1.89e-5 惯量）；kp 取 75.36（dq 模型值）会剧烈振荡

## 与 dq 模型的差异

| 模型 | b0 | 误差 |
|---|---|---|
| dq（手搭） | 531.5~532.5 | −0.7~−0.9% |
| **厂家 PMSM + 平均逆变器** | **545.1** | **+1.63%** |

差 ~2.5%，可能来自厂家块的通量/转矩常数定义或电流环动态，值得进一步核对。
