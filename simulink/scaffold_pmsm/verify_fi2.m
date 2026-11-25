function verify_fi2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
ch.Script = fileread('../b0_ident_m.m');
ch.ChartUpdate='DISCRETE'; ch.SampleTime='1e-3';
save_system('pmsm_foc');
% 1) double 输入基线
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
fprintf('A double 基线 : b0 %.1f  du %.4f\n', out.blog.signals.values(end), max(abs(out.dulog.signals.values(:))));
% 2) 定点输入
copyfile('pmsm_foc.slx', 'pmsm_fi.slx');
load_system('pmsm_fi');
h = @(b) get_param(['pmsm_fi/' b], 'PortHandles');
ph = h('ID');
for k = 1:numel(ph.Inport)
    l = get_param(ph.Inport(k), 'Line');
    if ~isempty(l) && l > 0
        src = get_param(l, 'SrcPortHandle'); delete_line(l);
        nm = sprintf('pmsm_fi/fx%d', k);
        add_block('simulink/Signal Attributes/Data Type Conversion', nm, ...
            'OutDataTypeStr', 'fixdt(1,16,12)', 'Position', [860 300+30*k 900 320+30*k]);
        hc = get_param(nm, 'PortHandles');
        add_line('pmsm_fi', src, hc.Inport(1));
        add_line('pmsm_fi', hc.Outport(1), ph.Inport(k));
    end
end
set_param('pmsm_fi', 'StopTime', '130');
try
    out = sim('pmsm_fi');
    fprintf('E 定点输入   : b0 %.1f  du %.4f\n', out.blog.signals.values(end), max(abs(out.dulog.signals.values(:))));
catch e
    fprintf('E 定点失败: %s\n', e.message);
    for i = 1:min(2,numel(e.cause)), fprintf('   %s\n', e.cause{i}.message); end
end
close_system('pmsm_fi', 0); delete('pmsm_fi.slx');
end
