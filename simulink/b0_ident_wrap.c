/* b0_ident_wrap.c —— 全局参数/状态 + C Caller 入口 */
#include "b0_ident_wrap.h"

/* ---- 硬件侧可调参数（按实机填写） ------------------------------------- */
#define CFG_WH_HZ        65.0f      /* 注入频率 [Hz]，必须 5 Hz 整数倍 */
#define CFG_AMP          0.118f     /* 注入幅值 [pu]，上限 0.25 */
#define CFG_WAVE         B0_WAVE_SINE   /* SINE / SQUARE / TRI */
#define CFG_B0_INIT      400.0f     /* 控制器标称 b0（实际值） */
#define CFG_B0_LO        200.0f     /* 硬下限 0.5x 标称 */
#define CFG_B0_HI        800.0f     /* 硬上限 2.0x 标称 */
#define CFG_KP           75.36f     /* 转速环 kp（与控制器一致） */
#define CFG_LP_DIV       50.0f      /* 低通带宽 = kp/50 */
#define CFG_WO           500.0f     /* 观测器带宽 [rad/s] */
#define CFG_DELTA        1.0f       /* fal 线性区半宽：取 1 使 kappa1=kappa2=1，
                                    * 与纯线性 ESO（beta1=2wo, beta2=wo^2）一致 */
#define CFG_A1           1.0f       /* eso_a1 */
#define CFG_A            0.75f      /* eso_a */

static b0_ident_P  s_P;
static b0_ident_DW s_DW;
static uint8_t     s_ready = 0u;

static B0_REAL b0_pow(B0_REAL x, B0_REAL y)   /* x^y, 仅 init 用 */
{
    /* 小指数展开：exp(y*ln x)，用级数避免依赖 math.h */
    B0_REAL lx = 0.0f, t, z, lz;
    int i;
    if (x <= 0.0f) { return 0.0f; }
    z = (x - 1.0f) / (x + 1.0f);          /* ln x = 2*atanh(z) */
    lz = z; t = z;
    for (i = 3; i <= 11; i += 2) { t *= z * z; lz += t / (B0_REAL)i; }
    lx = 2.0f * lz * y;
    /* exp(lx) */
    t = 1.0f; z = 1.0f;
    for (i = 1; i <= 10; i++) { t *= lx / (B0_REAL)i; z += t; }
    return z;
}

void b0_ident_setup(void)
{
    B0_REAL k1, k2, pi2;
    pi2 = 6.28318530718f;
    k1 = b0_pow(CFG_DELTA, CFG_A1 - 1.0f);      /* delta^(a1-1) */
    k2 = b0_pow(CFG_DELTA, CFG_A  - 1.0f);      /* delta^(a-1)  */

    s_P.dT        = 1.0e-3f;
    s_P.wh        = pi2 * CFG_WH_HZ;
    s_P.amp       = CFG_AMP;
    s_P.amp_max   = 0.25f;
    s_P.wave      = (uint8_t)CFG_WAVE;
    s_P.b1        = 2.0f * CFG_WO * k1;
    s_P.b2        = CFG_WO * CFG_WO * k2;
    s_P.b0_init   = CFG_B0_INIT;
    s_P.b0_lo     = CFG_B0_LO;
    s_P.b0_hi     = CFG_B0_HI;
    s_P.b_den_eps = 1.0e-3f;
    s_P.tcorr_en  = 0u;                 /* T 含采样延迟时开它反而有害 */
    s_P.kp        = CFG_KP;
    s_P.lp_div    = CFG_LP_DIV;
    s_P.d1        = 0.10f;
    s_P.d2        = 0.20f;
    s_P.dmax      = 0.50f;
    s_P.alpha_base= 0.30f;
    s_P.mu        = 0.35f;
    s_P.n_seg     = 200u;               /* 0.2 s */
    s_P.n_warm    = 3u;
    s_P.n_ident   = 24u;                /* 24*5 s = 120 s */
    s_P.n_freeze  = 4u;
    s_P.period_run = 5.0f;
    s_P.period_idle= 3600.0f;

    b0_ident_init(&s_P, &s_DW);
    s_ready = 1u;
}

void b0_ident_u(const float in[5], float out[2])
{
    if (!s_ready) { b0_ident_setup(); }
    b0_ident_step(&s_P, &s_DW,
                  in[0], in[1], in[2], in[3], in[4],
                  &out[0], &out[1]);
}

void b0_ident_sim(float iq, float u, float omega, float e1, float v,
                  float *b0, float *du)
{
    if (!s_ready) { b0_ident_setup(); }
    b0_ident_step(&s_P, &s_DW, iq, u, omega, e1, v, b0, du);
}

b0_res_t b0_ident_res(float iq, float u, float omega, float e1, float v)
{
    b0_res_t r;
    if (!s_ready) { b0_ident_setup(); }
    r.b0 = 0.0f; r.du = 0.0f;
    b0_ident_step(&s_P, &s_DW, iq, u, omega, e1, v, &r.b0, &r.du);
    return r;
}
