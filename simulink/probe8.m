% probe8.m
fid = fopen('out12.txt','w','n','UTF-8');
p = @(varargin) fprintf(fid, varargin{:});
mdl = 'p8';
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl);
srcDir = 'D:\Desktop\RCESO\simulink';
set_param(mdl,'SimUserIncludeDirs',srcDir);

forms = { sprintf('b0_ident.c\nb0_ident_wrap.c'), ...
          sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c', srcDir, srcDir) };
for k=1:numel(forms)
    try
        set_param(mdl,'SimUserSources',forms{k});
        p('FORM%d OK\n',k);
    catch e
        p('FORM%d fail %s\n',k,e.message); continue;
    end
    v = get_param(mdl,'SimUserSources');
    p('  raw = [%s]\n', strrep(v, sprintf('\n'), ' / '));
    blk = [mdl '/C'];
    if ~isempty(find_system(mdl,'SearchDepth',1,'Name','C')), delete_block(blk); end
    add_block('simulink/User-Defined Functions/C Caller',blk);
    try
        set_param(blk,'FunctionName','b0_ident_u');
    catch e
        p('  setFn fail %s\n', e.message);
    end
    av = get_param(blk,'AvailableFunctions');
    if iscell(av), avs = strjoin(av,' | '); else avs = av; end
    p('  AVAIL = [%s]\n', avs);
    p('  PORTS = %s\n', mat2str(get_param(blk,'Ports')));
    if ~isempty(av), break; end
end
bdclose(mdl);
fclose(fid);
