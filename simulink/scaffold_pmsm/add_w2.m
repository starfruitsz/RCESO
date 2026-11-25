function add_w2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
ch.ChartUpdate = 'DISCRETE'; ch.SampleTime = '1e-3';
h = @(b) get_param(['pmsm_foc/' b], 'PortHandles');
add_line('pmsm_foc', h('BS').Outport(4), h('ID').Inport(6));
add_block('simulink/Sources/Constant', 'pmsm_foc/wref_si', 'Value', '62.832', ...
    'Position', [700 560 740 580]);
add_line('pmsm_foc', h('wref_si').Outport(1), h('ID').Inport(7));
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
B = out.blog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
fprintf('w/wref 接入后：转速 %.1f rpm   b0 %.1f（%+.2f%%）\n', wm(end), B(end), 100*(B(end)/536.4-1));
Simulink.exportToVersion('pmsm_foc', 'pmsm_foc_2018b', 'R2018b');
fprintf('已导出 R2018b\n');
end
