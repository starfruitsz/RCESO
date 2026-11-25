function verify_guard()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
ch.ChartUpdate = 'DISCRETE'; ch.SampleTime = '1e-3';
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
B = out.blog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
fprintf('加判据后：转速 %.1f rpm   b0 %.1f（%+.2f%%）  b0 范围 %.1f..%.1f\n', ...
    wm(end), B(end), 100*(B(end)/536.4-1), min(B), max(B));
end
