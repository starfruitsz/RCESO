function add_ident()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/SL');
ch.Script = fileread('SL.m');
h = @(b) get_param(['pmsm_foc/' b], 'PortHandles');
IB = 6.3069;

% iq(A) -> pu
add_block('simulink/Math Operations/Gain', 'pmsm_foc/giq', 'Gain', num2str(1/IB), ...
    'Position', [700 420 730 450]);
add_line('pmsm_foc', h('BS').Outport(3), h('giq').Inport(1));

% v = 0（简化速度环无重复内模）
add_block('simulink/Sources/Constant', 'pmsm_foc/v0', 'Value', '0', 'Position', [700 470 730 490]);

% 辨识块
add_block('simulink/User-Defined Functions/MATLAB Function', 'pmsm_foc/ID', ...
    'Position', [760 380 900 520]);
ch2 = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
txt = fileread('../../../simulink/b0_ident_m.m');
ch2.Script = txt;
% 端口：iq,u,ge1,e1,v -> b0,du
add_line('pmsm_foc', h('giq').Outport(1), h('ID').Inport(1));
add_line('pmsm_foc', h('SL').Outport(2), h('ID').Inport(2));   % u_pu
add_line('pmsm_foc', h('SL').Outport(3), h('ID').Inport(3));   % ge1 = e1
add_line('pmsm_foc', h('SL').Outport(3), h('ID').Inport(4));   % e1
add_line('pmsm_foc', h('v0').Outport(1), h('ID').Inport(5));

% 用 Unit Delay 打断 b0/du 代数环
add_block('simulink/Discrete/Unit Delay', 'pmsm_foc/dB0', 'SampleTime', '1e-3', ...
    'InitialCondition', '536.4', 'Position', [920 400 950 430]);
add_block('simulink/Discrete/Unit Delay', 'pmsm_foc/dDU', 'SampleTime', '1e-3', ...
    'InitialCondition', '0', 'Position', [920 460 950 490]);
add_line('pmsm_foc', h('ID').Outport(1), h('dB0').Inport(1));
add_line('pmsm_foc', h('ID').Outport(2), h('dDU').Inport(1));
add_line('pmsm_foc', h('dB0').Outport(1), h('SL').Inport(3));
add_line('pmsm_foc', h('dDU').Outport(1), h('SL').Inport(4));

save_system('pmsm_foc');
disp('ident added');
end
