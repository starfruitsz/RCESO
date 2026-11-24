function fix_ts()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc/SL', 'SampleTime', '1e-3');
set_param('pmsm_foc/ID', 'SampleTime', '1e-3');
set_param('pmsm_foc/CC', 'SampleTime', '5e-5');
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); Q = out.bqlog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
nz = Q(Q > 0);
fprintf('转速 %.1f   b0 末值 %.1f   bq 非零 %d 个\n', wm(end), B(end), numel(nz));
if ~isempty(nz)
    fprintf('bq 前 10：%s\n', mat2str(round(nz(1:min(10,numel(nz))).'*10)/10));
    fprintf('bq 中位 %.1f（真值 536.4）\n', median(nz));
end
end
