import pdfplumber, re
f = '_refs/She2008_EID_IEEE_TIE_55-1-380.pdf'
with pdfplumber.open(f) as pdf:
    full = chr(10).join((p.extract_text() or '') for p in pdf.pages)
out = []
def grab(pat, before=60, after=700, label=''):
    m = re.search(pat, full, re.I)
    if not m:
        out.append('### %s : NOT FOUND' % (label or pat)); return
    s = full[max(0, m.start()-before):m.start()+after]
    s = re.sub(r'[ \t]+', ' ', s).replace(chr(10), ' ')
    out.append('### %s' % (label or pat)); out.append(s); out.append('')
grab(r'Definition\s*1', 20, 800, 'Definition 1 (EID)')
grab(r'Assumption\s*1', 20, 420, 'Assumption 1')
grab(r'Assumption\s*2', 20, 260, 'Assumption 2')
grab(r'Lemma\s*1', 20, 520, 'Lemma 1')
open('_refs/she2008_def.md','w',encoding='utf-8').write(chr(10).join(out))
print('OK')