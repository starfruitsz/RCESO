function run_ol6()
cd('D:\Desktop\RCESO\simulink');
out = sim('pmsm_ol');
T = out.wlog;
fn = fieldnames(T);
ws = T.(fn{find(contains(fn,'speed'),1)});
ts = T.(fn{find(contains(fn,'torque'),1)});
iqs = T.(fn{find(contains(fn,'is_q'),1)});
d = ws.Data(:); t = ws.Time(:);
fprintf('转速：末值 %.1f rpm  范围 %.1f..%.1f  (%d 点, %.1f s)\n', d(end)*30/pi, min(d)*30/pi, max(d)*30/pi, numel(d), t(end));
fprintf('转矩：末值 %.3f N·m\n', ts.Data(end));
q = iqs.Data(:);
fprintf('iq：末值 %.2f A  峰值 %.2f A\n', q(end), max(abs(q)));
end
