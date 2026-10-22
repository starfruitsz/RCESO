# -*- coding: utf-8 -*-
"""run_ppt_fig1.py —— PPT 图 1：纯 ESO（无重复通道）+ 类 fal 增益 应对角度锁相周期负载

工况（实验室档）：
    额定 600 rpm（10 Hz 机械转频），实验室噪声 3 rpm / 0.1 A / 0.01 N·m
    0–2 s   空载
    2–8 s   加载 0.50 额定（0.3185 N·m）
    2–8 s   叠加**角度锁相**周期分量：T(φ)=A·[sinφ+0.4sin3φ+0.2sin5φ]，T(φ)=T(φ+2π)，dφ/dt=ω
            A=0.1 N·m（峰值 ±0.1 N·m）
控制器：纯 ESO —— 重复通道关闭（beta3=0），无律 D / 无 F-B；ESO 增益取类 fal 默认档。

输出：_ppt_fig1.npz（t / TL / y / iq / iqr）、_ppt_fig1.json（指标）
"""
import json
import math

import numpy as np

from pmsm_inv_sim import sim_inv, I_BASE
import noise_cfg as NC

DT, TEND, TL0 = 2e-6, 8.0, 2.0
N_REF = 600.0
AMP_ANG = 0.1          # N·m 峰值
T_RATED = 0.637
NPROF = 4096


def profile_unit():
    """单位幅值、周期 2π 的角度表：sinφ + 0.4 sin3φ + 0.2 sin5φ（归一化到峰值 1）"""
    ph = np.linspace(0.0, 2 * math.pi, NPROF, endpoint=False)
    f = np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph)
    return f / np.max(np.abs(f))


def main():
    t = np.arange(0.0, TEND, DT)
    TL = (0.50 * (t >= TL0)).astype(float) * T_RATED       # 阶跃负载（时间域）
    cfg = dict(n_ref=N_REF, T=0.1, fci=500.0,
               beta3=0.0, tau0=20e-3,                    # 纯 ESO：重复通道关闭
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"],
               sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               seed_i=20261018,
               tl_ang=profile_unit(), tl_ang_amp=AMP_ANG, tl_ang_start=TL0,
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
    Y = sim_inv(t, TL, cfg)
    tt = Y["t"]
    e = (Y["y"] - 1.0) * N_REF
    np.savez("_ppt_fig1.npz", t=tt, TL=Y["tl"], y=Y["y"], iq=Y["iq"], iqr=Y["iqr"],
             ia=Y["ia"])
    m = (tt >= 4.0) & (tt < 8.0)
    m0 = (tt >= 7.0)
    out = dict(n_ref=N_REF, amp_ang=AMP_ANG, fci=500.0, beta3=0.0,
               steady_rms=round(float(np.sqrt(np.mean(e[m0] ** 2))), 2),
               load_rms=round(float(np.sqrt(np.mean(e[m] ** 2))), 2),
               iq_std=round(float(np.std(Y["iq"][m])), 3),
               iq_max=round(float(np.max(np.abs(Y["iq"][m]))), 2),
               iqr_max=round(float(np.max(np.abs(Y["iqr"][m]))), 2))
    json.dump(out, open("_ppt_fig1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
