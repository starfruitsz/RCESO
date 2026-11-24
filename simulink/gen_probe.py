import io
src = io.open(r'D:\Desktop\RCESO\simulink\b0_ident_m.m', encoding='utf-8').read()
s = src
s = s.replace('function [b0out, duout] = b0_ident_m(', 'function [b0out, duout, bqout] = b0_ident_m_probe(')
s = s.replace('persistent b0v goal gv base bvalid nest blast nblast nburst frozen',
              'persistent b0v goal gv base bvalid nest blast nblast nburst frozen bqlast')
s = s.replace('    b0v = b0_init; goal = b0_init; gv = 0;',
              '    b0v = b0_init; goal = b0_init; gv = 0; bqlast = 0;')
s = s.replace('                bq = min(max(bq, b0lo), b0hi);',
              '                bq = min(max(bq, b0lo), b0hi);\n                bqlast = bq;')
s = s.replace('b0out = b0v;\nduout = du;', 'b0out = b0v;\nduout = du;\nbqout = bqlast;')
# 本算例的 b_true ≈ 101.9，量程按它设（原值是 FOC 的 400/200/800）
s = s.replace('b0_init= 400;', 'b0_init= 120;')
s = s.replace('b0lo   = 200;', 'b0lo   = 50;')
s = s.replace('b0hi   = 800;', 'b0hi   = 300;')
assert 'bqout = bqlast' in s and 'b0lo   = 50;' in s and 'b0_init= 120;' in s
io.open(r'D:\Desktop\RCESO\simulink\b0_ident_m_probe.m', 'w', encoding='utf-8', newline='\n').write(s)
print('probe regenerated for b~102')
