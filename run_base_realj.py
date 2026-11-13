# -*- coding: utf-8 -*-
"""run_base_realj.py —— 真实 J（4.81e-5=2.545 J_nom）+ j_oracle 下“基准环”自身的重调

背景：J 由 J_nom 抬到 2.545 J_nom 后，b0 由 oracle 按真实 J 归一，归一化环路形状不变，
但加载阶跃的 iq 尖峰由 5.80 A 升到 6.72 A（> 额定 6.31 A）。律D 只会加增益，故必须
先重调基准环的 kp / wo（律D 关）。

阶段1：kp ∈ {40,50,60,75.36} × wo ∈ {300,400,500}，det_eps=0（律D 关），12 例，8 s
阶段2：在阶段1 的最优可行基准上叠律D 3 例（kb3/e2/d.01、kb3/e3/d.02、kb6/e3/d.01）
指标：dip、rec(±20 rpm)、stepRMS[2,2.5)、steady[7,8)、iq_global、iq_step[1.99,2.10]、
      另给 1 ms 块均值（基波包络，剔除 10 kHz PWM 纹波）与 100 us 块均值。
输出 _base_realj.json
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

STAGE1 = []
for kp in (40.0, 50.0, 60.0, 75.36):
    for wo in (300.0, 400.0, 500.0):
        STAGE1.append(("kp%g_wo%g" % (kp, wo), dict(kp=kp, wo=wo, det_eps=0.0)))


def bmean(x, n):
    m = len(x) // n * n
    return x[:m].reshape(-1, n).mean(axis=1)


def metrics(tt, y, iq):
    e = (y - 1.0) * N_REF
    m_dip = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(e[m_dip]))
    i_dip = int(np.where(m_dip)[0][int(np.argmin(e[m_dip]))])
    ok = (np.abs(e) <= 20.0) & (np.arange(len(e)) > i_dip) & (tt >= 2.0)
    idx = np.where(ok)[0]
    rec = float(tt[idx[0]] - 2.0) * 1e3 if len(idx) else float("nan")
    iqa = np.abs(iq)
    m1 = (tt >= 1.99) & (tt <= 2.10)
    av1 = np.abs(bmean(iq, 100))      # 1 ms 块均值（基波包络）
    av01 = np.abs(bmean(iq, 10))      # 100 us（一个 PWM 周期）
    n = 100
    t1 = tt[:len(tt) // n * n:n] + 0.5e-3
    return dict(dip=dip, rec_ms=rec,
                step_rms=float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))),
                steady=float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2))),
                iq_global=float(iqa.max()), iq_g_t=float(tt[int(iqa.argmax())]),
                iq_step=float(iqa[m1].max()),
                iq1ms=float(av1.max()), iq1ms_t=float(t1[int(av1.argmax())]),
                iq100us=float(av01.max()))


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kw = job
    t, TL = build_loads()
    cfg = dict(BASE); cfg["tl_ang"] = disc_unbalance_profile(); cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    d = metrics(tt, y, iq)
    d.update(kp=float(cfg["kp"]), wo=float(cfg["wo"]),
             kp_boost=float(cfg.get("kp_boost", 0.0)),
             kb_eso=float(cfg.get("kb_eso", 0.0)), det_eps=float(cfg.get("det_eps", 0.0)))
    d["ok"] = bool(d["iq_global"] <= I_RATED)
    d["ok1ms"] = bool(d["iq1ms"] <= I_RATED)
    print("%-14s dip %7.1f rec %6.1f stepRMS %5.1f steady %5.2f | iq_glob %5.2f(@%.3f) "
          "iq_step %5.2f iq1ms %5.2f(@%.3f) iq100us %5.2f %s"
          % (key, d["dip"], d["rec_ms"], d["step_rms"], d["steady"], d["iq_global"],
             d["iq_g_t"], d["iq_step"], d["iq1ms"], d["iq1ms_t"], d["iq100us"],
             "OK" if d["ok"] else "OVER"), flush=True)
    return key, d


if __name__ == "__main__":
    import hashlib
    from multiprocessing import Pool
    sha = hashlib.sha256(open("pmsm_inv_sim.py", "rb").read()).hexdigest()
    out = {}
    print("stage1: kp x wo, law D off", flush=True)
    with Pool(6) as p:
        for k, d in p.map(one, STAGE1):
            out[k] = d
    # 阶段2：最优可行基准 + 律D
    feas = sorted([(d["step_rms"], k) for k, d in out.items() if d["ok"]])
    pick = feas[0][1] if feas else min(out.items(), key=lambda kv: kv[1]["iq1ms"] * 10 + kv[1]["step_rms"])[0]
    print("\nstage1 feasible: %s ; pick=%s" % ([k for _, k in feas], pick), flush=True)
    b = out[pick]
    stage2 = []
    for tag, kw in [("lawd_kb3_e2_d01", dict(kp_boost=3.0, kb_eso=2.0, det_eps=0.01)),
                    ("lawd_kb3_e3_d02", dict(kp_boost=3.0, kb_eso=3.0, det_eps=0.02)),
                    ("lawd_kb6_e3_d01", dict(kp_boost=6.0, kb_eso=3.0, det_eps=0.01))]:
        stage2.append(("%s_%s" % (pick, tag),
                       dict(kp=b["kp"], wo=b["wo"], **kw)))
    print("stage2: law D on %s" % pick, flush=True)
    with Pool(3) as p:
        for k, d in p.map(one, stage2):
            out[k] = d
    out["_meta"] = dict(J_true=J_TRUE, J_nom=J_NOM, ratio=J_TRUE / J_NOM,
                        i_rated=I_RATED, sim_sha256=sha, n_stage1=len(STAGE1),
                        stage1_feasible=[k for _, k in feas], pick=pick,
                        n_stage2=len(stage2))
    json.dump(out, open("_base_realj.json", "w"), indent=1)
    print("done  sha=%s" % sha)
