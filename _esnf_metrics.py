# -*- coding: utf-8 -*-
import numpy as np, json
res = {}
for tag in ("fr","nf"):
    z = np.load("_esnf_%s.npz" % tag)
    t = np.asarray(z["t"]); y = np.asarray(z["y"]); es = np.asarray(z["es"])
    yref = np.where(t >= 5.0, 1.5, 1.0)
    e = (y - yref) * 600.0
    m1 = (t >= 3.5) & (t < 5.0); m2 = (t >= 12.0) & (t < 20.0)
    # 10 Hz 幅值（后段 12-20 s 用 5 s 窗）
    w = (t >= 13.0) & (t < 18.0)
    x = e[w] - e[w].mean()
    X = np.fft.rfft(x * np.hanning(len(x)))
    fr = np.fft.rfftfreq(len(x), d=float(t[1]-t[0]))
    k = int(np.argmin(np.abs(fr - 15.0)))   # 900 rpm -> 15 Hz 机械基频
    a15 = float(2*np.abs(X[k])/np.sum(np.hanning(len(x))))
    d = dict(tag=tag,
             es_pre=float(np.mean(es[m1])), es_post=float(np.mean(es[m2])), es_post_std=float(np.std(es[m2])),
             rms_pre=float(np.sqrt(np.mean(e[m1]**2))), rms_post=float(np.sqrt(np.mean(e[m2]**2))),
             amp15_post=a15)
    res[tag] = d
    json.dump(d, open("_esnf_%s.json" % tag, "w"), indent=1)
    print("%-3s δ 前 %.4f 后 %.4f±%.4f   RMS %.2f→%.2f   15 Hz(后) %.2f" % (
        tag, d["es_pre"], d["es_post"], d["es_post_std"], d["rms_pre"], d["rms_post"], d["amp15_post"]))
