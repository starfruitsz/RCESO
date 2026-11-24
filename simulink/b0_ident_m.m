function [b0out, duout, bqout] = b0_ident_m(iq, u, ge1, e1, v)
%#codegen
% 两段式高频注入 b0 在线辨识 —— MATLAB 版（配合 MATLAB Function 块，无需 C 编译器）
% 与 b0_ident.c 逐行等价：R2018b 及以后版本均可用
% ==================== 顶层可调参数（移植时只改这里）====================
dT     = 1e-3;      % 采样周期 [s]
f_inj  = 65;        % 注入频率 [Hz]：须为 5 Hz 整数倍，且约等于 6.5 x 机械频率
amp    = 0.118;     % 注入幅值 [pu]，上限 0.25
wave   = 0;         % 注入波形：0=正弦 1=方波 2=三角（三者峰值均为 1）
b0_init= 536.4;     % b0 初值：必须与控制器/ESO 用的标称一致
b0lo   = 1.0;       % 硬下限（诊断期临时放开）
b0hi   = 5000;      % 硬上限
wo     = 500;       % 观测器带宽 [rad/s]，必须与 ESO 一致
kp     = 75.36;     % 转速环比例增益
% ---- 反演用的增益由外部输入 ge1 提供（G(e1) 在块外计算）----
% 第 3 个入参 ge1 即 G(e1)：线性 ESO 时 ge1 = e1；类 fal 时由外部 G 块给出。
% ---- 识别使能：0 = 只注入不更新 b0（关闭识别，用于对照）----
upd_on  = 1;
% ---- 起跑延时 [s]：等闭环进入稳态后再开始注入（避开启动饱和）----
t_start = 8.0;
% ---- 运行使能：转速门限已移除（omega 不再作为入参，门限请在块外用使能信号实现）----
% ==================== 派生量（不要手改）====================
cyc    = f_inj*dT;          % 每拍相位增量 [周期]
wh     = 2*pi*f_inj;        % 注入角频率 [rad/s]
nseg   = round(0.2/dT);     % 段长 0.2 s 对应的拍数
% ---- 辨识调度 ----
warm   = 3;         % 预热 burst 数：前几次估计直接采用
nident = 24;        % 辨识 burst 总数：24 x 5 s = 120 s
nfrz   = 12;        % 冻结时取最近 12 次（60 s）均值：末 12 个覆盖 60–120 s
% ---- 门控：平台 + 陡降 + 软底 ----
d1     = 0.10;      % 平台半宽（偏离 <=10% 不衰减）
d2     = 0.20;      % 陡降宽度
dmax   = 0.50;      % 软底拐点（超过后权重不再下降）
abase  = 0.30;      % 基增益 alpha
mu     = 0.35;      % 基线滑动速率
% 一致性检查：cyc*nseg 必须是整数，否则段内不相干。
% 注意：MATLAB Function 块里不能放顶层 error() 断言——会让块的输出维度推断失败
% （"无法沿循环求取信号维度"），此检查只保留在 C 版与移植文档里。
cyc_nseg = cyc*nseg;   % 移植时人工确认该值为整数（65 Hz x 0.2 s = 13）
persistent init ph acc nacc seg active tick nxtick tstart d0 u0 q0 t0
persistent b0v goal gv base bvalid nest blast nblast nburst frozen
persistent pdC sdC lpa b1 b2 bc bqlast
if isempty(init)
    init = 1; ph = 0;
    acc = zeros(1,14); nacc = 0; seg = 0; active = 0;   % 11-14: SDFT(G1(e1)), SDFT(G2(e1))
    tick = 0; nxtick = round(t_start/dT); tstart = 0;   % 起跑延时后再注入
    d0 = 0; u0 = 0; q0 = 0; t0 = 1;
    b0v = b0_init; goal = b0_init; gv = 0; bqlast = 0;
    base = 0; bvalid = 0; nest = 0;
    blast = zeros(1,12); nblast = 0; nburst = 0; frozen = 0;
    % ---- 派生常量（只算一次）----
    b1 = 2*wo;                       % beta1 = 2*wo*kappa1，delta=1 时 kappa1=1
    b2 = wo*wo;                      % beta2 = wo^2*kappa2，delta=1 时 kappa2=1
    sdC = (exp(1i*wh*dT) - 1) / dT;
    pdC = sdC + b1 + b2/sdC;
    bc  = b2/sdC;                    % beta2/Sd（精确反演用，只算一次）
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
tick = tick + 1;                        % 整数拍计数：不漂
du = 0;
if (~active) && (~frozen) && (tick >= nxtick)
    active = 1; seg = 0; nacc = 0; acc(:) = 0;
    tstart = tick;                      % 周期按 burst 起点计
