# -*- coding: utf-8 -*-
"""_probe_im_diff.py —— 单窗 vs 差分双窗（撞频免疫验证）2026-11-18"""
import numpy as np, math, json, glob
from pmsm_inv_sim import J_M, I_BASE, W_REF
from pmsm_inv_sim import sim_inv  # noqa
kap = 0.10 ** (0.75 - 1.0)
b1 = 2.0 * 500.0 * 1.0; b2 = 500.0 ** 2 * kap
zeta = 0.2
B0 = 1.2 * 0.101 * I_BASE / (J_M * W_REF)
b_true = B0 * J_M / 9.95e-5

def Pj(w): return complex(b2 - w * w, b1 * w)
def amp(xx, ph):
    n = len(xx); return (2.0 / n) * (np.sum(xx * np.cos(ph)) - 1j * np.sum(xx * np.sin(ph)))

for tag in ("auto", "20"):
    f = "_probe_im_%s.npz" % tag
    d = np.load(f); lg = d["lg"]
    tk, e1, v, z2, u, B0e, woe = (lg[:, i] for i in range(7))
    fd = float(np.asarray(d["fd"])[-1][1]); w = 2 * math.pi * fd
    dB = b_true - B0e[-1]
    def ham(ta, tb):
        m = (tk >= ta) & (tk < tb); ph = w * tk[m]
        E = amp(e1[m], ph); V = amp(v[m], ph); U = amp(u[m], ph)
        return V + Pj(w) / (1j * w) * E, U
    print("\n===== TAG=%s  fd=%.1f Hz  delta_b_true=%+.2f =====" % (tag, fd, dB))
    W = [(3.22, 3.40), (3.42, 3.60), (3.62, 3.80), (4.00, 4.20), (5.00, 5.20), (7.00, 7.20)]
    rows = []
    for (ta, tb) in W:
        dd, UU = ham(ta, tb)
        rows.append((ta, tb, dd, UU))
    print("  窗            |d^|      ang(U)    |U|    d^/U 单窗")
    for (ta, tb, dd, UU) in rows:
        print("  [%.2f,%.2f)  %9.3f  %+7.1f  %6.3f   %+9.2f" % (ta, tb, abs(dd), math.degrees(np.angle(UU)), abs(UU), (dd / UU).real))
    print("  --- 单窗均值(前两窗) : %+9.2f  (误差 %+6.2f%%)" % (np.mean([(r[2] / r[3]).real for r in rows[:2]]),
          100 * (np.mean([(r[2] / r[3]).real for r in rows[:2]]) / dB - 1)))
    offs = rows[2:]
    print("  --- 差分（每个 on 窗 对 各个 off 窗）---")
    for i in range(2):
        dd0, U0 = rows[i][2], rows[i][3]
        vals = []
        for (ta, tb, dd, UU) in offs:
            vals.append(((dd0 - dd) / (U0 - UU)).real)
        vals = np.array(vals)
        print("    on=[%.2f,%.2f)  差分估计 %s  均值 %+9.2f (误差 %+6.2f%%)"
              % (rows[i][0], rows[i][1], np.array2string(vals, precision=1), vals.mean(),
                 100 * (vals.mean() / dB - 1)))
