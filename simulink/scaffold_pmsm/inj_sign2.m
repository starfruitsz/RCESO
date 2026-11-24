function inj_sign2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_cc');
fprintf('改前 Mechanical = %s\n', get_param('pmsm_cc/PMSM','Mechanical'));
set_param('pmsm_cc/PMSM', 'Mechanical', '[1.89e-5 0 4 0]');
fprintf('改后 Mechanical = %s\n', get_param('pmsm_cc/PMSM','Mechanical'));
set_param('pmsm_cc', 'StopTime', '0.6');
save_system('pmsm_cc');
out = sim('pmsm_cc');
V = out.mlog.signals.values; t = out.mlog.time(:);
iq = V(:,4); wm = V(:,11); te = V(:,13);
F = 65; m2 = (t > 0.3); ph = 2*pi*F*t(m2);
A_iq = 2/numel(iq(m2))*sum(iq(m2).*exp(-1j*ph));
A_w  = 2/numel(iq(m2))*sum(wm(m2).*exp(-1j*ph));
A_te = 2/numel(iq(m2))*sum(te(m2).*exp(-1j*ph));
fprintf('iq 幅 %.4f 相位 %+7.1f\n', abs(A_iq), angle(A_iq)*180/pi);
fprintf('wm 幅 %.4f 相位 %+7.1f  （差 %+7.1f）\n', abs(A_w), angle(A_w)*180/pi, (angle(A_w)-angle(A_iq))*180/pi);
fprintf('Te 幅 %.5f 相位 %+7.1f  （差 %+7.1f）\n', abs(A_te), angle(A_te)*180/pi, (angle(A_te)-angle(A_iq))*180/pi);
end
