function test_dbg()
cd('D:\Desktop\RCESO\simulink\port_2018b');
copyfile('../scaffold_pmsm/pmsm_foc.slx', 'pmsm_dbg.slx');
load_system('pmsm_dbg');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_dbg/ID');
ch.Script = fileread('b0_ident_dbg.m');
ch.ChartUpdate='DISCRETE'; ch.SampleTime='1e-3';
h = get_param('pmsm_dbg/ID','PortHandles');
add_block('simulink/Sinks/To Workspace', 'pmsm_dbg/D', 'VariableName', 'dlog', ...
    'SaveFormat', 'Structure With Time', 'Position', [980 620 1020 650]);
add_line('pmsm_dbg', h.Outport(3), get_param('pmsm_dbg/D','PortHandles').Inport(1));
set_param('pmsm_dbg', 'StopTime', '30');
out = sim('pmsm_dbg');
D = out.dlog.signals.values;
fprintf('列含义: 1upd 2frozen 3active 4tick 5nxtick 6wcnt 7r_ss 8w 9du/amp\n');
fprintf('upd 最大 %.0f  frozen 最大 %.0f  active 出现 %d 次\n', max(D(:,1)), max(D(:,2)), sum(D(:,3)>0));
fprintf('tick 末 %.0f  nxtick 末 %.0f  wcnt 最大 %.0f\n', D(end,4), D(end,5), max(D(:,6)));
fprintf('r_ss 末 %.5f  w 末 %.2f  du/amp 最大 %.2f\n', D(end,7), D(end,8), max(D(:,9)));
close_system('pmsm_dbg', 0); delete('pmsm_dbg.slx');
end
