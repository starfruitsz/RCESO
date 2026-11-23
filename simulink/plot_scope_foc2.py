# plot_scope_foc2.py —— 把 scope_foc2.m 导出的波形画成"示波器"图
# 用法：先跑 simulink/scope_foc2.m 生成 foc2_log.mat，再 python plot_scope_foc2.py
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
m = sio.loadmat(os.path.join(HERE, 'foc2_log.mat'))
tw, wv = m['tw'].ravel(), m['wv'].ravel()
tb, bv = m['tb'].ravel(), m['bv'].ravel()
td, dv = m['td'].ravel(), m['dv'].ravel()
tq, qv = m['tq'].ravel(), m['qv'].ravel()   # iq 单位 A
tu, uv = m['tu'].ravel(), m['uv'].ravel()

nz = np.nonzero(np.abs(dv) > 1e-9)[0]
starts, s, p = [], nz[0], nz[0]
for k in nz[1:]:
    if k != p + 1:
        starts.append(s); s = k
    p = k
starts.append(s)
cad = np.diff([td[i] for i in starts])
j = int(np.argmin([abs(td[i] - 100.0) for i in starts]))
s0 = starts[j]
win = np.arange(s0 - 100, s0 + 300)

fig = plt.figure(figsize=(10.2, 7.6))
gs = fig.add_gridspec(3, 2, hspace=0.62, wspace=0.28)

ax = fig.add_subplot(gs[0, 0])
ax.plot(td, dv, lw=0.6, color='#1f4e9c')
ax.set_xlim(0, 130); ax.set_xlabel('t / s'); ax.set_ylabel(r'$\Delta u$ / pu')
ax.grid(alpha=0.3)
ax.set_title('(a) 注入包络：24 个 burst，起始间隔 %.3f s' % cad.mean(), fontsize=9, loc='left')

ax = fig.add_subplot(gs[0, 1])
ax.plot(tb, bv, lw=1.0, color='#1f4e9c')
ax.axhline(531.67, color='#c0392b', ls='--', lw=0.9, label=r'末值 531.67')
ax.axvline(124.58, color='0.5', ls=':', lw=0.9)
ax.set_xlim(0, 150); ax.set_ylim(395, 545)
ax.set_xlabel('t / s'); ax.set_ylabel(r'$\hat b_0$'); ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=7.5, loc='lower right')
ax.set_title('(b) 预热期直接赋值：首个 burst 即落到 532，124.6 s 冻结', fontsize=9, loc='left')

z1 = (td >= 0.0) & (td <= 0.45)
ax = fig.add_subplot(gs[1, 0])
ax.plot(td[z1], dv[z1], lw=1.0, color='#1f4e9c')
ax.axvline(0.2, color='0.6', ls=':', lw=0.8)
ax.set_xlabel('t / s'); ax.set_ylabel(r'$\Delta u$ / pu'); ax.grid(alpha=0.3)
ax.set_title('(c) 两段式：前 0.2 s 不注入，后 0.2 s 注入', fontsize=9, loc='left')

z2 = (td >= 0.25) & (td <= 0.31)
ax = fig.add_subplot(gs[1, 1])
ax.plot(tu[z2], uv[z2], lw=1.1, color='#6c3483', label='指令 $u$')
ax.plot(td[z2], dv[z2], lw=1.1, color='#1f4e9c', ls='--', label=r'注入 $\Delta u$')
ax.set_xlabel('t / s'); ax.set_ylabel('pu'); ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=7.5, loc='upper right')
ax.set_title('(d) 细节：注入叠在转速环输出上（65 Hz）', fontsize=9, loc='left')

ax = fig.add_subplot(gs[2, 0])
ax.plot(tq[z2], qv[z2], lw=1.1, color='#117864')
ax.set_xlabel('t / s'); ax.set_ylabel(r'$i_q$ / A'); ax.grid(alpha=0.3)
ax.set_title('(e) 电流响应（同一窗，峰值 %.2f A）' % np.abs(qv[z2]).max(), fontsize=9, loc='left')

ax = fig.add_subplot(gs[2, 1])
ax.plot(tw[win], wv[win], lw=1.0, color='#c0392b')
pp = wv[s0:s0 + 200].max() - wv[s0:s0 + 200].min()
ax.set_xlabel('t / s'); ax.set_ylabel(r'$\omega$ / rpm'); ax.grid(alpha=0.3)
ax.set_title('(f) 稳态 burst（t=%.1f s）转速峰峰 %.0f rpm' % (td[s0], pp), fontsize=9, loc='left')

fig.savefig(os.path.join(ROOT, 'fig_scope_foc2.png'), dpi=200, bbox_inches='tight')
print('burst %d 个, 间隔 %.3f s, 末 burst 起 %.2f s, 末 burst 末 %.2f s' % (len(starts), cad.mean(), td[starts[-1]], td[nz[-1]]))
print('注入 ±%.4f pu; iq 峰值 %.3f A (= %.3f pu)' % (np.abs(dv).max(), np.abs(qv).max(), np.abs(qv).max()/6.3069))
print('稳态 burst 转速峰峰 %.1f rpm (t=%.2f s)' % (pp, td[s0]))
print('saved fig_scope_foc2.png')
