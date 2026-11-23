% probe5b.m
fid = fopen('out_p5.txt','w','n','UTF-8');
bs = Simulink.Bus;
e1 = Simulink.BusElement; e1.Name='b0'; e1.DataType='single';
e2 = Simulink.BusElement; e2.Name='du'; e2.DataType='single';
bs.Elements=[e1 e2]; assignin('base','b0_res_t',bs);
mdl='b0_closed';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system(fullfile(pwd,[mdl '.slx']));
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path',[mdl '/ctrl_rceso']);
ch.Script = fileread('ctrl_rceso.m');
fprintf(fid,'script_len=%d\n', numel(ch.Script));
try
    set_param(mdl,'SimulationCommand','update');
    fprintf(fid,'UPDATE_OK\n');
catch e
    fprintf(fid,'ERR %s\n', e.message);
    for i=1:numel(e.cause)
        fprintf(fid,' C%d %s\n', i, e.cause{i}.message);
    end
end
% 若更新通过，跑仿真
try
    out = sim(mdl);
    b=out.b0_log; w=out.w_log; d=out.du_log;
    fprintf(fid,'SIM_OK b0_end=%.1f b0_20_40=%.1f w_end=%.2f std_w=%.2f du_max=%.4f\n', ...
        b.Data(end), mean(b.Data(20000:40000)), w.Data(end), std(w.Data(40000:60000)), max(abs(d.Data)));
    figure('Visible','off');
    subplot(2,1,1); plot(b.Time,b.Data,'LineWidth',1.3); grid on; ylabel('b0'); title('b0');
    subplot(2,1,2); plot(w.Time,w.Data); grid on; ylabel('w/rpm'); xlabel('t/s');
    print('-dpng','-r110','fig_closed.png');
    fprintf(fid,'FIG_OK\n');
catch e
    fprintf(fid,'SIMERR %s\n', e.message);
end
fclose(fid);
