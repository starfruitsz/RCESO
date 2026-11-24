function wire_sl()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
h = @(b) get_param(['pmsm_foc/' b], 'PortHandles');
add_block('simulink/Sources/Constant', 'pmsm_foc/b0c', 'Value', '536.4', 'Position', [20 480 60 500]);
add_block('simulink/Sources/Constant', 'pmsm_foc/duc', 'Value', '0', 'Position', [20 510 60 530]);
add_line('pmsm_foc', h('b0c').Outport(1), h('SL').Inport(3));
add_line('pmsm_foc', h('duc').Outport(1), h('SL').Inport(4));
add_block('simulink/Sinks/To Workspace', 'pmsm_foc/L', 'VariableName', 'flog', ...
    'SaveFormat', 'Structure With Time', 'Position', [700 250 740 280]);
add_line('pmsm_foc', h('PMSM').Outport(1), h('L').Inport(1));
save_system('pmsm_foc');
out = sim('pmsm_foc');
V = out.flog.signals.values;
wm = V(:,11); iq = V(:,4); id = V(:,5); te = V(:,13);
fprintf('转速：末值 %.1f rpm  最小 %.1f  最大 %.1f\n', wm(end)*30/pi, min(wm)*30/pi, max(wm)*30/pi);
fprintf('iq 末值 %.2f A   峰值 %.2f A   id 末值 %.2f A\n', iq(end), max(abs(iq)), id(end));
fprintf('转矩 末值 %.3f N·m\n', te(end));
end
