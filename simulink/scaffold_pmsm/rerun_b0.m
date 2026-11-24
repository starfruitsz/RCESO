function rerun_b0()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot; ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
B = out.blog.signals.values; V = out.flog.signals.values;
wm = V(:,11)*30/pi; iq = V(:,4);
fprintf('转速 末值 %.1f   b0 末值 %.1f（真值 536.4）  b0 范围 %.1f..%.1f\n', ...
        wm(end), B(end), min(B), max(B));
fprintf('iq 末值 %.2f A\n', iq(end));
end
