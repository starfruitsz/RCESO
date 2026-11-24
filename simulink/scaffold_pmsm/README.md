# 厂家模块被控对象（进度）

## 已完成 ✅

| 项 | 状态 |
|---|---|
| SPS PMSM + 平均逆变器（3 受控源） | 可运行，1e-5 步长 |
| Park 角度约定标定 | **θe = p·θm + π/2**（静止注入扫描得出） |
| 20 kHz 电流环 | **iq 跟踪 3.00 A（误差<0.01），id = 0.00 A** |

### 标定数据（静止、1 V 电压矢量、J 临时加大）

| φ (deg) | id (A) | iq (A) | |I| |
|---|---|---|---|
| 0 | 0.01 | −5.71 | 5.71 |
| **90** | **5.71** | **−0.00** | 5.71 |
| 135 | 4.05 | 4.03 | 5.71 |
| 180 | 0.01 | 5.71 | 5.71 |

⇒ 机器 d 轴位于 phase-A 轴 **+90°**（与块参数 "RefAngle = 90 degrees behind phase A" 一致），
所以反 Park 用 `theta_e = p*thm + pi/2`。

## 关键坑

1. SPS PMSM 块名含换行：`...Permanent Magnet<newline>Synchronous Machine`
2. 物理端口用 PortHandles 连线
3. Bus Selector 信号名带空格括号，先读 InputSignals
4. To Workspace 接总线 → `out.x.signals.values`（N×13，列序见上）
5. **SPS 的 Controlled Voltage Source 是"受控 AC 源"**（Amplitude/Phase/Frequency 参数），
   不是瞬时电压源；Frequency 默认 0 = 直流量，做平均逆变器时须显式设 Frequency=0
6. 机械端口 Tm 是负载转矩，正号会反向拖动；标定时用大 J + Tm=0

## 下一步

1 kHz 速度环 + RCESO/ADRC，把 `b0_ident_m` 的 du 叠加到电流指令，跑 130 s 对表。
