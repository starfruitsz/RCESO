function rerun_act()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/SL');
ch.Script = fileread('SL.m');
ch.ChartUpdate = 'DISCRETE'; ch.SampleTime = '1e-3';
ch2 = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch2.Script = fileread('../b0_ident_m.m');
ch2.ChartUpdate = 'DISCRETE'; ch2.SampleTime = '1e-3';
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); Q = out.bqlog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
nz = Q(Q > 0);
fprintf('转速 %.1f   b0 末值 %.1f   bq 个数 %d\n', wm(end), B(end), numel(nz));
if ~isempty(nz)
    fprintf('bq 前 8：%s   中位 %.1f（真值 536.4）\n', ...
        mat2str(round(nz(1:min(8,numel(nz))).'*10)/10), median(nz));
end
end
