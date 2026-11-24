function run_wave_cmp()
% run_wave_cmp —— 正弦 / 方波 / 三角 注入波形对比（ADRC 闭环，MATLAB Function 版）
% 用法： run_wave_cmp
% 产物： wave_cmp.mat（三条 b0 轨迹与指标） + 控制台汇总表
% 注意： build_foc_m 是脚本，会把 b/w/d/out 等变量写进本函数工作区，
%        因此循环变量与中间量一律用不冲突的名字（wi / tt / bb）。
srcDir = fileparts(mfilename('fullpath'));
if isempty(srcDir), srcDir = pwd; end
cd(srcDir);
fid0 = fopen('b0_ident_m.m', 'r'); orig = fread(fid0, inf, 'char=>char').'; fclose(fid0);
names = {'正弦', '方波', '三角'};
bTrue = 536.40;
res = [];
for wi = 0:2
    txt = regexprep(orig, 'wave\s*=\s*0;', sprintf('wave   = %d;', wi));
    fid = fopen('b0_ident_m.m', 'w'); fwrite(fid, txt); fclose(fid);
    fprintf('--- 跑 %s 波 (wave=%d) ---\n', names{wi+1}, wi);
    build_foc_m;                        % 建模型 + 跑 130 s，并写 foc_m_log.mat
    L = load('foc_m_log.mat');
    tt = L.b0_log.Time(:); bb = L.b0_log.Data(:);
    rel = abs(bb - bTrue)/bTrue;
    t3 = NaN;
    idx3 = find(rel <= 0.03, 1, 'first');
    if ~isempty(idx3) && max(rel(idx3:end)) <= 0.05, t3 = tt(idx3); end
    t1 = NaN;
    idx1 = find(rel <= 0.01, 1, 'first');
    if ~isempty(idx1) && max(rel(idx1:end)) <= 0.02, t1 = tt(idx1); end
    r = struct();
    r.name = names{wi+1}; r.t = tt; r.b0 = bb; r.final = bb(end);
    r.err = 100*(bb(end)/bTrue - 1); r.t3 = t3; r.t1 = t1;
    res = [res, r];
    fprintf('    终值 %.3f  误差 %+.3f%%  3%%收敛 %s  1%%收敛 %s\n', ...
            bb(end), r.err, num2str(t3), num2str(t1));
end
fid = fopen('b0_ident_m.m', 'w'); fwrite(fid, orig); fclose(fid);   % 还原为 sine
save('wave_cmp.mat', 'res');
fprintf('\n%-6s %10s %9s %10s %10s\n', '波形', 'b0终值', '误差%', 't(3%)/s', 't(1%)/s');
for k = 1:numel(res)
    fprintf('%-6s %10.3f %9.3f %10s %10s\n', res(k).name, res(k).final, res(k).err, ...
            num2str(res(k).t3), num2str(res(k).t1));
end
end
