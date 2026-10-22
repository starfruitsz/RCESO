
import re, os
h = open("rcso_v3.html", encoding="utf-8").read()
b = h[h.index("<body>"):h.index("</body>")]
res = []
def chk(name, ok, detail=""):
    res.append((name, bool(ok), detail))

for pat, nm in [(r"\\label\{", r"\label{"), (r"\\caption\{", r"\caption{"), (r"\\multirow", r"\multirow"),
                (r"\\fbox", r"\fbox"), (r"\\setlength", r"\setlength"), (r"\\fussy", r"\fussy"),
                (r"\\sloppy", r"\sloppy"), (r"\\includegraphics", r"\includegraphics"),
                (r"\\resizebox", r"\resizebox"), (r"\\ref\{", r"\ref{"), (r"\\end\{center\}", r"\end{center}")]:
    n = len(re.findall(pat, b))
    chk("leak " + nm, n == 0, "n=%d" % n)

chk("no_backslash_underscore", "\\_" not in b, "n=%d" % b.count("\\_"))
bad_pct = re.findall(r"\$[^$\n]*?(?<!\\)%[^$\n]*\$", b)
chk("no_bare_percent_in_math", not bad_pct, "n=%d e.g.%s" % (len(bad_pct), bad_pct[:2]))
chk("no_amp_in_math", not re.findall(r"\$[^$\n]*&amp;[^$\n]*\$", b), "")

ids = re.findall(r'id="([^"]+)"', b)
hrefs = re.findall(r'href="#([^"]+)"', h)
missing = sorted(set(hrefs) - set(ids) - {""})
chk("anchors", not missing, "href=%d ids=%d missing=%s" % (len(hrefs), len(ids), missing[:6]))
chk("empty_id", "" not in ids, "empty=%d" % ids.count(""))
chk("id_unique", len(ids) == len(set(ids)), "dup=%s" % [x for x in set(ids) if ids.count(x) > 1][:4])

srcs = re.findall(r'<img src="([^"]+)"', b)
miss_img = [s for s in set(srcs) if not os.path.exists(s)]
chk("figures", len(srcs) == 13 and not miss_img, "n=%d missing=%s" % (len(srcs), miss_img))

chk("h2", len(re.findall(r"<h2 ", b)) == 10, str(len(re.findall(r"<h2 ", b))))
chk("h3", len(re.findall(r"<h3 ", b)) == 22, str(len(re.findall(r"<h3 ", b))))
chk("h4", len(re.findall(r"<h4>", b)) == 2, str(len(re.findall(r"<h4>", b))))
# 2026-10-22：16 -> 17（§1.3 注「校正通道的增益形状：类 fal 可选档」新增一张 ESO 增益形状对照表）
chk("tables", len(re.findall(r"<table>", b)) == 17, str(len(re.findall(r"<table>", b))))
chk("tabcap", len(re.findall(r'class="tabcap"', b)) == 1, str(len(re.findall(r'class="tabcap"', b))))
chk("notice", len(re.findall(r"box notice", b)) == 2, str(len(re.findall(r"box notice", b))))
chk("figcaption", len(re.findall(r"<figcaption>", b)) == 13, str(len(re.findall(r"<figcaption>", b))))

# 浏览器可见的转换缺陷（51 项之外的三类：未转换的 \textbf、二次转义的表格、列格式残留）
chk("no_visible_textbf", "\\textbf" not in b, "n=%d" % b.count("\\textbf"))
chk("no_escaped_table", '&lt;div class="tablewrap"' not in b, "found")
chk("no_tabular_spec", "{@{}" not in b, "found")

caps = re.findall(r"<figcaption>(.*?)</figcaption>", b, re.S)
short = [re.sub(r"<[^>]+>", "", c)[:36] for c in caps if len(re.sub(r"<[^>]+>", "", c)) < 40]
chk("caption_not_short", not short, str(short[:3]))

sub = re.search(r'<div class="sub">([^<]*)</div>', h).group(1)
chk("sub_v40", sub.startswith("v4.0"), sub[:40])
chk("sub_clean", ("\\" not in sub) and ("{" not in sub) and ("$" not in sub), sub)

must = ["7.91", "40.05", "7.24", "80.2", "37.24", "5.32", "32.80", "8.23", "3142", "pmsm_inv_sim", "记忆失配"]
gone = ["v3.1", "71.9", "36.5", "648.62", "折中最优", "突变优先选", "-50.8", "23.30"]
for m in must:
    chk("has:" + m, m in b, "" if m in b else "MISSING")
for m in gone:
    chk("gone:" + m, m not in b, "still@%d" % b.find(m) if m in b else "")

toc_t = [re.sub(r"<[^>]+>", "", x) for x in re.findall(r'<a class="l[23]" href="#[^"]*">(.*?)</a>', h)]
body_t = [re.sub(r"<[^>]+>", "", x) for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", b)]
chk("toc_matches_body", toc_t == body_t, "toc=%d body=%d" % (len(toc_t), len(body_t)))

odd_p = [re.sub(r"\s+", " ", p)[:56] for p in re.findall(r"<p>(.*?)</p>", b, re.S) if p.count("$") % 2]
chk("dollar_even_in_p", not odd_p, "n=%d e.g.%s" % (len(odd_p), odd_p[:2]))
odd_h = [x[:56] for x in re.findall(r"<h[234][^>]*>(.*?)</h[234]>", b) if x.count("$") % 2]
chk("dollar_even_in_head", not odd_h, str(odd_h[:2]))
odd_c = [x[:56] for x in re.findall(r"<figcaption>(.*?)</figcaption>", b, re.S) if x.count("$") % 2]
chk("dollar_even_in_caption", not odd_c, str(odd_c[:2]))

fails = [r for r in res if not r[1]]
print("TOTAL %d  PASS %d  FAIL %d" % (len(res), len(res) - len(fails), len(fails)))
for n, ok, d in res:
    if not ok:
        print("  FAIL  %-24s %s" % (n, d))
# 2026-10-22：自检失败必须让进程非零退出（此前即使 FAIL>0 也返回 0，等于自检形同虚设）
raise SystemExit(1 if fails else 0)

