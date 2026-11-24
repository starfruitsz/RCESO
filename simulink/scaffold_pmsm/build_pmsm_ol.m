function build_pmsm_ol()
% 平均逆变器（三个受控电压源）+ SPS PMSM：开环验证 40 Hz -> 600 rpm
mdl = 'pmsm_ol'; close_system(mdl, 0);
new_system(mdl); open_system(mdl);
set_param(mdl, 'Solver', 'FixedStepDiscrete', 'FixedStep', '1e-5', 'StopTime', '0.4');
NL = newline;
pmPath = ['sps_lib/Electrical Machines/Permanent Magnet' NL 'Synchronous Machine'];

add_block('sps_lib/powergui', [mdl '/powergui'], 'Position', [20 20 80 60]);
set_param([mdl '/powergui'], 'SimulationMode', 'discrete', 'Ts', '1e-5');

% ---- PMSM：参数映射 + 打开测量总线 ----
add_block(pmPath, [mdl '/PMSM'], 'Position', [320 80 440 220]);
set_param([mdl '/PMSM'], 'Resistance', '0.175', 'Inductance', '0.57e-3', ...
    'Flux', '0.016833', 'PolePairs', '4', 'Mechanical', '[1.89e-5 0 4 0]', ...
    'MeasurementBus', 'on', 'PresetModel', 'No');

% ---- 平均逆变器：三个受控电压源 ----
for k = 1:3
    ph = -120 * (k-1);
    add_block('simulink/Sources/Sine Wave', sprintf('%s/m%d', mdl, k), ...
        'Amplitude', '170', 'Frequency', '2*pi*40', 'Phase', num2str(ph*pi/180), ...
        'SampleTime', '1e-5', 'Position', [40 60+90*(k-1) 80 90+90*(k-1)]);
    add_block('sps_lib/Sources/Controlled Voltage Source', sprintf('%s/cvs%d', mdl, k), ...
        'Position', [150 50+90*(k-1) 210 100+90*(k-1)]);
end
add_line(mdl, 'm1/1', 'cvs1/1', 'autorouting', 'on');
add_line(mdl, 'm2/1', 'cvs2/1', 'autorouting', 'on');
add_line(mdl, 'm3/1', 'cvs3/1', 'autorouting', 'on');
% 三相到电机，负端接成星点
add_line(mdl, 'cvs1/2', 'PMSM/A', 'autorouting', 'on');
add_line(mdl, 'cvs2/2', 'PMSM/B', 'autorouting', 'on');
add_line(mdl, 'cvs3/2', 'PMSM/C', 'autorouting', 'on');
add_line(mdl, 'cvs1/3', 'cvs2/3', 'autorouting', 'on');
add_line(mdl, 'cvs2/3', 'cvs3/3', 'autorouting', 'on');

% ---- 测量总线 -> 转速 ----
add_block('simulink/Signal Routing/Bus Selector', [mdl '/BS'], ...
    'Position', [480 120 500 180]);
add_block('simulink/Sinks/To Workspace', [mdl '/w'], 'VariableName', 'wlog', ...
    'Position', [560 130 600 160]);
add_line(mdl, 'PMSM/meas', 'BS/1', 'autorouting', 'on');

save_system(mdl);
disp('--- PMSM 端口 ---');
ph = get_param([mdl '/PMSM'], 'PortHandles');
fn = fieldnames(ph);
for i = 1:numel(fn)
    h = ph.(fn{i});
    if ~isempty(h), fprintf('  %-10s n=%d\n', fn{i}, numel(h)); end
end
disp('--- 允许的测量信号 ---');
dp = get_param([mdl '/PMSM'], 'DialogParameters');
disp(fieldnames(dp)');
disp('built pmsm_ol');
end
