# -*- coding: utf-8 -*-
"""把 rcso_*.tex 转成自包含 HTML（内联 MathJax + PNG 图）；默认 v2"""
import re, os, html, json, sys

# 支持命令行指定源文件：python _mkhtml.py xxx.tex → 输出 xxx.html（默认仍为 v2）
SRC = sys.argv[1] if len(sys.argv) > 1 else "rcso_theory_v2.tex"
DST = os.path.splitext(SRC)[0] + ".html"
_raw = open(SRC, encoding="utf-8").read()
# 【预处理】把行内出现的 \begin{...} / \end{...} 规范到独立行，使行级解析器能捕获
for _e in ["equation","align","gather","tabular","center","figure","itemize","enumerate"]:
    _raw = _raw.replace("\\begin{%s}" % _e, "\n" + "\\begin{%s}" % _e)
    _raw = _raw.replace("\\end{%s}" % _e, "\n" + "\\end{%s}" % _e)
lines = _raw.split("\n")

# 去掉 \begin{document} 之前与 \end{document} 之后
try:
    b = next(i for i,t in enumerate(lines) if "\\begin{document}" in t)
except StopIteration:
    b = 0
e = next((i for i,t in enumerate(lines) if "\\end{document}" in t), len(lines))
lines = lines[b+1:e]

MATH_INLINE = re.compile(r"\$[^$]+\$")

def esc(t):
    """转义 HTML，但保留 $...$ 数学；数学段内的 < > 也要转义，否则浏览器会把 $t<t_0$ 当标签吞掉"""
    out = []
    for i, part in enumerate(re.split(r"(\$[^$]*\$)", t)):
        if i % 2:
            out.append(part.replace("<", "&lt;").replace(">", "&gt;"))
        else:
            out.append(html.escape(part, quote=False))
    return "".join(out)

def inline(t):
    """行内 LaTeX → HTML"""
    t = esc(t)
    # 自定义宏（来自导言）
    t = t.replace("\\ef", "e_f").replace("\\taub", "\\tau_B").replace("\\tauf", "\\tau_f").replace("\\taul", "\\tau_l")
    t = t.replace("\\sone", "\\sigma_1^{\\mathrm{ppt}}").replace("\\st", "\\operatorname{tanh}")
    t = t.replace("\\ath", "\\operatorname{tanh}^{-1}").replace("\\aeff", "a_{\\mathrm{eff}}").replace("\\Geff", "\\Gamma_{\\mathrm{eff}}")
    t = t.replace("\\pv", "\\textsf").replace("\\Geff", "\\Gamma_{\\mathrm{eff}}")
    t = t.replace("\\taub", "\\tau_B").replace("\\tauf", "\\tau_f").replace("\\taul", "\\tau_l")
    t = t.replace("\\ef", "e_f")
    # URL：\url{...} → 纯文本
    t = re.sub(r"\\url\{([^}]*)\}", r"\1", t)
    # 参考文献类
    t = re.sub(r"\\(eq)?ref\{([^}]+)\}", _ref_html, t)
    # 文本样式
    t = re.sub(r"\\textbf\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", r"<strong>\1</strong>", t)
    t = re.sub(r"\\emph\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", r"<em>\1</em>", t)
    t = re.sub(r"\\textit\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", r"<em>\1</em>", t)
    # 嵌套 \textbf：外层先转成 <strong>，内层还留着 \textbf{...}，循环到稳定
    for _ in range(4):
        _n = re.sub(r"\\textbf\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", r"<strong>\1</strong>", t)
        if _n == t:
            break
        t = _n
    t = re.sub(r"\\texttt\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", r"<code>\1</code>", t)
    t = re.sub(r"\\textsf\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", r'<span class="tag">\1</span>', t)
    t = re.sub(r"\\noindent\s*", "", t)
    t = t.replace("\\,", "\\,").replace("\\;", "\\;")
    # —— 只对正文段做符号反转义；$...$ 内部必须保留 \% \& \_，否则 MathJax 会把 % 当注释 ——
    _parts = re.split(r"(\$[^$]*\$)", t)
    for _k in range(len(_parts)):
        if _k % 2 == 0:
            _parts[_k] = (_parts[_k].replace("\\S", "§").replace("\\%", "%")
                          .replace("\\&", "&amp;").replace("\\_", "_"))
    t = "".join(_parts)
    t = t.replace("\\quad", "\\quad")
    t = t.replace("---", "—").replace("--", "–")
    t = t.replace("\\par", "")
    # —— 版式命令清洗（v3.2：label/setlength/resizebox/fussy 等不再泄漏进正文）——
    t = re.sub(r"\\label\{[^}]*\}", "", t)
    t = re.sub(r"\\(?:setlength|addtolength)\{[^}]*\}\{[^}]*\}", "", t)
    t = re.sub(r"\\resizebox\{[^}]*\}\{[^}]*\}\{", "", t)
    t = re.sub(r"\\(?:fussy|sloppy|allowdisplaybreaks|centering|noindent)\b", "", t)
    t = re.sub(r"\\(?:vspace|hspace)\*?\{[^}]*\}", "", t)
    t = re.sub(r"\\rule\{[^}]*\}\{[^}]*\}", "", t)
    t = t.replace("\\small", "").replace("\\footnotesize", "").replace("\\scriptsize", "")
    t = t.replace("\\begin{center}", "").replace("\\end{center}", "")
    return t

