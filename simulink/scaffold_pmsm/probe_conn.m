function probe_conn()
mdl = 'sc_probe2'; close_system(mdl, 0); new_system(mdl); open_system(mdl);
add_block('ee_lib/Electromechanical/Permanent Magnet/PMSM', [mdl '/PMSM']);
add_block('ee_lib/Semiconductors & Converters/Converters/Average-Value Voltage Source Converter (Three-Phase)', [mdl '/AVC']);
for nm = {'PMSM','AVC'}
    b = [mdl '/' nm{1}];
    fprintf('=== %s ===\n', nm{1});
    try
        pc = get_param(b, 'PortConnectivity');
        for i = 1:numel(pc)
            fprintf('  #%d Type=%-8s Ports=%s\n', i, pc(i).Type, mat2str(pc(i).Ports));
        end
    catch e
        fprintf('  读取失败 %s\n', e.message);
    end
    try
        ph = get_param(b, 'PortHandles');
        fn = fieldnames(ph);
        for k = 1:numel(fn)
            h = ph.(fn{k});
            if ~isempty(h)
                fprintf('  handle %-10s n=%d\n', fn{k}, numel(h));
            end
        end
    catch
    end
end
close_system(mdl, 0);
end
