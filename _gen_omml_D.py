# -*- coding: utf-8 -*-
"""_gen_omml_D.py - 附录 D（含 A5 证明 + L∞ 增益推导）OMML 片段生成。"""
import zipfile
from lxml import etree

NL = chr(10)
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
z = zipfile.ZipFile("_appxD.docx")
root = etree.fromstring(z.read("word/document.xml"))
omas = root.findall(".//{%s}oMath" % M)
assert len(omas) == 38, len(omas)

snips = []
for o in omas:
    el = etree.fromstring(etree.tostring(o))
    etree.cleanup_namespaces(el)
    s = etree.tostring(el, encoding="unicode", pretty_print=True).rstrip()
    etree.fromstring(s.encode("utf-8"))
    snips.append(s)

LAB = [
    ("D.1 符号与模型", [("① 对象与控制律", 0), ("② ESO 观测器", 1), ("③ 重复通道", 2), ("④ 外部输入能量", 3)]),
    ("D.2 假设", [("⑤ A2：律D 增益盒", 4), ("⑥ A3：律J 参数盒与速率", 5), ("⑦ A4：律T 参数盒", 6),
                 ("⑧ A5：盒内一致 ISS", 7), ("⑨ A6：参数灵敏度界", 8)]),
    ("D.2.1 假设 A5 的证明", [
        ("⑩ 消去 u 后的 z1 方程", 9), ("⑪ e 的方程", 10), ("⑫ e1 的方程", 11), ("⑬ z2 的方程", 12),
        ("⑭ 三阶矩阵 M", 13), ("⑮ 特征多项式 p(s)", 14), ("⑯ Routh–Hurwitz 余量", 15),
        ("⑰ Lyapunov 方程", 16), ("⑱ V0 的导数不等式", 17),
        ("⑲ 指数稳定界 ||e^{At}||", 18), ("⑳ 零状态解", 19), ("㉑ L∞ 增益不等式", 20),
        ("㉒ c_v, c_d, c_r 的定义", 21), ("㉓ 合并 c_w", 22),
        ("㉔ RC 输出的上界", 23), ("㉕ 小增益闭合", 24), ("㉖ 合成后的 A5", 25),
    ]),
    ("D.3 引理 1（参数紧致 + 速率有界）", [
        ("㉗ 律D：饱和门控", 26), ("㉘ 律J：低通解析解", 27), ("㉙ 律J：速率界", 28),
        ("㉚ 律T：抖动后的 δ 界", 29), ("㉛ 律T：时滞紧致区间", 30), ("㉜ 总速率上界 L", 31)]),
    ("D.4 引理 2（慢变参数 Lyapunov 界）", [("㉝ 引理 2 结论", 32), ("㉞ 链式法则不等式", 33), ("㉟ Gronwall 积分", 34)]),
    ("D.5 定理（三律联立有界性）", [("㊱ 定理：误差界", 35), ("㊲ 第 2 步：V 的上界", 36)]),
    ("D.6 注记", [("㊳ A5 的可检验形式（小增益）", 37)]),
]

fence = chr(96) * 3
out = []
out.append("# 附录 D：律 D / J / T 的稳定性与有界性（含 A5 证明 + L∞ 增益推导，OMML 片段）")
out.append("")
out.append("> 共 38 个式子；D.2.1 第四步拆成 (a) L∞ 增益 与 (b) RC 小增益闭合。")
out.append("> 用法：打开同目录「附录D_三律稳定性_含A5与L∞增益.docx」复制整条公式；或复制下面的 m:oMath 片段。")
out.append("")
for sec, items in LAB:
    out.append("## " + sec)
    out.append("")
    for lab, idx in items:
        out.append("### " + lab)
        out.append("")
        out.append(fence + "xml")
        out.append(snips[idx])
        out.append(fence)
        out.append("")
out.append("---")
out.append("")
out.append("说明：LaTeX 源在 _appxD_math.md，docx 由 pandoc 生成，OMML 已清理命名空间。")

open("附录D_三律稳定性_含A5与L∞增益_OMML.md", "w", encoding="utf-8").write(NL.join(out))
print("written 附录D_三律稳定性_含A5与L∞增益_OMML.md")
print("count:", len(snips))
