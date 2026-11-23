% build_min5.m —— 结构体返回版最小模型
mdl = 'b0_res'; srcDir = 'D:\Desktop\RCESO\simulink';
fid = fopen('out_b5.txt','w','n','UTF-8'); p=@(varargin) fprintf(fid,varargin{:});
if bdIsLoaded(mdl), close_system(mdl,0); end
% 注册总线类型 b0_res_t
bs = Simulink.Bus;
e1 = Simulink.BusElement; e1.Name = 'b0'; e1.DataType = 'single';
e2 = Simulink.BusElement; e2.Name = 'du'; e2.DataType = 'single';
bs.Elements = [e1 e2];
assignin('base','b0_res_t',bs);   % 变量名即总线类型名
new_system(mdl);
set_param(mdl,'StopTime','12','Solver','FixedStepDiscrete','FixedStep','0.001','SimTargetLang','C');
set_param(mdl,'SimCustomHeaderCode', [ ...
  'typedef struct { float b0; float du; } b0_res_t;' char(10) ...
  'extern b0_res_t b0_ident_res(float iq, float u, float omega, float e1, float v);']);
set_param(mdl,'SimUserSources', sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c',srcDir,srcDir));
set_param(mdl,'SimUserIncludeDirs', srcDir);
blk=[mdl '/C'];
add_block('simulink/User-Defined Functions/C Caller',blk,'Position',[380 70 520 230]);
try
    set_param(blk,'FunctionName','b0_ident_res');
    p('FN_OK\n');
catch e
    p('FN_FAIL %s\n', e.message);
end
p('PORTS=%s\n', mat2str(get_param(blk,'Ports')));

add_block('simulink/Sources/Sine Wave',[mdl '/sin'],'Amplitude','0.118','Frequency','2*pi*65','SampleTime','0.001','Position',[30 40 70 66]);
add_block('simulink/Signal Attributes/Data Type Conversion',[mdl '/u'],'OutDataTypeStr','single','Position',[100 40 140 66]);
add_block('simulink/Math Operations/Gain',[mdl '/iq'],'Gain','1','OutDataTypeStr','single','Position',[180 40 220 66]);
add_block('simulink/Sources/Constant',[mdl '/omega'],'Value','600','SampleTime','0.001','OutDataTypeStr','single','Position',[40 100 80 126]);
add_block('simulink/Sources/Constant',[mdl '/e1'],'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[40 150 80 176]);
add_block('simulink/Sources/Constant',[mdl '/v'],'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[40 200 80 226]);
add_block('simulink/Signal Routing/Bus Selector',[mdl '/BS'],'Position',[580 110 600 190]);
try, set_param([mdl '/BS'],'OutputSignals','b0,du'); catch e, p('BS set %s\n', e.message); end
add_block('simulink/Sinks/Scope',[mdl '/Scope'],'NumInputPorts','2','Position',[680 90 740 170]);
add_block('simulink/Sinks/To Workspace',[mdl '/b0ws'],'VariableName','b0_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[650 30 720 60]);
add_block('simulink/Sinks/To Workspace',[mdl '/duws'],'VariableName','du_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[650 210 720 240]);
add_line(mdl,'sin/1','u/1','autorouting','on');
add_line(mdl,'u/1','iq/1','autorouting','on');
add_line(mdl,'u/1','C/1','autorouting','on');
add_line(mdl,'iq/1','C/2','autorouting','on');
add_line(mdl,'omega/1','C/3','autorouting','on');
add_line(mdl,'e1/1','C/4','autorouting','on');
add_line(mdl,'v/1','C/5','autorouting','on');
add_line(mdl,'C/1','BS/1','autorouting','on');
add_line(mdl,'BS/1','Scope/1','autorouting','on');
add_line(mdl,'BS/2','Scope/2','autorouting','on');
add_line(mdl,'BS/1','b0ws/1','autorouting','on');
add_line(mdl,'BS/2','duws/1','autorouting','on');
save_system(mdl,[srcDir '\b0_res.slx']); p('SAVED\n'); fclose(fid); fprintf('SAVED\n');
try
    out = sim(mdl);
    b=out.b0_log; d=out.du_log;
    seg = d.Time>=0.2 & d.Time<=0.42;
    fid2=fopen('out_b5s.txt','w','n','UTF-8');
    fprintf(fid2,'SIM_OK b0_last=%.2f  du_in_burst max|.|=%.4f\n', b.Data(end), max(abs(d.Data(seg))));
    fprintf(fid2,'du 前三拍: %.5f %.5f %.5f\n', d.Data(201),d.Data(202),d.Data(203));
    fig=figure('Visible','off');
    subplot(2,1,1); plot(b.Time,b.Data,'LineWidth',1.2); grid on; ylabel('b0'); title('b0 (struct return)');
    subplot(2,1,2); plot(d.Time,d.Data); grid on; ylabel('deltau'); xlabel('t/s');
    print('-dpng','-r110',[srcDir '\fig_res_model.png']); fprintf(fid2,'FIG_OK\n'); fclose(fid2);
    fprintf('SIM_OK du_max=%.4f\n', max(abs(d.Data(seg))));
catch e
    fprintf('SIM_FAIL: %s\n', e.message);
    for i=1:numel(e.cause), fprintf('  C%d: %s\n', i, e.cause{i}.message); end
end
