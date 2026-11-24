# -*- coding: utf-8 -*-
"""plot_id_speed.py —— 识别开启 vs 关闭：转速对比（三波，单个 burst 放大 + 全程统计）"""
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

fig, axes = plt.subplots(3, 1, figsize=(9.2, 7.4), sharex=True)
for i, nm in enumerate(names):
    ax = axes[i]
    to = np.asarray(ON[i].t); wo = np.asarray(ON[i].w)
    tf = np.asarray(OFF[i].t); wf = np.asarray(OFF[i].w)
    m = (to >= 95.0) & (to <= 96.0); mf = (tf >= 95.0) & (tf <= 96.0)
    # 全程（60–130 s）峰峰统计
    mall = (to >= 60); mfall = (tf >= 60)
    pp_o = float(np.ptp(wo[mall])); pp_f = float(np.ptp(wf[mfall]))
    ax.plot(tf[mf], wf[mf], '--', lw=1.3, color='0.45', label='识别关（全程峰峰 %.0f rpm）' % pp_f)
    ax.plot(to[m], wo[m], '-', lw=1.4, color=colors[i], label='识别开（全程峰峰 %.0f rpm）' % pp_o)
    ax.axhline(600, color='0.8', lw=0.7, ls=':')
    ax.set_ylabel(r'$\omega$ / rpm'); ax.grid(alpha=0.3)
    ax.set_title('%s波：一个注入 burst（95.0–96.0 s）' % nm, fontsize=9, loc='left')
    ax.legend(frameon=False, fontsize=7.5, loc='lower right')
axes[2].set_xlabel('t / s'); axes[2].set_xlim(95.0, 96.0)
fig.suptitle('转速对比：b0 在线识别 开启（彩色实线） vs 关闭（灰色虚线）', fontsize=10)
fig.tight_layout()
fig.savefig('fig_id_speed.png', dpi=200, bbox_inches='tight')
print('saved fig_id_speed.png')
for i, nm in enumerate(names):
    to = np.asarray(ON[i].t); wo = np.asarray(ON[i].w)
    tf = np.asarray(OFF[i].t); wf = np.asarray(OFF[i].w)
    a = (to >= 60); b = (tf >= 60)
    eo = wo[a] - 600.0; ef = wf[b] - 600.0
    print('%-3s 峰峰 开 %.0f / 关 %.0f rpm   有效值 开 %.1f / 关 %.1f rpm   均值 开 %.2f / 关 %.2f'
          % (nm, np.ptp(wo[a]), np.ptp(wf[b]), np.sqrt(np.mean(eo**2)), np.sqrt(np.mean(ef**2)),
             wo[a].mean(), wf[b].mean()))
