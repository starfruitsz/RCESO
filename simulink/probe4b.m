% probe4b.m
fid = fopen('out_cl2.txt','w','n','UTF-8');
% 正确调用控制器（三输出）
try
    [uu, ee, vv] = ctrl_rceso(600, 0, 400);
    fprintf(fid,'CTRL_OK u=%.5f e1=%.5f v=%.5f\n', uu, ee, vv);
catch e
    fprintf(fid,'CTRL_ERR %s\n', e.message);
end
% 定义总线并加载模型
bs = Simulink.Bus;
e1 = Simulink.BusElement; e1.Name='b0'; e1.DataType='single';
e2 = Simulink.BusElement; e2.Name='du'; e2.DataType='single';
bs.Elements = [e1 e2]; assignin('base','b0_res_t',bs);
mdl='b0_closed';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system(fullfile(pwd,[mdl '.slx']));
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
