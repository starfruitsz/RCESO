# -*- coding: utf-8 -*-
import numpy as np, scipy.io as sio
S = sio.loadmat(r'simulink/scaffold_pmsm/_pm_foc_dump.mat')
t  = S['t'].ravel(); u = S['u'].ravel()
iq = S['iq'].ravel(); e1 = S['e1'].ravel()
F = 65.0; W = 2*np.pi*F; dT = 1e-3; B0 = 536.4
Sd = (np.exp(1j*W*dT) - 1)/dT
pd = Sd + 2*500.0 + 500.0**2/Sd

def dem(x, m):
    xx = x[m]
    k = np.round(t[m]/1e-3)
    ph = np.exp(-1j*2*np.pi*0.065*k)
    return 2.0/len(xx)*np.sum(xx*ph)

print('%-7s %9s %9s %9s %9s' % ('t_on', '|dD|', '|dU|', '|dQ|', 'bq'))
for s in [8.2, 13.2, 18.2, 23.2]:
    m0 = (t >= s-0.2-1e-9) & (t < s-1e-9)
    m1 = (t >= s) & (t < s+0.2)
    if m0.sum() < 50 or m1.sum() < 50:
        print('%.1f window too small' % s); continue
    E0, E1 = dem(e1, m0), dem(e1, m1)
    U0, U1 = dem(u, m0), dem(u, m1)
    Q0, Q1 = dem(iq, m0), dem(iq, m1)
    num = (pd*E1 - pd*E0) + B0*(U1-U0)
    den = Q1 - Q0
    print('%-7.2f %9.2f %9.4f %9.4f %9.2f' % (s, abs(pd*E1-pd*E0), abs(U1-U0), abs(den), abs(num)/max(abs(den),1e-12)))
print('\n真值 536.4；|dQ| 应约等于 2*0.118=0.236')
