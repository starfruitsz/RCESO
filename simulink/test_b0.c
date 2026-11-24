/* test_b0.c —— 解析自洽测试（3 个用例） */
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "b0_ident.h"

#define PI_F 3.14159265358979f
static b0_ident_P P; static b0_ident_DW DW;

static float run_case(const char *name, float b_true, float b0_init,
                      float Tmag, float Tdeg, int wave, int tcorr,
                      float stop_s)   /* stop_s 秒内转速为 0（验证运行使能门限） */
{
    int k, nseg = 200, nburst = 40, ntot = nburst * 2 * nseg;
    float dT = 1e-3f, fh = 65.0f, wh = 2*PI_F*fh, A = 0.1f;
    float ph, c, s, u, iq, e1, v, du, b0;
    float Tth = Tdeg * PI_F / 180.0f;
    float E1re = 1.0f, E1im = 0.0f;

    memset(&P, 0, sizeof(P));
    P.dT = dT; P.wh = wh; P.amp = A; P.amp_max = 0.25f; P.wave = (uint8_t)wave;
    P.b1 = 1000.0f; P.b2 = 444570.0f;
    P.b0_init = b0_init; P.b0_lo = 0.1f*b0_init; P.b0_hi = 5.0f*b0_init;
    P.b_den_eps = 1e-3f; P.tcorr_en = (uint8_t)tcorr;
    P.kp = 75.36f; P.lp_div = 50.0f;
    P.d1 = 0.10f; P.d2 = 0.20f; P.dmax = 0.50f;
    P.alpha_base = 0.30f; P.mu = 0.35f;
    P.n_seg = (uint16_t)nseg; P.n_warm = 3; P.n_ident = (uint16_t)(nburst+1);
    P.n_freeze = 4; P.period_run = 1.0f;  /* 起点周期 1 s：0.4 s 段 + 0.6 s 空闲 */
    P.period_idle = 3600.0f;
    P.omega_on = 180.0f; P.omega_off = 150.0f;   /* 运行使能门限 */
    b0_ident_init(&P, &DW);

    for (k = 0; k < ntot; k++) {
        int seg = (k / nseg) % 2;
        float Qre, Qim, Ure, Dr, Di, Vre, Vim;
        ph = fmodf(wh * (float)k * dT, 2*PI_F);
        c = cosf(ph); s = sinf(ph);
        u  = (seg == 1) ? (A * c) : 0.0f;
        Ure = (seg == 1) ? A : 0.0f;
        /* 实际电流 = T * u */
        Qre = Tmag * cosf(Tth) * Ure - Tmag * sinf(Tth) * 0.0f;
        Qim = Tmag * sinf(Tth) * Ure + Tmag * cosf(Tth) * 0.0f;
        iq = Qre * c - Qim * s;
        e1 = E1re * c - E1im * s;
        /* D = F(0) + b*Q - b0*U */
        Dr = b_true * Qre - DW.b0 * Ure;
        Di = b_true * Qim - DW.b0 * 0.0f;
        Vre = Dr - (P.pd_re*E1re - P.pd_im*E1im);
        Vim = Di - (P.pd_re*E1im + P.pd_im*E1re);
        v = Vre * c - Vim * s;
        {   /* 运行使能改由外部实现：停机段不调用 step（门限外置） */
            if ((float)k * dT >= stop_s) {
                b0_ident_step(&P, &DW, iq, u, e1, e1, v, &b0, &du);   /* 线性 ESO：ge1 = e1 */
            } }
        (void)du;
    }
    printf("  %-26s b_true=%6.1f  b0=%7.2f  误差=%+7.3f%%  bursts=%u\n",
           name, b_true, DW.b0, 100.0f*(DW.b0/b_true - 1.0f), DW.n_burst);
    return DW.b0;
}

int main(void)
{
    printf("--- 解析自洽测试（T=电流环复传函） ---\n");
    run_case("正弦 T=1.00<0deg  修正开", 400.0f, 300.0f, 1.00f, 0.0f, 0, 1, 0.0f);
    run_case("正弦 T=0.95<+5deg   修正关", 400.0f, 300.0f, 0.95f, 5.0f, 0, 0, 0.0f);
    run_case("正弦 T=0.95<+5deg   修正开", 400.0f, 300.0f, 0.95f, 5.0f, 0, 1, 0.0f);
    run_case("方波 T=1.00<0deg  修正开", 400.0f, 300.0f, 1.00f, 0.0f, 1, 1, 0.0f);
    run_case("三角 T=1.00<0deg  修正开", 400.0f, 300.0f, 1.00f, 0.0f, 2, 1, 0.0f);
    run_case("正弦 T=1.00 前8s停机", 400.0f, 300.0f, 1.00f, 0.0f, 0, 1, 8.0f);
    return 0;
}