BS = chr(92)

def grab(s, i):
    """从 s[i] == '{' 起做花括号配对，返回 (内容, 右括号之后的下标)"""
    if i >= len(s) or s[i] != "{":
        return "", i
    d = 0
    j = i
    while j < len(s):
        if s[j] == "{":
            d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)

def cmd_arg(s, name):
    """取 \name{...} 的配对内容（可跨行），找不到返回 ''"""
    k = s.find(name)
    if k < 0:
        return ""
    p = k + len(name)
    while p < len(s) and s[p] in " \t\r\n":
        p += 1
    if p < len(s) and s[p] == "[":
        q = s.find("]", p)
        p = (q + 1) if q > 0 else p
        while p < len(s) and s[p] in " \t\r\n":
            p += 1
    if p >= len(s) or s[p] != "{":
        return ""
    return grab(s, p)[0]

def strip_multirow(c):
    r"""把 \multirow{N}{*}{内容} 折叠成 内容（保留文本、去掉外层，不留残括号）"""
    while "\\multirow" in c:
        k = c.find("\\multirow")
        p = c.index("{", k)
        _w, p = grab(c, p)
        _s, p = grab(c, p)
        body, p = grab(c, p)
        c = c[:k] + body + c[p:]
    return c

def build_table(raw):
    rows = []
    for t in raw.split(BS*2):
        t = t.strip()
        for junk in [BS+"toprule", BS+"midrule", BS+"bottomrule"]:
            t = t.replace(junk, "")
        t = t.strip()
        if not t: continue
        rows.append([inline(c.strip()) for c in t.split("&")])
    if not rows: return ""
    head = rows[0]; body = rows[1:]
    th = "".join("<th>" + c + "</th>" for c in head)
    tb = "".join("<tr>" + "".join("<td>" + c + "</td>" for c in r) + "</tr>" for r in body)
    return '<div class="tablewrap"><table><thead><tr>' + th + '</tr></thead><tbody>' + tb + '</tbody></table></div>'

TABLES = []

def strip_nested_table(txt):
    """把 remark 内的 tabular 换成占位符，避免 inline() 把 <div> 二次转义；不再删正文花括号"""
    B = BS + "begin{tabular}"; E = BS + "end{tabular}"
    res = ""
    while B in txt:
        k = txt.index(B); m = txt.find(E, k)
        if m < 0: break
        pre = txt[:k]
        for junk in [BS+"end{center}", BS+"begin{center}", BS+"small"]:
            pre = pre.replace(junk, "")
        _body = txt[k+len(B):m].lstrip()
        if _body.startswith("{"):          # 去掉列格式 { @{}lcccc@{} }
            _spec, _p = grab(_body, 0)
            _body = _body[_p:]
        TABLES.append(build_table(_body))
        res += pre + "\x00TAB%d\x00" % (len(TABLES)-1)
        txt = txt[m+len(E):]
    return res + txt

