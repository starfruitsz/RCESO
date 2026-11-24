# -*- coding: utf-8 -*-
"""_bq_truth.py —— 用记录流自身反推物理增益 b（独立于辨识器）
原理：机械方程 ω̇ = b·i_q(pu) ⇒ 在注入频率上 ω(ω) = b·I_q/(j·2πf) ⇒ b = |ω_65|·2πf / |I_q,65|
"""
import numpy as np, scipy.io as sio
S = sio.loadmat('_bq_dump.mat')
t = S['t'].ravel(); iq = S['iq'].ravel(); u = S['u'].ravel(); om = S['om'].ravel()
F = 65.0; W = 2 * np.pi * F
om_pu = om / 600.0
print('%-8s %10s %10s %10s %10s %8s' % ('t_on', '|iq65|/pu', '|u65|/pu', '|w65|/pu', 'b(iq)', '相位/deg'))
bs = []
for k in range(0, 12):
    t0 = 3.2 + 5.0 * k
    m = (t >= t0) & (t < t0 + 0.2)
    if m.sum() < 150: break
    ph = np.exp(-1j * W * t[m])
    Q = 2.0 / m.sum() * np.sum(iq[m] * ph)
    U = 2.0 / m.sum() * np.sum(u[m] * ph)
    Om = 2.0 / m.sum() * np.sum(om_pu[m] * ph)
    b_iq = Om * 1j * W / Q if abs(Q) > 1e-9 else np.nan
    print('%-8.2f %10.3f %10.3f %10.4f %10.1f %8.1f'
          % (t0, abs(Q), abs(U), abs(Om), abs(b_iq), np.degrees(np.angle(b_iq))))
    if np.isfinite(b_iq): bs.append(abs(b_iq))
if bs:
    print('\n由 iq 反推的 b：中位 %.1f  范围 %.1f–%.1f  （名义 101.9）' % (np.median(bs), min(bs), max(bs)))
