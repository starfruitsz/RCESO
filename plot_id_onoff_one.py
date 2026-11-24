# -*- coding: utf-8 -*-
"""plot_id_onoff_one.py —— 识别开启 vs 关闭（同一张图）"""
import numpy as np, scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.8

ON = sio.loadmat('simulink/wave_full_on.mat', squeeze_me=True, struct_as_record=False)['res']
OFF = sio.loadmat('simulink/wave_full_off.mat', squeeze_me=True, struct_as_record=False)['res']
names = ['正弦', '方波', '三角']
colors = ['#1f4e9c', '#c0392b', '#117864']
TRUE = 536.40

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.2), gridspec_kw=dict(width_ratios=[1.5, 1]))
for i, nm in enumerate(names):
    r = ON[i]
    a1.plot(r.t, r.b0, lw=1.6, color=colors[i], label='%s·识别开' % nm)
    a1.plot(r.t, np.full_like(np.asarray(r.t), 400.0), ':', lw=1.0, color=colors[i], alpha=0.8)
a1.axhline(TRUE, color='0.35', lw=0.9, label='真值 536.4')
a1.text(70, 405, '点线：识别关闭（三波 b0 恒为 400）', fontsize=8, color='0.35')
a1.set_xlim(0, 130); a1.set_ylim(385, 555)
a1.set_xlabel('t / s'); a1.set_ylabel(r'$\hat b_0$'); a1.grid(alpha=0.3)
a1.set_title('(a) $\\hat b_0$：识别开（实线） vs 关（点线）', fontsize=9, loc='left')
a1.legend(frameon=False, fontsize=7.5, loc='center right')

x = np.arange(len(names)); bw = 0.36
wpp_o = [np.ptp(np.asarray(r.w)[np.asarray(r.t) > 60]) for r in ON]
wpp_f = [np.ptp(np.asarray(r.w)[np.asarray(r.t) > 60]) for r in OFF]
a2.bar(x - bw/2, wpp_o, bw, color=colors, label='识别开')
a2.bar(x + bw/2, wpp_f, bw, color='0.55', label='识别关')
for i in range(len(names)):
    a2.text(x[i]-bw/2, wpp_o[i]+5, '%.0f' % wpp_o[i], ha='center', va='bottom', fontsize=7)
    a2.text(x[i]+bw/2, wpp_f[i]+5, '%.0f' % wpp_f[i], ha='center', va='bottom', fontsize=7)
a2.set_xticks(x); a2.set_xticklabels(names)
a2.set_ylabel(r'$\omega$ 峰峰 / rpm'); a2.grid(alpha=0.3, axis='y')
a2.set_title('(b) 转速纹波（60 s 后）', fontsize=9, loc='left')
a2.legend(frameon=False, fontsize=7.5)

fig.suptitle('b0 在线识别：开启 vs 关闭（同一批工况、同一注入）', fontsize=10)
fig.tight_layout()
fig.savefig('fig_id_onoff_one.png', dpi=200, bbox_inches='tight')
print('saved fig_id_onoff_one.png')

iqo = [np.sqrt(np.mean((np.asarray(r.iq)[np.asarray(r.t)>60] - np.mean(np.asarray(r.iq)[np.asarray(r.t)>60]))**2)) for r in ON]
iqf = [np.sqrt(np.mean((np.asarray(r.iq)[np.asarray(r.t)>60] - np.mean(np.asarray(r.iq)[np.asarray(r.t)>60]))**2)) for r in OFF]
print('iq AC rms  on:', np.round(iqo,3), ' off:', np.round(iqf,3))
print('w pp       on:', np.round(wpp_o,1), ' off:', np.round(wpp_f,1))
