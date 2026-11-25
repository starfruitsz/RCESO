function verify_modes()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
base = fileread('../b0_ident_m.m');

% ---- 1) 基线：识别开、无故障 ----
ch.Script = base; ch.ChartUpdate='DISCRETE'; ch.SampleTime='1e-3';
set_param('pmsm_foc/TLf', 'Amplitude', '0');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); V = out.flog.signals.values;
fprintf('① 基线        : 转速 %.1f  b0 %.1f  du 峰值 %.4f\n', ...
    V(end,11)*30/pi, B(end), max(abs(out.dulog.signals.values(:))));

% ---- 2) upd_on = 0：不辨识也不注入 ----
txt = regexprep(base, 'upd_on\s*=\s*[01];', 'upd_on  = 0;');
f = fopen('ID_tmp.m','w'); fwrite(f, txt); fclose(f);
ch.Script = fileread('ID_tmp.m');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); V = out.flog.signals.values;
fprintf('② upd_on=0    : 转速 %.1f  b0 %.1f  du 峰值 %.4f\n', ...
    V(end,11)*30/pi, B(end), max(abs(out.dulog.signals.values(:))));

% ---- 3) 故障 0.1 N·m：稳态判据应拦住 burst ----
ch.Script = base;
set_param('pmsm_foc/TLf', 'Amplitude', '0.1');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); V = out.flog.signals.values;
fprintf('③ 10Hz 故障   : 转速 %.1f  b0 %.1f  du 峰值 %.4f\n', ...
    V(end,11)*30/pi, B(end), max(abs(out.dulog.signals.values(:))));
set_param('pmsm_foc/TLf', 'Amplitude', '0');
save_system('pmsm_foc');
end
