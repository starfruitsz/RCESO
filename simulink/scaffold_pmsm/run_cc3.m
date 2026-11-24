function run_cc3()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
out = sim('pmsm_cc');
V = out.mlog.signals.values;
iq = V(:,4); id = V(:,5); wm = V(:,11); te = V(:,13);
n = size(V,1); tail = round(n*0.7):n;
fprintf('iq: 末值 %.2f A  后段均值 %.2f A  峰值 %.2f A\n', iq(end), mean(iq(tail)), max(abs(iq)));
fprintf('id: 末值 %.2f A  后段均值 %.2f A  峰值 %.2f A\n', id(end), mean(id(tail)), max(abs(id)));
fprintf('转速 末值 %.1f rpm   转矩 末值 %.3f N·m\n', wm(end)*30/pi, te(end));
end
