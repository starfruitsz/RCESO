# -*- coding: utf-8 -*-
"""drivetrain_inertia.py —— 传动链真实转动惯量折算（仿真用 J_true）

    J_true = J_motor
           + J_coupling
           + J_disc / n_gear^2
           + n_bearings * J_bearing / n_gear^2        （轴承若在低速侧）

其中圆盘（均质，半径 R_d，质量 M_d）：
    J_disc = 0.5 * M_d * R_d^2

注意：
  * ESO 的标称 b0 只用 J_nom（通常取电机转子 + 已标定的少量折算），
    真实 J_true 与 J_nom 的差作为扰动由 ESO 估计——不要把 J_true 写进 b0。
  * 齿轮箱减速比 n_gear = ω_motor / ω_load（>1 时负载惯量折算回电机轴要除以 n^2）。
"""
import math


def disc_inertia(mass, radius):
    return 0.5 * mass * radius * radius


def bearing_inertia(mass, r_in, r_out):
    """薄壁轴承套圈近似：J ≈ 0.5*m*(r_in^2 + r_out^2)。"""
    return 0.5 * mass * (r_in * r_in + r_out * r_out)


def j_true(j_motor=1.89e-5, j_coupling=0.0, disc_mass=0.0, disc_radius=0.0,
           n_gear=1.0, n_bearings=0, j_bearing=0.0):
    n2 = max(float(n_gear), 1e-9) ** 2
    return (j_motor + j_coupling + disc_inertia(disc_mass, disc_radius) / n2
            + n_bearings * j_bearing / n2)


if __name__ == "__main__":
    # 示例：电机 1.89e-5 + 联轴器 2e-6 + 圆盘（0.5 kg, R=50 mm）+ 2 个轴承
    jb = bearing_inertia(0.02, 0.010, 0.022)
    print("J_disc  = %.3e" % disc_inertia(0.5, 0.05))
    print("J_bear  = %.3e" % jb)
    print("J_true  = %.3e" % j_true(j_coupling=2e-6, disc_mass=0.5, disc_radius=0.05,
                                    n_bearings=2, j_bearing=jb))
