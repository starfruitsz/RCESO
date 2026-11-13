# -*- coding: utf-8 -*-
"""run_realj_tables.py —— §9 全部表格在真实 J（4.81e-5=2.545 J_nom）+ j_oracle 下重跑

表源（原名义 J 版本）→ 本脚本对应键：
  §9 基准行/§9.1 1D          : base, kb4, kb8, kb16, kb8de005
  §9.2 2D                    : a2kb8, a15kb6, a3kb6(旧定稿), a25kb4, a3kb10
  §9.3 900 rpm               : base900, lawd900（律D 定稿 kp_boost=6,kb_eso=3）
  §9.4 beta3 调度（rc_bp=0） : b0_a05, b1_a05, b3_a05, b0_a1, b3_a1
  重调后推荐配置             : lawd_retuned（从 _lawd_realj.json 的 _best 读入）
协议同 run_batch2_scans.py / run_lawd900_final.py：8 s、t=2 s 加载 0.5 额定 +
圆盘型线 V2（峰值 0.095 N·m）+ 5.9 Hz 振动、实验室噪声、种子 20261018。
J_true=4.81e-5、j_oracle=True。输出 _realj_tables.json
"""
import json

import numpy as np

import noise_cfg as NC
from tl_profile import disc_unbalance_profile
from run_laws_compare import build_loads, N_REF, AMP, ANG_START

J_TRUE = 4.81e-5
J_NOM = 1.89e-5
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

CASES = [("base", dict(det_eps=0.0))]
# §9.1 一维扫描
CASES += [("kb4", dict(kp_boost=4.0, det_eps=0.01)),
          ("kb8", dict(kp_boost=8.0, det_eps=0.01)),
          ("kb16", dict(kp_boost=16.0, det_eps=0.005)),
          ("kb8de005", dict(kp_boost=8.0, det_eps=0.005))]
# §9.2 二维扫描
CASES += [("a2kb8", dict(kp_boost=8.0, kb_eso=2.0, det_eps=0.01)),
          ("a15kb6", dict(kp_boost=6.0, kb_eso=1.5, det_eps=0.01)),
          ("a3kb6", dict(kp_boost=6.0, kb_eso=3.0, det_eps=0.01)),
          ("a25kb4", dict(kp_boost=4.0, kb_eso=2.5, det_eps=0.01)),
          ("a3kb10", dict(kp_boost=10.0, kb_eso=3.0, det_eps=0.01))]
# §9.3 900 rpm
CASES += [("base900", dict(n_ref=900.0, T=1.0 / 15.0, det_eps=0.0)),
          ("lawd900", dict(n_ref=900.0, T=1.0 / 15.0,
                           kp_boost=6.0, kb_eso=3.0, det_eps=0.01))]
# §9.4 beta3 调度（rc_bp=0，走 kb_b3 分支）
CASES += [("b0_a05", dict(rc_bp=0.0, kp_boost=8.0, kb_eso=0.5, kb_b3=0.0, det_eps=0.01)),
          ("b1_a05", dict(rc_bp=0.0, kp_boost=8.0, kb_eso=0.5, kb_b3=1.0, det_eps=0.01)),
          ("b3_a05", dict(rc_bp=0.0, kp_boost=8.0, kb_eso=0.5, kb_b3=3.0, det_eps=0.01)),
          ("b0_a1", dict(rc_bp=0.0, kp_boost=8.0, kb_eso=1.0, kb_b3=0.0, det_eps=0.01)),
          ("b3_a1", dict(rc_bp=0.0, kp_boost=8.0, kb_eso=1.0, kb_b3=3.0, det_eps=0.01))]

try:
    _best = json.load(open("_lawd_realj.json"))["_best"]
    CASES.append(("lawd_retuned", dict(kp=_best["kp"], kp_boost=_best["kp_boost"],
                                       kb_eso=_best["kb_eso"], det_eps=_best["det_eps"])))
