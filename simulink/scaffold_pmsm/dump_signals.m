function dump_signals()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '25');
out = sim('pmsm_foc');
u  = out.ulog.signals.values(:);
du = out.dulog.signals.values(:);
iq = out.iqlog.signals.values(:);
e1 = out.e1log.signals.values(:);
bq = out.bqlog.signals.values(:);
b0 = out.blog.signals.values(:);
t  = out.ulog.time(:);
save('_pm_foc_dump.mat', 't', 'u', 'du', 'iq', 'e1', 'bq', 'b0');
fprintf('保存 %d 点（1 kHz）到 _pm_foc_dump.mat\n', numel(t));
fprintf('u 均值 %.3f  du 峰值 %.3f  iq 均值 %.3f  e1 rms %.5f\n', mean(u), max(abs(du)), mean(iq), sqrt(mean(e1.^2)));
end
