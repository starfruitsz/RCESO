# -*- coding: utf-8 -*-
"""plot_burst_est.py —— 24 个 burst 的结算估计：均值无偏，冻结抽到低尾"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

z = np.load('_tjc_ali10_sin.npz'); jn = np.asarray(z['jnew'])
e = [(float(r[0]), float(r[2])) for r in jn if r[0] > 0]
be = e[2::3]
idx = np.arange(1, len(be) + 1)
v = np.array([b[1] for b in be])
TRUE = 101.89

fig, ax = plt.subplots(figsize=(9.2, 4.2))
ax.plot(idx, v, 'o-', ms=4, lw=1.0, color='#1f4e9c', label='逐 burst 估计')
ax.axhline(TRUE, color='0.35', lw=0.9, label='真值 101.89')
ax.axhline(v.mean(), color='#117864', ls='--', lw=1.0, label='24 次均值 %.1f' % v.mean())
ax.plot(idx[-10:], v[-10:], 'o', ms=9, mfc='none', mec='#c0392b', mew=1.4,
        label='冻结取末 10 个（均值 %.1f）' % v[-10:].mean())
ax.set_xlabel('burst 序号（5 s 一个，共 24 个 = 120 s）')
ax.set_ylabel(r'$b_q$'); ax.grid(alpha=0.3)
ax.set_xlim(0.5, 24.5)
ax.legend(frameon=False, fontsize=8, ncol=2, loc='lower right')
ax.set_title('严格对齐的 24 burst：估计无偏（均值 %.1f，−%.1f%%）；冻结取末 10 个 = %.1f' % (v.mean(), 100*(1-v.mean()/TRUE), v[-10:].mean()), fontsize=9, loc='left')
fig.tight_layout()
fig.savefig('fig_burst_est.png', dpi=200, bbox_inches='tight')
print('saved fig_burst_est.png')
print('均值 %.1f 中位 %.1f 标准差 %.1f  最后4个 %s 均值 %.1f' % (v.mean(), np.median(v), v.std(), np.round(v[-4:],1), v[-4:].mean()))
