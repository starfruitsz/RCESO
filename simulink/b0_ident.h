/* ==========================================================================
 * b0_ident.h  --  两段式高频注入 b0 在线辨识（1 kHz，单精度，无动态内存）
 * 目标：F28335 / ERT / real32_T / no malloc
 * --------------------------------------------------------------------------
 * 算法：注入前段(off, 0.2 s) 与 注入段(on, 0.2 s) 各自做一次相干解调，
 *       用复幅值差分解出 b，再经"平台+软底"门控与 kp/N 低通平滑。
 * 端口：iq/u/omega/e1/v 进，b0/deltau 出。全部 1 ms。
 * ========================================================================== */
#ifndef B0_IDENT_H
#define B0_IDENT_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ---- 数据类型：上板为 single ------------------------------------------- */
#ifndef B0_REAL
typedef float B0_REAL;
#endif

/* ---- 编译期常数 -------------------------------------------------------- */
#define B0_LUT_BITS   8
#define B0_LUT_SIZE   (1u << B0_LUT_BITS)      /* 256 点 sin/cos 表 */
#define B0_MAX_FREEZE 8                        /* 冻结均值的最大样本数 */

/* ---- 注入波形 ---------------------------------------------------------- */
typedef enum {
    B0_WAVE_SINE   = 0,   /* 正弦，精度最好（仿真 -0.4%） */
    B0_WAVE_SQUARE = 1,   /* 方波，实现最省（仿真 +3%）   */
    B0_WAVE_TRI    = 2    /* 三角，折算 +1.4%             */
} b0_wave_e;

/* ---- 参数（初始化时写入，运行期只读） ---------------------------------- */
typedef struct {
    /* 时基 */
    B0_REAL dT;            /* 采样周期 [s]，1e-3 */
    B0_REAL wh;            /* 注入角频率 [rad/s] = 2*pi*fh，0.2 s 内须为整数周期 */
    B0_REAL dph_cyc;       /* 每拍相位增量 [cycle]，= wh*dT/(2*pi)，init 计算 */

    /* 注入 */
    B0_REAL amp;           /* 注入幅值 [pu]，建议 0.118 */
    B0_REAL amp_max;       /* 幅值上限 [pu]，0.25 */
    uint8_t  wave;         /* b0_wave_e */

    /* 观测器等效增益（离线常数） */
    B0_REAL b1;            /* beta1 = 2*wo*kappa1 */
    B0_REAL b2;            /* beta2 = wo^2*kappa2 */

    /* 离散算子 Sd = (e^{j*wh*dT}-1)/dT 及其组合 P(Sd)/Sd（init 计算） */
    B0_REAL sd_re, sd_im;
    B0_REAL pd_re, pd_im;  /* Sd + b1 + b2/Sd */

    /* b0 */
    B0_REAL b0_init;       /* 初值（控制器标称值，约 400） */
    B0_REAL b0_lo;         /* 硬下限，建议 0.5*b0_nom */
    B0_REAL b0_hi;         /* 硬上限，建议 2.0*b0_nom */
    B0_REAL b_den_eps;     /* 差分分母阈值（相对），1e-3 */
    uint8_t  tcorr_en;     /* 1 = 末端除以 T（仿真里必需，上板需实测确认） */

    /* 低通：tau = lp_div / kp，等价于带宽 kp/lp_div */
    B0_REAL kp;
    B0_REAL lp_div;        /* 50 */
    B0_REAL lp_a;          /* 1 - exp(-dT/tau)，init 计算 */

    /* 门控：平台 + 软底 */
    B0_REAL d1;            /* 平台半宽，0.10 */
    B0_REAL d2;            /* 陡降宽度，0.20 */
    B0_REAL dmax;          /* 软底拐点，0.50 */
    B0_REAL alpha_base;    /* 每次更新的基增益，0.30 */
    B0_REAL mu;            /* 基线指数滑动速率，0.35 */

    /* 调度 */
    uint16_t n_seg;        /* 每段拍数，200（0.2 s） */
    uint16_t n_warm;       /* 预热 burst 数，3（期间 alpha=1） */
    uint16_t n_ident;      /* 辨识 burst 总数，24（24*5 s = 120 s） */
    uint16_t n_freeze;     /* 冻结时取最近几个 burst 均值，4 */
    B0_REAL  period_run;   /* 辨识期 burst 周期 [s]，5.0 */
    B0_REAL  period_idle;  /* 冻结后周期 [s]，3600.0 */
} b0_ident_P;

/* ---- 状态（放在 DW 里，Simulink 自动生成 static） ---------------------- */
typedef struct {
    /* 相位累加 [0,1) */
    B0_REAL  ph;
    /* 相干解调累加器（5 路 × cos/sin） */
    B0_REAL  ac_e1, as_e1;
    B0_REAL  ac_v,  as_v;
    B0_REAL  ac_u,  as_u;
    B0_REAL  ac_q,  as_q;
    B0_REAL  ac_w,  as_w;

    /* 段机 */
    uint16_t n_acc;        /* 段内已累积拍数 */
    uint8_t  seg;          /* 0 = 注入前段(off)，1 = 注入段(on) */
    uint8_t  active;       /* 1 = burst 进行中 */
    uint32_t next_tick;    /* 下次 burst 起始的拍序号（整数，永不漂） */
    uint32_t tick;         /* 内部时基：已执行的拍数 */

    /* 前段锁存的复量 */
    B0_REAL  d0_re, d0_im;
    B0_REAL  u0_re, u0_im;
    B0_REAL  q0_re, q0_im;
    B0_REAL  t0_re, t0_im;

    /* 输出与平滑 */
    B0_REAL  b0;
    B0_REAL  goal;
    uint8_t  goal_valid;

    /* 门控 */
    B0_REAL  base;
    uint8_t  base_valid;
    uint16_t n_est;        /* 已产生估计的 burst 数 */

    /* 冻结 */
    B0_REAL  blast[B0_MAX_FREEZE];
    uint16_t n_blast;
    uint16_t n_burst;
    uint8_t  frozen;

    /* 诊断（可选输出） */
    B0_REAL  b_est;        /* 本次 burst 的原始估计 */
    B0_REAL  alpha_last;   /* 本次使用的 alpha */
} b0_ident_DW;

/* ---- 接口 -------------------------------------------------------------- */
void b0_ident_init(b0_ident_P *P, b0_ident_DW *DW);

/* 1 ms 调用一次。
 *   iq, u   : pu（±4.5）
 *   omega   : rpm
 *   e1      : pu（转速误差，观测器输出）
 *   v       : pu/s（重复内模状态，观测器输出）
 *   b0_out  : 辨识结果（初值=标称，收敛后=实测）
 *   du_out  : 注入增量，由外部叠加到控制量上
 */
void b0_ident_step(const b0_ident_P *P, b0_ident_DW *DW,
                   B0_REAL iq, B0_REAL u, B0_REAL omega,
                   B0_REAL e1, B0_REAL v,
                   B0_REAL *b0_out, B0_REAL *du_out);

#ifdef __cplusplus
}
#endif
#endif /* B0_IDENT_H */
