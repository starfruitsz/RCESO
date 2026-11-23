% build_loop.m —— ADRC 闭环：控制器全积木 + C Caller 辨识
mdl='b0_loop'; srcDir='D:\Desktop\RCESO\simulink';
fid=fopen('out_loop.txt','w','n','UTF-8'); p=@(varargin) fprintf(fid,varargin{:});
% 总线
bs=Simulink.Bus;
ea=Simulink.BusElement; ea.Name='b0'; ea.DataType='single';
eb=Simulink.BusElement; eb.Name='du'; eb.DataType='single';
bs.Elements=[ea eb]; assignin('base','b0_res_t',bs);
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl); open_system(mdl);
set_param(mdl,'StopTime','60','Solver','FixedStepDiscrete','FixedStep','0.001','SimTargetLang','C');
set_param(mdl,'SimCustomHeaderCode', ...
  'extern void b0_ident_sim(float iq, float u, float omega, float e1, float v, float *b0, float *du);');
set_param(mdl,'SimUserSources',sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c',srcDir,srcDir));
set_param(mdl,'SimUserIncludeDirs',srcDir);
% 常数
dt=0.001; kp=75.36; wo=500; b3=4000; zeta=0.2; Q0=0.98; tau0=20e-3;
ka=1-exp(-dt/tau0);
% ---- 给定 ----
add_block('simulink/Sources/Constant',[mdl '/wref'],'Value','600','SampleTime','0.001','Position',[30 30 70 60]);
add_block('simulink/Math Operations/Gain',[mdl '/yref'],'Gain','0.0016666667','Position',[90 30 130 60]);
% ---- e1 = yref - z1 ----
add_block('simulink/Math Operations/Sum',[mdl '/e1'],'Inputs','+-','Position',[170 90 190 130]);
% ---- tanh 通道 ----
add_block('simulink/Math Operations/Gain',[mdl '/g5'],'Gain',num2str(1/zeta),'Position',[220 200 250 230]);
add_block('simulink/Math Operations/Trigonometric Function',[mdl '/th'],'Operator','tanh','Position',[270 200 300 230]);
add_block('simulink/Math Operations/Gain',[mdl '/gb3'],'Gain',num2str(b3),'Position',[320 200 350 230]);
add_block('simulink/Math Operations/Gain',[mdl '/gQ'],'Gain',num2str(Q0),'Position',[320 250 350 280]);
add_block('simulink/Math Operations/Sum',[mdl '/vchi'],'Inputs','++','Position',[380 210 400 270]);
add_block('simulink/Math Operations/Sum',[mdl '/dv'],'Inputs','+-','Position',[430 220 450 260]);
add_block('simulink/Math Operations/Gain',[mdl '/gka'],'Gain',num2str(ka,10),'Position',[480 225 510 255]);
add_block('simulink/Discrete/Discrete-Time Integrator',[mdl '/vint'],'SampleTime','0.001','InitialCondition','0','Position',[540 225 570 255]);
% ---- ESO z1 ----
add_block('simulink/Math Operations/Gain',[mdl '/g2wo'],'Gain',num2str(2*wo),'Position',[220 100 250 130]);
add_block('simulink/Math Operations/Product',[mdl '/b0u'],'Inputs','2','Position',[220 145 250 175]);
add_block('simulink/Math Operations/Sum',[mdl '/z1s'],'Inputs','++++','Position',[320 100 340 200]);
add_block('simulink/Discrete/Discrete-Time Integrator',[mdl '/z1int'],'SampleTime','0.001','InitialCondition','0','Position',[380 130 410 170]);
% ---- ESO z2 ----
add_block('simulink/Math Operations/Gain',[mdl '/gwo2'],'Gain',num2str(wo*wo),'Position',[220 300 250 330]);
add_block('simulink/Discrete/Discrete-Time Integrator',[mdl '/z2int'],'SampleTime','0.001','InitialCondition','0','Position',[300 300 330 330]);
% ---- 控制律 ----
add_block('simulink/Math Operations/Sum',[mdl '/en'],'Inputs','+-','Position',[450 90 470 130]);
add_block('simulink/Math Operations/Gain',[mdl '/gkpe'],'Gain',num2str(kp),'Position',[500 95 530 125]);
add_block('simulink/Math Operations/Sum',[mdl '/us'],'Inputs','+--','Position',[570 110 590 170]);
add_block('simulink/Math Operations/Divide',[mdl '/udiv'],'Position',[620 120 650 160]);
add_block('simulink/Discrete/Unit Delay',[mdl '/uprev'],'SampleTime','0.001','InitialCondition','0','Position',[680 145 710 175]);
% ---- 对象 ----
add_block('simulink/Math Operations/Sum',[mdl '/sumu'],'Inputs','++','Position',[740 120 755 160]);
add_block('simulink/Discrete/Unit Delay',[mdl '/udiq'],'SampleTime','0.001','InitialCondition','0','Position',[780 125 810 155]);
add_block('simulink/Math Operations/Gain',[mdl '/gb'],'Gain','380','Position',[830 125 860 155]);
add_block('simulink/Sources/Constant',[mdl '/f'],'Value','-0.05','SampleTime','0.001','Position',[830 180 860 210]);
add_block('simulink/Math Operations/Sum',[mdl '/sumf'],'Inputs','++','Position',[880 130 900 200]);
add_block('simulink/Discrete/Discrete-Time Integrator',[mdl '/yint'],'SampleTime','0.001','InitialCondition','0','Position',[930 140 960 190]);
add_block('simulink/Math Operations/Gain',[mdl '/gw'],'Gain','600','Position',[990 145 1020 185]);
p('ctrl+plant blocks ok\n');
% ---- C Caller ----
add_block('simulink/User-Defined Functions/C Caller',[mdl '/C'],'Position',[740 330 860 500]);
set_param([mdl '/C'],'FunctionName','b0_ident_sim');
add_block('simulink/Sources/Constant',[mdl '/ic1'],'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[560 680 600 710]);
add_block('simulink/Sources/Constant',[mdl '/ic2'],'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[560 730 600 760]);
add_line(mdl,'ic1/1','C/6','autorouting','on');
add_line(mdl,'ic2/1','C/7','autorouting','on');
% 5 个输入转 single
names={'iq','uu','om','ee','vv'};
sig={'udiq/1','uprev/1','gw/1','e1/1','vint/1'};  % u 用延迟版，与 iq 同刻
for i=1:5
    add_block('simulink/Signal Attributes/Data Type Conversion',[mdl '/' names{i}], ...
        'OutDataTypeStr','single','Position',[560 330+70*(i-1) 600 360+70*(i-1)]);
    add_line(mdl,sig{i},[names{i} '/1'],'autorouting','on');
    add_line(mdl,[names{i} '/1'],['C/' num2str(i)],'autorouting','on');
end
% b0 single->double
add_block('simulink/Signal Attributes/Data Type Conversion',[mdl '/b0d'],'OutDataTypeStr','double','Position',[950 380 990 410]);
add_line(mdl,'C/1','b0d/1','autorouting','on');
add_block('simulink/Discrete/Unit Delay',[mdl '/b0z'],'SampleTime','0.001', ...
    'InitialCondition','400','Position',[1000 430 1030 460]);
add_line(mdl,'b0d/1','b0z/1','autorouting','on');
% ---- 连线 ----
add_line(mdl,'wref/1','yref/1','autorouting','on');
add_line(mdl,'yint/1','e1/1','autorouting','on');   % 观测器误差 = y - z1
add_line(mdl,'z1int/1','e1/2','autorouting','on');
add_line(mdl,'e1/1','g5/1','autorouting','on');
add_line(mdl,'g5/1','th/1','autorouting','on');
add_line(mdl,'th/1','gb3/1','autorouting','on');
% 重复内模延迟：一个机械周期 Td = 100 拍 @600rpm
add_block('simulink/Discrete/Discrete Transfer Fcn',[mdl '/td'], ...
    'Numerator','1','Denominator','[1 zeros(1,100)]','SampleTime','0.001', ...
    'Position',[440 250 470 290]);
add_line(mdl,'vint/1','td/1','autorouting','on');
add_line(mdl,'td/1','gQ/1','autorouting','on');
add_line(mdl,'gb3/1','vchi/1','autorouting','on');
add_line(mdl,'gQ/1','vchi/2','autorouting','on');
add_line(mdl,'vchi/1','dv/1','autorouting','on');
add_line(mdl,'vint/1','dv/2','autorouting','on');
add_line(mdl,'dv/1','gka/1','autorouting','on');
add_line(mdl,'gka/1','vint/1','autorouting','on');
add_line(mdl,'e1/1','g2wo/1','autorouting','on');
add_line(mdl,'b0z/1','b0u/1','autorouting','on');
add_line(mdl,'uprev/1','b0u/2','autorouting','on');
add_line(mdl,'z2int/1','z1s/1','autorouting','on');
add_line(mdl,'b0u/1','z1s/2','autorouting','on');
add_line(mdl,'vint/1','z1s/3','autorouting','on');
add_line(mdl,'g2wo/1','z1s/4','autorouting','on');
add_line(mdl,'z1s/1','z1int/1','autorouting','on');
add_line(mdl,'e1/1','gwo2/1','autorouting','on');
add_line(mdl,'gwo2/1','z2int/1','autorouting','on');
add_line(mdl,'yref/1','en/1','autorouting','on');
add_line(mdl,'z1int/1','en/2','autorouting','on');
add_line(mdl,'en/1','gkpe/1','autorouting','on');
add_line(mdl,'gkpe/1','us/1','autorouting','on');
add_line(mdl,'z2int/1','us/2','autorouting','on');
add_line(mdl,'vint/1','us/3','autorouting','on');
add_line(mdl,'us/1','udiv/1','autorouting','on');
add_line(mdl,'b0z/1','udiv/2','autorouting','on');
add_line(mdl,'udiv/1','uprev/1','autorouting','on');
add_line(mdl,'udiv/1','sumu/1','autorouting','on');
add_line(mdl,'C/2','sumu/2','autorouting','on');
add_line(mdl,'sumu/1','udiq/1','autorouting','on');
add_line(mdl,'udiq/1','gb/1','autorouting','on');
add_line(mdl,'gb/1','sumf/1','autorouting','on');
add_line(mdl,'f/1','sumf/2','autorouting','on');
add_line(mdl,'sumf/1','yint/1','autorouting','on');
add_line(mdl,'yint/1','gw/1','autorouting','on');
% ---- 记录 ----
add_block('simulink/Sinks/To Workspace',[mdl '/w_ws'],'VariableName','w_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[1060 60 1130 90]);
add_block('simulink/Sinks/To Workspace',[mdl '/b0_ws'],'VariableName','b0_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[1060 130 1130 160]);
add_block('simulink/Sinks/To Workspace',[mdl '/du_ws'],'VariableName','du_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[1060 200 1130 230]);
add_block('simulink/Sinks/To Workspace',[mdl '/u_ws'],'VariableName','u_log','SaveFormat','Timeseries','SampleTime','0.001','Position',[1060 270 1130 300]);
add_line(mdl,'gw/1','w_ws/1','autorouting','on');
add_line(mdl,'b0d/1','b0_ws/1','autorouting','on');
add_line(mdl,'C/2','du_ws/1','autorouting','on');
add_line(mdl,'udiv/1','u_ws/1','autorouting','on');
save_system(mdl,[srcDir '\b0_loop.slx']); p('SAVED\n'); fclose(fid); fprintf('SAVED\n');
try
    out=sim(mdl);
    b=out.b0_log; w=out.w_log; d=out.du_log;
    fid2=fopen('out_loops.txt','w','n','UTF-8');
    fprintf(fid2,'SIM_OK b0_end=%.2f b0_20_40=%.2f w_end=%.2f std_w_40_60=%.3f du_max=%.4f\n', ...
      b.Data(end), mean(b.Data(20000:40000)), w.Data(end), std(w.Data(40000:60000)), max(abs(d.Data)));
    figure('Visible','off');
    subplot(3,1,1); plot(w.Time,w.Data); grid on; ylabel('w/rpm'); title('closed loop');
    subplot(3,1,2); plot(b.Time,b.Data,'LineWidth',1.3); grid on; ylabel('b0'); yline(380,'r--');
    subplot(3,1,3); plot(d.Time,d.Data); grid on; ylabel('du'); xlabel('t/s');
    print('-dpng','-r110',[srcDir '\fig_loop.png']); fprintf(fid2,'FIG_OK\n'); fclose(fid2);
    fprintf('SIM_OK\n');
catch e
    fprintf('SIM_FAIL: %s\n', e.message);
    for i=1:numel(e.cause), fprintf('  C%d: %s\n', i, e.cause{i}.message); end
end
