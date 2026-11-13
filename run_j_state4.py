# -*- coding: utf-8 -*-
"""run_j_state4.py —— 上电状态机（0–5）与 J 应用后校验/回退（状态 4）的验证矩阵

复现附录 C.7 现有行，并补状态 4/5 用例（2026-11-13）：
  * 状态机：0 空闲 / 1 辨识 / 2 已应用 / 3 超时回退 / 4 校验回退 / 5 死区保持标称
  * 辨识完成后按 rho=Jhat/J_M 判死区（|rho-1|<=j_apply_thr=0.20 → 状态 5）；
    否则先采"dither 关 + b0 标称"的公平基线（静默 j_val_settle=0.2 s + 窗 j_base_win=0.5 s），
    再施加 B0e=B0*J_M/Jhat，等 j_val_delay=0.5 s 后取 j_val_win=0.5 s 后窗，
    iq 纹波 AC-RMS 或 10 Hz 转速误差幅值恶化 > j_val_tol=20% → 回退 b0、状态 4；否则状态 2。
  * j_val=False：辨识完成立即应用（旧行为，对照用）。
  * 小圆盘 J_true=4.81e-5 = 2.545 J_nom（C.1 轴承口径）用于 Js_T010/Js_T015。
  * 死区用例必须落在 J_nom 附近（|rho-1|<=0.2），故取 J_true=2.0e-5（1.058 J_nom）；
    若改成 4.81e-5 则 rho≈2.7，物理上不可能进入状态 5，只能演示状态 2/4。
  * 另加两条 j_id=False 的"纯标称 b0"参考行，用于核对状态 4/5 的终点确实回到标称。

运行：python run_j_state4.py   （Pool 6）
"""
import json
import math
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC

JM = 1.89e-5
JB = 9.95e-5            # 大圆盘 J_true（5.26 J_nom）
J_SMALL = 4.81e-5       # 小圆盘 J_true（2.545 J_nom，C.1 轴承口径）
K = lambda t1: t1 / (0.1 * 9.80665 * 1e-4)   # 不平衡等效 T1 → kappa

# key, 开关：T1（不平衡等效转矩）、A（dither 幅值）、nmin、t0、J_true、j_val、j_id
CASES = [
    # ---- 复现 C.7 现有行（j_val=True 新状态机）----
    ("fault_A157_nmin3_t05", dict(T1=0.057, A=0.157, nmin=3, t0=0.5)),   # C.7 行 1
    ("fault_A157_nmin5_t1",  dict(T1=0.057, A=0.157, nmin=5, t0=1.0)),   # C.7 行 2
    ("nofault_A157_nmin5",   dict(T1=0.0,   A=0.157, nmin=5, t0=1.0)),   # C.7 行 3（已知坏例）
    ("weak_A002",            dict(T1=0.057, A=0.02,  nmin=3, t0=0.5)),   # C.7 行 4
    ("nofault_A30",          dict(T1=0.0,   A=0.30,  nmin=5, t0=1.0)),   # C.7 行 5
    # ---- 小圆盘：J_true=4.81e-5（C.7 推荐演示点）----
    ("Js_T010",              dict(T1=0.10,  A=0.157, nmin=3, t0=0.5, J=J_SMALL)),
    ("Js_T015",              dict(T1=0.15,  A=0.157, nmin=3, t0=0.5, J=J_SMALL)),
    # ---- 状态 5：死区（估计落在 J_nom 附近，不更新 b0）----
    ("deadband_J20",         dict(T1=0.0,   A=0.157, nmin=5, t0=1.0, J=2.0e-5)),
    # ---- 对照：j_val=False（立即应用，旧行为）----
    ("nofault_A157_jvalF",   dict(T1=0.0,   A=0.157, nmin=5, t0=1.0, j_val=False)),
    # ---- 纯标称 b0 参考行（j_id=False，核对状态 4/5 的终点）----
    ("nominal_nofault_JB",   dict(T1=0.0,   J=JB,      j_id=False)),
    ("nominal_nofault_J20",  dict(T1=0.0,   J=2.0e-5,  j_id=False)),
]


def make_cfg(o):
    cfg = dict(n_ref=600.0, T=0.1, T_adapt=True, T_filt=50e-3, fci=500.0,
               beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
               i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
               sig_n=NC.NOISE_LAB["sig_n_rpm"], sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
               eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
               rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
               J_true=o.get("J", JB),
               j_adapt_b0=True)
    if o.get("T1", 0.0) > 0.0:
        cfg["tl_fault"] = {"start": 0.0,
                           "unbalance": dict(M=0.1, e=1e-4, kappa=K(o["T1"]))}
    if o.get("j_id", True):
        cfg.update(j_id=True, j_id_f=100.0, j_id_amp_u=o["A"], j_id_win=0.2,
                   j_id_lp=0.4, j_id_t0=o["t0"], j_id_tend=3.0,
                   j_id_snr_min=2.0, j_id_nmin=o["nmin"], j_id_std_max=0.15)
        if "j_val" in o:
            cfg["j_val"] = o["j_val"]
    return cfg


def _amp10(tt, e, a, b):
    m = (tt >= a) & (tt < b)
    tc, ec = tt[m], e[m]
    return float(np.hypot(2 * np.mean(ec * np.cos(2 * np.pi * 10 * tc)),
                          2 * np.mean(ec * np.sin(2 * np.pi * 10 * tc))))


