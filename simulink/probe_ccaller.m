load_system('simulink');
new_system('probe_mdl');
ok = false;
paths = {'simulink/User-Defined Functions/C Caller', 'simulink/C Caller'};
for i = 1:numel(paths)
    try
        add_block(paths{i}, 'probe_mdl/C');
        fprintf('CCALLER_OK: %s\n', paths{i});
        ok = true;
        break;
    catch e
        fprintf('fail %s: %s\n', paths{i}, e.message);
    end
end
if ok
    p = get_param('probe_mdl/C','ObjectParameters');
    f = fieldnames(p);
    fprintf('n_params=%d\n', numel(f));
    for i = 1:numel(f)
        if ~isempty(strfind(lower(f{i}), 'function')) || ~isempty(strfind(lower(f{i}), 'port'))
            fprintf('  %s\n', f{i});
        end
    end
    s = get_param('probe_mdl/C','Ports');
    disp(s);
end
bdclose('probe_mdl');
