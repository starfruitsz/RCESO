# plot_wave_cmp_py.py —— Python（带噪声）三波对比：注入 / 电流 / 转速
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.5

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, '_wave_cmp_py.json'), encoding='utf-8'))
colors = ['#1f4e9c', '#c0392b', '#117864']

fig = plt.figure(figsize=(10.6, 7.8))
gs = fig.add_gridspec(4, 3, hspace=0.55, wspace=0.26, height_ratios=[1, 1, 1, 1.05])
titles = ['注入 Δu / pu', r'$i_q$ / A', r'$\omega$ / rpm']

for i, d in enumerate(data):
    t = np.asarray(d['t']); t0 = float(d.get('t0', 3.0))
    for j, key in enumerate(['inj', 'iq', 'w']):
        ax = fig.add_subplot(gs[i, j])
        y = np.asarray(d[key])
        ax.plot(t, y, lw=0.8, color=colors[i])
        ax.axvspan(t0 + 0.2, t0 + 0.4, color='#f2e6c9', alpha=0.7, lw=0)
        ax.set_xlim(t0 - 0.1, t0 + 0.65); ax.grid(alpha=0.3)
        if i == 2: ax.set_xlabel('t / s')
        if i == 0: ax.set_title(titles[j], fontsize=9)
        if j == 0:
            ax.set_ylabel('%s\n%s' % (d['name'], titles[j]), fontsize=8.5)
        if j == 2:
            ax.set_ylabel('%s\n%s' % (d['name'], titles[j]), fontsize=8.5)

# 底部条形
x = np.arange(len(data)); bw = 0.26
ax = fig.add_subplot(gs[3, 0])
v = [d['inj_amp'] for d in data]
ax.bar(x, v, width=0.55, color=colors)
for i, val in enumerate(v):
    ax.text(x[i], val + 0.004, '%.3f' % val, ha='center', va='bottom', fontsize=7.5)
ax.set_xticks(x); ax.set_xticklabels([d['name'] for d in data])
ax.set_ylabel('注入基波 / pu'); ax.grid(alpha=0.3, axis='y')
ax.set_title('注入基波（65 Hz）', fontsize=9, loc='left')

ax = fig.add_subplot(gs[3, 1])
v = [d['iq_amp'] for d in data]
ax.bar(x, v, width=0.55, color=colors)
for i, val in enumerate(v):
    ax.text(x[i], val + 0.02, '%.2f' % val, ha='center', va='bottom', fontsize=7.5)
ax.set_xticks(x); ax.set_xticklabels([d['name'] for d in data])
ax.set_ylabel(r'$i_q$ 基波 / A'); ax.grid(alpha=0.3, axis='y')
ax.set_title('电流基波（65 Hz）', fontsize=9, loc='left')

ax = fig.add_subplot(gs[3, 2])
v = [d['w_pp'] for d in data]
ax.bar(x, v, width=0.55, color=colors)
for i, val in enumerate(v):
    ax.text(x[i], val + 0.6, '%.1f' % val, ha='center', va='bottom', fontsize=7.5)
ax.set_xticks(x); ax.set_xticklabels([d['name'] for d in data])
ax.set_ylabel(r'$\omega$ 峰峰 / rpm'); ax.grid(alpha=0.3, axis='y')
ax.set_title('转速峰峰（注入窗内）', fontsize=9, loc='left')

fig.savefig(os.path.join(HERE, 'fig_wave_cmp_py.png'), dpi=200, bbox_inches='tight')
for d in data:
    print('%-3s inj=%.4f pu  iq1=%.3f A  iq_pk=%.3f A  w1=%.1f rpm  w_pp=%.1f rpm'
          % (d['name'], d['inj_amp'], d['iq_amp'], d['iq_pk'], d['w_amp'], d['w_pp']))
print('saved fig_wave_cmp_py.png')
