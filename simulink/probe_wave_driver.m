% probe_wave_driver.m —— 只验证 driver 的指标/结构体逻辑，不建模型
S = load('foc_m_log.mat');
t = S.b0_log.Time; b = S.b0_log.Data;
bTrue = 536.40; rel = abs(b - bTrue)/bTrue;
idx3 = find(rel <= 0.03, 1, 'first'); t3 = NaN;
if ~isempty(idx3) && max(rel(idx3:end)) <= 0.05, t3 = t(idx3); end
idx1 = find(rel <= 0.01, 1, 'first'); t1 = NaN;
if ~isempty(idx1) && max(rel(idx1:end)) <= 0.02, t1 = t(idx1); end
r = struct(); r.name = '正弦'; r.tt = t(:); r.bb = b(:); r.final = b(end);
r.err = 100*(b(end)/bTrue - 1); r.t3 = t3; r.t1 = t1;
res = []; res = [res, r];
save('probe_res.mat', 'res');
fprintf('OK final=%.3f err=%+.3f t3=%s t1=%s\n', r.final, r.err, num2str(t3), num2str(t1));
% 再验证跨脚本变量冲突：定义 w 为 timeseries 后，用 wi 循环仍可
w = S.b0_log;
for wi = 0:2
    nm = {'正弦','方波','三角'};
    fprintf('  wi=%d -> %s\n', wi, nm{wi+1});
end
