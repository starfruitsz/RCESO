# -*- coding: utf-8 -*-
"""plot_quiet_cmp.py —— 冻结后（无注入）静默段对比：识别开 vs 关"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.8

def get(tag):
    z = np.load('_tjc_%s.npz' % tag)
    t = np.asarray(z['t']); step = max(1, len(t)//200000)
    return t[::step], np.asarray(z['y'])[::step]*600.0
t_on, w_on = get('ali12_sin'); t_off, w_off = get('off130')
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.4, 5.6), sharex=True)
for ax, (lo, hi, ttl) in zip((a1, a2), ((118, 132, '(a) 120 s 之后：识别开已冻结、停止注入'),
                                         (122, 126, '(b) 静默段放大 122–126 s'))):
    m = (t_on >= lo) & (t_on < hi); mf = (t_off >= lo) & (t_off < hi)
    ax.plot(t_off[mf], w_off[mf], lw=0.9, color='0.45', label='识别关（rms 7.70 rpm）')
    ax.plot(t_on[m], w_on[m], lw=0.9, color='#117864', label='识别开（rms 9.84 rpm）')
    ax.set_xlim(lo, min(hi, t_on[-1])); ax.set_ylabel(r'$\omega$ / rpm'); ax.grid(alpha=0.3)
    ax.set_title(ttl, fontsize=9, loc='left')
    ax.legend(frameon=False, fontsize=7.5, loc='upper right')
a2.set_xlabel('t / s')
fig.tight_layout()
fig.savefig('fig_quiet_cmp.png', dpi=200, bbox_inches='tight')
print('saved fig_quiet_cmp.png')
