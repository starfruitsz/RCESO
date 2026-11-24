function inj_sign()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_cc');
h = @(b) get_param(['pmsm_cc/' b], 'PortHandles');
% iqref = 0.5 + 0.118*sin(2*pi*65*t)
add_block('simulink/Sources/Constant', 'pmsm_cc/iq0', 'Value', '0.5', 'Position', [20 60 60 80]);
add_block('simulink/Sources/Sine Wave', 'pmsm_cc/du', 'Amplitude', '0.118', ...
    'Frequency', '2*pi*65', 'SampleTime', '5e-5', 'Position', [20 100 60 130]);
add_block('simulink/Math Operations/Sum', 'pmsm_cc/iqsum', 'Inputs', '++', 'Position', [90 70 110 120]);
add_line('pmsm_cc', h('iq0').Outport(1), h('iqsum').Inport(1));
add_line('pmsm_cc', h('du').Outport(1), h('iqsum').Inport(2));
% 断开原 iqref 恒值到 CC/2，改接 iqsum
try, delete_line('pmsm_cc', 'iqref/1', 'CC/2'); catch, end
add_line('pmsm_cc', h('iqsum').Outport(1), h('CC').Inport(2));
set_param('pmsm_cc', 'StopTime', '0.6');
save_system('pmsm_cc');
out = sim('pmsm_cc');
V = out.mlog.signals.values;
t = out.mlog.time(:); iq = V(:,4); wm = V(:,11);
F = 65; W = 2*pi*F;
m2 = (t > 0.3);
ph_du = 2*pi*F*t(m2);
A_du = 2/numel(iq(m2))*sum(iq(m2).*exp(-1j*ph_du));
A_w  = 2/numel(iq(m2))*sum(wm(m2).*exp(-1j*ph_du));
fprintf('iq 65Hz 幅值 %.4f  相位 %+7.2f deg\n', abs(A_du), angle(A_du)*180/pi);
fprintf('wm 65Hz 幅值 %.4f  相位 %+7.2f deg  （相对 iq）\n', abs(A_w), angle(A_w)*180/pi);
fprintf('相位差 %+7.2f deg（纯惯量应约 -90）\n', (angle(A_w)-angle(A_du))*180/pi);
end
