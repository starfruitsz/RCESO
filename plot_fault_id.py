# -*- coding: utf-8 -*-
"""plot_fault_id.py —— 引入三合一故障后：b0 识别 开 vs 关"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.8

ON = np.load('_tjc_flt_1.npz'); OFF = np.load('_tjc_flt_0.npz')
TRUE = 101.89
def series(z):
    t = np.asarray(z['t']); step = max(1, len(t) // 120000)
    return t[::step], np.asarray(z['y'])[::step] * 600.0, np.asarray(z['iq'])[::step], t[-1]
def bcurve(z):
    b = np.asarray(z['b0e']); return np.linspace(0, float(np.asarray(z['t'])[-1]), len(b)), b

t_on, w_on, iq_on, _ = series(ON)
t_off, w_off, iq_off, _ = series(OFF)
tb_on, b_on = bcurve(ON); tb_off, b_off = bcurve(OFF)

fig, axes = plt.subplots(3, 1, figsize=(9.4, 7.8))
a1, a2, a3 = axes
a1.plot(tb_off, b_off, '--', lw=1.4, color='0.45', label='识别关（b0 停在标称 128.7）')
a1.plot(tb_on, b_on, lw=1.5, color='#117864', label='识别开（终值 95.6）')
a1.axhline(TRUE, color='0.35', lw=0.9, label='物理真值 101.89')
a1.set_xlim(0, 60); a1.set_ylim(90, 132)
a1.set_xlabel('t / s'); a1.set_ylabel(r'$\hat b_0$'); a1.grid(alpha=0.3)
a1.legend(frameon=False, fontsize=7.5, loc='center right')
a1.set_title('(a) $\\hat b_0$（2 s 起加载 50% 并同时引入三合一故障）', fontsize=9, loc='left')

m = (t_on >= 40) & (t_on <= 41); mf = (t_off >= 40) & (t_off <= 41)
a2.plot(t_off[mf], w_off[mf], '--', lw=1.0, color='0.45', label='识别关')
a2.plot(t_on[m], w_on[m], lw=1.0, color='#117864', label='识别开')
a2.set_xlim(40, 41); a2.set_ylim(555, 645)
a2.set_xlabel('t / s'); a2.set_ylabel(r'$\omega$ / rpm'); a2.grid(alpha=0.3)
a2.legend(frameon=False, fontsize=7.5, loc='lower right')
a2.set_title('(b) 转速（40–41 s 放大；故障在 10 Hz 上摆动）', fontsize=9, loc='left')

a3.plot(t_off[mf], iq_off[mf], '--', lw=1.0, color='0.45', label='识别关')
a3.plot(t_on[m], iq_on[m], lw=1.0, color='#117864', label='识别开')
a3.set_xlim(40, 41); a3.set_xlabel('t / s'); a3.set_ylabel(r'$i_q$ / A'); a3.grid(alpha=0.3)
a3.set_title('(c) 电流（40–41 s 放大）', fontsize=9, loc='left')

fig.tight_layout()
fig.suptitle('引入故障后的识别对比（Python 闭环，带噪声：50% 负载 + 三合一故障）', fontsize=10)
fig.subplots_adjust(top=0.92)
fig.savefig('fig_fault_id.png', dpi=200, bbox_inches='tight')
for nm, w in (('识别开', w_on), ('识别关', w_off)):
    m2 = (t_on > 40)
    print('%-4s 10Hz 分量（后 20 s）：约 %.1f rpm' % (nm, np.ptp(w[(t_on > 40) & (t_on < 41)])))
print('saved fig_fault_id.png')
