function run_ol5()
cd('D:\Desktop\RCESO\simulink');
out = sim('pmsm_ol');
T = out.wlog;
fprintf('class=%s\n', class(T));
if isstruct(T)
    fn = fieldnames(T);
    for i = 1:numel(fn), fprintf('  %-40s %s\n', fn{i}, mat2str(size(T.(fn{i})))); end
    idx = find(contains(fn, 'speed'), 1);
    w = T.(fn{idx});
    if isstruct(w), w = w.signals.values; end
    w = w(:);
    fprintf('转速：末值 %.1f rpm  范围 %.1f..%.1f\n', w(end)*30/pi, min(w)*30/pi, max(w)*30/pi);
end
end
