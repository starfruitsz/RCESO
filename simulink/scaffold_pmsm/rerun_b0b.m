function rerun_b0b()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot; ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
set_param('pmsm_foc/dB0', 'InitialCondition', '536.4');
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
B = out.blog.signals.values; V = out.flog.signals.values;
wm = V(:,11)*30/pi;
fprintf('转速 末值 %.1f   b0 末值 %.1f  b0 范围 %.1f..%.1f（真值 536.4）\n', wm(end), B(end), min(B), max(B));
end
