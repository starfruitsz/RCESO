# -*- coding: utf-8 -*-
"""plot_matrix_vendor.py —— 厂家对象：严重失配 + 故障扰动 下的识别开/关"""
import numpy as np, scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.8

ON = sio.loadmat(r'simulink/scaffold_pmsm/_tr_upd1.mat')
OFF = sio.loadmat(r'simulink/scaffold_pmsm/_tr_upd0.mat')
TRUE = 536.4
def ser(S):
    t = S['t'].ravel(); V = S['V']
    step = max(1, len(t)//100000)
    return t[::step], V[::step, 10]*30/np.pi, V[::step, 3]
t_on, w_on, iq_on = ser(ON); t_off, w_off, iq_off = ser(OFF)
b_on = ON['b0'].ravel(); b_off = OFF['b0'].ravel()
tb_on = np.linspace(0, t_on[-1], len(b_on)); tb_off = np.linspace(0, t_off[-1], len(b_off))

fig = plt.figure(figsize=(10.4, 7.4))
gs = fig.add_gridspec(2, 2, hspace=0.34, wspace=0.26)
a1 = fig.add_subplot(gs[0, :]); a2 = fig.add_subplot(gs[1, 0]); a3 = fig.add_subplot(gs[1, 1])

a1.plot(tb_off, b_off, '--', lw=1.4, color='0.5', label=r'识别关（$\hat b_0$=800，+49%）')
a1.plot(tb_on, b_on, lw=1.6, color='#117864', label=r'识别开（终值 545.1，+1.6%）')
a1.axhline(TRUE, color='0.35', lw=0.9, label='真值 536.4')
a1.set_xlim(0, 130); a1.set_ylim(480, 830)
a1.set_xlabel('t / s'); a1.set_ylabel(r'$\hat b_0$'); a1.grid(alpha=0.3)
a1.legend(frameon=False, fontsize=8, ncol=3, loc='lower right', bbox_to_anchor=(0.99, 0.02))
a1.set_title('(a) 严重失配（初值 800 = 真值 +49%）下的收敛', fontsize=9, loc='left')

m = (t_on >= 60) & (t_on <= 61); mf = (t_off >= 60) & (t_off <= 61)
a2.plot(t_off[mf], w_off[mf], lw=1.1, color='0.5', label='识别关')
a2.plot(t_on[m], w_on[m], lw=1.1, color='#117864', label='识别开')
a2.set_xlim(60, 61); a2.set_xlabel('t / s'); a2.set_ylabel(r'$\omega$ / rpm'); a2.grid(alpha=0.3)
a2.legend(frameon=False, fontsize=8)
a2.set_title('(b) 转速放大 60–61 s（10 Hz 故障扰动）', fontsize=9, loc='left')

x = np.arange(2); bw = 0.35
a3.bar(x - bw/2, [201.4, 284.3], bw, color='0.55', label='识别关')
a3.bar(x + bw/2, [142.4, 201.0], bw, color='#117864', label='识别开')
for i, (v1, v2) in enumerate(((201.4, 142.4), (284.3, 201.0))):
    a3.text(i - bw/2, v1 + 3, '%.0f' % v1, ha='center', fontsize=7.5)
    a3.text(i + bw/2, v2 + 3, '%.0f' % v2, ha='center', fontsize=7.5)
a3.set_xticks(x); a3.set_xticklabels(['转速 rms', '10 Hz 幅值'])
a3.set_ylabel('rpm'); a3.grid(alpha=0.3, axis='y'); a3.legend(frameon=False, fontsize=7.5)
a3.set_title('(c) 统计（60–130 s）', fontsize=9, loc='left')

fig.suptitle('厂家 PMSM + 平均逆变器：严重失配 + 10 Hz 故障扰动下的识别开/关', fontsize=10)
fig.savefig('fig_vendor_mismatch.png', dpi=200, bbox_inches='tight')
print('saved fig_vendor_mismatch.png')
