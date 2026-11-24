function first_bursts2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
Q = out.bqlog.signals.values(:); D = out.dD.signals.values(:);
U = out.dU.signals.values(:); G = out.dQ.signals.values(:);
B = out.blog.signals.values(:);
idx = find(Q > 0);
chg = [true; diff(Q) ~= 0];
sel = idx(chg(idx));
fprintf('%-4s %8s %8s %8s %8s %8s\n', 'k', 'b0v', 'bq', 'num', 'dU', 'dQ');
for i = 1:min(10, numel(sel))
    k = sel(i);
    fprintf('%-4d %8.1f %8.1f %8.3f %8.4f %8.4f\n', i, B(k), Q(k), D(k), U(k), G(k));
end
end
