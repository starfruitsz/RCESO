# -*- coding: utf-8 -*-
"""plot_wave_compare.py —— 三波：左列 Simulink、右列 Python（同行同一物理量）"""
import numpy as np, scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.5

M = sio.loadmat('simulink/wave_full_on.mat', squeeze_me=True, struct_as_record=False)['res']
files = {'正弦': '_tjc_xe_W=sin.npz', '方波': '_tjc_xe_W=sq SQ=1.npz', '三角': '_tjc_xe_W=tri TRI=1.npz'}
names = ['正弦', '方波', '三角']
colors = ['#1f4e9c', '#c0392b', '#117864']
TRUE, PYTRUE = 536.40, 101.89

fig, ax = plt.subplots(3, 2, figsize=(10.2, 8.0))
for i, nm in enumerate(names):
    r = M[i]; z = np.load(files[nm])
    ts = np.asarray(r.t); bs = np.asarray(r.b0)
    tp = np.asarray(z['t']); bp = np.asarray(z['b0e'])
    tb = np.linspace(0, float(tp[-1]), len(bp))
    step = max(1, len(tp) // 40000)
    yp, iqp, tps = np.asarray(z['y'])[::step] * 600.0, np.asarray(z['iq'])[::step], tp[::step]

    ax[0, 0].plot(ts, bs, lw=1.5, color=colors[i], label=nm)
    ax[0, 1].plot(tb, bp, lw=1.5, color=colors[i], label=nm)
    for j, (yy, tt, lo, hi, f) in enumerate(((yp, tps, 20, 40, ax[1, 1]),)):
        pass
    m = (ts >= 20) & (ts <= 40)
    mp = (tps >= 20) & (tps <= 40)
    ax[1, 0].plot(ts[m], np.asarray(r.w)[m], lw=0.6, color=colors[i])
    ax[1, 1].plot(tps[mp], yp[mp], lw=0.6, color=colors[i])
    ax[2, 0].plot(ts[m], np.asarray(r.iq)[m], lw=0.6, color=colors[i])
    ax[2, 1].plot(tps[mp], iqp[mp], lw=0.6, color=colors[i])

ax[0, 0].axhline(TRUE, color='0.35', lw=0.9)
ax[0, 0].set_xlim(0, 130); ax[0, 0].set_ylim(390, 550)
ax[0, 0].set_title(r'Simulink：$\hat b_0$（130 s，1 ms，含噪声）', fontsize=9, loc='left')
ax[0, 0].legend(frameon=False, fontsize=7, loc='lower right')
ax[0, 1].axhline(PYTRUE, color='0.35', lw=0.9)
ax[0, 1].set_xlim(0, 60); ax[0, 1].set_ylim(60, 190)
ax[0, 1].set_title(r'Python：$\hat b_0$（60 s，50 μs，含噪声，真值 101.9）', fontsize=9, loc='left')
ax[0, 1].legend(frameon=False, fontsize=7, loc='lower right')

for j, ylab in ((1, r'$\omega$ / rpm'), (2, r'$i_q$ / A')):
    for k in (0, 1):
        ax[j, k].set_xlim(20, 40); ax[j, k].set_xlabel('t / s')
        ax[j, k].set_ylabel(ylab); ax[j, k].grid(alpha=0.3)
ax[1, 0].set_title('Simulink：转速（20–40 s）', fontsize=9, loc='left')
ax[1, 1].set_title('Python：转速（20–40 s）', fontsize=9, loc='left')
ax[2, 0].set_title('Simulink：电流（20–40 s）', fontsize=9, loc='left')
ax[2, 1].set_title('Python：电流（20–40 s）', fontsize=9, loc='left')
for k in (0, 1):
    ax[0, k].grid(alpha=0.3); ax[0, k].set_xlabel('t / s')

fig.suptitle('三波对比（左：Simulink / 右：Python）', fontsize=10)
fig.tight_layout()
fig.savefig('fig_wave_compare.png', dpi=200, bbox_inches='tight')
print('saved fig_wave_compare.png')
