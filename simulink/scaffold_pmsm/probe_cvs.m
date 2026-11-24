function probe_cvs()
mdl = 'cvs_probe'; close_system(mdl, 0); new_system(mdl); open_system(mdl);
NL = newline;
pmPath = ['sps_lib/Electrical Machines/Permanent Magnet' NL 'Synchronous Machine'];
add_block('sps_lib/Sources/Controlled Voltage Source', [mdl '/cvs']);
add_block(pmPath, [mdl '/PMSM']);
for nm = {'cvs','PMSM'}
    b = [mdl '/' nm{1}];
    fprintf('=== %s ===\n', nm{1});
    try
        fprintf('  Ports = %s\n', mat2str(get_param(b,'Ports')));
    catch e
        fprintf('  Ports 读取失败: %s\n', e.message);
    end
    ph = get_param(b,'PortHandles');
    fn = fieldnames(ph);
    for i = 1:numel(fn)
        h = ph.(fn{i});
        if ~isempty(h)
            fprintf('  %-8s n=%d\n', fn{i}, numel(h));
        end
    end
    try
        pc = get_param(b,'PortConnectivity');
        fprintf('  PortConnectivity 类型: %s\n', strjoin({pc.Type}, ','));
    catch
    end
end
close_system(mdl, 0);
end
