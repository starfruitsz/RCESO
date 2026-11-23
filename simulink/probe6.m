% probe6.m
fid = fopen('out10.txt','w','n','UTF-8');
p = @(varargin) fprintf(fid, varargin{:});
mdl = 'p6';
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl);
set_param(mdl,'SimUserSources','b0_ident.c b0_ident_wrap.c');
set_param(mdl,'SimUserIncludeDirs','D:\Desktop\RCESO\simulink');

f = fieldnames(get_param(mdl,'ObjectParameters'));
p('=== 含 head/custom/sim 的参数 ===\n');
for i=1:numel(f)
    nm = f{i};
    if ~isempty(regexpi(nm,'head|custom|simuser|simcustom'))
        try, v = get_param(mdl,nm); catch, v = '<err>'; end
        if ~ischar(v), v = mat2str(v); end
        p('%-26s = %s\n', nm, v);
    end
end

p('\n=== 尝试设置 header ===\n');
cands = {'SimCustomHeader','CustomHeader','SimCustomInclude','CustomInclude'};
for i=1:numel(cands)
    try
        set_param(mdl,cands{i},'b0_ident_wrap.h');
        p('OK set %s\n', cands{i});
    catch e
        p('FAIL %s : %s\n', cands{i}, e.message);
    end
end

p('\n=== C Caller ===\n');
add_block('simulink/User-Defined Functions/C Caller',[mdl '/C']);
set_param([mdl '/C'],'FunctionName','b0_ident_u');
av = get_param([mdl '/C'],'AvailableFunctions');
if iscell(av), av = strjoin(av,' | '); end
p('AVAIL = [%s]\n', av);
p('PORTS = %s\n', mat2str(get_param([mdl '/C'],'Ports')));
try
    ps = get_param([mdl '/C'],'FunctionPortSpecification');
    disp(ps)
catch e
    p('portSpec err %s\n', e.message);
end
bdclose(mdl);
fclose(fid);
