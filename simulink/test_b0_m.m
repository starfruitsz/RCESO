function test_b0_m()
% test_b0_m —— b0_ident_m（MATLAB Function 版）的解析自洽测试
% 不依赖 Simulink、不依赖任何编译器，R2018b 可直接跑。
% 用法：  test_b0_m
% 判据： 每个用例的相对误差 |err| < 0.05% 视为通过。
%
% 合成思路与 test_b0.c 相同：给定真实 b 与电流环复传函 T，构造
% iq = T*u、e1 = cos、V = b*q - b0*u - pd*e1，再逐拍喂给 b0_ident_m。
% 只要反演式与调度正确，估计必然回到 b_true。

cases = {
    '正弦 T=1.00<0deg ', 1.00,  0;
    '正弦 T=0.95<+5deg', 0.95,  5;
    '正弦 T=0.90<-10deg', 0.90, -10;
};

fprintf('\n=== b0_ident_m 解析自洽测试（24 个 burst，5 s 周期，冻结取末 4 次）===\n');
fprintf('%-20s %8s %10s %10s\n', '用例', 'b_true', 'b_est', '误差');
ok = true;
for i = 1:size(cases,1)
    [be, bt] = run_case(400, cases{i,2}, cases{i,3});
    err = 100*(be/bt - 1);
    fprintf('%-20s %8.1f %10.3f %9.3f%%\n', cases{i,1}, bt, be, err);
    if abs(err) > 0.05, ok = false; end
end
if ok
    fprintf('结论：全部通过（|误差| < 0.05%%）\n\n');
else
    fprintf('结论：存在超差用例，检查反演式与调度\n\n');
end
end

function [b_est, b_true] = run_case(b_true, Tmag, Tdeg)
dT = 1e-3; fh = 65; wh = 2*pi*fh;
A = 0.1;                       % 注入幅值（测试用，小于正式 0.118）
K = 115600;                    % 拍数：覆盖 24 个 burst（115.4 s）并跑到冻结
wo = 500; b1 = 2*wo; b2 = wo*wo;
sdC = (exp(1i*wh*dT) - 1)/dT;
pdC = sdC + b1 + b2/sdC;
Tth = Tdeg*pi/180;
b0 = 400;                      % 与 b0_ident_m 内部初值一致
clear b0_ident_m;              % 清 persistent，保证每个用例独立
for k = 0:K-1
    tick = k + 1;                          % b0_ident_m 每调一次 tick+1
    wk = mod(tick - 1, 5000);              % 5 s 周期（起点计）
    on = (wk >= 200) && (wk < 400);        % 前 0.2 s 空载、后 0.2 s 注入
    ph = mod(wh*k*dT, 2*pi);
    c = cos(ph); s = sin(ph);
    if on, Ure = A; else, Ure = 0; end
    Qre = Tmag*cos(Tth)*Ure;
    Qim = Tmag*sin(Tth)*Ure;
    iq = Qre*c - Qim*s;
    u  = Ure*c;
    e1 = c;                                % E1 = 1+0i
    Dr = b_true*Qre - b0*Ure;
    Di = b_true*Qim;
    Vre = Dr - real(pdC);
    Vim = Di - imag(pdC);
    v = Vre*c - Vim*s;
    [b0, ~] = b0_ident_m(iq, u, 600, e1, v);
end
b_est = b0;
end