def render_mixed(txt):
    """正文按 inline() 处理，表格占位符替换成预生成的 HTML"""
    parts = re.split(r"\x00TAB(\d+)\x00", txt)
    res = []
    for k, p in enumerate(parts):
        if k % 2:
            res.append(TABLES[int(p)])
        else:
            res.append(inline(p))
    return "".join(res)
def eq_to_html(body):
    """公式体 → MathJax"""
    body = body.replace("\\ef", "e_f").replace("\\taub", "\\tau_B").replace("\\tauf", "\\tau_f").replace("\\taul", "\\tau_l")
    body = body.replace("\\sone", "\\sigma_1^{\\mathrm{ppt}}").replace("\\st", "\\operatorname{tanh}")
    body = body.replace("\\ath", "\\operatorname{tanh}^{-1}").replace("\\aeff", "a_{\\mathrm{eff}}").replace("\\Geff", "\\Gamma_{\\mathrm{eff}}")
    body = re.sub(r"\\boxed\{\s*", "", body).replace("\\quad", "\\quad")
    body = re.sub(r"\\(eq)?ref\{([^}]+)\}",
                  lambda m: r"\text{%s}" % (("(%s)" % REF.get(m.group(2), m.group(2)))
                                            if m.group(1) else REF.get(m.group(2), m.group(2))), body)
    # —— v3.2：公式体里的 \label 与 \resizebox 包装必须去掉，否则 MathJax 报 Unknown command ——
    body = re.sub(r"\\label\{[^}]*\}", "", body)
    body = re.sub(r"\\resizebox\{[^}]*\}\{[^}]*\}\{\$(.*?)\$\}", r"\1", body, flags=re.S)
    body = re.sub(r"\\resizebox\{[^}]*\}\{[^}]*\}\{", "", body)
    body = body.replace("$}", "").replace("{$", "")
    # 显示公式里的 < > 也要转义（浏览器会当标签），MathJax 从 textContent 读回尖括号
    return body.replace("<", "&lt;").replace(">", "&gt;")

# ==== 预扫描：解析标签编号（供 \ref / \eqref 显示真实编号）====
REF = {}
_kc = {"sec": 0, "sub": 0, "eq": 0, "fig": 0, "tab": 0,
       "remark": 0, "lemma": 0, "theorem": 0, "corollary": 0, "proposition": 0, "definition": 0}
