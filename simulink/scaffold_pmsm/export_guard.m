function export_guard()
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
fprintf('导出前验证：b0 末值 %.1f，范围 %.1f..%.1f\n', B(end), min(B), max(B));
Simulink.exportToVersion('pmsm_foc', 'pmsm_foc_2018b', 'R2018b');
fprintf('已导出\n');
end
