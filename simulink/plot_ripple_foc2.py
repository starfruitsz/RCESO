# plot_ripple_foc2.py —— 电流纹波放大路径：65 Hz 相量与分解
# 依赖 foc2_log.mat（由 scope_foc2.m 导出，含 u/e1/v 记录）
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
def arr(k): return m[k].ravel()
tw, wv = arr('tw'), arr('wv'); td, dv = arr('td'), arr('dv')
tu, uv = arr('tu'), arr('uv'); tq, qv = arr('tq'), arr('qv')
te, ev = arr('te'), arr('ev'); tv, vv = arr('tv'), arr('vv')
WR, KP, IB = 62.832, 75.36, 6.3069

nz = np.nonzero(np.abs(dv) > 1e-9)[0]
starts, s, p = [], nz[0], nz[0]
for k in nz[1:]:
    if k != p + 1: starts.append(s); s = k
    p = k
starts.append(s)
j = int(np.argmin([abs(td[i] - 100.0) for i in starts]))
s0 = starts[j]; seg = np.arange(s0, s0 + 200); t = td[seg]
phw = np.exp(-1j * 2 * np.pi * 65.0 * t)
def PH(x): return 2 / len(seg) * np.sum(x * phw)

du = PH(dv[seg]); u = PH(uv[seg]); ul = PH((uv - dv)[seg])
iq = PH(qv[seg]) / IB
w_pu = PH(wv[seg]) / 600.0; e1 = PH(ev[seg]); en = -w_pu + e1
uP = KP * en / WR; uV = -PH(vv[seg]) / WR; uZ = u - uP - uV

fig = plt.figure(figsize=(10.2, 3.9))
gs = fig.add_gridspec(1, 3, wspace=0.32)

ax = fig.add_subplot(gs[0, 0])
tt = t - t[0]
ax.plot(tt, dv[seg], color='#1f4e9c', lw=1.0, label=r'注入 $\Delta u$')
ax.plot(tt, (uv - dv)[seg], color='#c0392b', lw=1.0, label=r'转速环反应 $u_{\rm loop}$')
ax.plot(tt, uv[seg], color='0.25', lw=0.9, ls='--', label=r'合计 $u$')
ax.set_xlabel('注入段内时间 / s'); ax.set_ylabel('pu')
ax.grid(alpha=0.3); ax.legend(frameon=False, fontsize=7.5, loc='lower right')
ax.set_title('(a) 同一窗的时域波形', fontsize=9, loc='left')

ax = fig.add_subplot(gs[0, 1])
for nm, v, c in [('$\\Delta u$', du, '#1f4e9c'), ('$u_{\\rm loop}$', ul, '#c0392b'),
                 ('$u$', u, '0.25'), ('$i_q$', iq, '#117864')]:
    ax.annotate('', xy=(v.real, v.imag), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.4))
    ax.text(v.real * 1.08, v.imag * 1.08, nm, color=c, fontsize=8)
lim = 0.26
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
ax.axhline(0, color='0.7', lw=0.6); ax.axvline(0, color='0.7', lw=0.6)
ax.set_aspect('equal'); ax.grid(alpha=0.25)
ax.set_xlabel('实部 / pu'); ax.set_ylabel('虚部 / pu')
ax.set_title('(b) 65 Hz 相量：$u=\\Delta u+u_{\\rm loop}$', fontsize=9, loc='left')

ax = fig.add_subplot(gs[0, 2])
names = ['$\\Delta u$', '$u_{\\rm loop}$', '$u$', '$P$ 项', '$z_2$ 项', '$v$ 项']
vals = [abs(du), abs(ul), abs(u), abs(uP), abs(uZ), abs(uV)]
cols = ['#1f4e9c', '#c0392b', '0.25', '#6c3483', '#b9770e', '#7d7d7d']
ax.barh(range(len(vals)), vals, color=cols, height=0.62)
ax.set_yticks(range(len(vals))); ax.set_yticklabels(names)
ax.invert_yaxis(); ax.set_xlabel('65 Hz 幅值 / pu'); ax.grid(alpha=0.3, axis='x')
for i, v in enumerate(vals):
    ax.text(v + 0.006, i, '%.3f' % v, va='center', fontsize=7.5)
ax.set_xlim(0, max(vals) * 1.25)
ax.set_title('(c) $u$ 的构成与放大', fontsize=9, loc='left')

fig.savefig(os.path.join(ROOT, 'fig_ripple_foc2.png'), dpi=200, bbox_inches='tight')
print('|du|=%.4f  |u|=%.4f  |iq|=%.4f pu  |u|/|du|=%.2f  |iq|/|du|=%.2f'
      % (abs(du), abs(u), abs(iq), abs(u) / abs(du), abs(iq) / abs(du)))
print('|P|=%.4f  |z2|=%.4f  |v|=%.4f  |u_loop|=%.4f' % (abs(uP), abs(uZ), abs(uV), abs(ul)))
print('相位: u=%.1f°, u_loop=%.1f°, iq=%.1f°（以 du 为 0°）'
      % (np.degrees(np.angle(u / du)), np.degrees(np.angle(ul / du)), np.degrees(np.angle(iq / du))))
print('转速 65 Hz 幅值 %.1f rpm；保存 fig_ripple_foc2.png' % abs(PH(wv[seg])))
