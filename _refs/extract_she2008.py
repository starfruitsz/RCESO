import pdfplumber, re
f = '_refs/She2008_EID_IEEE_TIE_55-1-380.pdf'
with pdfplumber.open(f) as pdf:
    pages = [(p.extract_text() or '') for p in pdf.pages]
full = chr(10).join(pages)
out = []
def show(pat, ctx=340, n=2, label=None):
    hits = [m.start() for m in re.finditer(pat, full, re.I)]
    out.append('### %s  (%d hit)' % (label or pat, len(hits)))
    for h in hits[:n]:
        s = full[max(0, h-100):h+ctx]
        s = re.sub(r'[ \t]+', ' ', s).replace(chr(10), ' ')
        out.append('   ...' + s + '...')
    out.append('')
show(r'Lemma\s*1')
show(r'is defined as', 380, 1, 'EID definition')
show(r'low-?pass filter', 340, 2, 'low-pass filter')
show(r'state observer', 340, 2, 'state observer')
show(r'Remark\s*1', 380, 1, 'Remark 1')
show(r'Theorem\s*1', 380, 1, 'Theorem 1')
open('_refs/she2008_passages.md','w',encoding='utf-8').write(chr(10).join(out))
print('OK', len(out))