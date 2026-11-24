import pdfplumber, re, glob
files = {
  'Ma2026': '_refs/Machines2026_misalign_unbalance_dualrotor.pdf',
  'Xing2024': '_refs/Machines2024_support_misalignment.pdf',
  'Jin2022': '_refs/Machines2022_rod_disk_inner_misalignment.pdf',
}
out = []
for nm, f in files.items():
    with pdfplumber.open(f) as pdf:
        pages = [(p.extract_text() or '') for p in pdf.pages]
    full = chr(10).join(pages)
    full = re.sub(r'[ \t]+', ' ', full)
    out.append('#'*20 + ' ' + nm + ' ' + '#'*20)
    for kw in ['equivalent force', 'unbalance force', 'excitation force', 'misalignment force',
               '2X', '2×', 'harmonic', 'gravity', 'mass eccentricity']:
        hits = [m.start() for m in re.finditer(re.escape(kw), full, re.I)]
        if not hits: continue
        out.append('--- [' + kw + '] ' + str(len(hits)) + ' hits ---')
        for h in hits[:2]:
            s = full[max(0,h-260):h+420].replace(chr(10), ' ')
            out.append('   ...' + s + '...')
        out.append('')
open('_refs/quotes_raw.md','w',encoding='utf-8').write(chr(10).join(out))
print('OK', len(out))