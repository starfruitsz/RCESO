# -*- coding: utf-8 -*-
"""_bq_terms.py —— 逐窗拆解：把 bq 的三个复分量算出来，看偏置来自哪一项"""
import numpy as np, scipy.io as sio
S = sio.loadmat('_bq_dump.mat')
t = S['t'].ravel(); iq = S['iq'].ravel(); u = S['u'].ravel(); e1 = S['e1'].ravel(); v = S['v'].ravel()
F = 65.0; W = 2*np.pi*F; dT = 1e-3
kappa2 = 0.10**(0.75 - 1.0)        # fal：a=0.75, δ=0.10
b1, b2 = 1000.0, 500.0**2 * kappa2  # β1=2ωo·κ1，β2=ωo²·κ2（κ1=1）
Sd = (np.exp(1j*W*dT) - 1.0)/dT
pd = Sd + b1 + b2/Sd
print('Sd=%.1f%+.1fj   pd=%.1f%+.1fj' % (Sd.real, Sd.imag, pd.real, pd.imag))
def dem(x, tseg):
    ph = np.exp(-1j*W*tseg)
    return 2.0/len(tseg)*np.sum(x*ph)
for k in range(4):
    t0 = 3.0 + 5.0*k
    moff = (t >= t0) & (t < t0+0.2)
    mon  = (t >= t0+0.2) & (t < t0+0.4)
    if mon.sum() < 150: break
    Eo, Vo, Uo, Qo = dem(e1[moff], t[moff]), dem(v[moff], t[moff]), dem(u[moff], t[moff]), dem(iq[moff], t[moff])
    En, Vn, Un, Qn = dem(e1[mon], t[mon]), dem(v[mon], t[mon]), dem(u[mon], t[mon]), dem(iq[mon], t[mon])
    dV = Vn - Vo; dE = En - Eo; dU = Un - Uo; dQ = Qn - Qo
    b0 = 120.0
    for name, b0v in (('b0=120', 120.0), ('b0=102', 102.0), ('b0=175', 175.0)):
        num = (dV + pd*dE) + b0v*dU
        bq = abs(num)/abs(dQ) if abs(dQ) > 1e-12 else float('nan')
        if name == 'b0=120':
            print('\nwin %d @%.2fs: |dV|=%.4g |pd*dE|=%.4g |dU|=%.3f |dQ|=%.4f  bq=%.1f'
                  % (k+1, t0, abs(dV), abs(pd*dE), abs(dU), abs(dQ), bq))
        else:
            print('        %s -> bq=%.1f' % (name, bq))