def _sanitize(x):
    """JSON 友好：numpy 标量 → float/int，NaN/inf → None。"""
    if isinstance(x, dict):
        return {str(k): _sanitize(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_sanitize(v) for v in x]
    if isinstance(x, (np.floating, float)):
        v = float(x)
        return v if math.isfinite(v) else None
    if isinstance(x, (np.integer, int)):
        return int(x)
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    return x


def _fmt(v, f):
    return (f % v) if v is not None else "   -  "


def one(job):
    from pmsm_inv_sim import sim_inv
    key, o = job
    t = np.arange(0.0, 10.0, 2e-6)
    TL = np.zeros_like(t)
    Y = sim_inv(t, TL, make_cfg(o))
    tt = np.asarray(Y["t"]); y = np.asarray(Y["y"]); iq = np.asarray(Y["iq"])
    e = (y - 1.0) * 600.0
    # C.7 稳态窗口径（9–10 s）
    m = (tt >= 9.0) & (tt < 10.0)
    a10 = _amp10(tt, e, 9.0, 10.0)
    rms = float(np.sqrt(np.mean(e[m] ** 2)))
    iq_ss = float(np.max(np.abs(iq[m])))
    iq_pk = float(np.max(np.abs(iq)))
    js = np.asarray(Y["jstate"]); jh = np.asarray(Y["jhat"])
    J = Y["jval"]
    Jtrue = float(o.get("J", JB))
    jfin = float(jh[-1])
    jid_on = bool(o.get("j_id", True))
    jerr = (jfin / Jtrue - 1.0) if jid_on else None   # j_id=False 参考行：Jhat 显示 J_nom，不算辨识误差
    # 辨识完成→判定期间的电流峰值（校验窗内的实际暴露）
    iq_val_pk = None
    b0e_final = float(np.asarray(Y["b0e"])[-1])
    if (J["t_decision"] is not None) and (J["t_final"] is not None):
        mv = (tt >= J["t_decision"]) & (tt < J["t_final"] + 1e-9)
        if mv.any():
            iq_val_pk = float(np.max(np.abs(iq[mv])))
    base = J["base"]; post = J["post"]
    line = ("%-22s state=%d Jhat=%.3e (%s) 10Hz %6.2f RMS %6.2f iq %5.2f | "
            "base iqRMS %s 10Hz %s | post iqRMS %s 10Hz %s | %s" % (
                key, int(js[-1]), jfin, _fmt(100.0 * jerr if jerr is not None else None, "%+6.1f%%"), a10, rms, iq_pk,
                _fmt(base["iq_rms"] if base else None, "%.4f"),
                _fmt(base["a10"] if base else None, "%6.2f"),
                _fmt(post["iq_rms"] if post else None, "%.4f"),
                _fmt(post["a10"] if post else None, "%6.2f"),
                str(J["decision"])))
    print(line, flush=True)
    rec = dict(cfg={k: o.get(k) for k in ("T1", "A", "nmin", "t0", "j_val", "j_id")},
               J_true=Jtrue, J_nom=JM, Jhat=jfin, Jhat_err=jerr, j_id=jid_on,
               rho=J["rho"], state=int(js[-1]), decision=J["decision"],
               applied=J["applied"], rollback=J["rollback"],
               t_decision=J["t_decision"], t_final=J["t_final"],
               b0e_final=b0e_final, b0e_nominal=float(Y["b0e"][0]),
               base=base, settle_win=J["settle_win"], post=post,
               merged=J["merged"], ratios=J["ratios"],
               a10_9_10=a10, rms_9_10=rms, iq_peak_total=iq_pk,
               iq_peak_ss=iq_ss, iq_peak_validation=iq_val_pk,
               iq_rated=J["iq_rated"],
               thr=J["thr"], tol=J["tol"], settle=J["settle"],
               base_win=J["base_win"], delay=J["delay"], win=J["win"],
               a10_floor=J["a10_floor"], enable=J["enable"])
    return key, _sanitize(rec)


if __name__ == "__main__":
    with Pool(6) as p:
        res = p.map(one, CASES)
    out = dict(meta=dict(
        what="J adaptive power-up state machine 0-5 (post-apply validation/rollback)",
        date="2026-11-13", sim="pmsm_inv_sim.py",
        states="0 idle / 1 identify / 2 applied / 3 timeout-fallback / 4 validation-rollback / 5 deadband-keep-nominal",
        J_nom=JM, J_true_big=JB, J_true_small=J_SMALL,
        j_apply_thr=0.20, j_val_tol=0.20, j_val_settle=0.2,
        j_base_win=0.5, j_val_delay=0.5, j_val_win=0.5, j_val_a10_floor=2.0,
        iq_metric="AC-RMS of 1 ms iq samples in window (window mean removed)",
        a10_metric="10 Hz speed-error amplitude (rpm) over window",
        iq_rated=float(0.637 / 0.101),
        note=("deadband case uses J_true=2.0e-5 (~1.06 J_nom) because state 5 requires "
              "|Jhat/J_nom-1|<=0.20; the small-disc J_true=4.81e-5=2.545 J_nom cannot "
              "enter the deadband. Js_T010/Js_T015 use 4.81e-5. j_val default True when "
              "j_id and j_adapt_b0; pass j_val=False to reproduce pre-2026-11-13 runs.")),
        cases=dict(res))
    json.dump(out, open("_j_state4.json", "w", encoding="utf-8"), indent=1)
    print("done:", ", ".join(k for k, _ in res))
