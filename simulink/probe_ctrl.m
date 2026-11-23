% probe_ctrl.m
fid = fopen('out_ctrl.txt','w','n','UTF-8');
try
    a = ctrl_rceso(600, 0, 400);
    fprintf(fid,'CTRL_OK u=%.4f e1=%.4f v=%.4f\n', a(1), a(2), a(3));
catch e
    fprintf(fid,'CTRL_ERR %s\n', e.message);
end
% 再试模型 update 的完整错误
mdl='b0_closed';
if ~bdIsLoaded(mdl)
    try, load_system(fullfile(pwd,[mdl '.slx'])); catch e, fprintf(fid,'LOAD_ERR %s\n', e.message); end
end
try
    set_param(mdl,'SimulationCommand','update');
    fprintf(fid,'UPDATE_OK\n');
catch e
    fprintf(fid,'UPDATE_ERR %s\n', e.message);
    for i=1:numel(e.cause)
        fprintf(fid,'  C%d: %s\n', i, e.cause{i}.message);
    end
end
fclose(fid);
