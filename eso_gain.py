# -*- coding: utf-8 -*-
"""eso_gain.py —— ESO 校正通道的“类 fal”非线性增益（2026-10-22）

形状（用户给定，原图见 _img_zoom/；公式逐字对应）：

    z1_dot = z2 (+ z3) + b0*u + v + beta1 * G(e; a1, delta, lam)
    z2_dot =                         beta2 * G(e; a,  delta, lam)

    G(e; a, delta, lam) := ( |e| + delta * lam**(-1/a) )**a * tanh( lam*e/delta )

其中 e = y - z1 为观测误差。原式第一行括号上**没有指数**（即 z1 通道指数恒为 1），
第二行指数为 a。因此本模块把两个通道的指数分开暴露：a1 给 z1（默认 1.0，与原图一致），
a 给 z2（fal 形态）。若要让 z1 也用 fal 指数，把 a1 设成与 a 相同即可。

（一）与线性 ESO 的关系
    beta1 = 2*wo, beta2 = wo^2 时，把 G 换成恒等映射即原线性 ESO。
    a = 1 且 lam -> 无穷 时 G(e) -> e，故线性 ESO 是本模块的极限情形。

（二）解析性质（推导见 eso_fal.md）
    P1 奇函数、连续、可微：G(0)=0，G(-e)=-G(e)（sign(e) 由 tanh 提供）。
    P2 小信号斜率：|e| << delta/lam 时 tanh(lam*e/delta) -> lam*e/delta，
       故 G(e) -> (delta*lam**(-1/a))**a * lam*e/delta = delta**(a-1) * e。
       **小信号斜率 = delta**(a-1)，与 lam 无关。**
       a<1 时 delta<1 => 斜率 > 1（小误差增益被放大），delta>1 => 斜率 < 1。
    P3 大信号：|e| >> delta/lam 时 tanh -> +-1，G(e) -> (|e| + c)**a * sign(e)，
       c = delta*lam**(-1/a)。a=1 时 G ~ e + c*sign(e)（与线性同阶，只是加了一个
       宽度 c 的偏移带）；a<1 时 G ~ |e|**a（次线性，fal 的典型形态）。
    P4 有界性/扇区性：|G(e)| <= (|e| + c)**a。a=1 时 |G(e)| <= |e| + c，故校正项与
       误差同阶增长——线性 ESO 的 UUB 论证中“误差项阶数”不被抬高，可沿用其结构，
       但 beta 的有效增益被 delta**(a-1) 重标定（见 P2）。
    P5 单调性：dG/de > 0（两项均为正系数），故不存在增益变号/多平衡点。
    P6 噪声：小误差段斜率 delta**(a-1)。取 a=0.9, delta=0.05 时斜率 1.35，
       等效观测带宽变成 wo*sqrt(1.35)=1.16*wo；取 a=0.75 时斜率 2.11（1.45*wo）。

（三）实现约定
    * 所有仿真里 e 与被控量同量纲：本项目 y、e1 均为标幺（pu），故 delta 也取 pu。
      例：delta=0.05 表示 5% 额定转速（600 rpm 下 30 rpm）。
    * 数值安全：delta>0、lam>0、0<a<=2；e=0 时返回 0，无除零。
    * 线性模式用 LinearGain 恒等映射，逐位保持旧行为（回归对账用）。
"""
import math

__all__ = ["FalGain", "LinearGain", "make_gains", "small_signal_slope"]


class LinearGain(object):
    """恒等映射：G(e)=e。与改动前的线性 ESO 逐位一致。"""

    law = "linear"

    def __call__(self, e):
        return e

    def __repr__(self):
        return "LinearGain()"


