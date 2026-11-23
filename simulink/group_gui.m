% group_gui.m —— 在 GUI 模式下封装 RCESO（createSubsystem 需要桌面）
srcDir = 'D:\Desktop\RCESO\simulink';
fid = fopen([srcDir '\out_gui.txt'],'w','n','UTF-8');
mdl = 'b0_foc';
try
    if bdIsLoaded(mdl), close_system(mdl,0); end
    load_system([srcDir '\b0_foc.slx']);
    open_system(mdl);
    drawnow; pause(2);
    A = @(n)[mdl '/' n];
    rceso = {'en','gkpe','us','udiv','uprev','b0u','z1s','z1int','z2int','g2wo', ...
             'gwo2','eo','ypu','g5','th','gb3','td','gq','vchi','dv','gka','vint'};
    blks = cellfun(@(s)A(s), rceso, 'UniformOutput', false);
    Simulink.BlockDiagram.createSubsystem(blks);
    fprintf(fid,'CREATE_OK\n');
    subs = find_system(mdl,'SearchDepth',1,'BlockType','SubSystem');
    renamed = 0;
    for i=1:numel(subs)
        [~,nm] = fileparts(subs{i});
        if strcmp(nm,'Subsystem')
            set_param(subs{i},'Name','RCESO');
            renamed = 1;
            break;
        end
    end
    fprintf(fid,'RENAMED=%d  nsubs=%d\n', renamed, numel(subs));
    save_system(mdl,[srcDir '\b0_foc.slx']);
    fprintf(fid,'SAVED\n');
catch e
    fprintf(fid,'FAIL %s\n', e.message);
end
fclose(fid);
exit
