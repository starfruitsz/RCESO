function probe_bq()
% probe_bq —— 用 Python 导出的 1 ms 输入流回放 b0_ident_m_probe，记录每个 burst 的 bq
% 与 _bq_dump.mat 里的 bpv 逐窗对照（同一段输入、同一套调度）
here = fileparts(mfilename('fullpath'));
f1 = fullfile(here, '_bq_dump.mat'); f2 = fullfile(fileparts(here), '_bq_dump.mat');
if exist(f1, 'file'), fsrc = f1; else, fsrc = f2; end
S = load(fsrc);
fprintf('读取 %s\n', fsrc);
t = S.t(:); iq = S.iq(:); u = S.u(:); om = S.om(:); e1 = S.e1(:); v = S.v(:);
% 对齐：Python 首个 burst 在 3.0 s，MATLAB 探针在回放起点后 1 ms 起 burst
k0 = find(t >= 3.0, 1);
t = t(k0:end); iq = iq(k0:end); u = u(k0:end); om = om(k0:end); e1 = e1(k0:end); v = v(k0:end);
N = numel(t);
clear b0_ident_m_probe;
bq = zeros(N,1);
for k = 1:N
    [~, ~, bq(k)] = b0_ident_m_probe(iq(k), u(k), om(k), e1(k), v(k));
end
idx = find([true; diff(bq) ~= 0]);
tb = t(idx); bqv = bq(idx);
save(fullfile(here, '_bq_ml.mat'), 'tb', 'bqv');
fprintf('回放 %d 点（%.1f s），产生 %d 个窗估计\n', N, t(end)-t(1), numel(idx));
for k = 1:min(6, numel(idx))
    fprintf('  t=%.3f s  bq=%.2f\n', tb(k), bqv(k));
end
end
