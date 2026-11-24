function upd_cc()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_cc');
rt = sfroot; ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_cc/CC');
ch.Script = fileread('CC.m');
set_param('pmsm_cc', 'StopTime', '0.4');
save_system('pmsm_cc');
out = sim('pmsm_cc');
V = out.mlog.signals.values;
iq = V(:,4); id = V(:,5); wm = V(:,11);
n = size(V,1); tail = round(n*0.7):n;
fprintf('iq 末值 %.2f A  后段均值 %.2f A  峰值 %.2f A\n', iq(end), mean(iq(tail)), max(abs(iq)));
fprintf('id 末值 %.2f A  峰值 %.2f A\n', id(end), max(abs(id)));
fprintf('转速 末值 %.1f rpm\n', wm(end)*30/pi);
end
