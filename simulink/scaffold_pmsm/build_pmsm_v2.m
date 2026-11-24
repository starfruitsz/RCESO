function build_pmsm_v2()
% v2：三台 AC 源星形驱动 SPS PMSM，验证机器参数与转速
mdl = 'pmsm_v2'; close_system(mdl, 0);
new_system(mdl); open_system(mdl);
set_param(mdl, 'Solver', 'FixedStepDiscrete', 'FixedStep', '1e-5', 'StopTime', '0.3');
NL = newline;
pmPath = ['sps_lib/Electrical Machines/Permanent Magnet' NL 'Synchronous Machine'];

add_block('sps_lib/powergui', [mdl '/powergui'], 'Position', [20 20 80 60]);
set_param([mdl '/powergui'], 'SimulationMode', 'discrete', 'Ts', '1e-5');

for k = 1:3
    ph = (k-1) * (-120);
    add_block('sps_lib/Sources/AC Voltage Source', sprintf('%s/AC%d', mdl, k), ...
        'Amplitude', '170', 'Phase', num2str(ph), 'Frequency', '40', ...
        'Position', [40 80+80*(k-1) 100 120+80*(k-1)]);
end

add_block(pmPath, [mdl '/PMSM'], 'Position', [260 90 380 230]);
add_block('sps_lib/Electrical Machines/Machines Measurement Demux', [mdl '/ML'], ...
    'Position', [440 130 510 190]);
add_block('simulink/Sinks/To Workspace', [mdl '/w'], 'VariableName', 'wlog', ...
    'Position', [560 130 600 160]);

% 电气接线：AC 正端 → 电机三相；AC 负端互连成星点
add_line(mdl, 'AC1/1', 'PMSM/A', 'autorouting', 'on');
add_line(mdl, 'AC2/1', 'PMSM/B', 'autorouting', 'on');
add_line(mdl, 'AC3/1', 'PMSM/C', 'autorouting', 'on');
add_line(mdl, 'AC1/2', 'AC2/2', 'autorouting', 'on');
add_line(mdl, 'AC2/2', 'AC3/2', 'autorouting', 'on');

% 机械测量
add_line(mdl, 'PMSM/m', 'ML/m', 'autorouting', 'on');
save_system(mdl);
disp('--- 端口检查 ---');
disp(get_param([mdl '/PMSM'], 'PortHandles'));
disp(get_param([mdl '/ML'], 'DialogParameters'));
disp('built v2');
end
