# -*- coding: utf-8 -*-
"""run_realj_900.py —— 相位D：900 rpm 律D 定稿在真实 J（4.50e-5）下 vs §9 名义 J 行

口径同 run_lawd900_final.py（8 s、t=2 s 加载 0.5 额定 + 圆盘型线 V2 + 5.9 Hz、实验室噪声、
fci=500、beta3=4000、tau0=20 ms、类 fal ESO、种子 20261018），J_true=4.50e-5 且 j_oracle=True。
输出 _realj_900.json
"""
import json

import numpy as np

import noise_cfg as NC
from tl_profile import disc_unbalance_profile
from run_laws_compare import build_loads, AMP, ANG_START

J_TRUE = 4.50e-5
BASE = dict(n_ref=900.0, T=1.0 / 15.0, T_adapt=True, T_filt=50e-3,
            fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
            i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
            sig_n=NC.NOISE_LAB["sig_n_rpm"],
            sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
            tl_ang=None, tl_ang_amp=AMP,
            tl_ang_start=ANG_START, tl_ang_rev=29.9,
            eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
            rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
            J_true=J_TRUE, j_oracle=True)
CASES = [("base900_j24", dict(det_eps=0.0)),
         ("lawd900_j24", dict(kp_boost=6.0, kb_eso=3.0, kb_b3=0.0, det_eps=0.01))]


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kw = job
    t, TL = build_loads()
    cfg = dict(BASE); cfg["tl_ang"] = disc_unbalance_profile(); cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 900.0
    m = (tt >= 1.9) & (tt <= 2.5)
    i0 = int(np.where(m)[0][int(np.argmin(e[m]))])
    idx = np.where((np.abs(e) <= 20.0) & (np.arange(len(e)) > i0) & (tt >= 2.0))[0]
    d = dict(dip=float(np.min(e[m])),
             rec=float((tt[idx[0]] - 2.0) * 1e3) if len(idx) else float("nan"),
             step_rms=float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))),
             steady=float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2))),
             iq=float(np.max(np.abs(iq))), J_true=J_TRUE, j_oracle=True)
    print("%-12s dip %7.1f  rec %5.1f  stepRMS %5.1f  steady %5.2f  iq %5.2f"
          % (key, d["dip"], d["rec"], d["step_rms"], d["steady"], d["iq"]), flush=True)
    return key, d


if __name__ == "__main__":
    from multiprocessing import Pool
    with Pool(2) as p:
        res = p.map(one, CASES)
    json.dump(dict(res), open("_realj_900.json", "w"), indent=1)
    print("done")
