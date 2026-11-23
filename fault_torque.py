# -*- coding: utf-8 -*-
"""fault_torque.py —— 两类机械故障的“绕轴负载转矩”解析模型（可移植）

物理口径见技术报告附录 A（转轴不对中）与附录 B（圆盘质量不平衡）。
两个函数都返回**绕实际旋转轴 Z 的负载转矩**（N·m，正方向与电磁转矩一致），
单位：theta rad、omega rad/s、质量 kg、长度 m、转矩 N·m。

模型（水平轴，重力沿 -Y）：
  不平衡：      T_u = -M g e sin(theta) + mu_b r_b M e omega^2 cos(theta)
  不对中：      T_m = -M g l sin(beta) sin(theta)
                      + (Hooke 联轴器可选) T0 * [ (1 - sin^2(beta) cos^2(theta))/cos(beta) - 1 ]
其中：
  * e 为质心偏心距（m）；对“圆盘 + 边缘质量 m0”有 e = m0 R / (M + m0)；
  * beta 为角不对中（rad），l 为质心沿几何轴到两轴交点的距离，故 d = l sin(beta)；
  * 第二项摩擦调制为二阶小量（mu_b、r_b 默认 0 即关闭）；
  * kappa 为**台架等效放大系数**：kappa=1 即物理值；由于物理量级只有 1e-4~1e-3 N·m，
    台架上要复现 0.05 N·m 级扰动必须用 kappa>>1，文档中必须注明“等效放大”。

注意：m e omega^2 是离心力（径向），不是绕轴转矩；不要把它当作 T 使用。
"""
import math

G = 9.80665


def unbalance_torque(theta, omega, M, e, kappa=1.0, mu_b=0.0, r_b=0.0, g=G):
    """圆盘质量不平衡的绕轴脉动转矩（N·m）。

    theta : 机械角 (rad)，以“偏心方向相对竖直向下”为相位零点
    omega : 机械角速度 (rad/s)
    M     : 转子质量 (kg)
    e     : 质心偏心距 (m)
    kappa : 等效放大系数（1=物理值）
    mu_b, r_b : 轴承摩擦系数与摩擦半径（默认 0，关闭摩擦调制项）
    """
    t = -M * g * e * math.sin(theta)
    if mu_b and r_b:
        t += mu_b * r_b * M * e * omega * omega * math.cos(theta)
    return kappa * t


def misalign_torque(theta, omega, M, beta, l, kappa=1.0,
                    T0=0.0, hooke=False, g=G):
    """转轴（角）不对中的绕轴脉动转矩（N·m）。

    theta : 机械角 (rad)
    omega : 机械角速度 (rad/s)
    M     : 转子质量 (kg)
    beta  : 角不对中 (rad)
    l     : 质心沿几何轴到两轴交点的距离 (m)，d = l sin(beta)
    kappa : 等效放大系数（1=物理值）
    T0    : 联轴器传递的名义转矩 (N·m)，仅 hooke=True 时用于 2× 调制
    hooke : True 时叠加 Hooke 联轴器的 2× 转矩调制
    """
    d = l * math.sin(beta)
    t = -M * g * d * math.sin(theta)
    if hooke and T0:
        cb = math.cos(beta)
        t += T0 * ((1.0 - math.sin(beta) ** 2 * math.cos(theta) ** 2) / cb - 1.0)
    return kappa * t


def parallel_torque(theta, omega, e, dk, kappa=1.0):
    """平行不对中的绕轴 2× 脉动转矩（N·m）。

    theta : 机械角 (rad)
    e     : 两轴平行偏移 (m)
    dk    : 联轴器径向刚度各向异性 |k_x - k_y| (N/m)
    kappa : 等效放大系数（1=物理值）

    模型：偏移矢量在联轴器坐标系中以 θ 旋转，弹性势能
          U(θ)=½e²(k_x cos²θ + k_y sin²θ) ⇒ T_θ=−∂U/∂θ=½e²(k_x−k_y) sin2θ。
    各向同性联轴器 dk=0 时无绕轴转矩纹波（只剩恒定径向力 F=k·e）。
    """
    return kappa * 0.5 * e * e * dk * math.sin(2.0 * theta)


def unbalance_force(omega, M, e):
    """离心力幅值（N），用于轴承/振动通道，不进入绕轴转矩。"""
    return M * e * omega * omega


def misalign_moment(omega, beta, It, Ip, M, l):
    """横向陀螺/弯曲力矩幅值（N·m），由轴承弯矩承担，不进入绕轴转矩。"""
    It_eff = It + M * l * l
    return abs(It_eff - Ip) * omega * omega * abs(math.sin(beta) * math.cos(beta))
