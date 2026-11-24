function run_ol4()
cd('D:\Desktop\RCESO\simulink');
out = sim('pmsm_ol');
T = out.wlog;
nm = T.Properties.VariableNames;
fprintf('变量 %d 个：\n', numel(nm));
for i = 1:numel(nm), fprintf('  %s\n', nm{i}); end
idx = find(contains(nm, 'speed'), 1);
w = T{:, idx};
fprintf('转速：末值 %.1f rpm  范围 %.1f..%.1f\n', w(end)*30/pi, min(w)*30/pi, max(w)*30/pi);
it = find(contains(nm, 'torque'), 1);
if ~isempty(it), te = T{:, it}; fprintf('转矩：末值 %.3f N·m\n', te(end)); end
end
