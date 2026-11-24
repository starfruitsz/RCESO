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
% 三组对照：正常 / v=0 / e1=0 —— 定位偏置来自哪一路输入
variants = {'kv=0', 0; 'kv=0.001', 0.001; 'kv=0.0028', 0.0028; 'kv=0.005', 0.005; 'kv=0.01', 0.01};
bq = zeros(N,1);
for iv = 1:size(variants,1)
    kv = variants{iv,2};
    clear b0_ident_m_probe;
    for k = 1:N
        [~, ~, bq(k)] = b0_ident_m_probe(iq(k), u(k), om(k), e1(k), v(k)*kv);
    end
    idx = find([true; diff(bq) ~= 0]);
    vv = bq(idx(2:end));
    fprintf('RESULT %s nwin=%d  bq=%s  median=%.1f\n', variants{iv,1}, numel(vv), ...
            strjoin(arrayfun(@(x) sprintf('%.1f', x), vv(1:min(6,numel(vv))), 'UniformOutput', false), ' '), median(vv));
    if iv == 3, tb1 = t(idx); bqv1 = bq(idx); end
end
tb = tb1; bqv = bqv1;
idx = find([true; diff(bqv) ~= 0]);
tb = t(idx); bqv = bq(idx);
save(fullfile(here, '_bq_ml.mat'), 'tb', 'bqv');
fprintf('回放 %d 点（%.1f s），产生 %d 个窗估计\n', N, t(end)-t(1), numel(idx));
for k = 1:min(6, numel(idx))
    fprintf('  t=%.3f s  bq=%.2f\n', tb(k), bqv(k));
end
end
