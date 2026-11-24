function build_pmsm_cc2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
mdl = 'pmsm_cc'; close_system(mdl, 0);
new_system(mdl); open_system(mdl);
set_param(mdl, 'Solver', 'FixedStepDiscrete', 'FixedStep', '1e-5', 'StopTime', '0.4');
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
end
add_line(mdl, 'cvs1/RConn1', 'cvs2/RConn1', 'autorouting', 'on');
add_line(mdl, 'cvs2/RConn1', 'cvs3/RConn1', 'autorouting', 'on');

% 机械负载 -> PMSM Inport（用句柄，避免端口号歧义）
add_block('simulink/Sources/Constant', [mdl '/Tm'], 'Value', '0.5', 'Position', [60 400 90 430]);
add_line(mdl, h('Tm').Outport(1), h('PMSM').Inport(1));

% 测量总线 -> Bus Selector
add_block('simulink/Signal Routing/Bus Selector', [mdl '/BS'], 'Position', [520 100 540 200]);
set_param([mdl '/BS'], 'OutputSignals', ...
    'Rotor_angle_thetam__rad_,Stator_current_is_d__A_,Stator_current_is_q__A_');
add_line(mdl, h('PMSM').Outport(1), h('BS').Inport(1));

% 电流环
add_block('simulink/User-Defined Functions/MATLAB Function', [mdl '/CC'], 'Position', [40 120 200 300]);
rt = sfroot; ch = rt.find('-isa','Stateflow.EMChart','Path',[mdl '/CC']);
ch.Script = fileread('CC.m');

add_block('simulink/Sources/Constant', [mdl '/idref'], 'Value', '0', 'Position', [40 60 80 80]);
add_block('simulink/Sources/Constant', [mdl '/iqref'], 'Value', '3', 'Position', [40 90 80 110]);
add_line(mdl, h('idref').Outport(1), h('CC').Inport(1));
add_line(mdl, h('iqref').Outport(1), h('CC').Inport(2));
add_line(mdl, h('BS').Outport(2), h('CC').Inport(3));   % id
add_line(mdl, h('BS').Outport(3), h('CC').Inport(4));   % iq
add_line(mdl, h('BS').Outport(1), h('CC').Inport(5));   % thm
for k = 1:3
    add_line(mdl, h('CC').Outport(k), h(sprintf('cvs%d', k)).Inport(1));
end

add_block('simulink/Sinks/To Workspace', [mdl '/L'], 'VariableName', 'mlog', ...
    'SaveFormat', 'Structure With Time', 'Position', [600 100 640 130]);
add_line(mdl, h('PMSM').Outport(1), h('L').Inport(1));

save_system(mdl);
disp('built pmsm_cc v2');
end
