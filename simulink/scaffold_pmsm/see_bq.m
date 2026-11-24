function see_bq()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot; ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '30');
out = sim('pmsm_foc');
Q = out.bqlog.signals.values(:);
nz = Q(Q > 0);
fprintf('bq 非零 %d 个，前 10：%s\n', numel(nz), mat2str(round(nz(1:min(10,numel(nz))).'*10)/10));
fprintf('bq 中位 %.1f  均值 %.1f  范围 %.1f..%.1f（真值 536.4）\n', median(nz), mean(nz), min(nz), max(nz));
end
