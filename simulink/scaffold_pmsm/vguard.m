function vguard()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
ch.ChartUpdate='DISCRETE'; ch.SampleTime='1e-3';
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
fprintf('GUARD %.1f %.4f\n', out.blog.signals.values(end), max(abs(out.dulog.signals.values(:))));
save_system('pmsm_foc');
Simulink.exportToVersion('pmsm_foc', 'pmsm_foc_2018b', 'R2018b');
end
