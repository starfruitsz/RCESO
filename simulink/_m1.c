/* ==========================================================================
 * b0_ident.c  --  两段式高频注入 b0 在线辨识（1 kHz，单精度，无动态内存）
 * 见 b0_ident.h 的接口说明。全部运算 real32，无 malloc，无阻塞。
 * ========================================================================== */
#include "b0_ident.h"

/* ---- 编译期常数 -------------------------------------------------------- */
#ifndef B0_TWO_PI
#define B0_TWO_PI 6.28318530718f
#endif
#ifndef B0_EPS
#define B0_EPS 1.0e-12f
#endif

/* ---- 模块内静态存储：sin/cos 表（256 点，1 KB） ------------------------ */
static B0_REAL b0_sin_tab[B0_LUT_SIZE];
static B0_REAL b0_cos_tab[B0_LUT_SIZE];
static uint8_t b0_tab_ready = 0u;

/* ---- 小工具（不依赖 math.h，便于 C28x 软浮点） ------------------------ */
static B0_REAL b0_absf(B0_REAL x) { return (x < 0.0f) ? -x : x; }

static B0_REAL b0_exp_neg(B0_REAL x)     /* exp(-x), x>=0, 泰勒+限幅 */
{
    /* C28x 上 expf 很贵；这里用 5 阶展开，x<=6 时误差 <2e-4，足够门控用 */
    B0_REAL t, s;
    if (x > 6.0f) { x = 6.0f; }
    t = 1.0f; s = 1.0f;
    t = t * (-x) / 1.0f; s += t;
    t = t * (-x) / 2.0f; s += t;
    t = t * (-x) / 3.0f; s += t;
    t = t * (-x) / 4.0f; s += t;
    t = t * (-x) / 5.0f; s += t;
    return s;
}

static void b0_build_tab(void)
{
    uint16_t i;
    B0_REAL a;
    for (i = 0u; i < B0_LUT_SIZE; i++) {
        a = B0_TWO_PI * (B0_REAL)i / (B0_REAL)B0_LUT_SIZE;
        /* 立方近似的展开式不好写；init 期只跑 256 次，直接用级数 */
        {
            B0_REAL s = a, term = a, n;
            for (n = 1.0f; n < 9.0f; n += 2.0f) {          /* sin 级数 */
                term = -term * a * a / ((n + 1.0f) * (n + 2.0f));
                s += term;
            }
            b0_sin_tab[i] = s;
        }
        {
            B0_REAL c = 1.0f, term = 1.0f, n;
            for (n = 0.0f; n < 10.0f; n += 2.0f) {         /* cos 级数 */
                term = -term * a * a / ((n + 1.0f) * (n + 2.0f));
                c += term;
            }
            b0_cos_tab[i] = c;
        }
    }
    b0_tab_ready = 1u;
}

/* ---- 波形：peak = 1 ---------------------------------------------------- */
static B0_REAL b0_wave_value(uint8_t wave, B0_REAL ph_cyc, B0_REAL s)
{
    if (wave == B0_WAVE_SQUARE) {
        return (s >= 0.0f) ? 1.0f : -1.0f;
    }
    if (wave == B0_WAVE_TRI) {          /* ph_cyc ∈ [0,1) */
        B0_REAL a = ph_cyc * 4.0f;
        if (a < 1.0f)      { return a; }
        if (a < 3.0f)      { return 2.0f - a; }
        return a - 4.0f;
    }
    return s;                            /* 正弦 */
}

/* ---- 清累加器 ---------------------------------------------------------- */
static void b0_clear_acc(b0_ident_DW *DW)
{
    DW->ac_e1 = 0.0f; DW->as_e1 = 0.0f;
    DW->ac_v  = 0.0f; DW->as_v  = 0.0f;
    DW->ac_u  = 0.0f; DW->as_u  = 0.0f;
    DW->ac_q  = 0.0f; DW->as_q  = 0.0f;
    DW->ac_w  = 0.0f; DW->as_w  = 0.0f;
}

/* ========================================================================
 * 初始化
 * ===================================================================== */
