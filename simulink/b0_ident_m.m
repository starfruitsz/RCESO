function [b0out, duout] = b0_ident_m(iq, u, omega, e1, v)
%#codegen
% 两段式高频注入 b0 在线辨识 —— MATLAB 版（配合 MATLAB Function 块，无需 C 编译器）
% 与 b0_ident.c 逐行等价：R2018b 及以后版本均可用
% ==================== 顶层可调参数（移植时只改这里）====================
dT     = 1e-3;      % 采样周期 [s]
f_inj  = 65;        % 注入频率 [Hz]：须为 5 Hz 整数倍，且约等于 6.5 x 机械频率
amp    = 0.118;     % 注入幅值 [pu]，上限 0.25
b0_init= 400;       % b0 初值，填控制器的标称值
b0lo   = 200;       % 硬下限（防发散）
b0hi   = 800;       % 硬上限
wo     = 500;       % 观测器带宽 [rad/s]，必须与 ESO 一致
kp     = 75.36;     % 转速环比例增益
% ==================== 派生量（不要手改）====================
cyc    = f_inj*dT;          % 每拍相位增量 [周期]
wh     = 2*pi*f_inj;        % 注入角频率 [rad/s]
nseg   = round(0.2/dT);     % 段长 0.2 s 对应的拍数
% ---- 辨识调度 ----
warm   = 3;         % 预热 burst 数：前几次估计直接采用
nident = 24;        % 辨识 burst 总数：24 x 5 s = 120 s
nfrz   = 4;         % 冻结时取最近 4 次（20 s）均值
% ---- 门控：平台 + 陡降 + 软底 ----
d1     = 0.10;      % 平台半宽（偏离 <=10% 不衰减）
d2     = 0.20;      % 陡降宽度
dmax   = 0.50;      % 软底拐点（超过后权重不再下降）
abase  = 0.30;      % 基增益 alpha
mu     = 0.35;      % 基线滑动速率
% 一致性检查：cyc*nseg 必须是整数，否则段内不相干
if abs(cyc*nseg - round(cyc*nseg)) > 1e-6
    % 该断言在仿真里会显式报错，避免静默失效
    error('注入频率 %g Hz 与段长 0.2 s 不相干（cyc*nseg 非整数）', f_inj);
end
persistent init ph acc nacc seg active tn xtnext d0 u0 q0 t0
persistent b0v goal gv base bvalid nest blast nblast nburst frozen
persistent pdC sdC lpa
if isempty(init)
    init = 1; ph = 0;
    acc = zeros(1,10); nacc = 0; seg = 0; active = 0;
    tn = 0; xtnext = 1e-3;
    d0 = 0; u0 = 0; q0 = 0; t0 = 1;
    b0v = b0_init; goal = b0_init; gv = 0;
    base = 0; bvalid = 0; nest = 0;
    blast = zeros(1,4); nblast = 0; nburst = 0; frozen = 0;
    % ---- 派生常量（只算一次）----
    b1 = 2*wo;                       % beta1 = 2*wo*kappa1，delta=1 时 kappa1=1
    b2 = wo*wo;                      % beta2 = wo^2*kappa2，delta=1 时 kappa2=1
    sdC = (exp(1i*wh*dT) - 1) / dT;
    pdC = sdC + b1 + b2/sdC;
    tau = 50/kp;                     % b0 低通时间常数 = 50/kp = 0.663 s（与 C 版一致）
    lpa = 1 - exp(-dT/tau);          % 低通系数，每拍执行一次
end
% （参数已移至函数开头，见上方“顶层可调参数”）
% ---- 相位推进 ----
ph = ph + cyc;
if ph >= 1, ph = ph - 1; end
c = cos(2*pi*ph); s = sin(2*pi*ph);
% ---- b0 低通（每拍） ----
if gv ~= 0
    b0v = b0v + lpa*(goal - b0v);
    if abs(goal - b0v) <= 1e-4*abs(goal)
        b0v = goal; gv = 0;
    end
end
% ---- 调度 ----
tn = tn + dT;
du = 0;
if (~active) && (~frozen) && (tn >= xtnext)
    active = 1; seg = 0; nacc = 0; acc(:) = 0;
end
if active
    acc(1) = acc(1) + e1*c;  acc(2) = acc(2) + e1*s;
    acc(3) = acc(3) + v*c;   acc(4) = acc(4) + v*s;
    acc(5) = acc(5) + u*c;   acc(6) = acc(6) + u*s;
    acc(7) = acc(7) + iq*c;  acc(8) = acc(8) + iq*s;
    acc(9) = acc(9) + omega*c; acc(10)= acc(10)+ omega*s;
    if seg == 1
        du = amp*s;
    end
    nacc = nacc + 1;
    if nacc >= nseg
        k = 2/nacc;
        E1 = k*(acc(1) - 1i*acc(2));
        Vc = k*(acc(3) - 1i*acc(4));
        Uc = k*(acc(5) - 1i*acc(6));
        Qc = k*(acc(7) - 1i*acc(8));
        D  = Vc + pdC*E1;
        if abs(Uc) > 1e-9, T = Qc/Uc; else, T = 1; end
        if seg == 0
            d0 = D; u0 = Uc; q0 = Qc; t0 = T;
            seg = 1;
        else
            num = (D - d0) + b0v*(Uc - u0);
            den = Qc - q0;
            if abs(den) > 1e-9
                bq = abs(num/den);              % 取模长：对相位误差免疫
                bq = min(max(bq, b0lo), b0hi);
                if ~bvalid
                    base = bq; bvalid = 1; b0v = bq; goal = bq; gv = 0; nest = 1;
                elseif nest < warm
                    base = bq; b0v = bq; goal = bq; gv = 0; nest = nest + 1;
                else
                    dd = abs(bq - base)/max(abs(base),1e-9);
                    if dd <= d1
                        w = 1;
                    elseif dd <= dmax
                        w = exp(-(dd - d1)/max(d2,1e-9));
                    else
                        w = exp(-(dmax - d1)/max(d2,1e-9));
                    end
                    goal = b0v + abase*w*(bq - b0v); gv = 1;
                    base = base + mu*(bq - base);
                    nest = nest + 1;
                end
                if nblast < nfrz
                    nblast = nblast + 1; blast(nblast) = bq;
                else
                    blast(1:nfrz-1) = blast(2:nfrz); blast(nfrz) = bq;
                end
            end
            active = 0;
            nburst = nburst + 1;
            if nburst >= nident
                b0v = mean(blast(1:max(nblast,1)));
                goal = b0v; gv = 0; frozen = 1; xtnext = tn + 3600;
            else
                xtnext = tn + 5;
            end
            seg = 0;
        end
        acc(:) = 0; nacc = 0;
    end
end
b0out = b0v;
duout = du;
end