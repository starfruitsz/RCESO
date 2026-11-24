import pdfplumber, re
def dump(f, kws, before=300, after=650, n=2):
    with pdfplumber.open(f) as pdf:
        full = chr(10).join((p.extract_text() or '') for p in pdf.pages)
    full = re.sub(r'[ \t]+', ' ', full)
    res = []
    for kw in kws:
        for m in list(re.finditer(re.escape(kw), full, re.I))[:n]:
            s = full[max(0,m.start()-before):m.start()+after].replace(chr(10),' ')
            res.append('[' + kw + '] ...' + s + '...')
    return res
out = []
out.append('===== Ma2026 misalignment =====')
out += dump('_refs/Machines2026_misalign_unbalance_dualrotor.pdf', ['misalignment force','misalignment excitation','2N1'], 300, 700, 2)
out.append('')
out.append('===== Xing2024 =====')
out += dump('_refs/Machines2024_support_misalignment.pdf', ['analytical excitation','misalignment force','Abstract'], 100, 900, 1)
open('_refs/quotes2.md','w',encoding='utf-8').write(chr(10).join(out))
print('OK')