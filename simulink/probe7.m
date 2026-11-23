% probe7.m
fid = fopen('out11.txt','w','n','UTF-8');
p = @(varargin) fprintf(fid, varargin{:});
mdl = 'p7';
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl);
srcDir = 'D:\Desktop\RCESO\simulink';
set_param(mdl,'SimUserIncludeDirs',srcDir);

% 试三种写法
forms = { {'b0_ident.c','b0_ident_wrap.c'}, ...
          {[srcDir '\b0_ident.c'],[srcDir '\b0_ident_wrap.c']} };
for k=1:numel(forms)
    try
        set_param(mdl,'SimUserSources',forms{k});
        p('FORM%d set OK\n',k);
    catch e
        p('FORM%d fail %s\n',k,e.message);
        continue;
    end
    v = get_param(mdl,'SimUserSources');
    if iscell(v), vs = strjoin(v,' ; '); else vs = v; end
    p('  value = [%s]\n', vs);
    blk = [mdl '/C'];
    if ~isempty(find_system(mdl,'SearchDepth',1,'Name','C')), delete_block(blk); end
    add_block('simulink/User-Defined Functions/C Caller',blk);
    set_param(blk,'FunctionName','b0_ident_u');
    av = get_param(blk,'AvailableFunctions');
    if iscell(av), avs = strjoin(av,' | '); else avs = av; end
    p('  AVAIL = [%s]\n', avs);
    p('  PORTS = %s\n', mat2str(get_param(blk,'Ports')));
    if ~isempty(av), break; end
end
bdclose(mdl);
fclose(fid);
