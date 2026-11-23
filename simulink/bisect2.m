% bisect2.m
fid = fopen('out_bi2.txt','w','n','UTF-8');
bs = Simulink.Bus;
ea = Simulink.BusElement; ea.Name='b0'; ea.DataType='single';
eb = Simulink.BusElement; eb.Name='du'; eb.DataType='single';
bs.Elements=[ea eb]; assignin('base','b0_res_t',bs);
mdl='b0_closed';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system(fullfile(pwd,[mdl '.slx']));
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path',[mdl '/ctrl_rceso']);

base = strsplit(fileread('ctrl_rceso.m'), sprintf('\n'));
full = strjoin(base, sprintf('\n'));
% V1: 去掉 %#codegen
v1 = strrep(full, '%#codegen', '');
% V2: 去掉 single 转换
v2 = regexprep(full, 'u = single\(u\);.*\n.*\n.*\n', '');
% V3: vbuf 改标量
v3 = strrep(full, 'vbuf = zeros(1,50);', 'vbuf = 0;');
v3 = strrep(v3, 'vd = vbuf(vi);', 'vd = vbuf;');
v3 = strrep(v3, 'vbuf(vi) = v;', 'vbuf = v;');

cases = {v1,'no_codegen'; v2,'no_single'; v3,'scalar_buf'; full,'full'};
for k=1:size(cases,1)
    ch.Script = cases{k,1};
    ok = true;
    try
        set_param(mdl,'SimulationCommand','update');
    catch e
        ok = false;
        fprintf(fid,'%s FAIL: %s\n', cases{k,2}, e.message);
    end
    if ok
        fprintf(fid,'%s OK\n', cases{k,2});
        break;
    end
end
fclose(fid);
