# -*- coding: utf-8 -*-
"""run_eso_trace.py —— 存一对照轨迹（线性档 vs 类 fal 档），供 plot_eso_fal.py 出图

同种子、同噪声实现，唯一差别是 ESO 校正增益形状。
输出：_eso_trace.npz（t / y_lin / y_fal / iq_lin / iq_fal / u_lin / u_fal）
"""
import math
import numpy as np
from pmsm_inv_sim import sim_inv, N_REF

T, DT, TEND, TL0, TW = 0.1, 2e-6, 8.0, 2.0, 6.0
BASE = dict(i_noise_peak=0.2, fci=500.0, beta3=4000.0, tau0=20e-3, seed_i=20261018)


def build_case():
    t = np.arange(0.0, TEND, DT)
    tau = np.maximum(t - TL0, 0.0)
    ph = 2 * math.pi * tau / T
    on = (t >= TL0).astype(float)
    onp = ((t >= TL0) & (t < TW)).astype(float)
    TL = (0.50 * on + 0.30 * onp *
          (np.sin(ph) + 0.4 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph))) * 0.637
    return t, TL


def main():
    t, TL = build_case()
    out = {}
    for name, kw in [("lin", dict(eso_law="linear")),
                     ("fal", dict(eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0))]:
        Y = sim_inv(t, TL, dict(BASE, **kw))
        out["t"] = Y["t"]
        out["y_" + name] = Y["y"]
        out["iq_" + name] = Y["iq"]
        out["u_" + name] = Y["u"]
        print(name, "done", flush=True)
    np.savez_compressed("_eso_trace.npz", **out)
    print("saved _eso_trace.npz", len(out["t"]))


if __name__ == "__main__":
    main()