_j = 0
while _j < len(lines):
    _s = lines[_j].strip()
    if _s.startswith("%") or not _s:
        _j += 1; continue
    if _s.startswith("\\section{"):
        _kc["sec"] += 1; _kc["sub"] = 0
        _lm = re.search(r"\\label\{([^}]+)\}", _s)
        if _lm: REF[_lm.group(1)] = "%d" % _kc["sec"]
        _j += 1; continue
    if _s.startswith("\\subsection{"):
        _kc["sub"] += 1
        _lm = re.search(r"\\label\{([^}]+)\}", _s)
        if _lm: REF[_lm.group(1)] = "%d.%d" % (_kc["sec"], _kc["sub"])
        _j += 1; continue
    _mE = re.match(r"\\begin\{(equation|align|gather)\}", _s)
    if _mE:
        _env = _mE.group(1); _kc["eq"] += 1
        _j += 1
        while _j < len(lines) and ("\\end{%s}" % _env) not in lines[_j]:
            _lm = re.search(r"\\label\{([^}]+)\}", lines[_j])
            if _lm and _lm.group(1) not in REF: REF[_lm.group(1)] = "%d" % _kc["eq"]
            _j += 1
        _j += 1; continue
    if _s.startswith("$$") and _s.endswith("$$") and len(_s) > 4:
        _kc["eq"] += 1; _j += 1; continue
    if _s.startswith("\\["):
        _kc["eq"] += 1
        while _j < len(lines) and "\\]" not in lines[_j]: _j += 1
        _j += 1; continue
    if _s.startswith("\\begin{figure}"):
        _kc["fig"] += 1
        _j += 1
        while _j < len(lines) and "\\end{figure}" not in lines[_j]:
            _lm = re.search(r"\\label\{(fig:[^}]+)\}", lines[_j])
            if _lm: REF[_lm.group(1)] = "%d" % _kc["fig"]
            _j += 1
        _j += 1; continue
    if _s.startswith("\\caption{"):
        _lt = re.search(r"\\label\{(tab:[^}]+)\}", _s)
        if _lt:
            _kc["tab"] += 1; REF[_lt.group(1)] = "%d" % _kc["tab"]
        _j += 1; continue
    _mT = re.match(r"\\begin\{(remark|lemma|theorem|corollary|proposition|definition)\}", _s)
    if _mT:
        _env = _mT.group(1); _kc[_env] += 1
        _lm = re.search(r"\\label\{([^}]+)\}", _s)
        if _lm: REF[_lm.group(1)] = "%d" % _kc[_env]
        _j += 1
        while _j < len(lines) and ("\\end{%s}" % _env) not in lines[_j]:
            _lm2 = re.search(r"\\label\{([^}]+)\}", lines[_j])
            if _lm2 and _lm2.group(1) not in REF: REF[_lm2.group(1)] = "%d" % _kc[_env]
            _j += 1
        _j += 1; continue
    _j += 1

def _ref_html(m):
    lab = m.group(2)
    num = REF.get(lab, lab)
    return '<a class="xref" href="#%s">%s</a>' % (lab, ("(%s)" % num) if m.group(1) else num)

out = []
out.append('<div class="doc">')
i = 0
fig_no = 0
eq_no = 0
tab_no = 0
box_no = {"remark":0,"lemma":0,"theorem":0,"corollary":0,"proposition":0,"definition":0}
pending_cap = ""
pending_cap_id = ""
auto_h = 0
in_disp = None
skip_until = None

