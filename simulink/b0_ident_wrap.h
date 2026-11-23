/* b0_ident_wrap.h —— Simulink C Caller 入口（单向量端口，最省接线） */
#ifndef B0_IDENT_WRAP_H
#define B0_IDENT_WRAP_H
#include "b0_ident.h"

/* in[0]=iq  in[1]=u  in[2]=omega  in[3]=e1  in[4]=v  （全部 single, 1 ms） */
/* out[0]=b0 out[1]=deltau                                                  */
/* 注意：此处刻意使用原生 float（不用 B0_REAL typedef），
 * 否则 Simulink C Caller 的解析器无法识别函数原型，端口数为 0。 */
void b0_ident_u(const float in[5], float out[2]);

/* 标量版本：给 Simulink C Caller 用，端口映射无歧义（5 进 2 出） */
void b0_ident_sim(float iq, float u, float omega, float e1, float v,
                  float *b0, float *du);

/* 结构体返回版本：彻底避开指针 inout 语义，C Caller 得到 5 进 1 出（总线） */
typedef struct {
    float b0;
    float du;
} b0_res_t;

b0_res_t b0_ident_res(float iq, float u, float omega, float e1, float v);

/* 模型 InitFcn 里调用一次（或放在 Initialize Function 中） */
void b0_ident_setup(void);

#endif
