function test_b0_m()
% test_b0_m —— b0_ident_m（MATLAB Function 版）的解析自洽测试
% 不依赖 Simulink、不依赖任何编译器，R2018b 可直接跑。
% 用法：  test_b0_m
% 判据：  解析用例相对误差 |err| < 0.05%；门限用例在停机段 b0 必须保持初值不变。
%
% 合成思路与 test_b0.c 相同：给定真实 b 与电流环复传函 T，构造
% iq = T*u、e1 = cos、V = b*q - b0*u - pd*e1，再逐拍喂给 b0_ident_m。

fprintf('\n=== b0_ident_m 解析自洽测试（24 个 burst，5 s 周期，冻结取末 4 次）===\n');
fprintf('%-22s %8s %10s %10s %s\n', '用例', 'b_true', 'b_est', '误差', '停机段 b0');

[be, bt, b0stop] = run_case(400, 1.00,   0,  0);
print_row('正弦 T=1.00<0deg', bt, be, b0stop);
ok = abs(100*(be/bt-1)) < 0.05;

[be, bt, b0stop] = run_case(400, 0.95,   5,  0);
print_row('正弦 T=0.95<+5deg', bt, be, b0stop);
ok = ok & (abs(100*(be/bt-1)) < 0.05);

[be, bt, b0stop] = run_case(400, 0.90, -10,  0);
print_row('正弦 T=0.90<-10deg', bt, be, b0stop);
ok = ok & (abs(100*(be/bt-1)) < 0.05);

% 运行使能：前 40 s 停机（omega=0，低于 omega_on=180），之后 600 rpm
[be, bt, b0stop] = run_case(400, 1.00,   0, 40);
print_row('正弦 T=1.00 前40s停机', bt, be, b0stop);
gated = abs(b0stop - 400) < 1e-9;      % 停机段必须一动不动
ok = ok & gated;

if ok
    fprintf('结论：全部通过（解析用例 |误差| < 0.05%%，停机段 b0 保持不变）\n\n');
else
    fprintf('结论：存在超差或门限未生效，检查反演式与调度\n\n');
end
end

function print_row(name, bt, be, b0stop)
fprintf('%-22s %8.1f %10.3f %9.3f%% %10.3f\n', name, bt, be, 100*(be/bt-1), b0stop);
end

function [b_est, b_true, b0_at_stop] = run_case(b_true, Tmag, Tdeg, stop_s)
dT = 1e-3; fh = 65; wh = 2*pi*fh;
A = 0.1;                       % 注入幅值（测试用，小于正式 0.118）
K = round((stop_s + 121)/dT);  % 停机段 + 121 s 运行（足够 24 个 burst）
wo = 500; b1 = 2*wo; b2 = wo*wo;
sdC = (exp(1i*wh*dT) - 1)/dT;
pdC = sdC + b1 + b2/sdC;
Tth = Tdeg*pi/180;
b0 = 400;                      % 与 b0_ident_m 内部初值一致
b0_at_stop = b0;
clear b0_ident_m;              % 清 persistent，保证每个用例独立
for k = 0:K-1
    tsec = k*dT;
    if tsec < stop_s
        om = 0;                % 停机：转速低于门限
    else
        om = 600;
    end
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
    [b0, ~] = b0_ident_m(iq, u, om, e1, v);
    if stop_s > 0 && tsec >= stop_s - dT && tsec < stop_s
        b0_at_stop = b0;                   % 停机段末尾读数
    end
end
b_est = b0;
end
