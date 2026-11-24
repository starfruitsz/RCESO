import pdfplumber, re
f = '_refs/She2008_EID_IEEE_TIE_55-1-380.pdf'
with pdfplumber.open(f) as pdf:
    out = []
    for i, p in enumerate(pdf.pages, 1):
        t = p.extract_text() or ''
        out.append('===== PAGE %d =====' % i)
        out.append(t)
open('_refs/she2008_full.txt', 'w', encoding='utf-8').write(chr(10).join(out))
print('pages', len(pdf.pages))
print('chars', sum(len(x) for x in out))