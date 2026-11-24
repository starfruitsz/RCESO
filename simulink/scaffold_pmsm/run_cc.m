function run_cc()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
out = sim('pmsm_cc');
T = out.mlog;
fn = fieldnames(T.signals);
get1 = @(kw) T.signals.(fn{find(contains(fn, kw), 1)}).values(:);
id = get1('is_d'); iq = get1('is_q'); wm = get1('speed');
fprintf('iq: 末值 %.2f A  均值(后段) %.2f A  峰值 %.2f A\n', iq(end), mean(iq(round(end*0.7):end)), max(abs(iq)));
fprintf('id: 末值 %.2f A  峰值 %.2f A\n', id(end), max(abs(id)));
fprintf('转速: 末值 %.1f rpm\n', wm(end)*30/pi);
end
