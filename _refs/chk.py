import pdfplumber
f='_refs/She2008_译述.pdf'
with pdfplumber.open(f) as pdf:
    print('pages', len(pdf.pages))
    t = pdf.pages[0].extract_text() or ''
    for ln in t.split(chr(10))[:14]: print('  ' + ln[:80])