void b0_ident_init(b0_ident_P *P, b0_ident_DW *DW)
{
    B0_REAL th, sn, cs, sr, si, sd2, tau;

    if (!b0_tab_ready) { b0_build_tab(); }

    /* 相位增量（cycle/tick）：须使 dph_cyc*n_seg 为整数（fh 取 5 Hz 整数倍） */
    P->dph_cyc = P->wh * P->dT / B0_TWO_PI;

    /* Sd = (e^{j*wh*dT} - 1)/dT */
    th = P->wh * P->dT;
    {
        B0_REAL s = th, term = th, n;
        for (n = 1.0f; n < 9.0f; n += 2.0f) {
            term = -term * th * th / ((n + 1.0f) * (n + 2.0f));
            s += term;
        }
        sn = s;
    }
    {
        B0_REAL c = 1.0f, term = 1.0f, n;
        for (n = 0.0f; n < 10.0f; n += 2.0f) {
            term = -term * th * th / ((n + 1.0f) * (n + 2.0f));
            c += term;
        }
        cs = c;
    }
    P->sd_re = (cs - 1.0f) / P->dT;
    P->sd_im = sn / P->dT;

    /* 1/Sd = conj(Sd)/|Sd|^2 ; pd = Sd + b1 + b2/Sd */
    sd2 = P->sd_re * P->sd_re + P->sd_im * P->sd_im;
    sr = (sd2 > B0_EPS) ? (P->sd_re / sd2) : 0.0f;
    si = (sd2 > B0_EPS) ? (-P->sd_im / sd2) : 0.0f;
    P->pd_re = P->sd_re + P->b1 + P->b2 * sr;
    P->pd_im = P->sd_im +         P->b2 * si;

    /* 低通系数：tau = lp_div/kp -> a = 1-exp(-dT/tau) */
    tau = (P->kp > B0_EPS) ? (P->lp_div / P->kp) : 1.0f;
    P->lp_a = 1.0f - b0_exp_neg(P->dT / tau);

    /* 状态复位 */
    DW->ph = 0.0f;
    b0_clear_acc(DW);
    DW->n_acc = 0u; DW->seg = 0u; DW->active = 0u;
    DW->t_now = 0.0f;
    DW->t_next = P->dT;                 /* 第一个 burst 在 1 ms 后 */
    DW->d0_re = 0.0f; DW->d0_im = 0.0f;
    DW->u0_re = 0.0f; DW->u0_im = 0.0f;
    DW->q0_re = 0.0f; DW->q0_im = 0.0f;
    DW->t0_re = 1.0f; DW->t0_im = 0.0f;
    DW->b0 = P->b0_init;
    DW->goal = P->b0_init;
    DW->goal_valid = 0u;
    DW->base = P->b0_init;
    DW->base_valid = 0u;
    DW->n_est = 0u;
    DW->n_blast = 0u;
    DW->n_burst = 0u;
    DW->frozen = 0u;
    DW->b_est = P->b0_init;
    DW->alpha_last = 0.0f;
}

/* ========================================================================
 * 段末解算 + 门控
 * ===================================================================== */
static void b0_seg_end(const b0_ident_P *P, b0_ident_DW *DW)
{
    B0_REAL k, e1r, e1i, vr, vi, ur, ui, qr, qi, wr, wi;
    B0_REAL dhr, dhi, den, tr, ti;
    B0_REAL nr, ni, dr, di, den2, bq, t2;

    k = 2.0f / (B0_REAL)DW->n_acc;
    e1r = k * DW->ac_e1; e1i = -k * DW->as_e1;
    vr  = k * DW->ac_v;  vi  = -k * DW->as_v;
    ur  = k * DW->ac_u;  ui  = -k * DW->as_u;
    qr  = k * DW->ac_q;  qi  = -k * DW->as_q;
    wr  = k * DW->ac_w;  wi  = -k * DW->as_w;   /* 仅诊断，见 (void) */
    (void)wr; (void)wi;

    /* dhat = V + pd * E1 */
    dhr = vr + P->pd_re * e1r - P->pd_im * e1i;
    dhi = vi + P->pd_re * e1i + P->pd_im * e1r;

    /* T = Q / U */
    den = ur * ur + ui * ui;
    if (den > B0_EPS) {
        tr = (qr * ur + qi * ui) / den;
        ti = (qi * ur - qr * ui) / den;
    } else {
        tr = 1.0f; ti = 0.0f;
    }

    if (DW->seg == 0u) {                       /* 注入前段：锁存 */
        DW->d0_re = dhr; DW->d0_im = dhi;
        DW->u0_re = ur;  DW->u0_im = ui;
        DW->q0_re = qr;  DW->q0_im = qi;
        DW->t0_re = tr;  DW->t0_im = ti;
        return;
    }

    /* 注入段：差分 */
    dr = qr - DW->q0_re;
    di = qi - DW->q0_im;
    den2 = dr * dr + di * di;
    if (den2 <= B0_EPS) { return; }            /* 分母过小，跳过本 burst */

    nr = (dhr - DW->d0_re) + DW->b0 * (ur - DW->u0_re);
    ni = (dhi - DW->d0_im) + DW->b0 * (ui - DW->u0_im);
    bq = (nr * dr + ni * di) / den2;           /* Re{num/den} */

    /* 末端 T 修正（可关）：bq / T -> Re{conj(T)}/|T|^2 */
    if (P->tcorr_en) {
        t2 = tr * tr + ti * ti;
        if (t2 > B0_EPS) { bq = (bq * tr) / t2; }
    }

    /* 限幅 */
    if (bq < P->b0_lo) { bq = P->b0_lo; }
    if (bq > P->b0_hi) { bq = P->b0_hi; }
    DW->b_est = bq;

    /* ---- 门控 ---- */
    if (!DW->base_valid) {                     /* 首次：直接赋值，alpha=1 */
        DW->base = bq; DW->base_valid = 1u;
        DW->b0 = bq; DW->goal = bq; DW->goal_valid = 0u;
        DW->n_est = 1u; DW->alpha_last = 1.0f;
    } else if (DW->n_est < P->n_warm) {        /* 预热：alpha=1 */
        DW->base = bq;
        DW->b0 = bq; DW->goal = bq; DW->goal_valid = 0u;
        DW->n_est++;
        DW->alpha_last = 1.0f;
    } else {                                   /* 平台 + 软底 */
        B0_REAL d, w, al;
        d = b0_absf(bq - DW->base) / (b0_absf(DW->base) + B0_EPS);
        if (d <= P->d1) {
            w = 1.0f;
        } else if (d <= P->dmax) {
            w = b0_exp_neg((d - P->d1) / (P->d2 + B0_EPS));
        } else {
            w = b0_exp_neg((P->dmax - P->d1) / (P->d2 + B0_EPS));
        }
        al = P->alpha_base * w;
        DW->alpha_last = al;
        DW->goal = DW->b0 + al * (bq - DW->b0);
        DW->goal_valid = 1u;
        DW->base += P->mu * (bq - DW->base);
        DW->n_est++;
    }

    /* ---- 冻结均值缓冲 ---- */
    if (DW->n_blast < P->n_freeze) {
        DW->blast[DW->n_blast++] = DW->b_est;
    } else {
        uint16_t i;
        for (i = 1u; i < P->n_freeze; i++) { DW->blast[i - 1u] = DW->blast[i]; }
        DW->blast[P->n_freeze - 1u] = DW->b_est;
    }
}

