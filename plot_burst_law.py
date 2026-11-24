# -*- coding: utf-8 -*-
"""plot_burst_law.py —— 逐 burst：原始估计 bq、门控权重 w、goal、以及低通后的 b̂0"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.8

z = np.load('_tjc_ali12_sin.npz'); jn = np.asarray(z['jnew'])
e = [(float(r[0]), float(r[2])) for r in jn if r[0] > 0]
be = e[2::3]
tbq = np.array([b[0] for b in be])          # 每个 burst 结束时刻
bq = np.array([b[1] for b in be])
TRUE = 101.89

# 离线复现更新律（warm=3, abase=0.30, mu=0.35, d1=0.10, d2=0.20, dmax=0.50）
D1, D2, DMAX, ABASE, MU, WARM = 0.10, 0.20, 0.50, 0.30, 0.35, 3
base = bq[0]; nest = 1; w = np.full(len(bq), np.nan); goal = np.full(len(bq), np.nan)
b0_at = []
for i in range(len(bq)):
    b0_now = np.interp(tbq[i], np.linspace(0, float(np.asarray(z['t'])[-1]), len(np.asarray(z['b0e']))), np.asarray(z['b0e']))
    b0_at.append(b0_now)
    if i == 0 or nest < WARM:
        goal[i] = bq[i]; w[i] = np.nan
        if i > 0: nest += 1
    else:
        dd = abs(bq[i] - base) / max(abs(base), 1e-9)
        wi = 1.0 if dd <= D1 else (np.exp(-(dd - D1)/D2) if dd <= DMAX else np.exp(-(DMAX - D1)/D2))
        w[i] = wi
        goal[i] = b0_now + ABASE * wi * (bq[i] - b0_now)
        base = base + MU * (bq[i] - base)
        nest += 1

fig, axes = plt.subplots(2, 1, figsize=(9.4, 7.0), gridspec_kw=dict(height_ratios=[1.25, 1]))
a1, a2 = axes
t1 = np.linspace(0, float(np.asarray(z['t'])[-1]), len(np.asarray(z['b0e'])))
a1.plot(t1, np.asarray(z['b0e']), lw=1.6, color='#117864', label=r'低通后的 $\hat b_0$（实际值）')
a1.plot(tbq, bq, 'o', ms=4, color='#1f4e9c', label='逐 burst 原始估计 $b_q$')
a1.plot(tbq, goal, 's', ms=3, mfc='none', mec='#c0392b', label='每个 burst 设定的 goal')
a1.axhline(TRUE, color='0.35', lw=0.9, label='真值 101.89')
a1.set_xlim(0, 130); a1.set_ylim(82, 132)
a1.set_xlabel('t / s'); a1.set_ylabel(r'$b$'); a1.grid(alpha=0.3)
a1.legend(frameon=False, fontsize=8, ncol=2)
a1.set_title('(a) 原始估计 → goal → 低通（τ=50/kp=0.663 s）→ $\\hat b_0$', fontsize=9, loc='left')

a2.vlines(tbq, 0, np.nan_to_num(w, nan=1.0), color='#c0392b', lw=1.6)
a2.plot(tbq, np.nan_to_num(w, nan=1.0), 'o', ms=3, color='#c0392b')
a2.axhline(1.0, color='0.7', lw=0.7, ls=':')
a2.set_xlim(0, 130); a2.set_ylim(0, 1.15)
a2.set_xlabel('t / s'); a2.set_ylabel('门控权重 $w$（1 = 直采）')
a2.grid(alpha=0.3)
a2.set_title('(b) 门控权重（前 3 个为预热，直接采用；之后 $w=\\exp(-(d-0.1)/0.2)$）', fontsize=9, loc='left')
fig.tight_layout()
fig.savefig('fig_burst_law.png', dpi=200, bbox_inches='tight')
print('w 序列:', ' '.join(('%.2f' % x) if np.isfinite(x) else '预' for x in w))
print('saved fig_burst_law.png')
