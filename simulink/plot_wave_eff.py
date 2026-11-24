# plot_wave_eff.py —— 三种注入波形对电流与转速的影响
import os
import numpy as np, scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.5

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
m = sio.loadmat(os.path.join(HERE, 'wave_eff.mat'), squeeze_me=True, struct_as_record=False)
res = m['res']
colors = ['#1f4e9c', '#c0392b', '#117864']

fig = plt.figure(figsize=(10.4, 8.6))
gs = fig.add_gridspec(4, 2, hspace=0.62, wspace=0.24, height_ratios=[1, 1, 1, 1.05])

for i, r in enumerate(res):
    ax = fig.add_subplot(gs[i, 0])
    ax.plot(r.t, r.iq, lw=1.0, color=colors[i])
    ax.axvspan(100.2, 100.4, color='#f2e6c9', alpha=0.7, lw=0)
    ax.set_xlim(100.0, 100.7)
    ax.set_ylabel(r'$i_q$ / A'); ax.grid(alpha=0.3)
    ax.set_title('%s：电流（基波 %.2f A，三次 %.2f A）' % (r.name, r.iq_f1, r.iq_f3), fontsize=9, loc='left')
    if i == 2:
        ax.set_xlabel('t / s')

    ax2 = fig.add_subplot(gs[i, 1])
    ax2.plot(r.t, r.w, lw=1.0, color=colors[i])
    ax2.axvspan(100.2, 100.4, color='#f2e6c9', alpha=0.7, lw=0)
    ax2.set_xlim(100.0, 100.7)
    ax2.set_ylabel(r'$\omega$ / rpm'); ax2.grid(alpha=0.3)
    ax2.set_title('%s：转速（峰峰 %.0f rpm）' % (r.name, r.w_pp), fontsize=9, loc='left')
    if i == 2:
        ax2.set_xlabel('t / s')

# 底部：条形对比
axb = fig.add_subplot(gs[3, 0])
x = np.arange(len(res)); bw = 0.36
f1 = [r.iq_f1 for r in res]; f3 = [r.iq_f3 for r in res]
axb.bar(x - bw/2, f1, width=bw, color=colors, label='65 Hz 基波')
axb.bar(x + bw/2, f3, width=bw, color='0.55', label='195 Hz 三次谐波')
for i in range(len(res)):
    axb.text(x[i]-bw/2, f1[i]+0.01, '%.2f' % f1[i], ha='center', va='bottom', fontsize=7)
    axb.text(x[i]+bw/2, f3[i]+0.01, '%.2f' % f3[i], ha='center', va='bottom', fontsize=7)
axb.set_xticks(x); axb.set_xticklabels([r.name for r in res])
axb.set_ylabel(r'$i_q$ 幅值 / A'); axb.grid(alpha=0.3, axis='y')
axb.legend(frameon=False, fontsize=7.5)
axb.set_title('(d) 电流的基波与三次谐波', fontsize=9, loc='left')

axw = fig.add_subplot(gs[3, 1])
pp = [r.w_pp for r in res]
axw.bar(x, pp, width=0.5, color=colors)
for i in range(len(res)):
    axw.text(x[i], pp[i]+3, '%.0f' % pp[i], ha='center', va='bottom', fontsize=7.5)
axw.set_xticks(x); axw.set_xticklabels([r.name for r in res])
axw.set_ylabel(r'$\omega$ 峰峰 / rpm'); axw.grid(alpha=0.3, axis='y')
axw.set_title('(e) 转速纹波（burst 窗口内）', fontsize=9, loc='left')

fig.savefig(os.path.join(ROOT, 'fig_wave_eff.png'), dpi=200, bbox_inches='tight')
for r in res:
    print('%-4s du1=%.4f iq1=%.3f iq3=%.3f w_pp=%.1f iq_pk=%.2f' % (r.name, r.du_f1, r.iq_f1, r.iq_f3, r.w_pp, r.iq_pk))
print('saved fig_wave_eff.png')
