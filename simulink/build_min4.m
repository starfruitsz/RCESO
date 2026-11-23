% build_min4.m —— 7 进 2 出（inout 指针），跑通编译与仿真
mdl = 'b0_caller'; srcDir = 'D:\Desktop\RCESO\simulink';
fid = fopen('out_b4.txt','w','n','UTF-8'); p=@(varargin) fprintf(fid,varargin{:});
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl);
set_param(mdl,'StopTime','12','Solver','FixedStepDiscrete','FixedStep','0.001','SimTargetLang','C');
set_param(mdl,'SimCustomHeaderCode', ...
   'extern void b0_ident_sim(float iq, float u, float omega, float e1, float v, float *b0, float *du);');
set_param(mdl,'SimUserSources', sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c',srcDir,srcDir));
set_param(mdl,'SimUserIncludeDirs', srcDir);
blk=[mdl '/C'];
add_block('simulink/User-Defined Functions/C Caller',blk,'Position',[380 70 520 250]);
set_param(blk,'FunctionName','b0_ident_sim');
p('PORTS=%s\n', mat2str(get_param(blk,'Ports')));

add_block('simulink/Sources/Sine Wave',[mdl '/sin'],'Amplitude','0.118','Frequency','2*pi*65','SampleTime','0.001','Position',[30 40 70 66]);
add_block('simulink/Signal Attributes/Data Type Conversion',[mdl '/u'], ...
    'OutDataTypeStr','single','Position',[100 40 140 66]);
add_block('simulink/Math Operations/Gain',[mdl '/iq'],'Gain','1','OutDataTypeStr','single','Position',[180 40 220 66]);
add_block('simulink/Sources/Constant',[mdl '/omega'],'Value','600','SampleTime','0.001','OutDataTypeStr','single','Position',[40 90 80 116]);
add_block('simulink/Sources/Constant',[mdl '/e1'],'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[40 140 80 166]);
add_block('simulink/Sources/Constant',[mdl '/v'],'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[40 190 80 216]);
add_block('simulink/Sources/Constant',[mdl '/ic1'],'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[40 240 80 266]);
add_block('simulink/Sources/Constant',[mdl '/ic2'],'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[40 290 80 316]);
add_block('simulink/Sinks/Scope',[mdl '/Scope'],'NumInputPorts','2','Position',[650 110 710 190]);
add_block('simulink/Sinks/To Workspace',[mdl '/b0ws'],'VariableName','b0_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[590 40 660 70]);
add_block('simulink/Sinks/To Workspace',[mdl '/duws'],'VariableName','du_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[590 240 660 270]);
add_line(mdl,'sin/1','u/1','autorouting','on');
add_line(mdl,'u/1','iq/1','autorouting','on');
add_line(mdl,'u/1','C/1','autorouting','on');
add_line(mdl,'iq/1','C/2','autorouting','on');
add_line(mdl,'omega/1','C/3','autorouting','on');
add_line(mdl,'e1/1','C/4','autorouting','on');
add_line(mdl,'v/1','C/5','autorouting','on');
add_line(mdl,'ic1/1','C/6','autorouting','on');
add_line(mdl,'ic2/1','C/7','autorouting','on');
add_line(mdl,'C/1','Scope/1','autorouting','on');
add_line(mdl,'C/2','Scope/2','autorouting','on');
add_line(mdl,'C/1','b0ws/1','autorouting','on');
add_line(mdl,'C/2','duws/1','autorouting','on');
save_system(mdl,[srcDir '\b0_caller.slx']); p('SAVED\n'); fclose(fid); fprintf('SAVED\n');
try
    out = sim(mdl);
    fprintf('SIM_OK\n');
    b=out.b0_log; d=out.du_log;
    fprintf('b0 last=%.2f  du max=%.4f  du nonzero=%.1f%%\n', b.Data(end), max(abs(d.Data)), 100*sum(d.Data~=0)/numel(d.Data));
    fid2=fopen('out_b4s.txt','w','n','UTF-8');
    fprintf(fid2,'SIM_OK b0=%.2f du_max=%.4f nz=%.1f%%\n', b.Data(end), max(abs(d.Data)), 100*sum(d.Data~=0)/numel(d.Data));
    figure('Visible','off');
    subplot(2,1,1); plot(b.Time,b.Data,'LineWidth',1.2); grid on; ylabel('b0'); title('b0 (C Caller)');
    subplot(2,1,2); plot(d.Time,d.Data); grid on; ylabel('deltau'); xlabel('t/s');
    print('-dpng','-r110',[srcDir '\fig_c_caller.png']); fprintf(fid2,'FIG_OK\n'); fclose(fid2);
catch e
    fprintf('SIM_FAIL: %s\n', e.message);
    for i=1:numel(e.cause), fprintf('  C%d: %s\n', i, e.cause{i}.message); end
end