class FalGain(object):
    """G(e; a, delta, lam) = (|e| + delta*lam**(-1/a))**a * tanh(lam*e/delta)。"""

    law = "fal"

    def __init__(self, a=0.75, delta=0.10, lam=10.0):
        a = float(a); delta = float(delta); lam = float(lam)
        if not (0.0 < a <= 2.0):
            raise ValueError("eso_a 必须在 (0, 2] 内，收到 %r" % (a,))
        if not (delta > 0.0):
            raise ValueError("eso_delta 必须 > 0，收到 %r" % (delta,))
        if not (lam > 0.0):
            raise ValueError("eso_lam 必须 > 0，收到 %r" % (lam,))
        self.a = a
        self.delta = delta
        self.lam = lam
        # 预计算：c = delta*lam**(-1/a)（保证 e->0 时 G -> delta**(a-1)*e，不出现 0**a 的奇异）
        self.c = delta * lam ** (-1.0 / a)
        self.slope0 = delta ** (a - 1.0)     # 小信号斜率（P2）

    def __call__(self, e):
        return (abs(e) + self.c) ** self.a * math.tanh(self.lam * e / self.delta)

    def __repr__(self):
        return "FalGain(a=%g, delta=%g, lam=%g)" % (self.a, self.delta, self.lam)


def small_signal_slope(a, delta):
    """小信号斜率 delta**(a-1)：把线性 ESO 的 wo 换算成非线性版的等效带宽。
    等效观测带宽 wo_eff = wo * delta**((a-1)/2)。"""
    return float(delta) ** (float(a) - 1.0)


def make_gains(cfg, law_key="eso_law", a_key="eso_a", a1_key="eso_a1",
               delta_key="eso_delta", lam_key="eso_lam", default_law="fal"):
    """从配置字典构造 (G1, G2)：G1 给 z1 通道（指数 a1），G2 给 z2 通道（指数 a）。

    默认 default_law="fal"（2026-10-22 用户指定）——不写配置时即走类 fal 增益。
    要回到旧行为：cfg["eso_law"]="linear"（逐位复现 v4.0 的全部历史数据）。
    """
    law = str(cfg.get(law_key, default_law)).strip().lower()
    if law in ("linear", "lin", "off", "0", ""):
        return LinearGain(), LinearGain()
    if law not in ("fal", "nonlinear", "nl", "1"):
        raise ValueError("未知 eso_law=%r（只支持 'linear' / 'fal'）" % (law,))
    a = float(cfg.get(a_key, 0.75))
    a1 = float(cfg.get(a1_key, 1.0))
    delta = float(cfg.get(delta_key, 0.10))
    lam = float(cfg.get(lam_key, 10.0))
    g2 = FalGain(a, delta, lam)
    g1 = g2 if abs(a1 - a) < 1e-12 else FalGain(a1, delta, lam)
    return g1, g2


if __name__ == "__main__":
    # 自检：性质 P1..P5 + 线性极限
    import random
    rnd = random.Random(0)
    for (a, d, l) in [(1.0, 0.05, 10.0), (0.75, 0.05, 10.0), (0.9, 0.02, 20.0), (0.5, 0.2, 5.0)]:
        G = FalGain(a, d, l)
        assert G(0.0) == 0.0, "G(0)!=0"
        for _ in range(200):
            e = rnd.uniform(-2.0, 2.0)
            assert abs(G(e) + G(-e)) < 1e-15, "非奇函数"
            assert (G(1.0001 * e) - G(e)) * (1.0001 * e - e) >= 0.0, "非单调"
            assert abs(G(e)) <= (abs(e) + G.c) ** a + 1e-15, "违反 P4"
        # 小信号斜率
        eps = 1e-9
        s = (G(eps) - G(-eps)) / (2 * eps)
        assert abs(s - d ** (a - 1.0)) < 1e-4 * max(1.0, abs(s)), "小信号斜率 %g != %g" % (s, d ** (a - 1.0))
    # 线性极限：a=1, lam 很大 -> G ≈ e
    G = FalGain(1.0, 0.05, 1e6)
    err = max(abs(G(e) - e) for e in (-1.0, -0.1, 0.0, 0.1, 1.0))
    assert err < 1e-3, "线性极限不成立 err=%g" % err
    # 线性模式
    assert LinearGain()(0.123456789) == 0.123456789
    print("eso_gain self-test: PASS")
    for (a, d) in [(1.0, 0.05), (0.9, 0.05), (0.75, 0.05), (0.6, 0.05), (0.75, 0.01)]:
        s = d ** (a - 1.0)
        print("  a=%.2f delta=%.3f  slope0=%.3f  wo_eff/wo=%.3f" % (a, d, s, s ** 0.5))
