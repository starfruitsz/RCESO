function verify_modes3()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
base = fileread('../b0_ident_m.m');
ch.Script = base; ch.ChartUpdate='DISCRETE'; ch.SampleTime='1e-3';
set_param('pmsm_foc/TLf', 'Amplitude', '0');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); V = out.flog.signals.values;
fprintf('① 基线      : 转速 %.1f  b0 %.1f  du %.4f\n', V(end,11)*30/pi, B(end), max(abs(out.dulog.signals.values(:))));
set_param('pmsm_foc/TLf', 'Amplitude', '0.1');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); V = out.flog.signals.values;
fprintf('② 10Hz 故障 : 转速 %.1f  b0 %.1f  du %.4f\n', V(end,11)*30/pi, B(end), max(abs(out.dulog.signals.values(:))));
set_param('pmsm_foc/TLf', 'Amplitude', '0');
save_system('pmsm_foc');
Simulink.exportToVersion('pmsm_foc', 'pmsm_foc_2018b', 'R2018b');
fprintf('已导出 R2018b\n');
end
