% build_min3.m
mdl = 'b0_min'; srcDir = 'D:\Desktop\RCESO\simulink';
fid = fopen('out_b3.txt','w','n','UTF-8'); p=@(varargin) fprintf(fid,varargin{:});
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl);
set_param(mdl,'StopTime','12','Solver','FixedStepDiscrete','FixedStep','0.001','SimTargetLang','C');
set_param(mdl,'SimCustomHeaderCode', ...
   'extern void b0_ident_sim(float iq, float u, float omega, float e1, float v, float *b0, float *du);');
set_param(mdl,'SimUserSources', sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c',srcDir,srcDir));
set_param(mdl,'SimUserIncludeDirs', srcDir);
add_block('simulink/User-Defined Functions/C Caller',[mdl '/C']);
av = get_param([mdl '/C'],'AvailableFunctions');
p('AVAIL=[%s]\n', strjoin(av,'|'));
try
    set_param([mdl '/C'],'FunctionName','b0_ident_sim');
    p('FN_OK\n');
catch e
    p('FN_FAIL %s\n', e.message);
end
p('PORTS=%s\n', mat2str(get_param([mdl '/C'],'Ports')));
save_system(mdl,[srcDir '\b0_min3.slx']);
p('SAVED\n'); fclose(fid); fprintf('SAVED\n');

set_param(mdl,'StopTime','0.6');
try
    set_param(mdl,'SimulationCommand','update');
    fprintf('UPDATE_OK\n');
catch e
    fprintf('UPDATE_FAIL: %s\n', e.message);
    for i=1:numel(e.cause)
        fprintf('  CAUSE%d: %s\n', i, e.cause{i}.message);
    end
end
fclose('all');
