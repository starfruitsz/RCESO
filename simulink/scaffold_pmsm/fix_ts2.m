function fix_ts2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
for nm = {'SL','ID'}
    ch = rt.find('-isa','Stateflow.EMChart','Path',['pmsm_foc/' nm{1}]);
    ch.ChartUpdate = 'DISCRETE';
    ch.SampleTime = '1e-3';
end
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/CC');
ch.ChartUpdate = 'DISCRETE';
ch.SampleTime = '5e-5';
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); Q = out.bqlog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
nz = Q(Q > 0);
fprintf('转速 %.1f   b0 末值 %.1f   bq 非零 %d 个\n', wm(end), B(end), numel(nz));
if ~isempty(nz)
    fprintf('bq 前 8：%s\n', mat2str(round(nz(1:min(8,numel(nz))).'*10)/10));
    fprintf('bq 中位 %.1f（真值 536.4）\n', median(nz));
end
end
