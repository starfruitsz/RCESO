function vfinal()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc/TLf', 'Amplitude', '0');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); V = out.flog.signals.values;
fprintf('A 基线 : 转速 %.1f  b0 %.1f  du %.4f\n', V(end,11)*30/pi, B(end), max(abs(out.dulog.signals.values(:))));
set_param('pmsm_foc/TLf', 'Amplitude', '0.1');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); V = out.flog.signals.values;
fprintf('B 故障 : 转速 %.1f  b0 %.1f  du %.4f\n', V(end,11)*30/pi, B(end), max(abs(out.dulog.signals.values(:))));
set_param('pmsm_foc/TLf', 'Amplitude', '0');
end
