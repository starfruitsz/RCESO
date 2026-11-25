function cleanup_model()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
for b = {'Lbq','dDlog','dUlog','dQlog'}
    try, delete_block(['pmsm_foc/' b{1}]); catch, end
end
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
ch.ChartUpdate = 'DISCRETE'; ch.SampleTime = '1e-3';
save_system('pmsm_foc');
fprintf('ID 输出口数：%d\n', numel(get_param('pmsm_foc/ID','Ports')) );
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
B = out.blog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
fprintf('转速后段 %.1f rpm   b0 %.1f（真值 536.4，%+.2f%%）\n', mean(wm(end-1000:end)), B(end), 100*(B(end)/536.4-1));
end
