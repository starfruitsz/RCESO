% verify_foc.m
srcDir='D:\Desktop\RCESO\simulink';
fid=fopen('out_ver.txt','w','n','UTF-8');
try
    load_system([srcDir '\b0_foc.slx']);
    fprintf(fid,'LOAD_OK\n');
    set_param('b0_foc','StopTime','8');
    out = sim('b0_foc');
    b=out.b0_log; w=out.w_log; d=out.du_log;
    fprintf(fid,'SIM_OK b0=%.1f w=%.1f du_max=%.4f\n', b.Data(end), w.Data(end), max(abs(d.Data)));
    % 统计颜色
    blks = find_system('b0_foc','SearchDepth',1,'Type','Block');
    nb=0;
    for i=1:numel(blks)
        try
            c=get_param(blks{i},'BackgroundColor');
            if ~strcmp(c,'white'), nb=nb+1; end
        catch
        end
    end
    fprintf(fid,'colored blocks at root: %d\n', nb);
catch e
    fprintf(fid,'FAIL %s\n', e.message);
end
fclose(fid); fprintf('DONE\n');
