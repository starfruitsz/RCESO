# plot_cmp_pointwise.py —— C 版 vs MATLAB 版逐点回放对比（时基修正后）
import os
import numpy as np, scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
m = sio.loadmat(os.path.join(HERE, 'cmp2.mat'))
b0c = m['b0c'].ravel(); b0m = m['b0m'].ravel()
duc = m['duc'].ravel(); dum = m['dum'].ravel()
N = len(b0c); t = np.arange(N) * 1e-3
d = np.abs(b0c - b0m); rel = d / np.abs(b0m)

fig = plt.figure(figsize=(7.0, 8.4))
gs = fig.add_gridspec(4, 1, height_ratios=[1.1, 1.1, 0.8, 0.7], hspace=0.6)
ax0, ax1, ax2, ax3 = [fig.add_subplot(gs[i]) for i in range(4)]

ax0.plot(t, b0c, color='#1f4e9c', lw=1.2, label='C 版（float32 + LUT）')
ax0.plot(t, b0m, color='#c0392b', lw=0.9, ls='--', label='MATLAB 版（double）')
ax0.axhline(536.40, color='0.45', lw=0.9, ls='-.', label='真值 536.40')
ax0.set_xlim(0, 130); ax0.set_ylim(395, 545)
ax0.set_xlabel('t / s'); ax0.set_ylabel(r'$\hat b_0$'); ax0.grid(alpha=0.3)
ax0.legend(frameon=False, fontsize=7.5, loc='lower right')
ax0.set_title('(a) 同一输入流回放：两条轨迹重合（末值差 %.2e）' % d[-1], fontsize=9, loc='left')

ax1.semilogy(t, np.maximum(d, 1e-12), color='#1f4e9c', lw=1.0)
ax1.annotate('预热期最大 %.2e\n（相对 %.1e）' % (d.max(), rel.max()),
             xy=(t[int(np.argmax(d))], d.max()), xytext=(30, 3e-2), fontsize=7.5,
             arrowprops=dict(arrowstyle='->', lw=0.7, color='0.3'))
ax1.annotate('冻结后 %.1e' % d[-1], xy=(128, d[-1]), xytext=(85, 2e-4), fontsize=7.5,
             arrowprops=dict(arrowstyle='->', lw=0.7, color='0.3'))
ax1.set_xlim(0, 130); ax1.set_ylim(1e-6, 1e0)
ax1.set_xlabel('t / s'); ax1.set_ylabel(r'$|\Delta \hat b_0|$'); ax1.grid(alpha=0.3, which='both')
ax1.set_title('(b) 逐点差：全程未超过 1e-4（相对）', fontsize=9, loc='left')

seg = np.arange(200, 240)
ax2.plot(seg - 200, duc[seg] * 1e3, 'o-', ms=3, lw=0.8, color='#1f4e9c', label='C 版（LUT）')
ax2.plot(seg - 200, dum[seg] * 1e3, 's--', ms=3, lw=0.8, color='#c0392b', label='MATLAB 版（sin）')
ax2.set_xlabel('注入段内的拍数'); ax2.set_ylabel(r'$\Delta u$ / $10^{-3}$ pu')
ax2.grid(alpha=0.3); ax2.legend(frameon=False, fontsize=8)
ax2.set_title('(c) 注入波形（两版几乎重合）', fontsize=9, loc='left')

ax3.step(seg - 200, (duc[seg] - dum[seg]) * 1e3, where='mid', color='#6c3483', lw=0.9)
ax3.axhline(0, color='0.6', lw=0.6)
ax3.set_xlabel('注入段内的拍数'); ax3.set_ylabel(r'$u_c-u_m$ / $10^{-3}$ pu')
ax3.grid(alpha=0.3)
ax3.set_title('(d) 注入波形之差：LUT 相位量化（峰值 %.1f%%）' % (100 * np.abs(duc[seg] - dum[seg]).max() / 0.118),
             fontsize=9, loc='left')

fig.savefig(os.path.join(ROOT, 'fig_cmp_pointwise.png'), dpi=200, bbox_inches='tight')
print('final d=%.2e rel=%.2e; max d=%.2e (t=%.2fs) rel_max=%.2e'
      % (d[-1], rel[-1], d.max(), t[int(np.argmax(d))], rel.max()))
print('du 逐点最大差 %.2e pu' % np.abs(duc - dum).max())
