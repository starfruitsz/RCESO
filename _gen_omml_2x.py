# -*- coding: utf-8 -*-
"""_gen_omml_2x.py - 从 _appx2x.docx 提取 OMML，生成 2x 来源公式片段 md。"""
import zipfile
from lxml import etree

NL = chr(10)
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
z = zipfile.ZipFile("_appx2x.docx")
root = etree.fromstring(z.read("word/document.xml"))
omas = root.findall(".//{%s}oMath" % M)
assert len(omas) == 16, len(omas)

snips = []
for o in omas:
    el = etree.fromstring(etree.tostring(o))
    etree.cleanup_namespaces(el)
    s = etree.tostring(el, encoding="unicode", pretty_print=True).rstrip()
    etree.fromstring(s.encode("utf-8"))
    snips.append(s)

LAB = [
    ("1 现有方程是通用的，2× 由 T(θ) 提供", [
        ("① 绕轴转矩方程（对任意谐波成立）", 0),
        ("② 第 k 次谐波的转速纹波", 1),
    ]),
    ("2 来源一：Hooke / 十字滑块运动学", [
        ("③ 两轴转角关系", 2),
        ("④ 从动轴角速度比", 3),
        ("⑤ 小角度展开（2× 项出现）", 4),
        ("⑥ 恒功率下的转矩 2× 纹波", 5),
    ]),
    ("3 来源二：联轴器刚度各向异性", [
        ("⑦ 弹性势能（偏移 a 在联轴器系中随 θ 转）", 6),
        ("⑧ 对 θ 的广义力矩", 7),
        ("⑨ 角不对中版本（a → β）", 8),
        ("⑩ 本质：三角恒等式", 9),
    ]),
    ("4 来源三：间隙 / 接触非线性", [
        ("⑪ 死区特性（傅里叶展开含 2×、3×）", 10),
    ]),
    ("5 代回纹波公式", [
        ("⑫ 2× 转速纹波", 11),
    ]),
    ("6 平行不对中：几何与 2× 转矩", [
        ("⑬ 平行偏移矢量（空间固定，随 θ 旋转）", 12),
        ("⑭ 恒定径向力（各向同性时唯一效果）", 13),
        ("⑮ 弹性势能（各向异性）", 14),
        ("⑯ 绕轴 2× 转矩（各向同性时为零）", 15),
    ]),
]

fence = chr(96) * 3
out = []
out.append("# 附录 A 补充：2× 分量的来源（OMML 片段）")
out.append("")
out.append("> 与报告附录 A.10 的 2× 来源一致；共 16 个式子。")
out.append("> 用法：打开同目录「附录A_2x来源_公式_含平行不对中.docx」复制整条公式；或复制下面的 m:oMath 片段。")
out.append("> 符号：β 角不对中；θ、ω 转角与角速度；a 平行偏移；k_x、k_y 联轴器两向刚度；S(s) 速度环灵敏度。")
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
out.append("说明：LaTeX 源在 _appx2x_math.md，docx 由 pandoc 生成，OMML 已清理命名空间；MathType 可直接识别 docx 里的公式。")

open("附录A_2x来源_OMML.md", "w", encoding="utf-8").write(NL.join(out))
print("written 附录A_2x来源_OMML.md")
print("sizes:", [len(s) for s in snips])