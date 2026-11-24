# 厂家模块被控对象（进度）

## 已跑通

- `pmsm_ol.slx`：SPS PMSM + 三个受控电压源（平均逆变器），1e-5 步长可运行
- `pmsm_cc.slx`：在 ol 基础上加了 **20 kHz 电流环**（MATLAB Function `CC.m`：PI + 反 Park），
  机器测量总线 → Bus Selector 取出 `Rotor angle thetam (rad)` / `Stator current is_d (A)` / `is_q (A)`
- 关键踩坑记录：
  1. SPS 的 PMSM 块名含**换行**：`sps_lib/Electrical Machines/Permanent Magnet<newline>Synchronous Machine`
  2. 物理端口必须用 **PortHandles 连线**（`add_line(mdl, srcHandle, dstHandle)`），不能写 `blk/2`
  3. Bus Selector 的信号名带空格和括号：`Rotor angle thetam (rad)`，要用 `InputSignals` 读出来再设
  4. To Workspace 接总线时是 `out.mlog.signals.values`（N×13 矩阵），列序：
     a,b,c, **q(4)**, **d(5)**, Vq, Vd, hall×3, **wm(11)**, thetam(12), Te(13)

## 当前问题

**20 kHz 电流环一发散就 NaN**。最可能原因是 SPS PMSM 的 Park 约定与我的反 Park 不匹配
（块参数里有 `RefAngle = 90 degrees behind phase A axis (modified Park)`）。

## 下一步

1. 标定约定：只给 vd（vq=0）看 id/iq 的响应方向，必要时用 θe = p·θm ± π/2 或反号
2. 电流环降增益验证稳定性（Kp 7.2 → 2，Ki 2200 → 500）
3. 稳定后加 1 kHz 速度环 + RCESO + b0_ident，跑 130 s 与 dq 模型对表

## 采样（用户指定）

| 环 | 频率 | 步长 |
|---|---|---|
| 转速环 | 1 kHz | 1e-3 |
| 电流环 | 20 kHz | 5e-5 |
| 对象 | >50 kHz | 1e-5 |
