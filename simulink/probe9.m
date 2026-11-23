% probe9.m
fid = fopen('out13.txt','w','n','UTF-8');
p = @(varargin) fprintf(fid, varargin{:});
srcDir = 'D:\Desktop\RCESO\simulink';
mdl = 'p9';
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl);
set_param(mdl,'SimUserIncludeDirs',srcDir);
set_param(mdl,'SimUserSources', sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c', srcDir, srcDir));
blk = [mdl '/C'];
add_block('simulink/User-Defined Functions/C Caller',blk);
set_param(blk,'FunctionName','b0_ident_u');

p('--- update 前 ---\n');
av = get_param(blk,'AvailableFunctions'); p('AVAIL=[%s]\n', strjoin(av,'|'));

try
    set_param(mdl,'SimulationCommand','update');
    p('UPDATE_OK\n');
catch e
    p('UPDATE_FAIL %s\n', e.message);
end
av = get_param(blk,'AvailableFunctions'); p('AVAIL_after_update=[%s]\n', strjoin(av,'|'));
p('PORTS=%s\n', mat2str(get_param(blk,'Ports')));

p('--- SimCustomHeaderCode ---\n');
try
    set_param(mdl,'SimCustomHeaderCode','extern void b0_ident_u(const float in[5], float out[2]);');
    p('HDR_OK\n');
    try, set_param(mdl,'SimulationCommand','update'); catch, end
    av = get_param(blk,'AvailableFunctions'); p('AVAIL_after_hdr=[%s]\n', strjoin(av,'|'));
catch e
    p('HDR_FAIL %s\n', e.message);
end

p('--- mex 测试 ---\n');
try
    if ~exist('_m1.c','file'), copyfile('b0_ident.c','_m1.c'); end
    if ~exist('_m2.c','file'), copyfile('b0_ident_wrap.c','_m2.c'); end
    mex('-c','_m1.c');
    p('MEX_OK\n');
catch e
    p('MEX_FAIL %s\n', e.message);
end
bdclose(mdl);
fclose(fid);
