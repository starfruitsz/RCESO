function build_pmsm_v1()
% 用 SPS 自带 PMSM 模块搭被控对象（v1：三相可编程电压源直接驱动，验证参数）
mdl = 'pmsm_v1'; close_system(mdl, 0);
new_system(mdl); open_system(mdl);
set_param(mdl, 'Solver', 'FixedStepDiscrete', 'FixedStep', '1e-5', 'StopTime', '0.5');
NL = newline;
pmPath = ['sps_lib/Electrical Machines/Permanent Magnet' NL 'Synchronous Machine'];

add_block('sps_lib/powergui', [mdl '/powergui'], 'Position', [20 20 80 60]);
set_param([mdl '/powergui'], 'SimulationMode', 'discrete', 'Ts', '1e-5');

% 三相可编程电压源（40 Hz 电频率 => 600 rpm 机械）
add_block('sps_lib/Sources/Three-Phase Programmable Voltage Source', [mdl '/Vs'], ...
    'Position', [40 120 120 220], 'PositiveSequence', '[1 0 40]');
set_param([mdl '/Vs'], 'Amplitude', '180', 'Frequency', '40');

% PMSM
add_block(pmPath, [mdl '/PMSM'], 'Position', [260 90 370 220]);
% 机器测量分离
add_block('sps_lib/Electrical Machines/Machines Measurement Demux', [mdl '/ML'], ...
    'Position', [430 130 500 190]);

add_block('simulink/Sinks/To Workspace', [mdl '/w'], 'VariableName', 'wlog', 'Position', [560 140 600 170]);
save_system(mdl);
disp('built v1 skeleton');
% 打印端口名，便于接线
p = get_param([mdl '/PMSM'], 'Ports');
disp(p);
disp(get_param([mdl '/PMSM'], 'PortConnectivity'));
end
