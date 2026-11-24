# plot_b0_curve_py.py —— Python 带噪声闭环的三波 b0 辨识曲线
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
src = sys.argv[1] if len(sys.argv) > 1 else '_b0_curve_py.json'
data = json.load(open(os.path.join(HERE, src), encoding='utf-8'))
colors = ['#1f4e9c', '#c0392b', '#117864']
bt = data[0]['b_true']

fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.6, 6.6), gridspec_kw=dict(height_ratios=[1.35, 1], hspace=0.32))
for i, d in enumerate(data):
    t = np.asarray(d['t']); b = np.asarray(d['b0'])
    ax.plot(t, b, lw=1.4, color=colors[i], label='%s（终值 %.1f，%+.2f%%）' % (d['name'], d['final'], d['err']))
    ax2.semilogy(t, np.abs(b - bt) / bt * 100, lw=1.2, color=colors[i], label=d['name'])
ax.axhline(bt, color='0.35', lw=0.9, label='真值 %.2f' % bt)
ax.axhspan(bt * 0.97, bt * 1.03, color='0.85', alpha=0.5, lw=0, label='±3%')
ax.set_xlim(0, 130); ax.set_ylim(78, 122)
ax.set_xlabel('t / s'); ax.set_ylabel(r'$\hat b_0$'); ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=8, loc='lower right')
ax.set_title('(a) 三种注入波形的 $\\hat b_0$ 辨识曲线（Python 带噪声闭环）', fontsize=9, loc='left')

ax2.axhline(3.0, color='0.6', ls=':', lw=0.8)
ax2.axhline(1.0, color='0.6', ls='--', lw=0.8)
ax2.set_xlim(0, 130); ax2.set_ylim(1e-2, 2e1)
ax2.set_xlabel('t / s'); ax2.set_ylabel(r'$|\hat b_0-b|/b$ / %')
ax2.grid(alpha=0.3, which='both')
for i, d in enumerate(data):
    lab = []
    if d['t3'] == d['t3']: lab.append('±3%%: %.1f s' % d['t3'])
    if d['t1'] == d['t1']: lab.append('±1%%: %.1f s' % d['t1'])
    ax2.text(4, 6.0 / (i + 1), '%s  %s' % (d['name'], '，'.join(lab)), color=colors[i], fontsize=8)
ax2.set_title('(b) 相对误差（对数）', fontsize=9, loc='left')

fig.savefig(os.path.join(HERE, 'fig_b0_final_py.png' if 'final' in src else 'fig_b0_curve_py.png'),
            dpi=200, bbox_inches='tight')
for d in data:
    print('%-3s final=%.2f err=%+.2f%% t3=%.1f t1=%.1f' % (d['name'], d['final'], d['err'],
          d['t3'] if d['t3'] == d['t3'] else -1, d['t1'] if d['t1'] == d['t1'] else -1))
print('saved fig_b0_curve_py.png')
