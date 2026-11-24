# plot_py_final_3wave.py —— Python（定稿更新律：预热直采 + 门控 + 冻结）三波 b0
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

RUNS = [('_tjc_pf_W=sin.npz', '正弦', '#1f4e9c'), ('_tjc_pf_W=sq SQ=1.npz', '方波', '#c0392b'),
        ('_tjc_pf_W=tri TRI=1.npz', '三角', '#117864')]
TRUE = 101.89
fig, ax = plt.subplots(figsize=(8.6, 4.5))
for f, name, c in RUNS:
    try:
        z = np.load(f)
    except Exception as e:
        print('skip', f, e); continue
    t = np.asarray(z['t']); b = np.asarray(z['b0e'])
    tb = np.linspace(0, float(t[-1]), len(b))
    ax.plot(tb, b, lw=1.7, color=c, label='%s：%.1f（%+.1f%%）' % (name, b[-1], 100*(b[-1]/TRUE-1)))
ax.axhline(TRUE, color='0.35', lw=0.9, label='物理真值 101.89')
ax.axhspan(TRUE*0.97, TRUE*1.03, color='0.85', alpha=0.5, lw=0, label='±3%')
ax.set_xlabel('t / s'); ax.set_ylabel(r'$\hat b_0$'); ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=8, loc='upper right')
ax.set_title('Python 带噪声闭环（预热直采 + 门控 + 冻结，与 Simulink 同律）', fontsize=9, loc='left')
fig.savefig('fig_py_final_3wave.png', dpi=200, bbox_inches='tight')
print('saved fig_py_final_3wave.png')
