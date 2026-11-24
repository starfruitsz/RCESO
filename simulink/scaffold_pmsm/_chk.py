import numpy as np, scipy.io as sio
S = sio.loadmat(r'simulink/scaffold_pmsm/_pm_foc_dump.mat')
t = S['t'].ravel(); iq = S['iq'].ravel(); u = S['u'].ravel(); du = S['du'].ravel()
for lo, hi, lab in ((8.20, 8.40, 'burst on'), (8.00, 8.20, 'off'), (13.20, 13.40, 'burst2 on')):
    m = (t >= lo) & (t < hi)
    print('%-10s iq: mean %.4f  pp %.4f | u: mean %.4f pp %.4f | du: pp %.4f'
          % (lab, iq[m].mean(), np.ptp(iq[m]), u[m].mean(), np.ptp(u[m]), np.ptp(du[m])))
