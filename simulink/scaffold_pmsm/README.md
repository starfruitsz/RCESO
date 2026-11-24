# 厂家模块 FOC 闭环（进度）

## 已完成 ✅

| 环节 | 频率 | 状态 |
|---|---|---|
| 对象 | 1e-5 | SPS PMSM + 平均逆变器（3 受控源） |
| 电流环 | 20 kHz | iq 跟踪 3.00 A、id 0.00 A |
| **速度环** | 1 kHz | **稳态 598.1 rpm（目标 600），iq 4.74 A，转矩 0.479 N·m（负载 0.5）** |
| b0 辨识 | — | 待接入（下一步） |

模型：`pmsm_foc.slx`（`build_pmsm_foc.m` + `wire_sl.m` 搭建）

## 现有问题

**启动超调大**：峰值 1165 rpm、iq 峰值 89 A。原因：kp=75.36 对 2 kHz 电流环偏大，
且没有参考斜坡/抗饱和。下一步调参（kp→30 或加斜坡）后再接辨识。

## 关键坑（SPS）

1. 块名含换行：`...Permanent Magnet<newline>Synchronous Machine`
2. 物理端口用 PortHandles 连线
3. Bus Selector 信号名带空格括号（先读 InputSignals）
4. To Workspace 接总线 → `out.x.signals.values`（N×13）
5. `Controlled Voltage Source` 是**受控 AC 源**（Frequency=0 才是直流）
6. 机械端口 Tm 正号会反向拖动
7. Park 约定：**θe = p·θm + π/2**（实测标定）
