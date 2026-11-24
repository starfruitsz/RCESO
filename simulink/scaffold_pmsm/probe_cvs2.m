function probe_cvs2()
mdl = 'p3'; close_system(mdl, 0); new_system(mdl); open_system(mdl);
add_block('sps_lib/Sources/Controlled Voltage Source', [mdl '/cvs']);
dp = get_param([mdl '/cvs'], 'DialogParameters');
f = fieldnames(dp);
for i = 1:numel(f)
    try
        v = get_param([mdl '/cvs'], f{i});
        if ischar(v), v = v(1:min(end,40)); end
        if isnumeric(v), v = mat2str(v); end
        fprintf('%-22s = %s\n', f{i}, v);
    catch
    end
end
close_system(mdl, 0);
end
