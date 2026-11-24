function ol_tune()
cd('D:\Desktop\RCESO\simulink');
load_system('pmsm_ol');
% 反电势：psi*w_e = 0.016833*2*pi*40 = 4.23 V 峰值；加 IR 留裕量
for k = 1:3, set_param(sprintf('pmsm_ol/m%d', k), 'Amplitude', '5.6'); end
set_param('pmsm_ol/Tm', 'Value', '0.5');          % 0.5 N·m 负载
set_param('pmsm_ol', 'StopTime', '1.0');
set_param('pmsm_ol/powergui', 'Ts', '1e-5');
save_system('pmsm_ol');
out = sim('pmsm_ol');
T = out.wlog; fn = fieldnames(T);
g = @(kw) T.(fn{find(contains(fn, kw), 1)}).Data(:);
wm = g('speed'); te = g('torque'); iq = g('is_q'); id = g('is_d');
fprintf('转速末值 %.1f rpm   iq 末值 %.2f A   峰值 %.2f A   转矩 %.3f N·m    id %.2f A\n', ...
        wm(end)*30/pi, iq(end), max(abs(iq)), te(end), id(end));
end
