# -*- coding: utf-8 -*-
"""角度锁相周期负载 T(phi) —— 圆盘质量不对中模式。

物理口径
--------
本模式定名为「圆盘质量不对中模式」。圆盘质量不对中的转矩主特征是
转频 1 次分量；2--6 次分量用于表示盘面偏摆、间隙、非线性刚度等引起
的谐波调制。本模式保留 1--6 次，基波为主；按用户给定谐波比，
THD（2--6 次相对基波）为 77.46%，已超过上一版 30% 约束。

    T(phi) = T(phi + 2*pi),  dphi/dt = omega
    T_L    = T0 + A * disc_unbalance_profile(phi)

disc_unbalance_profile 返回按峰值归一化的表（max|T| = 1），因此
tl_ang_amp=A 是峰值转矩（N·m），不是基波幅值；基波幅值约为
A / 1.664 = 0.601A。实现入口见 pmsm_inv_sim.sim_inv 的 tl_ang /
tl_ang_amp / tl_ang_start 三个 cfg 字段。

当前系数（a1..a6）与 THD:
    a = (1.00, 0.55, 0.10, 0.45, 0.25, 0.15)
    THD = sqrt(sum_{n=2}^6 a_n^2) / a_1 = 77.46%
    （上一版 30% 约束不再满足；若需 30%，把 2--6 次整体乘 0.3873）
"""
import math

import numpy as np

# 模式名（写入元数据/文档时使用这一字符串）
MODE_NAME = "圆盘质量不对中模式"
MODE_ID = "disc_mass_misalignment"

# a_1 ... a_6, relative to the fundamental
HARMONICS = (1.00, 0.55, 0.10, 0.45, 0.25, 0.15)
THD_LIMIT = 0.30          # 上一版约束，仅保留作对照；当前型线不强制
NPROF = 4096


def thd(harmonics=HARMONICS):
    """Return THD = sqrt(sum_{n>=2} a_n^2) / a_1."""
    a = np.asarray(harmonics, dtype=float)
    if a.ndim != 1 or a.size < 2:
        raise ValueError("harmonics must be a 1-D sequence with at least 2 entries")
    if not np.all(np.isfinite(a)) or a[0] <= 0.0:
        raise ValueError("harmonics must be finite and a_1 must be positive")
    if np.any(a < 0.0):
        raise ValueError("harmonic amplitudes must be non-negative")
    return float(np.sqrt(np.sum(a[1:] ** 2)) / a[0])


def _raw_profile(phi, harmonics, phases=None):
    phi = np.asarray(phi, dtype=float)
    a = np.asarray(harmonics, dtype=float)
    if phases is not None:
        ph = np.asarray(phases, dtype=float)
        if ph.shape != a.shape:
            raise ValueError("phases must have the same length as harmonics")
    else:
        ph = np.zeros_like(a)
    f = np.zeros_like(phi)
    for n, (amp, phase) in enumerate(zip(a, ph), start=1):
        f += amp * np.sin(n * phi + phase)
    return f


def disc_unbalance_profile(n=NPROF, harmonics=HARMONICS, phases=None,
                           normalize=True):
    """Return the 圆盘质量不对中模式 torque table over [0, 2*pi).

    Parameters
    ----------
    n : int
        Number of samples. The table is indexed by mechanical angle modulo 2*pi.
    harmonics : sequence of float
        Amplitudes a_1..a_N. Defaults to the 1--6 order disc-unbalance profile.
    phases : sequence of float, optional
        Phase of each harmonic in radians. Defaults to zero for all orders.
    normalize : bool
        If True (default), divide by max|T| so the table peak is 1.
    """
    n = int(n)
    if n < 8:
        raise ValueError("n must be >= 8")
    phi = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    f = _raw_profile(phi, harmonics, phases)
    if normalize:
        peak = float(np.max(np.abs(f)))
        if not np.isfinite(peak) or peak <= 0.0:
            raise ValueError("profile has zero or non-finite peak")
        f = f / peak
    return f


THD = thd(HARMONICS)


if __name__ == "__main__":
    prof = disc_unbalance_profile()
    spec = np.fft.rfft(prof) / len(prof) * 2.0
    print("harmonics a1..a6 =", HARMONICS)
    print("THD = %.2f%% (old limit %.0f%%)" % (100.0 * THD, 100.0 * THD_LIMIT))
    if THD > THD_LIMIT:
        print("WARNING: current ratios exceed the old 30% limit")
    print("peak-normalized table: max|T| = %.6f" % np.max(np.abs(prof)))
    print("FFT amplitudes 1..8:",
          " ".join("%.4f" % abs(spec[k]) for k in range(1, 9)))
