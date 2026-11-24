# -*- coding: utf-8 -*-
"""_seg_check.py —— 确认 off 窗是否真的零注入（离线检查）"""
import numpy as np, scipy.io as sio
S = sio.loadmat('_bq_dump.mat')
t = S['t'].ravel(); u = S['u'].ravel(); iq = S['iq'].ravel(); om = S['om'].ravel()
F = 65.0; W = 2*np.pi*F
print('%-6s %12s %12s %12s %10s' % ('burst', '|u|off/pu', '|u|on/pu', '|iq|on/pu', 'omega_pp'))
for k in range(6):
    t0 = 3.0 + 5.0*k
    moff = (t >= t0) & (t < t0+0.2)
    mon  = (t >= t0+0.2) & (t < t0+0.4)
    def amp(x, m):
        ph = np.exp(-1j*W*t[m]); return 2.0/m.sum()*abs(np.sum(x[m]*ph))
    print('%-6.1f %12.4f %12.4f %12.4f %10.1f'
          % (t0, amp(u, moff), amp(u, mon), amp(iq, mon), om[mon].max()-om[mon].min()))
