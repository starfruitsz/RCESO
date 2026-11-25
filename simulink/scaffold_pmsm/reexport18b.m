function reexport18b()
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
fprintf('验证：转速 %.1f rpm   b0 %.1f（%+.2f%%）\n', wm(end), B(end), 100*(B(end)/536.4-1));
Simulink.exportToVersion('pmsm_foc', 'pmsm_foc_2018b', 'R2018b');
fprintf('已导出\n');
end
