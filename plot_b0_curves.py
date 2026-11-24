# plot_b0_curves.py —— 定稿算法（Simulink C/MATLAB Function）的 b0 辨识曲线，三波对比
import os
import numpy as np, scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'wave_cmp.mat'
m = sio.loadmat(os.path.join(HERE, 'simulink', src), squeeze_me=True, struct_as_record=False)
res = m['res']
colors = ['#1f4e9c', '#c0392b', '#117864']
TRUE = 536.40

fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.8, 6.8), gridspec_kw=dict(height_ratios=[1.4, 1], hspace=0.34))
for r, c in zip(res, colors):
    ax.plot(r.t, r.b0, lw=1.3, color=c, label='%s：终值 %.1f（%+.2f%%）' % (r.name, r.final, r.err))
    ax2.semilogy(r.t, np.abs(np.asarray(r.b0) - TRUE) / TRUE * 100, lw=1.1, color=c, label=r.name)
ax.axhline(TRUE, color='0.35', lw=0.9, label='真值 536.40')
ax.axhspan(TRUE * 0.97, TRUE * 1.03, color='0.85', alpha=0.5, lw=0, label='±3%')
ax.set_xlim(0, 130); ax.set_ylim(395, 545)
ax.set_xlabel('t / s'); ax.set_ylabel(r'$\hat b_0$'); ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=8, loc='lower right')
ax.set_title('(a) 定稿算法（Simulink 闭环）三种注入波形的 $\\hat b_0$ 曲线', fontsize=9, loc='left')
axi = inset_axes(ax, width='46%', height='40%', loc='center right', borderpad=1.4)
for r, c in zip(res, colors):
    axi.plot(r.t, r.b0, lw=1.2, color=c)
axi.set_xlim(4, 30); axi.set_ylim(525, 545); axi.grid(alpha=0.3); axi.tick_params(labelsize=7)
axi.set_title('放大：4–30 s', fontsize=7.5)

ax2.axhline(3.0, color='0.6', ls=':', lw=0.8)
ax2.axhline(1.0, color='0.6', ls='--', lw=0.8)
ax2.set_xlim(0, 130); ax2.set_ylim(0.2, 40)
ax2.set_xlabel('t / s'); ax2.set_ylabel(r'$|\hat b_0-b|/b$ / %')
ax2.grid(alpha=0.3, which='both')
for i, r in enumerate(res):
    lab = []
    if np.isfinite(r.t3): lab.append('±3%%：%.1f s' % r.t3)
    if np.isfinite(r.t1): lab.append('±1%%：%.1f s' % r.t1)
    ax2.text(60, 8.0 / (i + 1), '%s  %s' % (r.name, '，'.join(lab)), color=colors[i], fontsize=8)
ax2.set_title('(b) 相对误差（对数）', fontsize=9, loc='left')

fig.savefig(os.path.join(HERE, 'fig_b0_curves_noise.png' if 'noise' in src else 'fig_b0_curves.png'),
            dpi=200, bbox_inches='tight')
for r in res:
    print('%-3s final=%.2f err=%+.2f%% t3=%.1f t1=%.1f' % (r.name, r.final, r.err, r.t3, r.t1))
print('saved fig_b0_curves.png')
