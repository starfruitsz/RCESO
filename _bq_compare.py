# -*- coding: utf-8 -*-
"""_bq_compare.py —— Python bpv 与 MATLAB bq 的逐窗对照"""
import numpy as np, scipy.io as sio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9
import sys
py_file = sys.argv[1] if len(sys.argv) > 1 else '_bq_dump.mat'
S = sio.loadmat(py_file)
bpv = np.asarray(S['bpv'])            # (t, bpv)
M = sio.loadmat(r'simulink\_bq_ml.mat')
tb = M['tb'].ravel(); bqv = M['bqv'].ravel()
TRUE = 101.89

print('%-6s %10s %10s' % ('窗', 'Python bq', 'MATLAB bq'))
pairs = []
for i in range(len(bpv)):
    t0 = bpv[i, 0]
    j = int(np.argmin(np.abs(tb - t0)))
    pyv, mlv = bpv[i, 1], bqv[j]
    pairs.append((t0, pyv, mlv))
    print('%-6.2f %10.2f %10.2f' % (t0, pyv, mlv))
pairs = np.asarray(pairs)
if len(pairs):
    print('\nPython: 均值 %.2f  中位 %.2f  |  偏差 vs 真值 %+.1f%%'
          % (pairs[:, 1].mean(), np.median(pairs[:, 1]), 100*(np.median(pairs[:, 1])/TRUE-1)))
    print('MATLAB: 均值 %.2f  中位 %.2f  |  偏差 vs 真值 %+.1f%%'
          % (pairs[:, 2].mean(), np.median(pairs[:, 2]), 100*(np.median(pairs[:, 2])/TRUE-1)))

fig, ax = plt.subplots(figsize=(8.4, 4.6))
ax.step(pairs[:, 0], pairs[:, 1], where='post', lw=1.6, color='#1f4e9c', label='Python（bpv）')
ax.step(pairs[:, 0], pairs[:, 2], where='post', lw=1.6, color='#c0392b', label='MATLAB（bq）')
ax.axhline(TRUE, color='0.35', lw=0.9, label='真值 101.89')
ax.set_xlabel('t / s'); ax.set_ylabel(r'逐窗原始估计 $b_q$'); ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=8)
ax.set_title('逐窗对照：同一段 1 ms 输入流，两套实现的 bq', fontsize=9, loc='left')
fig.savefig('fig_bq_compare.png', dpi=200, bbox_inches='tight')
print('saved fig_bq_compare.png')
