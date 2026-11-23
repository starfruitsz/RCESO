# replay_variants.py —— 由 foc_io.mat 生成输入流，用 4 个变体回放，量化漂移归因
# 用法：python replay_variants.py   （需要 gcc 在 PATH，或 MinGW gcc）
# 依赖：numpy scipy
import io, os, subprocess, tempfile, sys
import numpy as np, scipy.io as sio

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, 'b0_ident.c')
IO   = os.path.join(HERE, 'foc_io.mat')
CC   = os.environ.get('CC', 'gcc')

HARNESS = r'''
#include <stdio.h>
#include "b0_ident.h"
static b0_ident_P P; static b0_ident_DW DW;
static void setup(void){
    P.dT=1.0e-3f; P.wh=6.28318530718f*65.0f; P.amp=0.118f; P.amp_max=0.25f; P.wave=0;
    P.b1=2.0f*500.0f; P.b2=500.0f*500.0f;
    P.b0_init=400.0f; P.b0_lo=200.0f; P.b0_hi=800.0f;
    P.b_den_eps=1.0e-3f; P.tcorr_en=0u; P.kp=75.36f; P.lp_div=50.0f;
    P.d1=0.10f; P.d2=0.20f; P.dmax=0.50f; P.alpha_base=0.30f; P.mu=0.35f;
    P.n_seg=200u; P.n_warm=3u; P.n_ident=24u; P.n_freeze=4u;
    P.period_run=5.0f; P.period_idle=3600.0f;
    b0_ident_init(&P,&DW);
}
int main(int argc,char**argv){
    FILE*f; double row[5]; long k=0; B0_REAL b0=0.0f,du=0.0f;
    if(argc<2){return 1;} f=fopen(argv[1],"rb"); if(!f){return 1;}
    setup();
    while(fread(row,sizeof(double),5,f)==5){
        b0_ident_step(&P,&DW,(B0_REAL)row[0],(B0_REAL)row[1],(B0_REAL)row[2],
                      (B0_REAL)row[3],(B0_REAL)row[4],&b0,&du);
        k++;
    }
    printf("FINAL b0=%.4f\n",(double)b0); fclose(f); return 0;
}
'''

def patch(src, kind):
    s = src
    if kind == 'exact':
        old = ("    idx = (uint16_t)(DW->ph * (B0_REAL)B0_LUT_SIZE) & (uint16_t)(B0_LUT_SIZE - 1u);\n"
               "    c = b0_cos_tab[idx];\n"
               "    s = b0_sin_tab[idx];")
        new = ("    { double p2 = 6.283185307179586*(double)DW->ph;\n"
               "      c = (B0_REAL)cos(p2); s = (B0_REAL)sin(p2); }\n"
               "    idx = 0u;")
        assert old in s
        s = s.replace(old, new).replace('#include "b0_ident.h"', '#include "b0_ident.h"\n#include <math.h>')
    if kind == 'dtime':
        old = "    DW->t_now += P->dT;"
        new = ("    { static double s_t = 0.0; s_t += (double)P->dT; DW->t_now = (B0_REAL)s_t; }")
        assert old in s
        s = s.replace(old, new)
    return s

def main():
    m = sio.loadmat(IO)
    X = np.column_stack([m[c].ravel().astype(np.float64) for c in ('iqd','ud','omd','e1d','vd')])
    tmp = tempfile.mkdtemp(prefix='b0rep_')
    inp = os.path.join(tmp, 'io.bin'); X.tofile(inp)
    h = os.path.join(tmp, 'h.c'); io.open(h,'w',encoding='utf-8').write(HARNESS)
    src = io.open(SRC, encoding='utf-8').read()
    variants = {
        'float32+LUT（现役）':      dict(defs=[],      kind='none'),
        'float32+精确 sin/cos':     dict(defs=[],      kind='exact'),
        'float32+double 时基':      dict(defs=[],      kind='dtime'),
        'double 全程+LUT':          dict(defs=['-DB0_REAL=double'], kind='none'),
    }
    print('%-22s %10s' % ('变体', '末值 b0'))
    for name, cfg in variants.items():
        csrc = os.path.join(tmp, 'v_%d.c' % abs(hash(name))); io.open(csrc,'w',encoding='utf-8').write(patch(src, cfg['kind']))
        exe = csrc + '.exe'
        cmd = [CC,'-O2','-std=c99','-I',HERE] + cfg['defs'] + ['-o',exe,h,csrc,'-lm']
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(name, 'BUILD FAIL', r.stderr[:300]); continue
        out = subprocess.run([exe, inp], capture_output=True, text=True).stdout.strip()
        print('%-22s %s' % (name, out))

if __name__ == '__main__':
    main()
