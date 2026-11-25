function [b0out, duout, dbg] = b0_ident_dbg(iq, u, ge1, e1, v, w, wref)
%#codegen
% 两段式高频注入 b0 在线辨识 —— MATLAB 版（配合 MATLAB Function 块，无需 C 编译器）
% 与 b0_ident.c 逐行等价：R2018b 及以后版本均可用
% ==================== 顶层可调参数（移植时只改这里）====================
dT     = 1e-3;      % 采样周期 [s]
f_inj  = 65;        % 注入频率 [Hz]：须为 5 Hz 整数倍，且约等于 6.5 x 机械频率
amp    = 0.05;      % 注入幅值 [pu]（0.05 时 burst 冲击小；上限 0.25）
wave   = 0;         % 注入波形：0=正弦 1=方波 2=三角（三者峰值均为 1）
b0_init= 536.4;     % b0 初值：必须与控制器/ESO 用的标称一致
b0lo   = 300;       % 硬下限（约 0.56×标称）
b0hi   = 900;       % 硬上限（约 1.7×标称）
wo     = 500;       % 观测器带宽 [rad/s]，必须与 ESO 一致
kp     = 75.36;     % 转速环比例增益
% ---- 反演用的增益由外部输入 ge1 提供（G(e1) 在块外计算）----
% 第 3 个入参 ge1 即 G(e1)：线性 ESO 时 ge1 = e1；类 fal 时由外部 G 块给出。
% ---- 识别使能：0 = 只注入不更新 b0（关闭识别，用于对照）----
upd_on  = 1;
% ---- 起跑延时 [s]：等闭环进入稳态后再开始注入（避开启动饱和）----
t_start = 8.0;
% ---- 运行使能（转速门限）：w = 实测转速, wref = 参考转速（两者单位必须一致，如都用 rad/s）----
% w_gate = 0    关闭门限
% w_gate = 0.3  转速低于 0.3*wref 时不启动 burst（本轮跳过、不消耗 24 次预算）
w_gate = 0;
% ---- 稳态判据：|w - w_lp| < w_ss*|wref| 且连续保持 w_hold 秒（0 = 关闭）----
% w_lp 是 w 的一阶低通（tau = 0.2 s），用于滤掉注入/故障造成的抖动。
% 必须"连续"满足：故障扰动（如 10 Hz）每个过零瞬间都会短暂满足判据，
% 只判瞬时会让 burst 在过零点偷偷启动（实测 b0 仍会爬），故加保持时间。
w_ss   = 0.02;      % 2% 参考转速
tau_w  = 0.2;       % 转速低通时间常数 [s]
w_hold = 0.1;       % 需连续保持 [s]
% 说明：不再设“首窗守卫”。严重失配（如 b0_init 与真值差 1 倍以上）时，
% 任何基于 b0_init 的首窗限幅都会把正确的估计挡掉，使辨识永久失效。
% 现只保留相对判据 ①（|Δĩ| > 0.25*amp），它不依赖 b0 的标称值。
% ---- 类型统一（重要）：目标机若把输入定成 fi（定点），与 double 混合运算/比较会报
%      "In fi .* non-fi ... the non-fi must be a constant"。
%      例：ge1*s（ge1 是 fi、s 是 double）、|w-wlp| < w_ss*|wref|。
%      入口一次性全转 double，块内从此只有 double。----
iqd  = double(iq);
ud   = double(u);
ge1d = double(ge1);
e1d  = double(e1);
vd   = double(v);
wd   = double(w);
wrd  = double(wref);
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
persistent b0v goal gv base bvalid nest blast nblast nburst frozen wlp wcnt
persistent dg_en dg_num dg_den dg_bq      % 诊断量（供 b0_ident_dbg 输出，主接口不用）
persistent pdC sdC lpa b1 b2 bc
if isempty(init)
    init = 1; ph = 0;
    acc = zeros(1,14); nacc = 0; seg = 0; active = 0;   % 11-14: SDFT(G1(e1)), SDFT(G2(e1))
    tick = 0; nxtick = round(t_start/dT); tstart = 0;   % 起跑延时后再注入
    d0 = 0; u0 = 0; q0 = 0; t0 = 1;
    b0v = b0_init; goal = b0_init; gv = 0; wlp = wd; wcnt = 0;
    dg_en = 0; dg_num = 0; dg_den = 0; dg_bq = 0;
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
% ---- 转速低通 + 稳态计时（每拍无条件更新，burst 起点才不会被人为推后）----
wlp = wlp + (wd - wlp)*min(dT/max(tau_w, dT), 1);
% 相对转速脉动：r_ss = |w-w_lp| / max(|w|,eps)，与常量 w_ss 比。
% 用 |w| 作分母（而不是 |wref|）：这样 w 与 wref 单位不一致时判据依然成立。
if abs(wd) > 1e-6
    r_ss = abs(wd - wlp)/abs(wd);
