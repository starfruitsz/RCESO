function log_b0()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
h = @(b) get_param(['pmsm_foc/' b], 'PortHandles');
add_block('simulink/Sinks/To Workspace', 'pmsm_foc/Lb', 'VariableName', 'blog', ...
    'SaveFormat', 'Structure With Time', 'Position', [980 400 1020 430]);
add_line('pmsm_foc', h('ID').Outport(1), h('Lb').Inport(1));
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '30');
tic; out = sim('pmsm_foc'); el = toc;
V = out.flog.signals.values; wm = V(:,11)*30/pi; iq = V(:,4);
B = out.blog.signals.values;
fprintf('仿真 %.1f s 用时 %.1f s（1e-5 步长）\n', 30, el);
fprintf('转速 末值 %.1f   b0 末值 %.1f   真值 536.4\n', wm(end), B(end));
fprintf('b0 范围 %.1f..%.1f   iq 末值 %.2f A\n', min(B), max(B), iq(end));
end
