# -*- coding: utf-8 -*-
"""plot_vendor.py —— 厂家 PMSM + 平均逆变器模型的辨识结果"""
import numpy as np, scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.8

S = sio.loadmat(r'simulink/scaffold_pmsm/_vendor_run.mat')
t = S['t'].ravel(); V = S['V']
b0 = S['b0'].ravel(); bq = S['bq'].ravel()
iq = V[:, 3]; id_ = V[:, 4]; wm = V[:, 10] * 30 / np.pi
step = max(1, len(t) // 80000)
ts, wms = t[::step], wm[::step]
TRUE = 536.4
M = sio.loadmat('simulink/wave_full_on.mat', squeeze_me=True, struct_as_record=False)['res'][0]

fig = plt.figure(figsize=(10.4, 7.4))
gs = fig.add_gridspec(2, 2, hspace=0.34, wspace=0.26)
a1 = fig.add_subplot(gs[0, :]); a2 = fig.add_subplot(gs[1, 0]); a3 = fig.add_subplot(gs[1, 1])

a1.plot(ts, wms, lw=0.5, color='#1f4e9c')
a1.axhline(600, color='0.8', lw=0.7, ls=':')
a1.set_xlim(0, 130); a1.set_ylim(500, 800)
a1.set_xlabel('t / s'); a1.set_ylabel(r'$\omega$ / rpm'); a1.grid(alpha=0.3)
a1.set_title('(a) 厂家对象闭环：转速（后段均值 599.4 rpm；每 5 s 的尖峰是注入 burst）', fontsize=9, loc='left')

tb = np.linspace(0, t[-1], len(b0))
a2.plot(np.asarray(M.t), np.asarray(M.b0), lw=1.2, color='0.55', label='dq 手搭模型（531.5）')
a2.plot(tb, b0, lw=1.5, color='#117864', label='厂家模型（545.1）')
a2.axhline(TRUE, color='0.35', lw=0.9, label='真值 536.4')
a2.set_xlim(0, 130); a2.set_ylim(480, 580)
a2.set_xlabel('t / s'); a2.set_ylabel(r'$\hat b_0$'); a2.grid(alpha=0.3)
a2.legend(frameon=False, fontsize=7.5, loc='lower right')
a2.set_title(r'(b) 辨识结果 $\hat b_0$：厂家 vs dq', fontsize=9, loc='left')

# (c) 逐窗 bq（取变化点）
chg = np.concatenate(([True], np.diff(bq) != 0))
idx = np.where(chg & (bq > 0))[0]
tbq = np.linspace(0, t[-1], len(bq))[idx]
vbq = bq[idx]
a3.plot(tbq, vbq, 'o', ms=3, color='#117864')
a3.axhline(TRUE, color='0.35', lw=0.9, label='真值 536.4')
a3.axhline(np.median(vbq), color='#c0392b', ls='--', lw=0.9, label='中位 %.1f' % np.median(vbq))
a3.set_xlim(0, 130); a3.set_ylim(480, 600)
a3.set_xlabel('t / s'); a3.set_ylabel(r'$b_q$'); a3.grid(alpha=0.3)
a3.legend(frameon=False, fontsize=7.5)
a3.set_title('(c) 逐窗原始估计 bq', fontsize=9, loc='left')

fig.suptitle('用 Simulink 自带 PMSM + 平均逆变器重建被控对象后的闭环辨识', fontsize=10)
fig.savefig('fig_vendor_plant.png', dpi=200, bbox_inches='tight')
print('saved；bq 中位 %.1f，b0 %.1f，转速后段 %.1f' % (np.median(vbq), b0[-1], wm[t > 100].mean()))
