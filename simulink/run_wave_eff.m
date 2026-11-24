function run_wave_eff()
% run_wave_eff —— 三种注入波形对【电流】与【转速】的影响（ADRC 闭环，MATLAB Function 版）
% 用法： run_wave_eff
% 产物： wave_eff.mat（每种波形的稳态 burst 片段 + 指标）
srcDir = fileparts(mfilename('fullpath'));
if isempty(srcDir), srcDir = pwd; end
cd(srcDir);
fid0 = fopen('b0_ident_m.m', 'r'); orig = fread(fid0, inf, 'char=>char').'; fclose(fid0);
names = {'正弦', '方波', '三角'};
res = [];
w0 = 100.0; w1 = 100.7;          % 取稳态 burst 片段（含 off/on 段）
for wi = 0:2
    txt = regexprep(orig, 'wave\s*=\s*0;', sprintf('wave   = %d;', wi));
    fid = fopen('b0_ident_m.m', 'w'); fwrite(fid, txt); fclose(fid);
    fprintf('--- 跑 %s (wave=%d) ---\n', names{wi+1}, wi);
    build_foc_m;                            % 建模型 + 跑 130 s，写 foc_m_log.mat
    L = load('foc_m_log.mat');
    t = L.w_log.Time(:);
    wv = L.w_log.Data(:);
    dv = L.du_log.Data(:);
    qv = L.iq_log.Data(:);
    sel = (t >= w0) & (t <= w1);
    tt = t(sel); ww = wv(sel); dd = dv(sel); qq = qv(sel);
    % 定指标：取 on 段 200 拍（65 Hz 的 13 个整周期）
    on = (tt >= 100.2) & (tt < 100.4);
    ph = exp(-1j*2*pi*65.0*tt(on));
    PH = @(x) 2/numel(ph)*sum(x.*ph);
    ph3 = exp(-1j*2*pi*195.0*tt(on));
    PH3 = @(x) 2/numel(ph3)*sum(x.*ph3);
    r = struct();
    r.name = names{wi+1};
    r.t = tt; r.w = ww; r.du = dd; r.iq = qq;
    r.du_f1   = abs(PH(dd(on)));          % 注入基波 (pu)
    r.iq_f1   = abs(PH(qq(on)));          % 电流基波 (A)
    r.iq_f3   = abs(PH3(qq(on)));         % 电流三次谐波 (A)
    r.w_f1    = abs(PH(ww(on)));          % 转速基波 (rpm)
    r.w_pp    = max(ww(on)) - min(ww(on));% 转速峰峰 (rpm)
    r.iq_pk   = max(abs(qq(on)));         % 电流峰值 (A)
    res = [res, r];
    fprintf('    du1=%.4f pu  iq1=%.3f A  iq3=%.3f A  w1=%.1f rpm  w_pp=%.1f rpm  iq_pk=%.2f A\n', ...
            r.du_f1, r.iq_f1, r.iq_f3, r.w_f1, r.w_pp, r.iq_pk);
end
fid = fopen('b0_ident_m.m', 'w'); fwrite(fid, orig); fclose(fid);
save('wave_eff.mat', 'res');
fprintf('\n%-6s %9s %9s %9s %9s %9s\n', '波形', 'du1/pu', 'iq1/A', 'iq3/A', 'w_pp/rpm', 'iq_pk/A');
for k = 1:numel(res)
    fprintf('%-6s %9.4f %9.3f %9.3f %9.1f %9.2f\n', res(k).name, res(k).du_f1, res(k).iq_f1, ...
            res(k).iq_f3, res(k).w_pp, res(k).iq_pk);
end
end
