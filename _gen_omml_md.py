# -*- coding: utf-8 -*-
"""_gen_omml_md.py - 从 _appx_math.docx 提取 OMML，生成附录 A 三部分公式片段 md。"""
import zipfile
from lxml import etree

NL = chr(10)
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
z = zipfile.ZipFile("_appx_math.docx")
root = etree.fromstring(z.read("word/document.xml"))
omas = root.findall(".//{%s}oMath" % M)
assert len(omas) == 11, len(omas)

snippets = []
for o in omas:
    el = etree.fromstring(etree.tostring(o))
    etree.cleanup_namespaces(el)
    s = etree.tostring(el, encoding="unicode", pretty_print=True).rstrip()
    etree.fromstring(s.encode("utf-8"))
    snippets.append(s)

LAB = [
    ("1 轴承反力（力平衡 + 力矩平衡）", [
        ("① 质心向心加速度", 0),
        ("② 力平衡", 1),
        ("③ 对 O 点力矩平衡（两轴承 r_A = −aẐ、r_B = +bẐ）", 2),
        ("④ 投影到 ⊥Z 平面", 3),
        ("⑤ 两轴承径向反力", 4),
    ]),
    ("2 轴承摩擦转矩", [
        ("⑥ 摩擦转矩模型", 5),
        ("⑦ 载荷相关项的一阶展开", 6),
    ]),
    ("3 绕轴转矩方程与转速纹波", [
        ("⑧ 实际轴等效惯量", 7),
        ("⑨ 绕轴转矩方程", 8),
        ("⑩ 第 k 次谐波的开环转速纹波", 9),
        ("⑪ 计入速度环灵敏度 S(s) 的转速纹波", 10),
    ]),
]

fence = chr(96) * 3
out = []
out.append("# 附录 A 补充：三部分公式（OMML 片段）")
out.append("")
out.append("> 与报告附录 A.7–A.9（rcso_v3.tex）一致，共 11 个式子。")
out.append("> 用法：打开同目录「附录A_三部分_公式.docx」直接复制整条公式；或复制下面的 m:oMath 片段。")
out.append("> 符号：β 角不对中；θ、ω 转角与机械角速度；I_p、I_t 极/赤道惯量；I_n = I_t sin²β + I_p cos²β；")
out.append("> m、l、d = l sinβ；a、b、L = a+b 轴承位置与跨距；μ_b、r_b 轴承摩擦系数/半径；c_v 粘性阻尼；S(s) 速度环灵敏度。")
out.append("")
for sec, items in LAB:
    out.append("## " + sec)
    out.append("")
    for lab, idx in items:
        out.append("### " + lab)
        out.append("")
        out.append(fence + "xml")
        out.append(snippets[idx])
        out.append(fence)
        out.append("")
out.append("---")
out.append("")
out.append("说明：11 个式子的 LaTeX 源在 _appx_math.md，docx 由 pandoc 生成，OMML 已做命名空间清理；")
out.append("MathType 可直接识别 docx 里的公式，也可用 MathType 的 Toggle TeX 从 _appx_math.md 的 LaTeX 转入。")

open("附录A_三部分_OMML.md", "w", encoding="utf-8").write(NL.join(out))
print("written 附录A_三部分_OMML.md")
print("snippet sizes:", [len(s) for s in snippets])
