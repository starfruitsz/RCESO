function check_kt()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_cc');
h = @(b) get_param(['pmsm_cc/' b], 'PortHandles');
% 恒定 iq = 1 A、无注入、负载 0，量 Te
set_param('pmsm_cc/iqref', 'Value', '1');
set_param('pmsm_cc/Tm', 'Value', '0');
set_param('pmsm_cc/PMSM', 'Mechanical', '[1.89e-5 0 4 0]');
set_param('pmsm_cc', 'StopTime', '0.15');
out = sim('pmsm_cc');
V = out.mlog.signals.values; iq = V(:,4); te = V(:,13); wm = V(:,11);
n = size(V,1); tail = round(0.8*n):n;
fprintf('iq 后段均值 %.4f A   Te 后段均值 %.5f N·m\n', mean(iq(tail)), mean(te(tail)));
fprintf('实测 kt = Te/iq = %.5f N·m/A\n', mean(te(tail))/max(mean(iq(tail)),1e-9));
fprintf('理论 kt = 1.5*p*psi = 1.5*4*0.016833 = %.5f\n', 1.5*4*0.016833);
fprintf('转速 %.1f rpm（0.15 s 内）\n', wm(end)*30/pi);
% 静止标定电阻：给 vd 直流量
end
