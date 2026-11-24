function fix_J()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc/PMSM', 'Mechanical', '[1.89e-5 0 4 0]');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/SL');
ch.Script = fileread('SL.m'); ch.ChartUpdate='DISCRETE'; ch.SampleTime='1e-3';
ch2 = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch2.Script = fileread('../b0_ident_m.m'); ch2.ChartUpdate='DISCRETE'; ch2.SampleTime='1e-3';
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
V = out.flog.signals.values; wm = V(:,11)*30/pi;
Q = out.bqlog.signals.values(:); B = out.blog.signals.values(:);
nz = Q(Q > 0);
fprintf('转速 末值 %.1f 峰值 %.1f\n', wm(end), max(wm));
fprintf('b0 末值 %.1f   bq 中位 %.1f（真值 536.4）\n', B(end), median(nz));
end
