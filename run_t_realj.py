# -*- coding: utf-8 -*-
"""run_t_realj.py —— §10（T 自适应实测）全部表格在真实惯量 J_true=4.81e-5 下重跑

背景：报告 §9–§10 由 J_true=J_nom 切到真实台架 J_true=4.81e-5 = 2.545 J_nom
（J_nom=1.89e-5）；控制器 b0 由 J 自适应整定完成，故所有工况取 j_oracle=True
（即 b0 = B0*J_nom/J_true，控制器与对象一致）。J 辨识本身不在本脚本（见附录 C）。

与名义 J 脚本逐项一致的部分：种子 20261018、实验室噪声（3 rpm / 0.1 A / 0.01 N·m）、
圆盘型线 V2（峰值 0.095 N·m，2.01868 s 投入）、5.9 Hz 振动、fci=500 Hz、beta3=4000、
Q0=0.98、tau0=20 ms、类 fal ESO、T_adapt + T_filt=50 ms、rc_bp=5。
唯一改动：J_true=4.81e-5、j_oracle=True。

协议（每个相位的窗口口径与来源脚本一致）：
  P1 600 rpm δ 扫描（9+2 点）: run_scan_fix.py / run_batch2_scans.py
      8 s；A = mean(amp[5,8))；稳态 RMS = sqrt(mean(e[7,8)^2))，e=(y-1)*600
  P2 ESC 收敛 30 s（5 例）  : run_t_es3.py / run_t_cmp_600.py
      δ终 = mean(es[25,30))；A终 = mean(amp[25,30))；稳态 RMS = sqrt(mean(e[25,30)^2))
  P3 抖动权衡 30 s（5 例）  : run_t_es4.py
      δ均/p2p、A 取 [20,30)；RMS 取 [25,30)
  P4a 300 rpm δ 扫描（8 点）: run_scan_fix.py r300
      20 s；A = mean(amp[14,20))；RMS = sqrt(mean(e[14,20)^2))，e=(y-1)*300
  P4b 前馈重置 600→300（5 例）: run_t_es_ff.py
      40 s；δ前 = mean(es[10,14.9))；δ后 = mean(es[30,40))；A后 = mean(amp[30,40))；
      RMS后 = sqrt(mean(e[35,40)^2))；RMS 15.5–20 s
  P4c 往返 600→300→600（1 例）: run_t_es_roundtrip.py
      60 s；三段 10–14.9 / 25–34.9 / 50–59.9 s，RMS 取各段末 4 s

输出：_tes_realj.json（指标 + 元数据，含每例 pmsm_inv_sim.py 的 sha256）、
      _wave_t_realj_<case>.npz（1 ms 抽样的 t/y/es/amp 小轨迹，供画图）

用法：
    python run_t_realj.py                     # 默认 P1+P2+P3，Pool=4
    python run_t_realj.py --phases 4          # 只跑 P4（追加到已有 json）
    python run_t_realj.py --phases 1,2,3,4    # 全部
    python run_t_realj.py --pool 3
    python run_t_realj.py --retune dith       # 追加一个最小重调试验（Δ=0.5%→0.2%）
    python run_t_realj.py --retune step       # 追加一个最小重调试验（σ=1%→2%）
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

import noise_cfg as NC
from tl_profile import disc_unbalance_profile

J_NOM = 1.89e-5          # ESO 标称惯量（= 电机转子惯量 J_M）
J_TRUE = 4.81e-5         # 真实台架惯量（2026-11-13 用户口径）= 2.545 J_nom
RATIO = J_TRUE / J_NOM

DT = 2e-6
N_REF = 600.0
AMP = 0.095
ANG_START = 2.01868
VIB_H = (1.0, 0.2654, 0.0408, 0.2245, 0.0612, 0.1837)
SIM = "pmsm_inv_sim.py"


# ---------------------------------------------------------------- 载荷/配置构造
def _common(n_ref, T):
    """所有相位的公共物理/控制器口径（逐项同名义脚本）。"""
    return dict(n_ref=n_ref, T=T, T_adapt=True, T_filt=50e-3,
                fci=500.0, beta3=4000.0, Q0=0.98, tau0=20e-3, seed_i=20261018,
                i_noise_peak=NC.NOISE_LAB["i_noise_peak"],
                sig_n=NC.NOISE_LAB["sig_n_rpm"],
                sig_T_nm=NC.NOISE_LAB["sig_T_nm"],
                tl_ang=disc_unbalance_profile(), tl_ang_amp=AMP,
                tl_ang_start=ANG_START, tl_ang_rev=29.9,
                eso_law="fal", eso_a=0.75, eso_delta=0.10, eso_lam=10.0,
                rc_bp=5.0, b3_min=4000.0, b3_max=4000.0, a_ref=1.0,
                J_true=J_TRUE, j_oracle=True)


def _b8():
    """8 s 工况：run_laws_compare.build_loads（2 s 加载 0.5 额定 + 型线 V2 + 5.9 Hz）。"""
    from run_laws_compare import build_loads
    t, TL = build_loads()
    return t, TL, _common(600.0, 0.1)


def _b30():
    """30 s 工况：run_t_es.build（同载荷，30 s 窗，型线 29.9 s 反相）。"""
    from run_t_es import build
    t, TL = build()
    cfg = _common(600.0, 0.1)
    cfg.update(es_step=0.01, es_dith=0.01, es_Pd=1.5, es_N=3, es_dead=1e-5,
               es_dmax=0.20, es_t0=3.0)
    return t, TL, cfg


def _b300():
    """20 s、300 rpm 工况：run_scan_fix.py 的 r300 分支（逐位复制）。"""
    t = np.arange(0.0, 20.0, DT)
    vib = np.zeros_like(t)
    for n, a in enumerate(VIB_H, start=1):
        vib += a * np.sin(2.0 * math.pi * 5.9 * n * (t - 2.0) * (t >= 2.0))
    TL = (0.5 * (t >= 2.0)).astype(float) * 0.637 + 0.03 * vib
    cfg = _common(300.0, 0.2)
    cfg.update(es_step=0.0, es_dith=0.0, es_Pd=1.5, es_N=3, es_dead=1e-5,
               es_dmax=0.20, es_t0=3.0)
    return t, TL, cfg


def _b40():
    """40 s、600→300 换速（15 s）工况：run_t_es_speedstep.build。"""
    from run_t_es_speedstep import build
    t, TL = build()
    cfg = _common(600.0, 0.1)
    cfg.update(T_es=True, n_ref2=300.0, t_nref=15.0,
               es_d0=-0.143, es_dith=0.005, es_step=0.01, es_Pd=1.5, es_N=3,
               es_dead=1e-5, es_dmax=0.20, es_t0=3.0, es_freeze=2.0)
    return t, TL, cfg


def _b60():
    """60 s、600→300→600 往返（15/35 s）工况：run_t_es_roundtrip.build。"""
    from run_t_es_roundtrip import build
    t, TL = build()
    cfg = _common(600.0, 0.1)
    cfg.update(T_es=True, n_ref2=300.0, t_nref=15.0, n_ref3=600.0, t_nref2=35.0,
               es_ff=True, es_d0=-0.143, es_dith=0.005, es_step=0.01,
               es_Pd=1.5, es_N=3, es_dead=1e-5, es_dmax=0.30, es_t0=3.0,
               es_freeze=2.0)
    return t, TL, cfg


BUILDERS = {"b8": _b8, "b30": _b30, "b300": _b300, "b40": _b40, "b60": _b60}


# ---------------------------------------------------------------------- 指标
def _win(tt, a, b):
    return (tt >= a) & (tt < b)


def _rms(e):
    return float(np.sqrt(np.mean(np.square(e))))


def met_p1(tt, Y, cfg):
    e = (np.asarray(Y["y"]) - 1.0) * 600.0
    amp = np.asarray(Y["amp"])
    ms = _win(tt, 5.0, 8.0)
    return dict(
        A=float(np.mean(amp[ms])),
        RMS=_rms(e[_win(tt, 7.0, 8.0)]),
        A_noise_floor=float(np.mean(amp[_win(tt, 0.5, 1.9)])),
        RMS_noise_floor=_rms(e[_win(tt, 0.5, 1.9)]),
        delta=float(cfg["es_d0"]),
    )


def met_p2(tt, Y, cfg):
    e = (np.asarray(Y["y"]) - 1.0) * 600.0
    amp = np.asarray(Y["amp"]); es = np.asarray(Y["es"])
    m = tt >= 25.0
    traj = {}
    for a in (10.0, 15.0, 20.0, 25.0, 29.0):
        w = _win(tt, a, a + 1.0)
        traj["%g" % a] = float(np.mean(es[w]))
    return dict(
        delta_end=float(np.mean(es[m])),
        delta_p2p_pct=100.0 * float(np.ptp(es[_win(tt, 20.0, 30.0)])),
        A=float(np.mean(amp[m])),
        RMS=_rms(e[m]),
        RMS_20_25=_rms(e[_win(tt, 20.0, 25.0)]),
        delta_traj=traj,
        es_step=float(cfg.get("es_step", 0.01)),
        es_dith=float(cfg.get("es_dith", 0.01)),
        es_N=int(cfg.get("es_N", 3)),
    )


def met_p3(tt, Y, cfg):
    e = (np.asarray(Y["y"]) - 1.0) * 600.0
    amp = np.asarray(Y["amp"]); es = np.asarray(Y["es"])
    m = tt >= 20.0
    return dict(
        delta_mean=float(np.mean(es[m])),
        delta_p2p_pct=100.0 * float(np.ptp(es[m])),
        A=float(np.mean(amp[m])),
        RMS=_rms(e[tt >= 25.0]),
        es_step=float(cfg.get("es_step", 0.01)),
        es_dith=float(cfg.get("es_dith", 0.01)),
        es_N=int(cfg.get("es_N", 3)),
    )


def met_p4a(tt, Y, cfg):
    e = (np.asarray(Y["y"]) - 1.0) * 300.0
    amp = np.asarray(Y["amp"])
    m = tt >= 14.0
    return dict(A=float(np.mean(amp[m])),
                RMS=_rms(e[m]),
                A_noise_floor=float(np.mean(amp[_win(tt, 0.5, 1.9)])),
                delta=float(cfg["es_d0"]))


def _eref40(tt):
    return np.where(tt >= 15.0, 0.5, 1.0)


def met_p4b(tt, Y, cfg):
    y = np.asarray(Y["y"])
    e = (y - _eref40(tt)) * 600.0
    es = np.asarray(Y["es"]); amp = np.asarray(Y["amp"])
    return dict(
        delta_pre=float(np.mean(es[_win(tt, 10.0, 14.9)])),
        delta_post=float(np.mean(es[tt >= 30.0])),
        delta_post_p2p_pct=100.0 * float(np.ptp(es[tt >= 30.0])),
        A_pre=float(np.mean(amp[_win(tt, 10.0, 14.9)])),
        A_post=float(np.mean(amp[tt >= 30.0])),
        RMS_post=_rms(e[tt >= 35.0]),
        RMS_15_20=_rms(e[_win(tt, 15.5, 20.0)]),
        es_ff=bool(cfg.get("es_ff", False)),
        T_es=bool(cfg.get("T_es", False)),
    )


def met_p4c(tt, Y, cfg):
    y = np.asarray(Y["y"])
    yref = np.ones_like(tt)
    yref[tt >= 15.0] = 0.5
    yref[tt >= 35.0] = 1.0
    e = (y - yref) * 600.0
    es = np.asarray(Y["es"]); amp = np.asarray(Y["amp"])
    out = {}
    for a, b, lab in ((10.0, 14.9, "s600a"), (25.0, 34.9, "s300"), (50.0, 59.9, "s600b")):
        m = _win(tt, a, b)
        out[lab] = dict(delta_mean=float(np.mean(es[m])),
                        delta_p2p_pct=100.0 * float(np.ptp(es[m])),
                        A=float(np.mean(amp[m])),
                        RMS=_rms(e[_win(tt, b - 4.0, b)]))
    return out


METERS = {"p1": met_p1, "p2": met_p2, "p3": met_p3,
          "p4a": met_p4a, "p4b": met_p4b, "p4c": met_p4c}


# ---------------------------------------------------------------------- 用例表
def case_list():
    C = []
    # P1 600 rpm δ 扫描（9 个名义点 + 2 个加密点）
    for pc in (-20, -15, -13, -12, -11, -10, -8, -6, -4, 0, 2):
        C.append(dict(phase="p1", key="p1_d%+d" % pc, builder="b8",
                      meter="p1",
                      kw=dict(T_es=True, es_d0=pc / 100.0, es_step=0.0, es_dith=0.0)))
    # P2 ESC 收敛 30 s
    esc = dict(T_es=True, es_Pd=1.5, es_N=3, es_dead=1e-5, es_dmax=0.20, es_t0=3.0)
    C += [
        dict(phase="p2", key="p2_notune", builder="b30", meter="p2",
             kw=dict(esc, es_d0=0.0, es_step=0.0, es_dith=0.0)),
        dict(phase="p2", key="p2_fix_m12", builder="b30", meter="p2",
             kw=dict(esc, es_d0=-0.12, es_step=0.0, es_dith=0.0)),
        dict(phase="p2", key="p2_fix_m143", builder="b30", meter="p2",
             kw=dict(esc, es_d0=-0.143, es_step=0.0, es_dith=0.0)),
        dict(phase="p2", key="p2_esc_m143", builder="b30", meter="p2",
             kw=dict(esc, es_d0=-0.143, es_step=0.01, es_dith=0.01)),
        dict(phase="p2", key="p2_esc_m5", builder="b30", meter="p2",
             kw=dict(esc, es_d0=-0.05, es_step=0.01, es_dith=0.01)),
    ]
    # P3 抖动权衡 30 s
    C += [
        dict(phase="p3", key="p3_d10_s10", builder="b30", meter="p3",
             kw=dict(esc, es_d0=-0.143, es_dith=0.010, es_step=0.010, es_N=3)),
        dict(phase="p3", key="p3_d05_s05_N3", builder="b30", meter="p3",
             kw=dict(esc, es_d0=-0.143, es_dith=0.005, es_step=0.005, es_N=3)),
        dict(phase="p3", key="p3_d05_s10_N3", builder="b30", meter="p3",
             kw=dict(esc, es_d0=-0.143, es_dith=0.005, es_step=0.010, es_N=3)),
        dict(phase="p3", key="p3_d05_s05_N6", builder="b30", meter="p3",
             kw=dict(esc, es_d0=-0.143, es_dith=0.005, es_step=0.005, es_N=6)),
        dict(phase="p3", key="p3_fix_m12", builder="b30", meter="p3",
             kw=dict(esc, es_d0=-0.12, es_dith=0.0, es_step=0.0)),
    ]
    # P4a 300 rpm δ 扫描
    for pc in (-12, -10, -8, -6, -4, -2, 0, 2):
        C.append(dict(phase="p4a", key="p4a_d%+d" % pc, builder="b300", meter="p4a",
                      kw=dict(T_es=True, es_d0=pc / 100.0, es_step=0.0, es_dith=0.0)))
    # P4b 前馈重置 600→300
    C += [
        dict(phase="p4b", key="p4b_ff", builder="b40", meter="p4b",
             kw=dict(es_ff=True)),
        dict(phase="p4b", key="p4b_ff_nofreeze", builder="b40", meter="p4b",
             kw=dict(es_ff=True, es_freeze=0.0)),
        dict(phase="p4b", key="p4b_frozen", builder="b40", meter="p4b",
             kw=dict(es_ff=False)),
        dict(phase="p4b", key="p4b_fix_m12_nominal", builder="b40", meter="p4b",
             kw=dict(T_es=False, es_d0=-0.12, es_step=0.0, es_dith=0.0)),
        dict(phase="p4b", key="p4b_fix_m12_on", builder="b40", meter="p4b",
             kw=dict(T_es=True, es_d0=-0.12, es_step=0.0, es_dith=0.0)),
    ]
    # P4c 往返
    C.append(dict(phase="p4c", key="p4c_rt", builder="b60", meter="p4c", kw={}))
    return C


def retune_cases(kind):
    """最小重调试验（仅在 ESC 因 A 变小而失锁/变噪时启用，结果单列并披露）。"""
    esc = dict(T_es=True, es_Pd=1.5, es_N=3, es_dead=1e-5, es_dmax=0.20, es_t0=3.0)
    if kind == "dith":
        kw = dict(esc, es_d0=-0.143, es_step=0.01, es_dith=0.002)
        return [dict(phase="rt", key="rt_dith02", builder="b30", meter="p3", kw=kw)]
    if kind == "step":
        kw = dict(esc, es_d0=-0.143, es_step=0.02, es_dith=0.01)
        return [dict(phase="rt", key="rt_step20", builder="b30", meter="p3", kw=kw)]
    raise SystemExit("--retune must be dith or step")


# ---------------------------------------------------------------------- 执行
def one(job):
    from pmsm_inv_sim import sim_inv
    sha = hashlib.sha256(open(SIM, "rb").read()).hexdigest()
    t0 = time.perf_counter()
    t, TL, cfg = BUILDERS[job["builder"]]()
    cfg.update(job["kw"])
    Y = sim_inv(t, TL, cfg)
    wall = time.perf_counter() - t0
    tt = np.asarray(Y["t"])
    met = METERS[job["meter"]](tt, Y, cfg)
    met["wall_s"] = round(wall, 1)
    met["tend"] = float(tt[-1])
    met["sha_sim"] = sha[:16]
    # 1 ms 抽样小轨迹（画图/复核用，单例 < 2 MB）
    step = float(tt[1] - tt[0])
    d = max(1, int(round(1e-3 / step)))
    trace = dict(t=tt[::d], y=np.asarray(Y["y"])[::d],
                 es=np.asarray(Y["es"])[::d], amp=np.asarray(Y["amp"])[::d])
    print("%-18s %-4s wall %5.1f s  %s"
          % (job["key"], job["phase"], wall,
             " ".join("%s=%.4g" % (k, v) for k, v in met.items()
                      if isinstance(v, float) and not k.startswith("delta_t"))),
          flush=True)
    return job["key"], job["phase"], met, trace, sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phases", default="1,2,3")
    ap.add_argument("--pool", type=int, default=4)
    ap.add_argument("--out", default="_tes_realj.json")
    ap.add_argument("--retune", default=None, choices=[None, "dith", "step"])
    ap.add_argument("--no-npz", action="store_true")
    ap.add_argument("--only", default=None, help="只跑 key 含该子串的用例（冒烟/分批用）")
    ap.add_argument("--force", action="store_true", help="不跳过已完成用例")
    args = ap.parse_args()

    ph = set("p" + s.strip() for s in args.phases.split(",") if s.strip())
    cases = [c for c in case_list()
             if any(c["phase"] == x or c["phase"].startswith(x) for x in ph)]
    if args.only:
        cases = [c for c in cases if args.only in c["key"]]
    if args.retune:
        cases += retune_cases(args.retune)
    if not cases:
        raise SystemExit("no cases for phases %s" % args.phases)

    sha0 = hashlib.sha256(open(SIM, "rb").read()).hexdigest()
    cur = sha0[:16]

    # 增量续跑：同 sha 已完成的用例跳过（--force 强制重跑）
    out = {}
    if os.path.exists(args.out):
        try:
            out = json.load(open(args.out, encoding="utf-8"))
        except Exception:
            out = {}
    todo, done = [], []
    for c in cases:
        m = out.get(c["key"])
        if (not args.force) and isinstance(m, dict) and m.get("sha_sim") == cur:
            done.append(c["key"])
        else:
            todo.append(c)
    if done:
        print("skip %d cases with sha=%s: %s" % (len(done), cur, ",".join(done)), flush=True)
    if not todo:
        print("nothing to do (all cases already in %s with sha=%s)" % (args.out, cur), flush=True)
        return

    meta = dict(out.get("_meta", {}))
    meta.update(dict(
        script="run_t_realj.py",
        protocol=dict(p1="8 s, A[5,8), RMS[7,8)", p2="30 s, [25,30)",
                      p3="30 s, d/A [20,30), RMS[25,30)", p4a="20 s, [14,20)",
                      p4b="40 s, d[10,14.9)/[30,40), RMS[35,40)",
                      p4c="60 s, segs 10-14.9/25-34.9/50-59.9"),
        J_nom=J_NOM, J_true=J_TRUE, ratio=RATIO, j_oracle=True,
        noise=dict(NC.NOISE_LAB), seed_i=20261018,
        sha256_pmsm_inv_sim_start=sha0,
        pool=args.pool, retune=args.retune))
    out["_meta"] = meta

    def dump():
        json.dump(out, open(args.out, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

    print("J_true=%.3e (=%.3f J_nom)  j_oracle=True  cases=%d  pool=%d"
          % (J_TRUE, RATIO, len(todo), args.pool), flush=True)
    print("sha256(%s)=%s" % (SIM, sha0), flush=True)
    t0 = time.perf_counter()
    res = []
    with Pool(args.pool) as p:
        for r in p.imap_unordered(one, todo, chunksize=1):
            key, phase, met, trace, sha = r
            out[key] = met
            if not args.no_npz:
                np.savez("_wave_t_realj_%s.npz" % key, **trace)
            res.append(r)
            dump()
            print("  [%d/%d] %s done  (%.0f s elapsed)"
                  % (len(res), len(todo), key, time.perf_counter() - t0), flush=True)
    wall = time.perf_counter() - t0
    sha1 = hashlib.sha256(open(SIM, "rb").read()).hexdigest()

    shas = sorted(set(r[4] for r in res))
    meta.update(dict(
        sha256_pmsm_inv_sim_end=sha1,
        sha256_pmsm_inv_sim_per_case=shas,
        sim_stable_during_run=(sha0 == sha1 and shas == [sha0]),
        n_cases=len([k for k in out if not k.startswith("_")]),
        runtime_s_last_batch=round(wall, 1)))
    dump()
    print("runtime %.1f s  cases=%d  sim_stable=%s  -> %s"
          % (wall, len(res), meta["sim_stable_during_run"], args.out), flush=True)
    print("done")


if __name__ == "__main__":
    main()
