# -*- coding: utf-8 -*-
"""run_lawd_realj.py —— 真实 J（4.81e-5=2.545 J_nom）下律D 的电流受限重调

协议同 run_lawd_cmp_600.py：8 s、600 rpm、t=2 s 加载 0.5 额定 + 圆盘型线 V2 + 5.9 Hz
振动、实验室噪声、fci=500、beta3=4000、tau0=20 ms、类 fal ESO、种子 20261018。
J_true=4.81e-5、j_oracle=True（b0 用真实 J）。约束：max|iq| <= 6.31 A（额定 6.31 A）。

三族：
  A 用户指定网格：kp_boost {3,4,5,6} x kb_eso {2,3} x det_eps {0.005,0.01,0.02,0.04}
  B 基准增益族：无律D，kp {75.36,70,65,60}（真实 J 下基准自身超额定时的降增益方案）
  C 在 B 最优 kp 上叠律D：kp_boost {3,6} x kb_eso {3} x det_eps {0.01,0.02}
输出 _lawd_realj.json（含 _meta 与 _best）
"""
import json

import numpy as np

import noise_cfg as NC
from tl_profile import disc_unbalance_profile
from run_laws_compare import build_loads, N_REF, AMP, ANG_START

J_TRUE = 4.81e-5
J_NOM = 1.89e-5
I_RATED = 6.31
BASE = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
            rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
            fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3,
            seed_i=20261018,
            i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
            sig_n=NC.NOISE_LAB["sig_n_rpm"],
            sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
            tl_ang=None, tl_ang_amp=AMP,
            tl_ang_start=ANG_START, tl_ang_rev=29.9,
            eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
            J_true=J_TRUE, j_oracle=True)

CASES = []
# A 用户指定网格
for kb in (3.0, 4.0, 5.0, 6.0):
    for ke in (2.0, 3.0):
        for de in (0.005, 0.01, 0.02, 0.04):
            CASES.append(("A_kb%g_e%g_d%g" % (kb, ke, de),
                          dict(kp_boost=kb, kb_eso=ke, det_eps=de)))
# B 基准增益族（无律D）
for kp in (75.36, 70.0, 65.0, 60.0):
    CASES.append(("B_kp%g" % kp, dict(kp=kp, det_eps=0.0)))
# C 降增益 + 律D
for kb in (3.0, 6.0):
    for de in (0.01, 0.02):
        CASES.append(("C_kp65_kb%g_d%g" % (kb, de),
                      dict(kp=65.0, kp_boost=kb, kb_eso=3.0, det_eps=de)))


def metrics(tt, y, iq):
    e = (y - 1.0) * N_REF
    m_dip = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(e[m_dip]))
    i_dip = int(np.where(m_dip)[0][int(np.argmin(e[m_dip]))])
    ok = (np.abs(e) <= 20.0) & (np.arange(len(e)) > i_dip) & (tt >= 2.0)
    idx = np.where(ok)[0]
    rec = float(tt[idx[0]] - 2.0) * 1e3 if len(idx) else float("nan")
    iqa = np.abs(iq)
    return dict(dip=dip, rec_ms=rec,
                step_rms=float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))),
                steady=float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2))),
                iq_max=float(np.max(iqa)),
                iq_peak_t=float(tt[int(np.argmax(iqa))]),
                iq_step=float(np.max(iqa[(tt >= 1.99) & (tt <= 2.10)])))


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kw = job
    t, TL = build_loads()
    cfg = dict(BASE); cfg["tl_ang"] = disc_unbalance_profile(); cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    d = metrics(tt, y, iq)
    d.update(kp_boost=float(cfg.get("kp_boost", 0.0)), kb_eso=float(cfg.get("kb_eso", 0.0)),
             det_eps=float(cfg.get("det_eps", 0.0)), kp=float(cfg.get("kp", 75.36)))
    d["ok"] = bool(d["iq_max"] <= I_RATED)
    print("%-18s dip %7.1f rec %6.1f stepRMS %5.1f steady %5.2f iq %5.2f(@%.3f) iq_step %5.2f %s"
          % (key, d["dip"], d["rec_ms"], d["step_rms"], d["steady"], d["iq_max"],
             d["iq_peak_t"], d["iq_step"], "OK" if d["ok"] else "OVER"), flush=True)
    return key, d


if __name__ == "__main__":
    import hashlib
    from multiprocessing import Pool
    sha = hashlib.sha256(open("pmsm_inv_sim.py", "rb").read()).hexdigest()
    with Pool(6) as p:
        res = p.map(one, CASES)
    out = dict(res)
    feas = [(v["step_rms"], k, v) for k, v in out.items() if v["ok"]]
    feas.sort()
    best = feas[0] if feas else None
    out["_meta"] = dict(J_true=J_TRUE, J_nom=J_NOM, ratio=J_TRUE / J_NOM,
                        i_rated=I_RATED, sim_sha256=sha, n_cases=len(CASES),
                        feasible=[k for _, k, _ in feas],
                        best=best[1] if best else None)
    out["_best"] = best[2] if best else None
    json.dump(out, open("_lawd_realj.json", "w"), indent=1)
    print("\nfeasible(iq<=%.2f): %s" % (I_RATED, [k for _, k, _ in feas]))
    print("best by step_rms: %s" % (best[1] if best else "NONE"))
    print("done  sim_sha256=%s" % sha)
