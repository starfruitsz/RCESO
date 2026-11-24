# plot_wave_cmp.py —— 三种注入波形的闭环对比图
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
ROOT = os.path.dirname(HERE)
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'wave_cmp.mat'
m = sio.loadmat(os.path.join(HERE, src), squeeze_me=True, struct_as_record=False)
res = m['res']
colors = ['#1f4e9c', '#c0392b', '#117864']
TRUE = 536.40

fig = plt.figure(figsize=(9.8, 6.6))
gs = fig.add_gridspec(2, 2, hspace=0.45, wspace=0.28)

# (a) 全程 + 放大窗
ax = fig.add_subplot(gs[:, 0])
for r, c in zip(res, colors):
    ax.plot(r.t, r.b0, lw=1.3, color=c, label='%s（终值 %.1f）' % (r.name, r.final))
ax.axhline(TRUE, color='0.4', lw=0.9, label='真值 536.40')
ax.axhspan(TRUE*0.97, TRUE*1.03, color='0.85', alpha=0.5, lw=0, label='±3%')
ax.set_xlim(0, 130); ax.set_ylim(395, 545)
ax.set_xlabel('t / s'); ax.set_ylabel(r'$\hat b_0$'); ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=7.5, loc='lower right')
ax.set_title('(a) 三种注入波形的 $\\hat b_0$ 收敛过程', fontsize=9, loc='left')

axi = inset_axes(ax, width='52%', height='38%', loc='center right', borderpad=1.6)
for r, c in zip(res, colors):
    axi.plot(r.t, r.b0, lw=1.3, color=c)
axi.set_xlim(4, 16); axi.set_ylim(528.5, 533.5)
axi.grid(alpha=0.3); axi.tick_params(labelsize=7)
axi.set_title('放大：4–16 s', fontsize=7.5)

# (b) 波形
ax = fig.add_subplot(gs[0, 1])
ph = np.linspace(0, 1, 1200, endpoint=False)
s = np.sin(2*np.pi*ph)
tri = np.where(ph*4 < 1, ph*4, np.where(ph*4 < 3, 2-ph*4, ph*4-4))
sq = np.sign(s)
for y, c, nm in [(s, colors[0], '正弦'), (sq, colors[1], '方波'), (tri, colors[2], '三角')]:
    ax.plot(ph, 0.118*y, lw=1.3, color=c, label=nm)
ax.axhline(0, color='0.7', lw=0.6)
ax.set_xlabel('一个注入周期'); ax.set_ylabel(r'$\Delta u$ / pu')
ax.grid(alpha=0.3); ax.legend(frameon=False, fontsize=7.5, ncol=3, loc='lower center')
ax.set_title('(b) 注入波形（峰值均 0.118 pu）', fontsize=9, loc='left')

# (c) 误差与收敛时间
ax = fig.add_subplot(gs[1, 1])
x = np.arange(len(res))
err = [abs(r.err) for r in res]
t3 = [r.t3 if np.isfinite(r.t3) else np.nan for r in res]
t1 = [r.t1 if np.isfinite(r.t1) else np.nan for r in res]
bw = 0.26
ax.bar(x - bw, err, width=bw, color=colors, label='|误差| / %')
ax.set_ylabel('|误差| / %', color='0.2')
ax.set_ylim(0, max(err)*1.45)
for i, v in enumerate(err):
    ax.text(x[i]-bw, v + max(err)*0.03, '%.2f%%' % v, ha='center', va='bottom', fontsize=7)
ax2 = ax.twinx()
ax2.bar(x, t3, width=bw, color='0.62', label='进入 ±3% / s')
ax2.bar(x + bw, t1, width=bw, color='0.40', label='进入 ±1% / s')
ax2.set_ylabel('收敛时间 / s')
ax2.set_ylim(0, 22)
for i in range(len(res)):
    ax2.text(x[i], (t3[i] if np.isfinite(t3[i]) else 0) + 0.4, '%.1f' % t3[i], ha='center', va='bottom', fontsize=7)
    lab = '%.1f' % t1[i] if np.isfinite(t1[i]) else '未达'
    ax2.text(x[i]+bw, (t1[i] if np.isfinite(t1[i]) else 0) + 0.4, lab, ha='center', va='bottom', fontsize=7)
ax.set_xticks(x); ax.set_xticklabels([r.name for r in res])
ax.grid(alpha=0.3, axis='y')
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, frameon=False, fontsize=7, loc='upper left', ncol=1)
ax.set_title('(c) 终值误差与收敛时间', fontsize=9, loc='left')

fig.savefig(os.path.join(ROOT, 'fig_wave_cmp_noise.png' if 'noise' in src else 'fig_wave_cmp.png'),
            dpi=200, bbox_inches='tight')
for r in res:
    print('%-4s final=%8.2f  err=%+.3f%%  t3=%s  t1=%s' % (r.name, r.final, r.err,
          ('%.2f' % r.t3) if np.isfinite(r.t3) else 'nan',
          ('%.2f' % r.t1) if np.isfinite(r.t1) else 'nan'))
print('saved fig_wave_cmp.png')
