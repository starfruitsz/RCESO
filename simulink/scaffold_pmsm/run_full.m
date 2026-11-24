function run_full()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/SL');
ch.Script = fileread('SL.m'); ch.ChartUpdate='DISCRETE'; ch.SampleTime='1e-3';
ch2 = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch2.Script = fileread('../b0_ident_m.m'); ch2.ChartUpdate='DISCRETE'; ch2.SampleTime='1e-3';
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '130');
tic; out = sim('pmsm_foc'); el = toc;
V = out.flog.signals.values; wm = V(:,11)*30/pi;
B = out.blog.signals.values(:); Q = out.bqlog.signals.values(:);
nz = Q(Q > 0);
fprintf('仿真 130 s 用时 %.1f s\n', el);
fprintf('转速 末值 %.1f  后段均值 %.1f\n', wm(end), mean(wm(round(0.8*numel(wm)):end)));
fprintf('b0 终值 %.1f（真值 536.4，%+.2f%%）\n', B(end), 100*(B(end)/536.4-1));
fprintf('bq 个数 %d  中位 %.1f  均值 %.1f\n', numel(nz), median(nz), mean(nz));
end