else
    r_ss = 1;                       % 接近零速视为"不稳态"，不注入
end
if (w_ss > 0) && (r_ss < w_ss)
    wcnt = wcnt + 1;
else
    wcnt = 0;
end
% ---- 调度 ----
tick = tick + 1;                        % 整数拍计数：不漂
du = 0;
% upd_on = 0：既不辨识也不注入（整段关闭）
if (upd_on ~= 0) && (~active) && (~frozen) && (tick >= nxtick)
    % ① 启动判据：转速够高（同样用归一化比值，与常量比）
    if abs(wrd) > 1e-6
        r_w = abs(wd)/abs(wrd);
    else
        r_w = 1;
    end
    ok_w = (w_gate <= 0) || (abs(wrd) < 1e-6) || (r_w >= w_gate);
    % ② 稳态判据：偏差已在上面连续保持 w_hold 秒
    ok_ss = (w_ss <= 0) || (wcnt >= round(w_hold/dT));
    if ok_w && ok_ss
        active = 1; seg = 0; nacc = 0; acc(:) = 0;
        tstart = tick;                  % 周期按 burst 起点计
    end
    % 不满足：本轮跳过，不消耗预算，下一拍再判
end
if active
    acc(1) = acc(1) + e1d*c;  acc(2) = acc(2) + e1d*s;
    acc(3) = acc(3) + vd*c;   acc(4) = acc(4) + vd*s;
    acc(5) = acc(5) + ud*c;   acc(6) = acc(6) + ud*s;
    acc(7) = acc(7) + iqd*c;  acc(8) = acc(8) + iqd*s;
    % G(e1) 由外部输入 ge1 提供（不在块内推导）
    acc(11)= acc(11)+ ge1d*c;  acc(12)= acc(12)+ ge1d*s;
    acc(13)= acc(13)+ ge1d*c;  acc(14)= acc(14)+ ge1d*s;
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
            % 判据①：电流必须真的跟上了注入（Δĩ ≈ amp），否则本窗作废。
            % 用相对判据（1e-9 那种绝对阈值等于没门槛，会把噪声放大成 b0max）
            if abs(den) > 0.25*amp
                bq = abs(num/den);              % 取模长：对相位误差免疫
                bq = min(max(bq, b0lo), b0hi);
            else
                bq = 0;                         % 0 = 本窗无效，下面跳过所有更新
            end
            dg_en  = abs(E1);  dg_num = abs(num);  dg_den = abs(den);  dg_bq = bq;
            if bq > 0
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
                % 冻结：末 nfrz 个 burst 的均值
                % 注意：这里不能用 blast(1:max(nblast,1))——ERT 代码生成会把动态上界
                % 当成变长切片而报错（"Variable-size arrays are currently disabled"）。
                % 改成定长数组 + 动态循环上界，代码生成器可接受。
                nf = nblast;
                if nf < 1, nf = 1; end
                bs = 0;
                for i = 1:nf
                    bs = bs + blast(i);
                end
                b0v = bs / nf;
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
dbg = [double(upd_on ~= 0), double(frozen), double(active), double(tick), double(nxtick), double(wcnt), r_ss, wd, double(du)/amp, dg_en, dg_num, dg_den, dg_bq];
end
