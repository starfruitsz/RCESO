# -*- coding: utf-8 -*-
"""_tj_recompute.py —— 指标重算（含校验开关）。"""
import numpy as np, json

TAGS = ("base","t","j","fusion","j10","fusion10","jd2","jd10","fd2","fd10","o2","o10","d2","d10",
        "d2n","d10n","o2n","o10n")
for tag in TAGS:
    try:
        z = np.load("_tj_%s.npz" % tag)
    except FileNotFoundError:
        continue
    tt = np.asarray(z["t"]); y = np.asarray(z["y"]); iq = np.asarray(z["iq"])
    es = np.asarray(z["es"]); b0 = np.asarray(z["b0e"])
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
    d = dict(tag=tag, J_true=9.95e-5, b0e=float(b0[-1]),
             b0_err_pct=float(100.0 * (b0[-1] / 122.3 - 1.0)),
             es_mean=float(np.mean(es[tt >= 25.0])) if es.size else 0.0,
             rms=rms, amp10=a10, iq1ms=float(iq1.max()), iq_raw=float(np.abs(iq).max()))
    json.dump(d, open("_tj_%s.json" % tag, "w"), indent=1)
    print("%-8s RMS %6.2f  10Hz %6.2f  iq1ms %5.2f  b0e %6.1f (%+6.1f%%)  es %7.3f" % (
        tag, rms, a10, d["iq1ms"], d["b0e"], d["b0_err_pct"], d["es_mean"]), flush=True)
