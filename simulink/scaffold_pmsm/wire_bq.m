function wire_bq()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
h = @(b) get_param(['pmsm_foc/' b], 'PortHandles');
add_block('simulink/Sinks/To Workspace', 'pmsm_foc/Lbq', 'VariableName', 'bqlog', ...
    'SaveFormat', 'Structure With Time', 'Position', [980 520 1020 550]);
add_line('pmsm_foc', h('ID').Outport(3), h('Lbq').Inport(1));
% 1 kHz 侧信号（u, e1, iq_pu）记录下来供离线分析
add_block('simulink/Sinks/To Workspace', 'pmsm_foc/Le1', 'VariableName', 'e1log', ...
    'SaveFormat', 'Structure With Time', 'Position', [760 560 800 590]);
add_line('pmsm_foc', h('SL').Outport(3), h('Le1').Inport(1));
add_block('simulink/Sinks/To Workspace', 'pmsm_foc/Liq', 'VariableName', 'iqlog', ...
    'SaveFormat', 'Structure With Time', 'Position', [760 600 800 630]);
add_line('pmsm_foc', h('giq').Outport(1), h('Liq').Inport(1));
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '40');
out = sim('pmsm_foc');
B = out.blog.signals.values(:); Q = out.bqlog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
fprintf('转速 %.1f   b0 末值 %.1f\n', wm(end), B(end));
nz = Q(Q > 0);
fprintf('bq 序列（前 12 个非零）：%s\n', mat2str(round(nz(1:min(12,numel(nz))).'*10)/10));
fprintf('bq 统计：n=%d  中位 %.1f  均值 %.1f  （真值 536.4）\n', numel(nz), median(nz), mean(nz));
end
