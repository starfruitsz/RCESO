% bisect_ctrl.m
fid = fopen('out_bi.txt','w','n','UTF-8');
bs = Simulink.Bus;
e1 = Simulink.BusElement; e1.Name='b0'; e1.DataType='single';
e2 = Simulink.BusElement; e2.Name='du'; e2.DataType='single';
bs.Elements=[e1 e2]; assignin('base','b0_res_t',bs);
mdl='b0_closed';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system(fullfile(pwd,[mdl '.slx']));
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path',[mdl '/ctrl_rceso']);
fprintf(fid,'script_len_before=%d\n', numel(ch.Script));
% 1) 最简函数
ch.Script = sprintf('function [u,e1o,vo] = ctrl_rceso(wref,w,b0)\nu = wref;\ne1o = 0;\nvo = 0;\nend');
try
    set_param(mdl,'SimulationCommand','update');
    fprintf(fid,'TRIVIAL_OK\n');
catch e
    fprintf(fid,'TRIVIAL_ERR %s\n', e.message);
end
% 2) 加 persistent
ch.Script = sprintf(['function [u,e1o,vo] = ctrl_rceso(wref,w,b0)\n' ...
  'persistent z1\nif isempty(z1), z1 = 0; end\nz1 = z1 + 1e-3;\n' ...
  'u = wref - z1; e1o = 0; vo = 0;\nend']);
try
    set_param(mdl,'SimulationCommand','update');
    fprintf(fid,'PERSIST_OK\n');
catch e
    fprintf(fid,'PERSIST_ERR %s\n', e.message);
end
% 3) 加 persistent 向量
ch.Script = sprintf(['function [u,e1o,vo] = ctrl_rceso(wref,w,b0)\n' ...
  'persistent vb vi\nif isempty(vb), vb = zeros(1,50); vi = 1; end\n' ...
  'v = vb(vi); vb(vi) = v + wref; vi = vi + 1;\nif vi > 50, vi = 1; end\n' ...
  'u = v; e1o = 0; vo = 0;\nend']);
try
    set_param(mdl,'SimulationCommand','update');
    fprintf(fid,'VEC_OK\n');
catch e
    fprintf(fid,'VEC_ERR %s\n', e.message);
end
fclose(fid);
