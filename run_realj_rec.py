# -*- coding: utf-8 -*-
"""run_realj_rec.py —— 相位C：真实 J（2.4 J_nom）下 D+T+J 主线的推荐工况表

12 s、600 rpm、单种子 20261018、实验室噪声、圆盘故障 T1∈{0.10,0.15,0.20} N·m
（κ=K(T1)=T1/(0.1*9.80665*1e-4)，M=0.1 kg、e=1e-4 m）；配置逐项同 run_trio.py，
只有 J_true=4.81e-5（=2.545 J_nom，自洽传动链口径）不同：
  J 辨识：j_id=True、A=0.157、t0=1 s、tend=3 s、nmin=5、std_max=0.15、snr_min=2
  律D   ：kp_boost=6、kb_eso=3、det_eps=0.01
  T 自适应：T_es=True（run_trio 默认 δ0=-14.3%、Δ=1%、σ=1%、Pd=1.5 s、N=3、t0=3 s）
另加一档 T1=0.15 但 j_id 关（D+T only）作对比。
指标同 run_trio：11–12 s 的 10 Hz 分量与 RMS；另记 |iq| 峰值、Jhat、末状态。
输出 _realj_rec.json
"""
import json
import math

import numpy as np

import noise_cfg as NC

JM = 1.89e-5
J_TRUE = 4.81e-5
K = lambda t1: t1 / (0.1 * 9.80665 * 1e-4)
DITH_FINAL = 0.005      # §10.3 终版 Δ=0.5%（run_trio 未显式给，默认 0.01；见 es_dith 变量）
ES_DITH = 0.01          # run_trio 默认值 —— 本表主口径

CASES = [
    ("T010_jid", dict(T1=0.10, j=True)),
    ("T015_jid", dict(T1=0.15, j=True)),
    ("T020_jid", dict(T1=0.20, j=True)),
    ("T015_dt", dict(T1=0.15, j=False)),
    ("T015_jid_d05", dict(T1=0.15, j=True, dith=DITH_FINAL)),
]
# 若基准环重调已有结果，额外加一档“重调基准 + 律D + J”的推荐点
try:
    _bm = json.load(open("_base_realj.json"))["_meta"]
    _pick = _bm["pick"]
    _row = json.load(open("_base_realj.json"))[_pick]
    CASES.append(("T015_jid_basepick", dict(T1=0.15, j=True,
                                            kp=_row["kp"], wo=_row["wo"])))
    print("basepick: %s kp=%g wo=%g" % (_pick, _row["kp"], _row["wo"]), flush=True)
except Exception as _exc:
    print("no _base_realj.json pick: %s" % _exc, flush=True)


def one(job):
    from pmsm_inv_sim import sim_inv
    key, o = job
    t = np.arange(0.0, 12.0, 2e-6); TL = np.zeros_like(t)
    cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0, J_true=J_TRUE,
               kp_boost=6.0, kb_eso=3.0, det_eps=0.01,
               tl_fault={"start": 0.0, "unbalance": dict(M=0.1, e=1e-4, kappa=K(o["T1"]))},
               T_es=True, es_dith=o.get("dith", ES_DITH))
    if o["j"]:
        cfg.update(j_id=True, j_id_f=100.0, j_id_amp_u=0.157, j_id_win=0.2,
                   j_id_lp=0.4, j_id_t0=1.0, j_id_tend=3.0, j_adapt_b0=True,
                   j_id_snr_min=2.0, j_id_nmin=5, j_id_std_max=0.15)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 600.0
    m = (tt >= 11) & (tt < 12); tc, ec = tt[m], e[m]
    a10 = float(np.hypot(2 * np.mean(ec * np.cos(2 * np.pi * 10 * tc)),
                         2 * np.mean(ec * np.sin(2 * np.pi * 10 * tc))))
    rms = float(np.sqrt(np.mean(ec ** 2)))
    js = np.asarray(Y["jstate"]); jh = np.asarray(Y["jhat"]); tj = np.asarray(Y["t_j"])
    jfin = float(jh[-1]); state = int(js[-1])
    # J 收敛时刻：首次进入 ±10% 并此后保持
    tconv = float("nan")
    if o["j"] and jh.size:
        band = np.abs(jh - J_TRUE) / J_TRUE <= 0.10
        idx = np.where(band)[0]
        for i0 in idx:
            if band[i0:].all():
                tconv = float(tj[i0]); break
    m_dip = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(e[m_dip]))
    i0 = int(np.where(m_dip)[0][int(np.argmin(e[m_dip]))])
    ok = (np.abs(e) <= 20.0) & (np.arange(len(e)) > i0) & (tt >= 2.0)
    idx = np.where(ok)[0]
    rec = float(tt[idx[0]] - 2.0) * 1e3 if len(idx) else float("nan")
    es_end = float(np.mean(np.asarray(Y["es"])[tt >= 11])) if o["j"] is not None else float("nan")
    print("%-14s T1=%.3f kappa=%7.1f 10Hz %6.2f RMS %6.2f iq %5.2f Jhat %.3e state=%d tconv=%.2f dip %7.1f rec %5.1f delta=%.3f"
          % (key, o["T1"], K(o["T1"]), a10, rms, float(np.max(np.abs(iq))), jfin, state,
             tconv, dip, rec, es_end), flush=True)
    return key, dict(T1=o["T1"], kappa=K(o["T1"]), j_id=bool(o["j"]),
                     es_dith=o.get("dith", ES_DITH), a10=a10, rms=rms,
                     iq=float(np.max(np.abs(iq))), jhat=jfin, state=state,
                     tconv=tconv, dip=dip, rec_ms=rec, es_end=es_end)


if __name__ == "__main__":
    from multiprocessing import Pool
    with Pool(4) as p:
        res = p.map(one, CASES)
    out = dict(res)
    out["_meta"] = dict(J_true=J_TRUE, J_nom=JM, ratio=J_TRUE / JM,
                        sim_sha_note="see _realj_meta.log / report", protocol="12 s, 600 rpm, D+T+J")
    json.dump(out, open("_realj_rec.json", "w"), indent=1)
    print("done")
