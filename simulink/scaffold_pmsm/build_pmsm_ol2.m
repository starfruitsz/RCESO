function build_pmsm_ol2()
% 平均逆变器（3 个受控电压源）+ SPS PMSM，开环验证
mdl = 'pmsm_ol'; close_system(mdl, 0);
new_system(mdl); open_system(mdl);
set_param(mdl, 'Solver', 'FixedStepDiscrete', 'FixedStep', '1e-5', 'StopTime', '0.4');
NL = newline;
pmPath = ['sps_lib/Electrical Machines/Permanent Magnet' NL 'Synchronous Machine'];

add_block('sps_lib/powergui', [mdl '/powergui'], 'Position', [20 20 80 60]);
set_param([mdl '/powergui'], 'SimulationMode', 'discrete', 'Ts', '1e-5');

add_block(pmPath, [mdl '/PMSM'], 'Position', [330 80 450 230]);
set_param([mdl '/PMSM'], 'Resistance', '0.175', 'Inductance', '0.57e-3', ...
    'Flux', '0.016833', 'PolePairs', '4', 'PresetModel', 'No');

% 三相电压（平均逆变器）：受控电压源
for k = 1:3
    ph = -120*(k-1);
    add_block('simulink/Sources/Sine Wave', sprintf('%s/m%d', mdl, k), ...
        'Amplitude', '170', 'Frequency', '2*pi*40', 'Phase', num2str(ph*pi/180), ...
        'SampleTime', '1e-5', 'Position', [40 50+90*(k-1) 80 80+90*(k-1)]);
    add_block('sps_lib/Sources/Controlled Voltage Source', sprintf('%s/cvs%d', mdl, k), ...
        'Position', [150 40+90*(k-1) 210 100+90*(k-1)]);
    add_line(mdl, sprintf('m%d/1', k), sprintf('cvs%d/1', k), 'autorouting', 'on');
    add_line(mdl, sprintf('cvs%d/LConn1', k), sprintf('PMSM/LConn%d', k), 'autorouting', 'on');
end
% 星点：三个负端互连
add_line(mdl, 'cvs1/RConn1', 'cvs2/RConn1', 'autorouting', 'on');
add_line(mdl, 'cvs2/RConn1', 'cvs3/RConn1', 'autorouting', 'on');

% 机械端：负载转矩 = 0，转速输出
add_block('simulink/Sources/Constant', [mdl '/Tm'], 'Value', '0', 'Position', [40 400 70 430]);
add_line(mdl, 'Tm/1', 'PMSM/1', 'autorouting', 'on');
add_block('simulink/Sinks/To Workspace', [mdl '/w'], 'VariableName', 'wlog', ...
    'Position', [520 130 560 160]);
add_line(mdl, 'PMSM/1', 'w/1', 'autorouting', 'on');

save_system(mdl);
disp('built pmsm_ol v2');
end
