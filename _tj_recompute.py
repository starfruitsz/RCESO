# -*- coding: utf-8 -*-
"""_tj_recompute.py —— 从 _tj_*.npz 重算指标（含 iq1ms 峰值时刻与去启动值）。"""
import numpy as np, json

for tag, mode in (("base","base"),("t","t"),("j","j"),("fusion","fusion")):
    z = np.load("_tj_%s.npz" % tag)
    tt = np.asarray(z["t"]); y = np.asarray(z["y"]); iq = np.asarray(z["iq"])
    es = np.asarray(z["es"]); jh = np.asarray(z["jhat"]); b0 = np.asarray(z["b0e"])
    e = (y - 1.0) * 600.0
    m = tt >= 25.0
    rms = float(np.sqrt(np.mean(e[m] ** 2)))
    w = (tt >= 25.0) & (tt < 30.0)
    x = e[w] - e[w].mean()
    X = np.fft.rfft(x * np.hanning(len(x)))
    fr = np.fft.rfftfreq(len(x), d=float(tt[1] - tt[0]))
    k10 = int(np.argmin(np.abs(fr - 10.0)))
    a10 = float(2.0 * np.abs(X[k10]) / np.sum(np.hanning(len(x))))
    n1 = int(round(1e-3 / (tt[1] - tt[0])))
    iq1 = np.abs(iq[:len(iq)//n1*n1].reshape(-1, n1).mean(axis=1))
    t1 = tt[:len(iq1)*n1:n1]
    k = int(iq1.argmax())
    iq1ms = float(iq1.max()); tpk = float(t1[k])
    iq1ms_ss = float(iq1[t1 >= 3.0].max())
    d = dict(tag=tag, mode=mode, use_t=("t" in mode), use_j=("j" in mode), J_true=9.95e-5,
             jfin=float(jh[-1]), jerr_pct=float(100.0 * (jh[-1] / 9.95e-5 - 1.0)),
             b0e=float(b0[-1]), es_end=float(es[-1] if es.size else 0.0),
             es_mean=float(np.mean(es[tt >= 25.0])) if es.size else 0.0,
             rms=rms, amp10=a10, iq1ms=iq1ms, iq1ms_t=tpk, iq1ms_ss=iq1ms_ss,
             iq_raw=float(np.abs(iq).max()))
    json.dump(d, open("_tj_%s.json" % tag, "w"), indent=1)
    print("%-7s RMS %6.2f  10Hz %6.2f  iq1ms %5.2f @%.2fs (去启动 %5.2f)  Jhat %+6.1f%%  b0e %6.1f  es %7.3f" % (
        tag, rms, a10, iq1ms, tpk, iq1ms_ss, d["jerr_pct"], d["b0e"], d["es_mean"]), flush=True)
