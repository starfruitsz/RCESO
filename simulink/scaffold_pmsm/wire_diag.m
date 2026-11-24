function wire_diag()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
ch.ChartUpdate = 'DISCRETE'; ch.SampleTime = '1e-3';
h = @(b) get_param(['pmsm_foc/' b], 'PortHandles');
names = {'dDlog','dUlog','dQlog'};
for i = 1:3
    add_block('simulink/Sinks/To Workspace', ['pmsm_foc/' names{i}], ...
        'VariableName', names{i}(1:2), 'SaveFormat', 'Structure With Time', ...
        'Position', [980 560+40*i 1020 590+40*i]);
    add_line('pmsm_foc', h('ID').Outport(3+i), h(names{i}).Inport(1));
end
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
nz = @(x) x(x > 0);
D = nz(out.dD.signals.values(:)); U = nz(out.dU.signals.values(:)); Q = nz(out.dQ.signals.values(:));
fprintf('|Δd̂ + b0Δu| 中位 %.3f\n', median(D));
fprintf('|Δu|       中位 %.4f   （期望 ≈ 2*0.118 = 0.236）\n', median(U));
fprintf('|Δĩ|       中位 %.4f   （期望 ≈ 0.236）\n', median(Q));
end
