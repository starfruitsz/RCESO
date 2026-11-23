% build_min2.m —— 最小验证模型（标量端口 + 关闭源码解析）
mdl = 'b0_min'; srcDir = 'D:\Desktop\RCESO\simulink';
fid = fopen('out_b2.txt','w','n','UTF-8'); p = @(v) fprintf(fid,'%s\n',v);
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl); open_system(mdl);
set_param(mdl,'StopTime','12','Solver','FixedStepDiscrete','FixedStep','0.001','SolverType','Fixed-step','SimTargetLang','C');
set_param(mdl,'SimParseCustomCode','off');
set_param(mdl,'SimCustomHeaderCode', ...
   'extern void b0_ident_sim(float iq, float u, float omega, float e1, float v, float *b0, float *du);');
set_param(mdl,'SimUserSources', sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c',srcDir,srcDir));
set_param(mdl,'SimUserIncludeDirs', srcDir);
p('params ok');
blk=[mdl '/C'];
add_block('simulink/User-Defined Functions/C Caller',blk,'Position',[380 80 520 220]);
set_param(blk,'FunctionName','b0_ident_sim');
p(['PORTS=' mat2str(get_param(blk,'Ports'))]);
add_block('simulink/Sources/Sine Wave',[mdl '/u'],'Amplitude','0.118','Frequency','2*pi*65','SampleTime','0.001','Position',[50 52 90 78]);
add_block('simulink/Math Operations/Gain',[mdl '/iq'],'Gain','1','Position',[140 52 180 78]);
add_block('simulink/Sources/Constant',[mdl '/omega'],'Value','600','SampleTime','0.001','Position',[50 112 90 138]);
add_block('simulink/Sources/Constant',[mdl '/e1'],'Value','0','SampleTime','0.001','Position',[50 172 90 198]);
add_block('simulink/Sources/Constant',[mdl '/v'],'Value','0','SampleTime','0.001','Position',[50 232 90 258]);
add_block('simulink/Sinks/Scope',[mdl '/Scope'],'NumInputPorts','2','Position',[700 90 760 170]);
add_block('simulink/Sinks/To Workspace',[mdl '/b0ws'],'VariableName','b0_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[640 30 710 60]);
add_block('simulink/Sinks/To Workspace',[mdl '/duws'],'VariableName','du_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[640 210 710 240]);
add_line(mdl,'u/1','iq/1','autorouting','on');
add_line(mdl,'u/1','C/1','autorouting','on');
add_line(mdl,'iq/1','C/2','autorouting','on');
add_line(mdl,'omega/1','C/3','autorouting','on');
add_line(mdl,'e1/1','C/4','autorouting','on');
add_line(mdl,'v/1','C/5','autorouting','on');
add_line(mdl,'C/1','Scope/1','autorouting','on');
add_line(mdl,'C/2','Scope/2','autorouting','on');
add_line(mdl,'C/1','b0ws/1','autorouting','on');
add_line(mdl,'C/2','duws/1','autorouting','on');
save_system(mdl,[srcDir '\b0_min.slx']); p('SAVED'); fclose(fid); fprintf('SAVED\n');
try
    out = sim(mdl);
    fid=fopen('out_b2s.txt','w','n','UTF-8');
    fprintf(fid,'SIM_OK\n');
    b=out.b0_log; d=out.du_log;
    fprintf(fid,'b0 n=%d min=%.2f max=%.2f last=%.2f\n',numel(b.Data),min(b.Data),max(b.Data),b.Data(end));
    fprintf(fid,'du min=%.4f max=%.4f nonzero=%.2f%%\n',min(d.Data),max(d.Data),100*sum(d.Data~=0)/numel(d.Data));
    figure('Visible','off');
    subplot(2,1,1); plot(b.Time,b.Data,'LineWidth',1.2); grid on; ylabel('b0'); title('b0');
    subplot(2,1,2); plot(d.Time,d.Data); grid on; ylabel('deltau'); xlabel('t/s');
    print('-dpng','-r110',[srcDir '\fig_min_model.png']);
    fprintf(fid,'FIG_OK\n'); fclose(fid);
    fprintf('SIM_OK\n');
catch e
    fprintf('SIM_FAIL: %s\n', e.message);
end
