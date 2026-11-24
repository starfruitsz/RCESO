# -*- coding: utf-8 -*-
"""plot_severe.py —— b0 严重失配（标称 322 vs 真值 102）下的识别开/关对比"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8.8

ON = np.load('_tjc_sev_1.npz'); OFF = np.load('_tjc_sev_0.npz')
TRUE = 101.89
def ser(z):
    t = np.asarray(z['t']); step = max(1, len(t) // 120000)
    return t[::step], np.asarray(z['y'])[::step] * 600.0
def bcur(z):
    b = np.asarray(z['b0e']); return np.linspace(0, float(np.asarray(z['t'])[-1]), len(b)), b
t_on, w_on = ser(ON); t_off, w_off = ser(OFF)
tb_on, b_on = bcur(ON); tb_off, b_off = bcur(OFF)

def m10(t, w):
    m = (t > 40); x = w[m] - w[m].mean()
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), t[1]-t[0])
    return 2*np.abs(X[int(np.argmin(np.abs(fr - 10.0)))])/len(x)
a_on, a_off = m10(t_on, w_on), m10(t_off, w_off)
r_on = np.sqrt(np.mean((w_on[t_on > 40] - w_on[t_on > 40].mean())**2))
r_off = np.sqrt(np.mean((w_off[t_off > 40] - w_off[t_off > 40].mean())**2))

fig = plt.figure(figsize=(10.4, 6.8))
gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1], hspace=0.36, wspace=0.26)
a1 = fig.add_subplot(gs[0, :]); a2 = fig.add_subplot(gs[1, 0]); a3 = fig.add_subplot(gs[1, 1])

a1.plot(tb_off, b_off, '--', lw=1.4, color='0.45', label=r'识别关（恒 321.8，+216%）')
a1.plot(tb_on, b_on, lw=1.6, color='#117864', label=r'识别开（终值 95.7，−6.1%）')
a1.axhline(TRUE, color='0.35', lw=0.9, label='物理真值 101.89')
a1.set_xlim(0, 60); a1.set_ylim(60, 360)
a1.set_xlabel('t / s'); a1.set_ylabel(r'$\hat b_0$'); a1.grid(alpha=0.3)
a1.legend(frameon=False, fontsize=8, ncol=3, loc='upper right')
a1.set_title('(a) $\\hat b_0$：标称 321.8（真值的 3.2 倍）——严重失配', fontsize=9, loc='left')

m = (t_on >= 40) & (t_on <= 41); mf = (t_off >= 40) & (t_off <= 41)
a2.plot(t_off[mf], w_off[mf], lw=0.9, color='0.45', label='识别关')
a2.plot(t_on[m], w_on[m], lw=0.9, color='#117864', label='识别开')
a2.set_xlim(40, 41); a2.set_xlabel('t / s'); a2.set_ylabel(r'$\omega$ / rpm'); a2.grid(alpha=0.3)
a2.legend(frameon=False, fontsize=8, loc='upper right')
a2.set_title('(b) 转速放大 40–41 s', fontsize=9, loc='left')

x = np.arange(2); bw = 0.35
a3.bar(x - bw/2, [a_off, r_off], bw, color='0.55', label='识别关')
a3.bar(x + bw/2, [a_on, r_on], bw, color='#117864', label='识别开')
for i, (v1, v2) in enumerate(((a_off, a_on), (r_off, r_on))):
    a3.text(i - bw/2, v1 + 0.3, '%.1f' % v1, ha='center', fontsize=7.5)
    a3.text(i + bw/2, v2 + 0.3, '%.1f' % v2, ha='center', fontsize=7.5)
a3.set_xticks(x); a3.set_xticklabels(['10 Hz 幅值', '总 rms'])
a3.set_ylabel('rpm'); a3.grid(alpha=0.3, axis='y'); a3.legend(frameon=False, fontsize=7.5)
a3.set_title('(c) 40–60 s 统计', fontsize=9, loc='left')

fig.suptitle('b0 严重失配下的识别对比（标称 3.2× 真值；50% 负载 + 三合一故障）', fontsize=10)
fig.savefig('fig_severe.png', dpi=200, bbox_inches='tight')
print('10 Hz 开 %.2f / 关 %.2f   rms 开 %.2f / 关 %.2f' % (a_on, a_off, r_on, r_off))
print('saved fig_severe.png')
