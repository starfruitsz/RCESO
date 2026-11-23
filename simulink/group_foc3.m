% group_foc3.m
srcDir='D:\Desktop\RCESO\simulink'; mdl='b0_foc';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system([srcDir '\b0_foc.slx']);
fid=fopen('out_grp3.txt','w','n','UTF-8');
A=@(n)[mdl '/' n];
% 先试最小例子，确认调用形式
try
    Simulink.BlockDiagram.createSubsystem([mdl '/tl']);
    fprintf(fid,'single OK\n');
catch e
    fprintf(fid,'single FAIL %s\n', e.message);
end
groups = { {'gwe','emf','gRq','diqnum','giL','iqp','gkt','tl','dw','gJ','wint'}, 'PMSM_Plant'; ...
           {'eq','gkp','iqint','gki','vq'}, 'CurrentLoop_PI'; ...
           {'en','gkpe','us','udiv','uprev','b0u','z1s','z1int','z2int','g2wo','gwo2','eo','ypu','g5','th','gb3','td','gq','vchi','dv','gka','vint'}, 'ADRC_SpeedLoop' };
for k=1:size(groups,1)
    blks = cellfun(@(s)A(s), groups{k,1}, 'UniformOutput', false);
    blks = blks(:);
    ok = false;
    try
        Simulink.BlockDiagram.createSubsystem(blks);
        ok = true;
    catch e1
        try
            Simulink.BlockDiagram.createSubsystem(blks, 'Name', groups{k,2});
            ok = true;
        catch e2
            fprintf(fid,'FAIL %s : %s | %s\n', groups{k,2}, e1.message, e2.message);
        end
    end
    if ok
        subs = find_system(mdl,'SearchDepth',1,'BlockType','SubSystem');
        for i=1:numel(subs)
            [~,nm] = fileparts(subs{i});
            if strcmp(nm,'Subsystem'), set_param(subs{i},'Name',groups{k,2}); break; end
        end
        fprintf(fid,'OK %s\n', groups{k,2});
    end
end
save_system(mdl,[srcDir '\b0_foc.slx']);
fprintf(fid,'SAVED\n'); fclose(fid); fprintf('DONE\n');
