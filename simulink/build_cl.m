% build_cl.m —— 完整 ADRC 闭环 + C Caller b0 辨识
mdl = 'b0_closed'; srcDir = 'D:\Desktop\RCESO\simulink';
fid = fopen('out_cl.txt','w','n','UTF-8'); p=@(varargin) fprintf(fid,varargin{:});
if bdIsLoaded(mdl), close_system(mdl,0); end
bs = Simulink.Bus;
e1 = Simulink.BusElement; e1.Name='b0'; e1.DataType='single';
e2 = Simulink.BusElement; e2.Name='du'; e2.DataType='single';
bs.Elements = [e1 e2]; assignin('base','b0_res_t',bs);
new_system(mdl);
set_param(mdl,'StopTime','60','Solver','FixedStepDiscrete','FixedStep','0.001','SimTargetLang','C');
set_param(mdl,'SimCustomHeaderCode', [ ...
  'typedef struct { float b0; float du; } b0_res_t;' char(10) ...
  'extern b0_res_t b0_ident_res(float iq, float u, float omega, float e1, float v);']);
set_param(mdl,'SimUserSources', sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c',srcDir,srcDir));
set_param(mdl,'SimUserIncludeDirs', srcDir);

% ---- 控制器 ----
add_block('simulink/User-Defined Functions/MATLAB Function',[mdl '/ctrl_rceso'], ...
    'Position',[250 70 360 160]);
rt = sfroot;
ch = rt.find('-isa','Stateflow.EMChart','Path',[mdl '/ctrl_rceso']);
ch.Script = fileread([srcDir '\ctrl_rceso.m']);
p('ctrl script set\n');
% ---- 对象（原生积木）：y' = b*iq + f, iq = ucmd 延迟一拍 ----
add_block('simulink/Discrete/Unit Delay',[mdl '/udiq'],'InitialCondition','0', ...
    'SampleTime','0.001','Position',[520 105 560 135]);
add_block('simulink/Math Operations/Gain',[mdl '/gb'],'Gain','380', ...
    'OutDataTypeStr','single','Position',[600 105 640 135]);
add_block('simulink/Sources/Constant',[mdl '/f'],'Value','-0.05','SampleTime','0.001', ...
    'OutDataTypeStr','single','Position',[600 165 640 195]);
add_block('simulink/Math Operations/Sum',[mdl '/sumf'],'Inputs','++', ...
    'OutDataTypeStr','single','Position',[680 115 700 185]);
add_block('simulink/Discrete/Discrete-Time Integrator',[mdl '/yint'], ...
    'InitialCondition','0','OutDataTypeStr','single','SampleTime','0.001', ...
    'Position',[730 120 770 180]);
add_block('simulink/Math Operations/Gain',[mdl '/gw'],'Gain','600', ...
    'OutDataTypeStr','single','Position',[800 130 840 170]);
p('plant blocks ok\n');
% ---- 输入 ----
add_block('simulink/Sources/Constant',[mdl '/wref'],'Value','600','SampleTime','0.001','OutDataTypeStr','single','Position',[80 40 120 66]);
% ---- 求和 u+du ----
add_block('simulink/Math Operations/Sum',[mdl '/sumu'],'Inputs','++','OutDataTypeStr','single','Position',[420 105 435 135]);
% ---- C Caller ----
add_block('simulink/User-Defined Functions/C Caller',[mdl '/C'],'Position',[250 300 380 460]);
set_param([mdl '/C'],'FunctionName','b0_ident_res');
p(['PORTS=' mat2str(get_param([mdl '/C'],'Ports')) '\n']);
add_block('simulink/Signal Routing/Bus Selector',[mdl '/BS'],'OutputSignals','b0,du','Position',[420 330 440 410]);
% ---- 记录 ----
add_block('simulink/Sinks/To Workspace',[mdl '/w_ws'],'VariableName','w_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[760 30 830 60]);
add_block('simulink/Sinks/To Workspace',[mdl '/b0_ws'],'VariableName','b0_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[760 100 830 130]);
add_block('simulink/Sinks/To Workspace',[mdl '/du_ws'],'VariableName','du_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[760 170 830 200]);
add_block('simulink/Sinks/To Workspace',[mdl '/u_ws'],'VariableName','u_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[760 240 830 270]);
add_block('simulink/Sinks/Scope',[mdl '/Scope'],'NumInputPorts','2','Position',[880 60 940 200]);
% ---- 连线 ----
add_line(mdl,'wref/1','ctrl_rceso/1','autorouting','on');
add_line(mdl,'ctrl_rceso/1','sumu/1','autorouting','on');
add_line(mdl,'BS/2','sumu/2','autorouting','on');
add_line(mdl,'sumu/1','udiq/1','autorouting','on');
add_line(mdl,'udiq/1','gb/1','autorouting','on');
add_line(mdl,'gb/1','sumf/1','autorouting','on');
add_line(mdl,'f/1','sumf/2','autorouting','on');
add_line(mdl,'sumf/1','yint/1','autorouting','on');
add_line(mdl,'yint/1','gw/1','autorouting','on');
add_line(mdl,'gw/1','ctrl_rceso/2','autorouting','on');
add_line(mdl,'BS/1','ctrl_rceso/3','autorouting','on');
add_line(mdl,'udiq/1','C/1','autorouting','on');
add_line(mdl,'ctrl_rceso/1','C/2','autorouting','on');
add_line(mdl,'gw/1','C/3','autorouting','on');
add_line(mdl,'ctrl_rceso/2','C/4','autorouting','on');
add_line(mdl,'ctrl_rceso/3','C/5','autorouting','on');
add_line(mdl,'C/1','BS/1','autorouting','on');
add_line(mdl,'gw/1','w_ws/1','autorouting','on');
add_line(mdl,'BS/1','b0_ws/1','autorouting','on');
add_line(mdl,'BS/2','du_ws/1','autorouting','on');
add_line(mdl,'ctrl_rceso/1','u_ws/1','autorouting','on');
add_line(mdl,'gw/1','Scope/1','autorouting','on');
add_line(mdl,'BS/1','Scope/2','autorouting','on');
save_system(mdl,[srcDir '\b0_closed.slx']); p('SAVED\n'); fclose(fid); fprintf('SAVED\n');
try
    out = sim(mdl);
    fid2=fopen('out_cls.txt','w','n','UTF-8');
    b=out.b0_log; w=out.w_log; d=out.du_log;
    fprintf(fid2,'SIM_OK b0_end=%.1f  b0_20_40=%.1f  w_end=%.2f  w_rms_40_60=%.3f\n', ...
        b.Data(end), mean(b.Data(20000:40000)), w.Data(end), std(w.Data(40000:60000)));
    fprintf(fid2,'du_max=%.4f\n', max(abs(d.Data)));
    figure('Visible','off');
    subplot(2,1,1); plot(b.Time,b.Data,'LineWidth',1.3); grid on; ylabel('b0'); title('b0 (C Caller, closed loop)');
    subplot(2,1,2); plot(w.Time,w.Data); grid on; ylabel('w / rpm'); xlabel('t / s');
    print('-dpng','-r110',[srcDir '\fig_closed.png']); fprintf(fid2,'FIG_OK\n'); fclose(fid2);
    fprintf('SIM_OK\n');
catch e
    fprintf('SIM_FAIL: %s\n', e.message);
    for i=1:numel(e.cause), fprintf('  C%d: %s\n', i, e.cause{i}.message); end
end