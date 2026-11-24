function run_ol()
cd('D:\Desktop\RCESO\simulink');
out = sim('pmsm_ol');
w = out.wlog;   % timeseries
d = w.Data(:); t = w.Time(:);
fprintf('转速末值 %.1f rpm  范围 %.1f..%.1f  时间 %d 点\n', d(end)*30/pi, min(d)*30/pi, max(d)*30/pi, numel(d));
fprintf('40 Hz 电频率 / 4 极对 = 10 Hz 机械 = 600 rpm\n');
end