while i < len(lines):
    ln = lines[i]
    s = ln.strip()

    # ---- 跳过纯注释/空 ----
    if s.startswith("%"):
        i += 1; continue
    # 过滤导言/标题残留
    if s.startswith("{\\Large") or s.startswith("{\\small v3") or "\\bfseries 自适应低通重复控制" in s:
        i += 1; continue
    if s == "":
        out.append("")
        i += 1; continue

    # ---- 表格外壳 / 题注 / 长度设置（v3.2：这些行以前作为正文泄漏）----
    if s.startswith("\\begin{table}") or s.startswith("\\end{table}"):
        i += 1; continue
    if s.startswith("\\caption{"):
        pending_cap = cmd_arg(s, "\\caption")
        _tl = re.search(r"\\label\{(tab:[^}]+)\}", s)
        pending_cap_id = _tl.group(1) if _tl else ""
        i += 1; continue
    if s.startswith("\\setlength{") or s.startswith("\\renewcommand{\\arraystretch}"):
        i += 1; continue

    # ---- section / subsection（花括号配对：标题含 } 或 ^ 不再截断）----
    if s.startswith("\\subsection{") or s.startswith("\\section{"):
        _tag = "h3" if s.startswith("\\subsection{") else "h2"
        _pre = "\\subsection{" if _tag == "h3" else "\\section{"
        _t, _p = grab(s, len(_pre) - 1)
        _lm = re.search(r"\\label\{([^}]+)\}", s[_p:])
        _id = _lm.group(1) if _lm else ""
        if not _id:
            auto_h += 1
            _id = "h%d" % auto_h
        out.append(f'<{_tag} id="{_id}">{inline(_t)}</{_tag}>')
        i += 1; continue
    _PRE = "\\subsubsection{"
    if s.startswith(_PRE):
        # 【修复】原来用 r"\\subsubsection\{([^}]*)\}"：标题里出现 } （例如 $T_{\rm end}$）就截断，
        #         留下未闭合的 $，使该处之后所有行内公式的 $ 配对整体错位。改为花括号配对提取。
        _d = 0; _j = len(_PRE)
        while _j < len(s):
            if s[_j] == "{": _d += 1
            elif s[_j] == "}":
                if _d == 0: break
                _d -= 1
            _j += 1
        out.append(f'<h4>{inline(s[len(_PRE):_j])}</h4>')
        i += 1; continue

    # ---- 显示公式 ----
    m = re.match(r"\\begin\{(equation|align|gather)\}", s)
    if m:
        env = m.group(1)
        buf = []; labs = []
        i += 1
        while i < len(lines) and not re.match(r"\\end\{%s\}" % env, lines[i].strip()):
            t = lines[i]
            for _lm in re.findall(r"\\label\{([^}]+)\}", t): labs.append(_lm)
            t = re.sub(r"\^\{\}", "", t)
            t = t.replace("\\\\", " \\\\ ")
            buf.append(t)
            i += 1
        i += 1
        body = " ".join(x.strip() for x in buf if x.strip())
        eq_no += 1
        aid = (' id="%s"' % labs[0]) if labs else ""
        out.append(f'<div class="eqwrap"{aid}><div class="eq">\\[{eq_to_html(body)}\\]</div><div class="eqno">({eq_no})</div></div>')
        continue

    # ---- 行间 $...$ 独立成行 ----
    if s.startswith("$$") and s.endswith("$$") and len(s) > 4:
        eq_no += 1
        out.append(f'<div class="eqwrap"><div class="eq">\\[{eq_to_html(s[2:-2])}\\]</div><div class="eqno">({eq_no})</div></div>')
        i += 1; continue

    # ---- figure ----
    if s.startswith("\\begin{figure}"):
        j = i
        while j < len(lines) and "\\end{figure}" not in lines[j]:
            j += 1
        block = " ".join(x.strip() for x in lines[i:j + 1])
        _mm = re.search(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", block)
        img = _mm.group(1) if _mm else ""
        cap = re.sub(r"\s+", " ", cmd_arg(block, "\\caption")).strip()
        _lm = re.search(r"\\label\{(fig:[^}]+)\}", block)
        lab = _lm.group(1) if _lm else ""
        i = j + 1
        fig_no += 1
        png = (img or "").replace(".pdf", ".png")
        out.append(f'<figure id="{lab}"><img src="{png}" alt="图 {fig_no}">'
                   f'<figcaption><span class="fignum">图 {fig_no}</span> {inline(cap)}</figcaption></figure>')
        continue

    # ---- table ----
    if s.startswith("\\begin{tabular}"):
        rows = []
        j = i + 1
        while j < len(lines) and "\\end{tabular}" not in lines[j]:
            t = lines[j].strip()
            if t.startswith("\\toprule") or t.startswith("\\midrule") or t.startswith("\\bottomrule") or t == "":
                j += 1; continue
            if t.endswith("\\\\"):
                t = t[:-2]
            cells = [inline(strip_multirow(c.strip())) for c in t.split("&")]
            rows.append(cells)
            j += 1
        i = j + 1
        # 跳过 \end{center}
        if i < len(lines) and "\\end{center}" in lines[i]: i += 1
        if rows:
            head = rows[0]; body = rows[1:]
            th = "".join(f"<th>{c}</th>" for c in head)
            tb = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in body)
            if pending_cap:
                tab_no += 1
                _cap = f'<div class="tabcap">表 {tab_no}：{inline(pending_cap)}</div>'
            else:
                _cap = ""
            _idattr = f' id="{pending_cap_id}"' if pending_cap_id else ""
            out.append(_cap + f'<div class="tablewrap"{_idattr}><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
        pending_cap = ""
        pending_cap_id = ""
        continue

    # ---- 列表 ----
    if s.startswith("\\begin{itemize}") or s.startswith("\\begin{enumerate}"):
        ordered = s.startswith("\\begin{en") 
        tag = "ol" if ordered else "ul"
        j = i + 1
        items = []
        while j < len(lines) and "\\end{" + ("enumerate" if ordered else "itemize") + "}" not in lines[j]:
            t = lines[j].strip()
            if t.startswith("\\item"):
                items.append(inline(t[5:].strip()))
            elif items and t:
                items[-1] += " " + inline(t)
            j += 1
        i = j + 1
        lis = "".join(f"<li>{x}</li>" for x in items)
        out.append(f"<{tag}>{lis}</{tag}>")
        continue

    # ---- 定理类环境 ----
    m = re.match(r"\\begin\{(remark|lemma|proposition|theorem|corollary|definition)\}(\[(.*?)\])?(.*)$", s)
    if m:
        env, _, title, rest = m.group(1), m.group(2), m.group(3), m.group(4)
        lab = ""
        lm = re.search(r"\\label\{([^}]+)\}", rest)
        if lm: lab = lm.group(1)
        rest = re.sub(r"\\label\{[^}]+\}", "", rest)
        names = {"remark":"注","lemma":"引理","proposition":"命题","theorem":"定理","corollary":"推论","definition":"定义"}
        body = [rest.strip()] if rest.strip() else []
        j = i + 1
        while j < len(lines) and ("\\end{%s}" % env) not in lines[j]:
            body.append(lines[j])
            j += 1
        i = j + 1
        # 去掉结尾 \end 同行残留
        ttl = f"（{inline(title)}）" if title else ""
        _bt = " ".join(x.strip() for x in body if x.strip())
        # 框内的 display math 环境 → \[...\]（交给 MathJax）
        for _de in ["equation","align","gather"]:
            _bt = _bt.replace("\\begin{%s}" % _de, "\\[").replace("\\end{%s}" % _de, "\\]")
        _bt = re.sub(r"\\label\{[^}]+\}", "", _bt)
        txt = _bt
        txt = strip_nested_table(txt)
        box_no[env] += 1
        out.append(f'<div class="box {env}" id="{lab}"><div class="box-h">{names.get(env,env)} {box_no[env]}{ttl}</div><div class="box-b">{render_mixed(txt)}</div></div>')
        continue

    # ---- 其他环境忽略标记 ----
    if s.startswith("\\end{") or s.startswith("\\begin{center}") or s.startswith("\\end{center}") \
       or s.startswith("\\vspace") or s.startswith("\\noindent") and len(s) < 12 \
       or s.startswith("\\small") or s.startswith("{\\small") or s == "}" or s.startswith("\\footnotesize") \
       or s.startswith("\\centering"):
        if s.startswith("\\noindent") and len(s) > 12:
            out.append(f"<p>{inline(s[9:].strip())}</p>")
        i += 1; continue

    # ---- 提示框（\fbox{\parbox{...}}）与页首逻辑链（避免重复）----
    if s.startswith("\\noindent\\fbox{\\parbox{"):
        _k = s.index("\\parbox")
        _w, _p = grab(s, _k + len("\\parbox"))
        _body, _p2 = grab(s, _p)
        out.append(f'<div class="box notice"><div class="box-b">{inline(_body)}</div></div>')
        i += 1; continue
    if s.startswith("\\noindent\\textbf{逻辑链}"):
        i += 1; continue

    # ---- 普通段落 ----
    if s.startswith("\\["):
        j = i; buf=[]
        while j < len(lines) and "\\]" not in lines[j]:
            buf.append(lines[j].replace("\\[","")); j += 1
        if j < len(lines): buf.append(lines[j].replace("\\]",""))
        i = j + 1
        eq_no += 1
        out.append(f'<div class="eqwrap"><div class="eq">\\[{eq_to_html(" ".join(buf))}\\]</div><div class="eqno">({eq_no})</div></div>')
        continue

    out.append(f"<p>{inline(s)}</p>")
    i += 1

# 正文标题（从 PDF 抄录）
TITLE = "自适应低通重复控制（RCESO）：建模、自适应律与一致稳定性证明"
# SUB 由 tex 副标题行解析：旧版硬编码 "v3.1"，导致 HTML 版本行与正文漂移
SUB = ""
for _ln in lines:
    _m = re.search(r"\{\\small\s+v\d+\.", _ln)
    if _m:
        SUB = grab(_ln, _m.start())[0]; break
if not SUB:
    SUB = "版本未解析"
SUB = re.sub(r"\\texttt\{([^}]*)\}", lambda x: x.group(1), SUB)
SUB = re.sub(r"\$([^$]*)\$", lambda x: x.group(1), SUB)
SUB = SUB.replace("\\small", "")
SUB = SUB.replace("\\to", "→").replace("\\_", "_").replace("\\,", " ")
SUB = SUB.replace("{", "").replace("}", "").replace("  ", " ").strip()
CHAIN = ""

body_html = "\n".join(out)
body_html = re.sub(r"\n{3,}", "\n\n", body_html)

mj = open("mathjax.js", encoding="utf-8").read()

CSS = """
:root{--ink:#1a1a1a;--muted:#666;--line:#e2e2e2;--accent:#1f4e79;--bg:#fff;--soft:#f7f8fa;--warn:#8a1c1c}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Source Han Serif SC","Songti SC","SimSun",Georgia,"Times New Roman",serif;
  font-size:16.5px;line-height:1.78;}
.layout{display:grid;grid-template-columns:250px minmax(0,1fr);gap:0;max-width:1280px;margin:0 auto}
nav{position:sticky;top:0;align-self:start;max-height:100vh;overflow-y:auto;
  padding:28px 18px 40px;border-right:1px solid var(--line);font-family:system-ui,"Segoe UI","Microsoft YaHei",sans-serif;font-size:13.5px}
nav h1{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 14px}
nav a{display:block;color:#333;text-decoration:none;padding:4px 8px;border-left:2px solid transparent;border-radius:0 4px 4px 0}
nav a:hover{background:var(--soft);color:var(--accent)}
nav a.l2{font-weight:600;margin-top:10px}
nav a.l3{padding-left:20px;color:#555;font-size:13px}
main{padding:44px 54px 90px;min-width:0}
header.doc-h{border-bottom:2px solid var(--ink);padding-bottom:16px;margin-bottom:26px}
header.doc-h h1{font-size:25px;line-height:1.42;margin:0 0 8px;font-weight:700}
header.doc-h .sub{color:var(--muted);font-size:13.5px;font-family:system-ui,"Microsoft YaHei",sans-serif}
.chain{margin-top:14px;padding:10px 14px;background:var(--soft);border-left:3px solid var(--accent);
  font-size:14px;font-family:system-ui,"Microsoft YaHei",sans-serif;color:#333;border-radius:0 5px 5px 0}
h2{font-size:20.5px;margin:44px 0 14px;padding-bottom:7px;border-bottom:1px solid var(--line);font-weight:700}
h3{font-size:17px;margin:30px 0 10px;color:var(--accent);font-weight:700}
h4{font-size:15.5px;margin:22px 0 8px;font-weight:700}
p{margin:12px 0;text-align:justify}
code{font-family:"Cascadia Mono",Consolas,monospace;font-size:.88em;background:#f1f3f5;padding:1.5px 5px;border-radius:4px;color:#b03030}
.tag{font-family:system-ui,sans-serif;font-size:.85em;background:#eef3f8;color:var(--accent);padding:1px 6px;border-radius:4px}
a.xref{color:var(--accent);text-decoration:none;border-bottom:1px dotted var(--accent);cursor:help}
.eqwrap{display:grid;grid-template-columns:minmax(0,1fr) 62px;align-items:center;margin:18px 0;gap:6px}
.eq{overflow-x:auto;overflow-y:hidden}
.eqno{text-align:right;color:var(--muted);font-size:14px}
figure{margin:26px 0;padding:0}
figure img{width:100%;height:auto;border:1px solid var(--line);border-radius:6px;background:#fff}
figcaption{margin-top:10px;font-size:14px;line-height:1.72;color:#333;text-align:justify;
  font-family:system-ui,"Microsoft YaHei",sans-serif}
.fignum{font-weight:700;color:var(--accent);margin-right:6px}
.tablewrap{overflow-x:auto;margin:22px 0}
table{border-collapse:collapse;width:100%;font-size:14.5px;
  font-family:system-ui,"Microsoft YaHei",sans-serif}
th,td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
thead th{border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);font-weight:700}
tbody tr:hover{background:var(--soft)}
.box{margin:20px 0;border-radius:6px;overflow:hidden;border:1px solid var(--line)}
.box-h{padding:7px 14px;font-weight:700;font-size:14px;
  font-family:system-ui,"Microsoft YaHei",sans-serif;background:var(--soft);border-bottom:1px solid var(--line)}
.box-b{padding:12px 16px;font-size:15.5px;background:#fff}
.tabcap{font-size:14px;color:#333;margin:18px 0 -8px;font-weight:600;
  font-family:system-ui,"Microsoft YaHei",sans-serif}
.box.notice{border-left:3px solid #b8860b;background:#fdf9ef}
.box.remark{border-left:3px solid #b8860b}.box.remark .box-h{color:#8a6508;background:#fdf9ef}
.box.lemma{border-left:3px solid var(--accent)}.box.lemma .box-h{color:var(--accent);background:#f2f7fc}
.box.proposition{border-left:3px solid #2e7d32}.box.proposition .box-h{color:#2e7d32;background:#f1f8f2}
.box.theorem{border-left:3px solid var(--warn)}.box.theorem .box-h{color:var(--warn);background:#fdf3f3}
ul,ol{margin:12px 0;padding-left:26px}
li{margin:6px 0}
@media(max-width:900px){.layout{grid-template-columns:1fr}nav{position:static;max-height:none;border-right:none;border-bottom:1px solid var(--line)}main{padding:28px 20px 60px}}
@media print{nav{display:none}.layout{grid-template-columns:1fr;max-width:none}main{padding:0}figure{break-inside:avoid}.box{break-inside:avoid}}
"""

# 生成 TOC
toc = []
auto_t = 0
for ln in lines:
    _s = ln.strip()
    for _pre, _lvl in (("\\section{", "l2"), ("\\subsection{", "l3")):
        if _s.startswith(_pre):
            _t, _p = grab(_s, len(_pre) - 1)
            _lm = re.search(r"\\label\{([^}]+)\}", _s[_p:])
            _id = _lm.group(1) if _lm else ""
            if not _id:
                auto_t += 1
                _id = "h%d" % auto_t
            toc.append((_lvl, _id, _t))
            break
nav = "".join(f'<a class="{c}" href="#{i}">{inline(t)}</a>' for c,i,t in toc)
CHAIN = "逻辑链：" + " → ".join(f"{k+1} {t}" for k, (c, _i, t) in enumerate([x for x in toc if x[0] == "l2"]))

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TITLE)}</title>
<style>{CSS}</style>
<script>
window.MathJax = {{
  tex: {{inlineMath: [['$','$']], displayMath: [['\\\\[','\\\\]']], processEscapes: true,
         macros: {{ef:"e_f", taub:"\\\\tau_B", tauf:"\\\\tau_f", taul:"\\\\tau_l",
                   ath:"\\\\operatorname{{tanh}}^{{-1}}", st:"\\\\operatorname{{tanh}}"}}}},
  svg: {{fontCache: 'global'}},
  options: {{skipHtmlTags: ['script','noscript','style','textarea','pre','code']}}
}};
</script>
<script>{mj}</script>
</head>
<body>
<div class="layout">
<nav>
  <h1>目录</h1>
  {nav}
</nav>
<main>
<header class="doc-h">
  <h1>{html.escape(TITLE)}</h1>
  <div class="sub">{html.escape(SUB)}</div>
  <div class="chain">{html.escape(CHAIN)}</div>
</header>
{body_html}
</div>
</main>
</div>
</body>
</html>
"""

open(DST,"w",encoding="utf-8").write(HTML)
print("HTML OK:", round(len(HTML.encode("utf-8"))/1024), "KB")
print("  图:", fig_no, "| 公式:", eq_no, "| 章节:", len(toc))
