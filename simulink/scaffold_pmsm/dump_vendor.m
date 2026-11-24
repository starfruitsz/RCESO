function dump_vendor()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
V = out.flog.signals.values; t = out.flog.time(:);
save('_vendor_run.mat', 't', 'V', ...
     'b0', 'bq', 'u', 'du');
b0 = out.blog.signals.values(:); bq = out.bqlog.signals.values(:);
u = out.ulog.signals.values(:); du = out.dulog.signals.values(:);
save('_vendor_run.mat', 't', 'V', 'b0', 'bq', 'u', 'du');
fprintf('保存 _vendor_run.mat：%d 点，b0 末值 %.1f\n', numel(t), b0(end));
end
