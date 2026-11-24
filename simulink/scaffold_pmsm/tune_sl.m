function tune_sl()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot; ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/SL');
ch.Script = fileread('SL.m');
set_param('pmsm_foc', 'StopTime', '5');
save_system('pmsm_foc');
out = sim('pmsm_foc');
V = out.flog.signals.values;
wm = V(:,11)*30/pi; iq = V(:,4);
fprintf('转速：末值 %.1f  峰值 %.1f  超调 %.1f%%\n', wm(end), max(wm), 100*(max(wm)/600-1));
fprintf('iq：末值 %.2f  峰值 %.2f A\n', iq(end), max(abs(iq)));
end
