# -*- coding: utf-8 -*-
"""plot_id_onoff.py —— b0 识别版 / 关闭识别版 各一张"""
import numpy as np, scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9
names = ['正弦', '方波', '三角']
colors = ['#1f4e9c', '#c0392b', '#117864']
TRUE = 536.40

def make(tag, fname, title):
    M = sio.loadmat('simulink/wave_full_%s.mat' % tag, squeeze_me=True, struct_as_record=False)['res']
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    for i, nm in enumerate(names):
        r = M[i]
        a1.plot(r.t, r.b0, lw=1.5, color=colors[i], label=nm)
        a2.plot(r.t, r.w, lw=0.8, color=colors[i], label=nm)
    a1.axhline(TRUE, color='0.35', lw=0.9, label='真值 536.4')
    a1.axhline(400, color='0.6', ls=':', lw=0.9, label='标称 400')
    a1.set_xlim(0, 130); a1.set_ylim(380, 560)
    a1.set_xlabel('t / s'); a1.set_ylabel(r'$\hat b_0$'); a1.grid(alpha=0.3)
    a1.set_title('(a) $\\hat b_0$', fontsize=9, loc='left'); a1.legend(frameon=False, fontsize=7)
    a2.set_xlim(0, 130); a2.set_xlabel('t / s'); a2.set_ylabel(r'$\omega$ / rpm'); a2.grid(alpha=0.3)
    a2.set_title('(b) 转速', fontsize=9, loc='left')
    fig.suptitle(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(fname, dpi=200, bbox_inches='tight')
    for r in M:
        print('%-3s b0末值 %.1f  w均值 %.0f' % (r.name, r.b0[-1], np.mean(np.asarray(r.w)[np.asarray(r.t) > 60])))
    print('saved', fname)

make('on', 'fig_id_on.png', 'b0 识别开启（24 burst 后冻结，标称 400 → 真值附近）')
make('off', 'fig_id_off.png', 'b0 识别关闭（注入照常，仅不更新 b0，停在标称 400）')
