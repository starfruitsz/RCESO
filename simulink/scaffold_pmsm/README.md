# 厂家模块被控对象（进行中）

## 已完成

- `pmsm_ol.slx`：**SPS 的 PMSM 模块 + 三个受控电压源（平均逆变器模型）**，1e-5 步长可运行
- PMSM 参数已映射：R=0.175 Ω，L=0.57 mH，ψ=0.016833 Wb，p=4，J=1.89e-5
- 机器自带测量总线直接给出 **id、iq、ωm、Te、θm**，省掉 Clarke/Park 测量链路：
  `Stator_current_is_d__A_` / `is_q` / `Rotor_speed_wm__rad_s_` / `Electromagnetic_torque_Te__N_m_`
- 电气端接线：受控源 LConn→PMSM LConn1..3，三个 RConn 互连成星点；机械端 Tm 接 Inport，总线出 Outport

## 待解决

1. **开环 V/f 未标定**：反电势 ψ·ωe = 0.016833×2π×40 ≈ **4.23 V**（峰值），
   当前给 4.8 V 仍出现反向旋转（−80 rpm）与 iq 6.6 A，说明相序/角度符号与机器约定不一致
2. 需按机器约定重定相序（A/B/C 相移 ±120°），或直接用 `Rotor_angle_thetam` 做闭环（不用 V/f 开环）
3. 下一步：**电流环 20 kHz**（dq PI + 反 Park 由 θe = p·θm 生成三相电压）→ 再加速度环 1 kHz + RCESO + b0_ident

## 采样配置（用户指定）

| 环 | 频率 | 步长 |
|---|---|---|
| 转速环 | 1 kHz | 1e-3 |
| 电流环 | 20 kHz | 5e-5 |
| 对象求解 | >50 kHz | **1e-5** |
