function verify_unit2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc/TLf', 'Amplitude', '0');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
fprintf('AAA %.1f %.4f\n', out.blog.signals.values(end), max(abs(out.dulog.signals.values(:))));
set_param('pmsm_foc/wref_si', 'Value', '600');
out = sim('pmsm_foc');
fprintf('BBB %.1f %.4f\n', out.blog.signals.values(end), max(abs(out.dulog.signals.values(:))));
set_param('pmsm_foc/wref_si', 'Value', '62.832');
set_param('pmsm_foc/TLf', 'Amplitude', '0.1');
out = sim('pmsm_foc');
fprintf('CCC %.1f %.4f\n', out.blog.signals.values(end), max(abs(out.dulog.signals.values(:))));
set_param('pmsm_foc/TLf', 'Amplitude', '0');
save_system('pmsm_foc');
end