/* ========================================================================
 * 1 ms 主步
 * ===================================================================== */
void b0_ident_step(const b0_ident_P *P, b0_ident_DW *DW,
                   B0_REAL iq, B0_REAL u, B0_REAL omega,
                   B0_REAL e1, B0_REAL v,
                   B0_REAL *b0_out, B0_REAL *du_out)
{
    B0_REAL c, s, du;
    uint16_t idx;

    du = 0.0f;

    /* ---- A. 相位推进（连续，跨段不重置 => 两段同一绝对参考） ---- */
    DW->ph += P->dph_cyc;
    if (DW->ph >= 1.0f) { DW->ph -= 1.0f; }
    idx = (uint16_t)(DW->ph * (B0_REAL)B0_LUT_SIZE) & (uint16_t)(B0_LUT_SIZE - 1u);
    c = b0_cos_tab[idx];
    s = b0_sin_tab[idx];

    /* ---- B. b0 低通：每拍无条件执行 ---- */
    if (DW->goal_valid) {
        DW->b0 += P->lp_a * (DW->goal - DW->b0);
        if (b0_absf(DW->goal - DW->b0) <= 1.0e-4f * b0_absf(DW->goal)) {
            DW->b0 = DW->goal;
            DW->goal_valid = 0u;
        }
    }

    /* ---- C. 调度 ---- */
    DW->t_now += P->dT;
    if (!DW->active) {
        if (DW->frozen || (DW->t_now < DW->t_next)) {
            *b0_out = DW->b0; *du_out = 0.0f;
            return;
        }
        DW->active = 1u;
        DW->seg = 0u;
        DW->n_acc = 0u;
        b0_clear_acc(DW);
    }

    /* ---- D. 段内累积 ---- */
    DW->ac_e1 += e1 * c; DW->as_e1 += e1 * s;
    DW->ac_v  += v  * c; DW->as_v  += v  * s;
    DW->ac_u  += u  * c; DW->as_u  += u  * s;
    DW->ac_q  += iq * c; DW->as_q  += iq * s;
    DW->ac_w  += omega * c; DW->as_w += omega * s;   /* 仅诊断 */

    /* ---- E. 注入（仅注入段） ---- */
    if (DW->seg == 1u) {
        B0_REAL a = P->amp;
        if (a > P->amp_max) { a = P->amp_max; }
        du = a * b0_wave_value(P->wave, DW->ph, s);
    }

    /* ---- F. 段末 ---- */
    DW->n_acc++;
    if (DW->n_acc >= P->n_seg) {
        b0_seg_end(P, DW);
        b0_clear_acc(DW);
        DW->n_acc = 0u;
        if (DW->seg == 0u) {
            DW->seg = 1u;                       /* 进入注入段 */
        } else {                                /* burst 结束 */
            DW->active = 0u;
            DW->n_burst++;
            if (DW->n_burst >= P->n_ident) {    /* 辨识期结束：冻结 */
                uint16_t i;
                B0_REAL acc = 0.0f, n = (B0_REAL)DW->n_blast;
                if (n < 1.0f) { n = 1.0f; }
                for (i = 0u; i < DW->n_blast; i++) { acc += DW->blast[i]; }
                DW->b0 = acc / n;
                DW->goal = DW->b0;
                DW->goal_valid = 0u;
                DW->frozen = 1u;
                DW->t_next = DW->t_now + P->period_idle;
            } else {
                DW->t_next = DW->t_now + P->period_run;
            }
        }
    }

    *b0_out = DW->b0;
    *du_out = du;
}

/* end of file */
