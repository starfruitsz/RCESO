# -*- coding: utf-8 -*-
"""plot_inv_exact.py —— 精确代数恒等式 vs 线性化反演（同一 fal 观测器）"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.8

LIN = '_tjc_pf_W=sin.npz'   # 线性化（pd·E1）
EXA = '_tjc_xe_W=sin.npz'   # 精确（β1·Ĝ1 + β2/Sd·Ĝ2）
TRUE = 101.89
z1 = np.load(LIN); z2 = np.load(EXA)
t1 = np.asarray(z1['t']); b1 = np.asarray(z1['b0e'])
t2 = np.asarray(z2['t']); b2 = np.asarray(z2['b0e'])
tb1 = np.linspace(0, float(t1[-1]), len(b1)); tb2 = np.linspace(0, float(t2[-1]), len(b2))
j1 = np.asarray(z1['jnew']); j2 = np.asarray(z2['jnew'])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.2), gridspec_kw=dict(width_ratios=[1.4, 1]))
a1.plot(tb1, b1, lw=1.6, color='#c0392b', label='线性化反演')
a1.plot(tb2, b2, lw=1.6, color='#117864', label='精确反演（Ĝ）')
a1.axhline(TRUE, color='0.35', lw=0.9, label='真值 101.89')
a1.set_xlim(0, 60); a1.set_ylim(60, 210)
a1.set_xlabel('t / s'); a1.set_ylabel(r'$\hat b_0$'); a1.grid(alpha=0.3)
a1.set_title('(a) 闭环 $\\hat b_0$（正弦波，fal 观测器）', fontsize=9, loc='left')
a1.legend(frameon=False, fontsize=8, loc='lower right')

a2.step(j1[:18, 0], j1[:18, 2], where='post', lw=1.4, color='#c0392b', label='线性化反演')
a2.step(j2[:18, 0], j2[:18, 2], where='post', lw=1.4, color='#117864', label='精确反演（Ĝ）')
a2.axhline(TRUE, color='0.35', lw=0.9, ls='--')
a2.set_xlim(0, 55); a2.set_ylim(0, 320)
a2.set_xlabel('t / s'); a2.set_ylabel(r'逐窗原始估计 $b_q$'); a2.grid(alpha=0.3)
a2.set_title('(b) 逐窗原始估计（虚线=真值）', fontsize=9, loc='left')
a2.legend(frameon=False, fontsize=8)

fig.suptitle('反演口径对比：$\\hat d = V + S_d E_1 + \\beta_1\\hat G_1 + (\\beta_2/S_d)\\hat G_2$（精确） vs $(S_d+\\beta_1+\\beta_2/S_d)E_1$（线性化）', fontsize=9.5)
fig.tight_layout()
fig.savefig('fig_inv_exact.png', dpi=200, bbox_inches='tight')
print('saved fig_inv_exact.png')
print('首个 burst 原始估计： 线性化 %.1f  精确 %.1f  （真值 %.1f）' % (j1[2,2], j2[2,2], TRUE))
