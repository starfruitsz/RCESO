% probe2.m —— 探查 MEX 编译器与 C Caller 块
fprintf('=== MEX ===\n');
try
    cc = mex.getCompilerConfigurations('C','Selected');
    if isempty(cc)
        fprintf('MEX_NONE\n');
    else
        for i=1:numel(cc)
            fprintf('MEX_OK=%s | %s\n', cc(i).Name, cc(i).Version);
        end
    end
catch e
    fprintf('MEX_ERR %s\n', e.message);
end

fprintf('=== CCALLER ===\n');
load_system('simulink');
new_system('probe2');
paths = {'simulink/User-Defined Functions/C Caller','simulink/C Caller'};
ok=false;
for i=1:numel(paths)
    try
        add_block(paths{i},'probe2/C');
        fprintf('BLOCK_OK %s\n', paths{i});
        ok=true; break;
    catch e
        fprintf('block fail %s : %s\n', paths{i}, e.message);
    end
end
if ok
    p = get_param('probe2/C','ObjectParameters');
    f = fieldnames(p);
    n=0;
    for i=1:numel(f)
        nm = f{i};
        if ~isempty(strfind(lower(nm),'function'))
            fprintf('PARAM %s\n', nm); n=n+1;
        end
    end
    if n==0, fprintf('NO_FUNCTION_PARAM\n'); end
end
bdclose('probe2');
fprintf('=== DONE ===\n');
