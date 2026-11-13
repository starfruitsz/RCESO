
import numpy as np, json
Z = np.load("_wave_realj_check.npz")
t = Z["t"]
print("npz keys:", list(Z.keys()))
print("t range %.3f..%.3f  dt=%.1e" % (t[0], t[-1], t[1]-t[0]))
for k in ["base_jnom","lawd_jnom","base_j24","lawd_j24"]:
    iq = Z["iq_"+k]; y = Z["y_"+k]
    m = (t>=1.98)&(t<=2.12)
    idx = np.where(m)[0]
    # 1 ms 抽样
    sel = idx[::100]
    print("\n=== %s ===  max|iq|=%.3f @ %.4f   dip=%.1f rpm @ %.4f" % (k, np.abs(iq).max(), t[np.abs(iq).argmax()], (y.min()-1)*600, t[y.argmin()]))
    print("  t      iq(A)   n(rpm)")
    for j in sel:
        print("  %.4f  %6.3f  %7.1f" % (t[j], iq[j], (y[j]-1)*600))
