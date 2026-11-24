function build_pmsm_foc()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
mdl = 'pmsm_foc'; close_system(mdl, 0);
new_system(mdl); open_system(mdl);
set_param(mdl, 'Solver', 'FixedStepDiscrete', 'FixedStep', '1e-5', 'StopTime', '5');
NL = newline;
pmPath = ['sps_lib/Electrical Machines/Permanent Magnet' NL 'Synchronous Machine'];
h = @(b) get_param([mdl '/' b], 'PortHandles');

add_block('sps_lib/powergui', [mdl '/powergui'], 'Position', [20 20 80 60]);
set_param([mdl '/powergui'], 'SimulationMode', 'discrete', 'Ts', '1e-5');

add_block(pmPath, [mdl '/PMSM'], 'Position', [520 80 640 230]);
set_param([mdl '/PMSM'], 'Resistance', '0.175', 'Inductance', '0.57e-3', ...
    'Flux', '0.016833', 'PolePairs', '4', 'PresetModel', 'No');

for k = 1:3
    add_block('sps_lib/Sources/Controlled Voltage Source', sprintf('%s/cvs%d', mdl, k), ...
        'Position', [400 40+90*(k-1) 460 100+90*(k-1)]);
    add_line(mdl, sprintf('cvs%d/LConn1', k), sprintf('PMSM/LConn%d', k), 'autorouting', 'on');
end
add_line(mdl, 'cvs1/RConn1', 'cvs2/RConn1', 'autorouting', 'on');
add_line(mdl, 'cvs2/RConn1', 'cvs3/RConn1', 'autorouting', 'on');

add_block('simulink/Sources/Constant', [mdl '/Tm'], 'Value', '0.5', 'Position', [300 400 330 430]);
add_line(mdl, h('Tm').Outport(1), h('PMSM').Inport(1));

% 测量总线：θm, id, iq, wm
add_block('simulink/Signal Routing/Bus Selector', [mdl '/BS'], 'Position', [660 90 680 210]);
set_param([mdl '/BS'], 'OutputSignals', strjoin({ ...
    'Rotor angle thetam (rad)', 'Stator current is_d (A)', ...
    'Stator current is_q (A)', 'Rotor speed wm (rad/s)'}, ','));
add_line(mdl, h('PMSM').Outport(1), h('BS').Inport(1));

% 20 kHz 电流环
add_block('simulink/User-Defined Functions/MATLAB Function', [mdl '/CC'], 'Position', [240 120 380 300]);
rt = sfroot; ch = rt.find('-isa','Stateflow.EMChart','Path',[mdl '/CC']);
ch.Script = fileread('CC.m');
for k = 1:3
    add_line(mdl, h('CC').Outport(k), h(sprintf('cvs%d', k)).Inport(1));
end
add_line(mdl, h('BS').Outport(2), h('CC').Inport(3));   % id
add_line(mdl, h('BS').Outport(3), h('CC').Inport(4));   % iq
add_line(mdl, h('BS').Outport(1), h('CC').Inport(5));   % thm

% 1 kHz 速度环
add_block('simulink/User-Defined Functions/MATLAB Function', [mdl '/SL'], 'Position', [40 300 220 480]);
rt = sfroot; ch = rt.find('-isa','Stateflow.EMChart','Path',[mdl '/SL']);
ch.Script = fileread('SL.m');
add_block('simulink/Sources/Constant', [mdl '/wref'], 'Value', '600', 'Position', [20 250 60 270]);
add_line(mdl, h('wref').Outport(1), h('SL').Inport(1));
add_line(mdl, h('BS').Outport(4), h('SL').Inport(2));   % wm
add_line(mdl, h('BS').Outport(3), h('SL').Inport(5));   % iq（诊断用）
add_line(mdl, h('SL').Outport(1), h('CC').Inport(2));   % iref_A -> iqr
save_system(mdl);
disp('built pmsm_foc（暂无 b0 辨识：先验证速度环）');
end
