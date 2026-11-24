# 用厂家模块重建被控对象（WIP，2026-11-24）

目标：用 Simulink/Simscape 自带的 **PMSM** 与 **逆变器** 模块替换现有手搭 dq 对象。

## 已确认（本机 R2023b）

| 用途 | 库路径 | 备注 |
|---|---|---|
| PMSM（SPS 域） | `sps_lib/Electrical Machines/Permanent Magnet<换行>Synchronous Machine` | 名字含**换行符**，add_block 需 newline |
| 逆变器（开关级） | `sps_lib/Power Electronics/Universal Bridge` | 需 PWM 门极 |
| 直流母线 | `sps_lib/Sources/DC Voltage Source` | |
| powergui | `sps_lib/powergui` | SPS 域必需 |
| PMSM（Simscape 域） | `ee_lib/Electromechanical/Permanent Magnet/PMSM` | 物理端口 LConn/RConn |
| 平均逆变器 | `ee_lib/Semiconductors & Converters/Converters/Average-Value Voltage Source Converter (Three-Phase)` | 物理端口 |
| 求解器配置 | `nesl_utility/Solver Configuration` | Simscape 域必需 |

SPS PMSM 参数名：`Resistance / Inductance / Flux / PolePairs / Mechanical=[J F p] / MeasurementBus`。
本对象：R=0.175, L=0.57e-3, Flux=0.016833, p=4, J=1.89e-5, F=0。

## 方案 A（已选定）

SPS PMSM + **平均逆变器**，步长 1e-4（130 s ≈ 130 万步，单次 2–4 分钟）。
接口保持 `vq/vd → iq/id/ω`，直接替换 `b0_foc_m` 里手搭的对象。

## 待办

1. 连接 Simscape 物理端口：两个块各有 2 个 LConn + 2 个 RConn，需按端口标签确认
   （PMSM：三相 ~ / 机械 R；AVC：DC+ / DC- / 三相 ~ / 调制输入 m）
2. AVC 的调制输入是 PS 信号，需要 `Simulink-PS Converter` 把 1 ms 的 dq 电压转成 PS 量
3. 测量：`Current Sensor`(PS) + `PS-Simulink Converter` → idq；机械端 `Inertia` + `Rotational Sensor`
4. 接入 RCESO + `b0_ident_m`（1 ms），先开环验证 40 Hz ↔ 600 rpm，再闭环对表

## 已有脚手架

- `build_pmsm_v1.m` / `build_pmsm_v2.m`：SPS 域开环尝试（块路径已修正处见上表）
