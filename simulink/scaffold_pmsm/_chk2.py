import numpy as np, scipy.io as sio
S = sio.loadmat(r'simulink/scaffold_pmsm/_pm_foc_dump.mat')
t = S['t'].ravel(); du = S['du'].ravel(); iq = S['iq'].ravel(); u = S['u'].ravel()
nz = np.abs(du) > 1e-6
print('du 非零样本 %d / %d' % (nz.sum(), len(du)))
if nz.any():
    tt = t[nz]
    # 连续段
    br = np.where(np.diff(tt) > 0.5)[0]
    segs, s0 = [], tt[0]
    for i in br:
        segs.append((s0, tt[i])); s0 = tt[i+1]
    segs.append((s0, tt[-1]))
    print('非零段 %d 个，前 6 个：' % len(segs), [(round(a,2), round(b,2)) for a, b in segs[:6]])
print('iq 全局 pp %.4f   u 全局 pp %.4f' % (np.ptp(iq), np.ptp(u)))
