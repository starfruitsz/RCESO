import pdfplumber, glob, re
for f in sorted(glob.glob('_refs/Machines*.pdf')):
    with pdfplumber.open(f) as pdf:
        n = len(pdf.pages)
        t = pdf.pages[0].extract_text() or ''
    lines = [l.strip() for l in t.split(chr(10)) if l.strip()]
    print('='*70)
    print('FILE:', f.split(chr(92))[-1], '|', n, 'pages')
    for l in lines[:6]: print('  ', l[:95])
    ab = ' '.join(lines[6:20])[:700]
    print('  [摘要]', ab)
    print()