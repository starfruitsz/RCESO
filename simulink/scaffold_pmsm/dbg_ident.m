function dbg_ident()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
h = @(b) get_param(['pmsm_foc/' b], 'PortHandles');
add_block('simulink/Sinks/To Workspace', 'pmsm_foc/Lu', 'VariableName', 'ulog', ...
    'SaveFormat', 'Structure With Time', 'Position', [760 540 800 570]);
add_line('pmsm_foc', h('SL').Outport(2), h('Lu').Inport(1));
add_block('simulink/Sinks/To Workspace', 'pmsm_foc/Ldu', 'VariableName', 'dulog', ...
    'SaveFormat', 'Structure With Time', 'Position', [980 460 1020 490]);
add_line('pmsm_foc', h('ID').Outport(2), h('Ldu').Inport(1));
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '15');
out = sim('pmsm_foc');
U = out.ulog.signals.values(:);
D = out.dulog.signals.values(:);
V = out.flog.signals.values; iq = V(:,4); iqp = iq/6.3069;
fprintf('u_pu 范围 %.3f..%.3f\n', min(U), max(U));
fprintf('du   范围 %.4f..%.4f  (峰值 %.4f)\n', min(D), max(D), max(abs(D)));
fprintf('iq_pu 范围 %.3f..%.3f\n', min(iqp), max(iqp));
B = out.blog.signals.values;
fprintf('b0 范围 %.1f..%.1f 末值 %.1f\n', min(B), max(B), B(end));
end
