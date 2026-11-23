# replay_variants.py —— 由 foc_io.mat 生成输入流，用 4 个变体回放，量化漂移归因
# 用法：python replay_variants.py   （需要 gcc 在 PATH，或 MinGW gcc）
# 依赖：numpy scipy
#
# 变体：
#   1 原实现     float32 秒时基 + 256 点 LUT          -> 573.17（漂移）
#   2 C-1        float32 秒时基 + 精确 sin/cos        -> 573.10（LUT 无关）
#   3 C-2        float32 + double 累加时基            -> 531.68（时间基是主因）
#   4 现役       整数拍计数（uint32 tick）            -> 531.17（漂移消除）
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
    FILE*f; double row[5]; B0_REAL b0=0.0f,du=0.0f;
    if(argc<2){return 1;} f=fopen(argv[1],"rb"); if(!f){return 1;}
    setup();
    while(fread(row,sizeof(double),5,f)==5){
        b0_ident_step(&P,&DW,(B0_REAL)row[0],(B0_REAL)row[1],(B0_REAL)row[2],
                      (B0_REAL)row[3],(B0_REAL)row[4],&b0,&du);
    }
    printf("FINAL b0=%.4f\n",(double)b0); fclose(f); return 0;
}
'''

def _patch_exact(s):
    old = ("    idx = (uint16_t)(DW->ph * (B0_REAL)B0_LUT_SIZE) & (uint16_t)(B0_LUT_SIZE - 1u);\n"
           "    c = b0_cos_tab[idx];\n"
           "    s = b0_sin_tab[idx];")
    new = ("    { double p2 = 6.283185307179586*(double)DW->ph;\n"
           "      c = (B0_REAL)cos(p2); s = (B0_REAL)sin(p2); }\n"
           "    idx = 0u;")
    assert old in s
    return s.replace(old, new).replace('#include "b0_ident.h"', '#include "b0_ident.h"\n#include <math.h>')

def _patch_stime(s, daccum):
    """把整数拍时基改回浮点秒时基（原实现）。daccum=True 表示用 double 累加。"""
    s = s.replace('static uint32_t b0_ticks(',
                  'static float s_tn = 0.0f, s_tx = 1.0e-3f;\nstatic uint32_t b0_ticks_unused(')
    rep = [
        ("    DW->tick = 0u;\n    DW->next_tick = 1u;",
         "    s_tn = 0.0f; s_tx = P->dT;"),
        ("    DW->tick++;                         /* 整数拍计数：130 s 不漂 45 ms */",
         ("    { static double s_d = 0.0; s_d += (double)P->dT; s_tn = (float)s_d; }"
          if daccum else "    s_tn += P->dT;")),
        ("(DW->tick < DW->next_tick)", "(s_tn < s_tx)"),
        ("DW->next_tick = DW->tick + b0_ticks(P->period_idle, P->dT);",
         "s_tx = s_tn + P->period_idle;"),
        ("DW->next_tick = DW->tick + b0_ticks(P->period_run, P->dT);",
         "s_tx = s_tn + P->period_run;"),
    ]
    for old, new in rep:
        assert old in s, old[:40]
        s = s.replace(old, new)
    return s

def build_variant(src, kind, exact):
    s = src
    if kind == 'stime':
        s = _patch_stime(s, daccum=False)
    elif kind == 'stime_d':
        s = _patch_stime(s, daccum=True)
    if exact:
        s = _patch_exact(s)
    return s

def main():
    m = sio.loadmat(IO)
    X = np.column_stack([m[c].ravel().astype(np.float64) for c in ('iqd','ud','omd','e1d','vd')])
    tmp = tempfile.mkdtemp(prefix='b0rep_')
    inp = os.path.join(tmp, 'io.bin'); X.tofile(inp)
    h = os.path.join(tmp, 'h.c'); io.open(h,'w',encoding='utf-8').write(HARNESS)
    src = io.open(SRC, encoding='utf-8').read()
    variants = [
        ('原实现 float32 秒时基 + LUT', 'stime',   False, []),
        ('C-1  秒时基 + 精确 sin/cos',  'stime',   True,  []),
        ('C-2  秒时基 + double 累加',   'stime_d', False, []),
        ('现役 整数拍计数 + LUT',        'tick',    False, []),
        ('参考 double 全程 + LUT',       'tick',    False, ['-DB0_REAL=double']),
    ]
    print('%-30s %14s' % ('变体', '末值 b0'))
    for name, kind, exact, defs in variants:
        csrc = os.path.join(tmp, 'v_%d.c' % abs(hash(name)))
        io.open(csrc,'w',encoding='utf-8').write(build_variant(src, kind, exact))
        exe = csrc + '.exe'
        cmd = [CC,'-O2','-std=c99','-I',HERE] + defs + ['-o',exe,h,csrc,'-lm']
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(name, 'BUILD FAIL', r.stderr[:300]); continue
        out = subprocess.run([exe, inp], capture_output=True, text=True).stdout.strip()
        print('%-30s %14s' % (name, out))

if __name__ == '__main__':
    main()