except Exception as exc:                      # 没有重调结果时跳过该行
    print("no _lawd_realj.json _best: %s" % exc, flush=True)


def bmean(x, n):
    """块均值：iq 采样 10 us，n=100 → 1 ms（速度环一拍），n=10 → 一个 PWM 周期 100 us。
    原始 max|iq| 含 10 kHz PWM/死区纹波（峰峰约 3 A），块均值才是基波包络。"""
    m = len(x) // n * n
    return x[:m].reshape(-1, n).mean(axis=1)


def met8(tt, y, iq, nref):
    e = (y - 1.0) * nref
    m = (tt >= 1.9) & (tt <= 2.5)
    i0 = int(np.where(m)[0][int(np.argmin(e[m]))])
    idx = np.where((np.abs(e) <= 20.0) & (np.arange(len(e)) > i0) & (tt >= 2.0))[0]
    iqa = np.abs(iq)
    av1 = np.abs(bmean(iq, 100))
    t1 = tt[:len(tt) // 100 * 100:100] + 0.5e-3
    return dict(dip=float(np.min(e[m])),
                rec=float((tt[idx[0]] - 2.0) * 1e3) if len(idx) else float("nan"),
                step_rms=float(np.sqrt(np.mean(e[(tt >= 2.0) & (tt < 2.5)] ** 2))),
                steady=float(np.sqrt(np.mean(e[(tt >= 7.0) & (tt < 8.0)] ** 2))),
                iq=float(np.max(iqa)),
                iq_peak_t=float(tt[int(np.argmax(iqa))]),
                iq1ms=float(av1.max()), iq1ms_t=float(t1[int(av1.argmax())]),
                iq100us=float(np.max(np.abs(bmean(iq, 10)))))


def one(job):
    from pmsm_inv_sim import sim_inv
    key, kw = job
    t, TL = build_loads()
    cfg = dict(BASE); cfg["tl_ang"] = disc_unbalance_profile(); cfg.update(kw)
    Y = sim_inv(t, TL, cfg)
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    nref = float(cfg["n_ref"])
    d = met8(tt, y, iq, nref)
    print("%-12s n=%3.0f dip %7.1f rec %6.1f stepRMS %5.1f steady %5.2f | iq_raw %5.2f @%.3f "
          "iq1ms %5.2f @%.3f iq100us %5.2f"
          % (key, nref, d["dip"], d["rec"], d["step_rms"], d["steady"], d["iq"], d["iq_peak_t"],
             d["iq1ms"], d["iq1ms_t"], d["iq100us"]), flush=True)
    # 只为 base / a3kb6（新 §9 定稿律D）保留波形，供 fig_lawd_cmp_600_j24 重画
    trace = (tt, y, iq, np.asarray(Y["tl"])) if key in ("base", "a3kb6") else None
    return key, d, trace


if __name__ == "__main__":
    import hashlib
    from multiprocessing import Pool
    sha = hashlib.sha256(open("pmsm_inv_sim.py", "rb").read()).hexdigest()
    with Pool(6) as p:
        res = p.map(one, CASES)
    out, npz = {}, {}
    for key, d, tr in res:
        out[key] = d
        if tr is not None:
            tt, y, iq, tl = tr
            tag = "base" if key == "base" else "lawd"
            npz["t"] = tt
            npz["y_" + tag] = y
            npz["iq_" + tag] = iq
            npz["tl"] = tl
    out["_meta"] = dict(J_true=J_TRUE, J_nom=J_NOM, ratio=J_TRUE / J_NOM,
                        sim_sha256=sha, n_cases=len(CASES),
                        iq_metric="raw 10us max (footnote) + 1ms block-mean max (primary, rated 6.31 A)")
    json.dump(out, open("_realj_tables.json", "w"), indent=1)
    np.savez("_wave_lawd_cmp_600_j24.npz", **npz)
    print("done  sim_sha256=%s" % sha)
