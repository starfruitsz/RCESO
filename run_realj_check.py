# -*- coding: utf-8 -*-
"""run_realj_check.py —— 相位A：真实 J（2.4 J_nom 小圆盘）下的 §9 表复现性检查

协议与 run_lawd_cmp_600.py 完全一致（8 s、t=2 s 加载 0.5 额定 + 圆盘型线 V2 + 5.9 Hz
振动、实验室噪声、fci=500 Hz、beta3=4000、tau0=20 ms、类 fal ESO、种子 20261018）：
  base : det_eps=0.0（无自适应）
  lawd : kp_boost=6, kb_eso=3, det_eps=0.01（§9 定稿律D）
四个工况：
  base_jnom / lawd_jnom : J_true=1.89e-5（=J_nom，§9 原口径），复现 §9 表行（harness 锚点）
  base_j24  / lawd_j24  : J_true=4.81e-5（=2.545 J_nom，小圆盘 R=20mm/M=0.08kg 的
                          自洽传动链：1.89e-5 电机 + 1.5e-6 联轴器 + 1.60e-5 圆盘 + 1.168e-5 轴承），
                          j_oracle=True（b0 用真实 J 归一）

指标口径同 run_lawd_cmp_600.metrics：跌落 min[1.9,2.5]、恢复（回到 ±20 rpm，从 t>=2 起）、
突变窗 RMS[2.0,2.5)、稳态 RMS[7,8)、max|iq|。
输出 _realj_check.json、_wave_realj_check.npz
"""
import hashlib
import json

import numpy as np

import noise_cfg as NC
from run_laws_compare import build_loads, N_REF, AMP, ANG_START

JBASE = dict(n_ref=N_REF, T=0.1, T_adapt=True, T_filt=50e-3,
             rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
             fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3,
             seed_i=20261018,
             i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
             sig_n=NC.NOISE_LAB["sig_n_rpm"],
             sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
             tl_ang=None, tl_ang_amp=AMP,
             tl_ang_start=ANG_START, tl_ang_rev=29.9,
             eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0)
LAWD = dict(kp_boost=6.0, det_eps=0.01, kb_eso=3.0, kb_b3=0.0)
J_NOM = 1.89e-5
J_24 = 4.81e-5      # 2.545 J_nom（2026-11-13 用户定：自洽传动链口径）
CASES = [
    ("base_jnom", dict(J_true=J_NOM, det_eps=0.0)),
    ("lawd_jnom", dict(J_true=J_NOM, **LAWD)),
    ("base_j24", dict(J_true=J_24, j_oracle=True, det_eps=0.0)),
    ("lawd_j24", dict(J_true=J_24, j_oracle=True, **LAWD)),
]


def metrics(tt, y, iq):
    e = (np.asarray(y) - 1.0) * N_REF
    m_dip = (tt >= 1.9) & (tt <= 2.5)
    dip = float(np.min(e[m_dip]))
    i_dip = int(np.where(m_dip)[0][int(np.argmin(e[m_dip]))])
    ok = (np.abs(e) <= 20.0) & (np.arange(len(e)) > i_dip) & (tt >= 2.0)
    idx = np.where(ok)[0]
    rec = float(tt[idx[0]] - 2.0) * 1e3 if len(idx) else float("nan")
    step_rms = float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2)))
    steady = float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2)))
    iqa = np.abs(iq)
    return dict(dip=dip, rec_ms=rec, step_rms=step_rms,
                steady=steady, iq_max=float(np.max(iqa)),
                iq_peak_t=float(tt[int(np.argmax(iqa))]),
                iq_step=float(np.max(iqa[(tt >= 1.99) & (tt <= 2.10)])),
                dip_t=float(tt[i_dip]))


def one(job):
    from pmsm_inv_sim import sim_inv
    from tl_profile import disc_unbalance_profile
    key, kw = job
    t, TL = build_loads()
    cfg = dict(JBASE)
    cfg["tl_ang"] = disc_unbalance_profile()
    cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    mt = metrics(tt, y, iq)
    mt["J_true"] = float(cfg["J_true"])
    mt["j_oracle"] = bool(cfg.get("j_oracle", False))
    print("%-10s 跌落 %7.1f rpm  恢复 %6.1f ms  突变RMS %5.1f  稳态 %5.2f  iq %5.2f"
          % (key, mt["dip"], mt["rec_ms"], mt["step_rms"], mt["steady"], mt["iq_max"]),
          flush=True)
    return key, mt, tt, y, iq


if __name__ == "__main__":
    from multiprocessing import Pool
    sha = hashlib.sha256(open("pmsm_inv_sim.py", "rb").read()).hexdigest()
    with Pool(4) as p:
        res = p.map(one, CASES)
    out = {}
    npz = {}
    for key, mt, tt, y, iq in res:
        out[key] = mt
        npz["t"] = tt
        npz["y_" + key] = y
        npz["iq_" + key] = iq
    out["_meta"] = dict(sha256_pmsm_inv_sim=sha, n_cases=len(CASES),
                        protocol="8s, load step 0.5 rated at t=2s, disc V2 + 5.9Hz, lab noise",
                        J_nom=J_NOM, J_24=J_24, ratio=J_24 / J_NOM)
    json.dump(out, open("_realj_check.json", "w"), indent=1)
    np.savez("_wave_realj_check.npz", **npz)
    print("done  sha256(pmsm_inv_sim)=%s" % sha)
