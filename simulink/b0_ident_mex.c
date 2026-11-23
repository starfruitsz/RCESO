/* b0_ident_mex.c —— 把 b0_ident_res 暴露成 MATLAB 函数，用于逐点对比 */
#include "mex.h"
#include "b0_ident_wrap.h"

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
    double iq, u, om, e1, v;
    b0_res_t r;
    if (nrhs != 5) { mexErrMsgIdAndTxt("b0:nrhs", "need 5 inputs"); }
    iq = mxGetScalar(prhs[0]);
    u  = mxGetScalar(prhs[1]);
    om = mxGetScalar(prhs[2]);
    e1 = mxGetScalar(prhs[3]);
    v  = mxGetScalar(prhs[4]);
    r = b0_ident_res((float)iq, (float)u, (float)om, (float)e1, (float)v);
    plhs[0] = mxCreateDoubleScalar((double)r.b0);
    if (nlhs > 1) { plhs[1] = mxCreateDoubleScalar((double)r.du); }
}
