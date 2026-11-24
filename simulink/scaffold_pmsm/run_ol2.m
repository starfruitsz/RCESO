function run_ol2()
cd('D:\Desktop\RCESO\simulink');
open_system('pmsm_ol');
set_param('pmsm_ol/w', 'SaveFormat', 'Timeseries');
save_system('pmsm_ol');
out = sim('pmsm_ol');
w = out.wlog;
if isa(w, 'timeseries')
    d = w.Data(:);
elseif isstruct(w)
    d = w.signals.values(:);
else
    d = w(:);
end
fprintf('转速末值 %.1f rpm  范围 %.1f..%.1f  点数 %d\n', d(end)*30/pi, min(d)*30/pi, max(d)*30/pi, numel(d));
end
