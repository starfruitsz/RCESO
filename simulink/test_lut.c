#include <stdio.h>
#include <math.h>
#include "b0_ident.h"
int main(void){
    b0_ident_P P; b0_ident_DW DW; int i;
    P.dT=1e-3f; P.wh=2*3.14159265f*65.0f; P.amp=0.118f; P.amp_max=0.25f; P.wave=0;
    P.b1=1000.0f; P.b2=444570.0f; P.b0_init=400.0f; P.b0_lo=200.0f; P.b0_hi=800.0f;
    P.b_den_eps=1e-3f; P.tcorr_en=0; P.kp=75.36f; P.lp_div=50.0f;
    P.d1=0.1f; P.d2=0.2f; P.dmax=0.5f; P.alpha_base=0.3f; P.mu=0.35f;
    P.n_seg=200; P.n_warm=3; P.n_ident=24; P.n_freeze=4;
    P.period_run=5.0f; P.period_idle=3600.0f;
    b0_ident_init(&P,&DW);
    { float b0,du,mx=0; int cnt=0;
      for(i=0;i<900;i++){ b0_ident_step(&P,&DW,0.1f,0.1f,600.0f,0.0f,0.0f,&b0,&du);
        if(du>mx) mx=du; if(du< -mx) mx=-du; if(du!=0.0f) cnt++; }
      printf("LUT 检验: du_max=%.5f (期望 <=0.118)  du 非零拍数=%d/900\n", mx, cnt);
      printf("%s\n", (mx<=0.1185f)?"LUT_OK":"LUT_BAD");
    }
    return 0;
}
