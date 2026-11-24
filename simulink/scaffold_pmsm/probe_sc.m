function probe_sc()
mdl = 'sc_probe'; close_system(mdl, 0); new_system(mdl); open_system(mdl);
NL = newline;
paths = {'ee_lib/Electromechanical/Permanent Magnet/PMSM', ...
         ['ee_lib/Semiconductors & Converters/Converters/Average-Value Voltage Source Converter (Three-Phase)'], ...
         'nesl_utility/Solver Configuration'};
names = {'PMSM','AVC','SolverCfg'};
for i = 1:numel(paths)
    try
        add_block(paths{i}, [mdl '/' names{i}]);
        ph = get_param([mdl '/' names{i}], 'PortHandles');
        fprintf('=== %s OK ===\n', names{i});
        fn = fieldnames(ph);
        for k = 1:numel(fn)
            h = ph.(fn{k});
            if ~isempty(h) && h(1) > 0
                try, nm = get_param(h(1), 'Name'); catch, nm = '?'; end
                fprintf('   port %-10s name=%s\n', fn{k}, nm);
            end
        end
    catch e
        fprintf('=== %s FAIL: %s\n', names{i}, e.message);
    end
end
% 打印 AVC 的参数名
try
    dp = get_param([mdl '/AVC'], 'DialogParameters');
    f = fieldnames(dp);
    fprintf('AVC 参数 %d 个：\n', numel(f));
    for i = 1:min(numel(f), 20)
        try
            v = get_param([mdl '/AVC'], f{i});
            if ischar(v), v = v(1:min(end,50)); end
            if isnumeric(v), v = mat2str(v); end
            fprintf('   %-24s = %s\n', f{i}, v);
        catch
        end
    end
catch e
    fprintf('AVC 参数读取失败: %s\n', e.message);
end
close_system(mdl, 0);
end
