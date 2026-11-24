# -*- coding: utf-8 -*-
"""_inv_compare.py —— 对比两种反演：线性化 pd·E1  vs  精确 β1·SDFT(G1) + β2/Sd·SDFT(G2)"""
import numpy as np, scipy.io as sio
S = sio.loadmat('_bq_dump_fal.mat')
t = S['t'].ravel(); e1 = S['e1'].ravel(); v = S['v'].ravel()
u = S['u'].ravel(); q = S['iq'].ravel()
F = 65.0; W = 2*np.pi*F; dT = 1e-3
A, A1, DEL, LAM = 0.75, 1.0, 0.10, 10.0
B1, B2 = 1000.0, 250000.0        # 与 sim 一致：2*wo, wo^2
Sd = (np.exp(1j*W*dT) - 1.0)/dT
TRUE = 101.89
c2 = DEL*LAM**(-1/A); c1 = DEL*LAM**(-1/A1)
G1 = lambda e: (np.abs(e) + c1)**A1 * np.tanh(LAM*e/DEL)
G2 = lambda e: (np.abs(e) + c2)**A  * np.tanh(LAM*e/DEL)
def sd(x, ts):
    ph = np.exp(-1j*W*ts); return 2.0/len(ts)*np.sum(x*ph)
print('%-6s %10s %10s %10s %10s' % ('burst', 'bq 线性', 'bq 精确', '线性误差%', '精确误差%'))
rows = []
for k in range(3):
    t0 = 3.0 + 10.0*k
    m0 = (t >= t0) & (t < t0+0.2); m1 = (t >= t0+0.2) & (t < t0+0.4)
    if m1.sum() < 150: break
    out = {}
    for nm, m in (('off', m0), ('on', m1)):
        E = sd(e1[m], t[m]); V = sd(v[m], t[m]); U = sd(u[m], t[m]); Q = sd(q[m], t[m])
        g1 = sd(G1(e1[m]), t[m]); g2 = sd(G2(e1[m]), t[m])
        out[nm] = dict(E=E, V=V, U=U, Q=Q, g1=g1, g2=g2)
    b0 = 643.7
    lin = (out['on']['V'] + (Sd + B1 + B2/Sd)*out['on']['E']) - \
          (out['off']['V'] + (Sd + B1 + B2/Sd)*out['off']['E'])
    exa = (out['on']['V'] + Sd*out['on']['E'] + B1*out['on']['g1'] + B2/Sd*out['on']['g2']) - \
          (out['off']['V'] + Sd*out['off']['E'] + B1*out['off']['g1'] + B2/Sd*out['off']['g2'])
    dU = out['on']['U'] - out['off']['U']; dQ = out['on']['Q'] - out['off']['Q']
    bq_l = abs(lin + b0*dU)/abs(dQ); bq_e = abs(exa + b0*dU)/abs(dQ)
    rows.append((bq_l, bq_e))
    print('%-6.1f %10.1f %10.1f %10.1f %10.1f' % (t0, bq_l, bq_e, 100*(bq_l/TRUE-1), 100*(bq_e/TRUE-1)))
if rows:
    a = np.asarray(rows)
    print('\n中位：线性 %.1f（%+.1f%%）  精确 %.1f（%+.1f%%）'
          % (np.median(a[:,0]), 100*(np.median(a[:,0])/TRUE-1), np.median(a[:,1]), 100*(np.median(a[:,1])/TRUE-1)))