end
if active
    acc(1) = acc(1) + e1*c;  acc(2) = acc(2) + e1*s;
    acc(3) = acc(3) + v*c;   acc(4) = acc(4) + v*s;
    acc(5) = acc(5) + u*c;   acc(6) = acc(6) + u*s;
    acc(7) = acc(7) + iq*c;  acc(8) = acc(8) + iq*s;
    % G(e1) 由外部输入 ge1 提供（不在块内推导）
    acc(11)= acc(11)+ ge1*c;  acc(12)= acc(12)+ ge1*s;
    acc(13)= acc(13)+ ge1*c;  acc(14)= acc(14)+ ge1*s;
    if seg == 1
        % 波形（峰值=1，与 C 版 b0_wave_value 一致）
        if wave == 1
            if s >= 0, wv = 1; else, wv = -1; end
        elseif wave == 2
            a4 = ph*4;
            if a4 < 1,        wv = a4;
            elseif a4 < 3,    wv = 2 - a4;
            else,             wv = a4 - 4;
            end
        else
            wv = s;
        end
        du = amp*wv;
    end
    nacc = nacc + 1;
    if nacc >= nseg
        k = 2/nacc;
        E1 = k*(acc(1) - 1i*acc(2));
        Vc = k*(acc(3) - 1i*acc(4));
        Uc = k*(acc(5) - 1i*acc(6));
        Qc = k*(acc(7) - 1i*acc(8));
        % 代数恒等式（只依赖观测器方程，不含任何线性化）：
        %   d^ = V + Sd*E1 + beta1*SDFT(G1(e1)) + (beta2/Sd)*SDFT(G2(e1))
        % 线性观测器时 G1=G2=e1，自动退化为 V + (Sd+beta1+beta2/Sd)*E1
        G1c = k*(acc(11) - 1i*acc(12));
        G2c = k*(acc(13) - 1i*acc(14));
        D  = Vc + sdC*E1 + b1*G1c + bc*G2c;
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
                bqlast = bq;                       % 诊断输出：本窗原始估计
                if upd_on == 0
                    % 识别关闭：只算 bq，不更新 b0（b0 停在 b0_init）
                elseif ~bvalid
                    base = bq; bvalid = 1; goal = bq; gv = 1; nest = 1;   % 经低通
                elseif nest < warm
                    base = bq; goal = bq; gv = 1; nest = nest + 1;        % 经低通
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
                if upd_on == 0
                    % 识别关闭：不记录、不冻结
                elseif nblast < nfrz
                    nblast = nblast + 1; blast(nblast) = bq;
                else
                    blast(1:nfrz-1) = blast(2:nfrz); blast(nfrz) = bq;
                end
            end
            active = 0;
            nburst = nburst + 1;
            if (upd_on ~= 0) && (nburst >= nident)
                b0v = mean(blast(1:max(nblast,1)));
                goal = b0v; gv = 0; frozen = 1; nxtick = tick + round(3600/dT);
            else
                nxtick = tstart + round(5/dT);        % 5 s 起点周期
            end
            seg = 0;
        end
        acc(:) = 0; nacc = 0;
    end
end
b0out = b0v;
duout = du;
bqout = bqlast;
end
