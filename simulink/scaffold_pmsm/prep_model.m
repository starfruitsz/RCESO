function prep_model()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
h = @(b) get_param(['pmsm_foc/' b], 'PortHandles');
% 负载 = 0.5 + 0.1*sin(2*pi*10*t)（10 Hz 故障扰动）
try, delete_line('pmsm_foc', 'Tm/1', 'PMSM/1'); catch, end
add_block('simulink/Sources/Constant', 'pmsm_foc/TL0', 'Value', '0.5', 'Position', [240 400 270 430]);
add_block('simulink/Sources/Sine Wave', 'pmsm_foc/TLf', 'Amplitude', '0.1', ...
    'Frequency', '2*pi*10', 'SampleTime', '1e-5', 'Position', [240 440 280 470]);
add_block('simulink/Math Operations/Sum', 'pmsm_foc/TLsum', 'Inputs', '++', 'Position', [300 400 320 450]);
add_line('pmsm_foc', h('TL0').Outport(1), h('TLsum').Inport(1));
add_line('pmsm_foc', h('TLf').Outport(1), h('TLsum').Inport(2));
add_line('pmsm_foc', h('TLsum').Outport(1), h('PMSM').Inport(1));
set_param('pmsm_foc/dB0', 'InitialCondition', '800');
save_system('pmsm_foc');
fprintf('TL 已改为 0.5+0.1sin(10Hz)，dB0 初值 800\n');
end
