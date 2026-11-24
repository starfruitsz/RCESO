function first_bursts()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
Q = out.bq.signals.values(:); D = out.dD.signals.values(:);
U = out.dU.signals.values(:); G = out.dQ.signals.values(:);
B = out.blog.signals.values(:);
idx = find(Q > 0);
% 只取每次窗末（值变化的点）
chg = [true; diff(Q) ~= 0];
sel = idx(chg(idx));
fprintf('%-6s %8s %8s %8s %8s %8s\n', 'k', 'b0v', 'bq', 'num', 'dU', 'dQ');
for i = 1:min(10, numel(sel))
    k = sel(i);
    fprintf('%-6d %8.1f %8.1f %8.3f %8.4f %8.4f\n', i, B(k), Q(k), D(k), U(k), G(k));
end
end
