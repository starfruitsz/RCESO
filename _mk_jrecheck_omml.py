# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
NS='xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
GREEK={'α':0x1D6FC,'ω':0x1D714,'ρ':0x1D70C,'π':0x1D70B}
def mi(s):
    out=[]
    for c in s:
        if 'A'<=c<='Z': out.append(chr(0x1D434+ord(c)-65))
        elif 'a'<=c<='z': out.append(chr(0x1D44E+ord(c)-97))
        elif c in GREEK: out.append(chr(GREEK[c]))
        else: out.append(c)
    return ''.join(out)
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def r(s): return '<m:r><m:t>%s</m:t></m:r>'%esc(mi(s))
def up(s): return '<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>%s</m:t></m:r>'%esc(s)
def sub(b,s): return '<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>'%(b,s)
def sup(b,s): return '<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>'%(b,s)
def frac(n,d): return '<m:f><m:num>%s</m:num><m:den>%s</m:den></m:f>'%(n,d)
def acc(b): return '<m:acc><m:accPr><m:chr m:val="\u0302"/></m:accPr><m:e>%s</m:e></m:acc>'%b
def par(inner,beg='(',end=')'): return '<m:d><m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/></m:dPr><m:e>%s</m:e></m:d>'%(beg,end,inner)
def om(inner): return '<m:oMath %s>%s</m:oMath>'%(NS,inner)
J=r('J'); Jn=sub(J,r('nom')); Jt=sub(J,r('true')); b=r('b'); b0=sub(b,r('0')); w=r('ω')
S={}
S['J_nom']=om(Jn); S['J_true']=om(Jt); S['Jhat']=om(acc(J)); S['b0']=om(b0); S['b']=om(b)
S['omega_d']=om(sub(w,r('d'))); S['f_d']=om(sub(r('f'),r('d'))); S['T_b']=om(sub(r('T'),r('b'))); S['T_rc']=om(sub(r('T'),r('rc')))
S['D']=om(r('D')); S['a_d']=om(sub(r('a'),r('d'))); S['A']=om(r('A')); S['N']=om(r('N'))
S['T_e']=om(sub(r('T'),r('e'))); S['omega']=om(w); S['a_T']=om(sub(r('a'),r('T'))); S['a_omega']=om(sub(r('a'),w))
S['alpha']=om(r('α')); S['rho_b']=om(sub(r('ρ'),r('b')))
S['Jhat_i']=om(sub(acc(J),r('i'))+r('=')+frac(sub(r('a'),r('T')),sub(w,r('d'))+sub(r('a'),w)))
S['b0_update']=om(sub(b,r('0'))+r('←')+sub(b,r('0'))+r('+')+r('α')+par(sup(sub(b,r('0')),r('★'))+r('−')+sub(b,r('0'))))
S['schedule']=om(sub(r('t'),r('k'))+r('=')+sub(r('t'),r('0'))+r('+')+r('k')+sub(r('T'),r('rc')))
S['duty']=om(r('D')+r('=')+frac(sub(r('T'),r('b')),sub(r('T'),r('rc'))))
S['aw_rpm']=om(sub(r('a'),w)+r(',rpm')+r('=')+sub(r('a'),w)+frac(r('60'),r('2')+r('π')))
lines=['', chr(96)*3+'xml']
for k in ['J_nom','J_true','Jhat','b0','b','omega_d','f_d','T_b','T_rc','D','a_d','A','N','T_e','omega','a_T','a_omega','alpha','rho_b','Jhat_i','b0_update','schedule','duty','aw_rpm']:
    lines.append('<!-- %s -->'%k); lines.append(S[k])
lines.append(chr(96)*3); lines.append('')
open('律J_周期复检_公式与实现.md','a',encoding='utf-8').write('\n'.join(lines))
bad=0
for k,v in S.items():
    try: ET.fromstring(v)
    except Exception as e: print('XML ERR',k,e); bad+=1
print('appended',len(S),'bad',bad)
