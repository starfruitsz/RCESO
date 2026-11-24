function build_align()
% 静止标定：给固定电压矢量，看机器 id/iq 响应，确定 Park 约定
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
mdl = 'pmsm_align'; close_system(mdl, 0);
new_system(mdl); open_system(mdl);
set_param(mdl, 'Solver', 'FixedStepDiscrete', 'FixedStep', '1e-5', 'StopTime', '0.05');
NL = newline;
pmPath = ['sps_lib/Electrical Machines/Permanent Magnet' NL 'Synchronous Machine'];
h = @(b) get_param([mdl '/' b], 'PortHandles');

add_block('sps_lib/powergui', [mdl '/powergui'], 'Position', [20 20 80 60]);
set_param([mdl '/powergui'], 'SimulationMode', 'discrete', 'Ts', '1e-5');

add_block(pmPath, [mdl '/PMSM'], 'Position', [340 80 460 230]);
set_param([mdl '/PMSM'], 'Resistance', '0.175', 'Inductance', '0.57e-3', ...
    'Flux', '0.016833', 'PolePairs', '4', 'PresetModel', 'No');

for k = 1:3
    add_block('sps_lib/Sources/Controlled Voltage Source', sprintf('%s/cvs%d', mdl, k), ...
        'Position', [230 40+90*(k-1) 290 100+90*(k-1)]);
    add_line(mdl, sprintf('cvs%d/LConn1', k), sprintf('PMSM/LConn%d', k), 'autorouting', 'on');
    add_block('simulink/Sources/Constant', sprintf('%s/v%d', mdl, k), 'Value', '0', ...
        'Position', [80 40+90*(k-1) 130 70+90*(k-1)]);
    add_line(mdl, h(sprintf('v%d', k)).Outport(1), h(sprintf('cvs%d', k)).Inport(1));
end
add_line(mdl, 'cvs1/RConn1', 'cvs2/RConn1', 'autorouting', 'on');
add_line(mdl, 'cvs2/RConn1', 'cvs3/RConn1', 'autorouting', 'on');

% 大负载把转子压住（静止标定）
add_block('simulink/Sources/Constant', [mdl '/Tm'], 'Value', '20', 'Position', [60 400 90 430]);
add_line(mdl, h('Tm').Outport(1), h('PMSM').Inport(1));

add_block('simulink/Sinks/To Workspace', [mdl '/L'], 'VariableName', 'alog', ...
    'SaveFormat', 'Structure With Time', 'Position', [600 100 640 130]);
add_line(mdl, h('PMSM').Outport(1), h('L').Inport(1));
save_system(mdl);
disp('built pmsm_align');
end
