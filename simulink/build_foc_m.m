% build_foc2.m —— RCESO 自带子系统版 FOC
mdl='b0_foc_m'; srcDir='D:\Desktop\RCESO\simulink';
fid=fopen('out_f2.txt','w','n','UTF-8'); p=@(varargin) fprintf(fid,varargin{:});
R=0.175; L=0.57e-3; PSI=0.016833; PP=4; Jm=1.89e-5; IB=6.3069; WR=62.832;
wci=2*pi*150; kpi=L*wci; kii=R*wci; kp=75.36; wo=500; q0=0.98; ka=1-exp(-1e-3/20e-3);
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl); open_system(mdl);
set_param(mdl,'StopTime','130','Solver','FixedStepDiscrete','FixedStep','0.001','SimTargetLang','C');
A=@(n)[mdl '/' n]; B=@(n)[mdl '/RCESO/' n];
% ---------- RCESO 子系统 ----------
add_block('simulink/Ports & Subsystems/Subsystem',A('RCESO'),'Position',[250 60 420 320]);
delete_block(B('In1')); delete_block(B('Out1'));
for i=1:3
    add_block('simulink/Ports & Subsystems/In1',B(['wref' num2str(i)]),'Position',[20 40+90*(i-1) 50 60+90*(i-1)]);
end
add_block('simulink/Ports & Subsystems/Out1',B('u'),'Position',[640 40 670 60]);
add_block('simulink/Ports & Subsystems/Out1',B('eo_o'),'Position',[640 140 670 160]);
add_block('simulink/Ports & Subsystems/Out1',B('v_o'),'Position',[640 240 670 260]);
add_block('simulink/Ports & Subsystems/Out1',B('up_o'),'Position',[640 340 670 360]);
% 内部块
add_block('simulink/Math Operations/Gain',B('yref'),'Gain',num2str(1/WR),'Position',[90 35 120 65]);
add_block('simulink/Math Operations/Gain',B('ypu'),'Gain',num2str(1/WR),'Position',[90 125 120 155]);
add_block('simulink/Math Operations/Sum',B('en'),'Inputs','+-','Position',[160 35 180 75]);
add_block('simulink/Math Operations/Gain',B('gkpe'),'Gain',num2str(kp),'Position',[200 40 230 70]);
add_block('simulink/Math Operations/Sum',B('us'),'Inputs','+--','Position',[260 30 280 80]);
add_block('simulink/Math Operations/Divide',B('udiv'),'Position',[310 40 340 70]);
add_block('simulink/Discrete/Unit Delay',B('uprev'),'SampleTime','0.001','InitialCondition','0','Position',[380 45 410 75]);
add_block('simulink/Math Operations/Sum',B('eo'),'Inputs','+-','Position',[160 150 180 190]);
add_block('simulink/Math Operations/Gain',B('g2wo'),'Gain',num2str(2*wo),'Position',[200 150 230 180]);
add_block('simulink/Math Operations/Gain',B('gwo2'),'Gain',num2str(wo*wo),'Position',[200 250 230 280]);
add_block('simulink/Math Operations/Product',B('b0u'),'Inputs','2','Position',[260 180 290 210]);
add_block('simulink/Math Operations/Sum',B('z1s'),'Inputs','++++','Position',[320 160 340 250]);
add_block('simulink/Discrete/Discrete-Time Integrator',B('z1int'),'SampleTime','0.001','InitialCondition','0','Position',[370 190 400 220]);
add_block('simulink/Discrete/Discrete-Time Integrator',B('z2int'),'SampleTime','0.001','InitialCondition','0','Position',[320 260 350 290]);
add_block('simulink/Math Operations/Gain',B('g5'),'Gain',num2str(1/0.2),'Position',[200 320 230 350]);
add_block('simulink/Math Operations/Trigonometric Function',B('th'),'Operator','tanh','Position',[250 320 280 350]);
add_block('simulink/Math Operations/Gain',B('gb3'),'Gain','4000','Position',[300 320 330 350]);
add_block('simulink/Discrete/Discrete Transfer Fcn',B('td'),'Numerator','1','Denominator','[1 zeros(1,100)]','SampleTime','0.001','Position',[300 400 340 440]);
add_block('simulink/Math Operations/Gain',B('gq'),'Gain',num2str(q0),'Position',[380 400 410 430]);
add_block('simulink/Math Operations/Sum',B('vchi'),'Inputs','++','Position',[440 330 460 390]);
add_block('simulink/Math Operations/Sum',B('dv'),'Inputs','+-','Position',[490 340 510 380]);
add_block('simulink/Math Operations/Gain',B('gka'),'Gain',num2str(ka,10),'Position',[530 345 560 375]);
add_block('simulink/Discrete/Discrete-Time Integrator',B('vint'),'SampleTime','0.001','InitialCondition','0','Position',[580 345 610 375]);
p('RCESO blocks ok\n');
% ---------- 对象与电流环 ----------
add_block('simulink/Math Operations/Sum',A('sumu'),'Inputs','++','Position',[470 60 490 110]);
add_block('simulink/Math Operations/Gain',A('giqr'),'Gain',num2str(IB),'Position',[520 65 550 95]);
add_block('simulink/Math Operations/Sum',A('eq'),'Inputs','+-','Position',[590 60 610 100]);
add_block('simulink/Math Operations/Gain',A('gkp'),'Gain',num2str(kpi),'Position',[640 45 670 75]);
add_block('simulink/Discrete/Discrete-Time Integrator',A('iqint'),'SampleTime','0.001','InitialCondition','0','Position',[640 100 670 130]);
add_block('simulink/Math Operations/Gain',A('gki'),'Gain',num2str(kii),'Position',[690 100 720 130]);
add_block('simulink/Math Operations/Sum',A('vq'),'Inputs','++','Position',[750 60 770 120]);
add_block('simulink/Math Operations/Gain',A('gRq'),'Gain',num2str(R),'Position',[700 210 730 240]);
add_block('simulink/Math Operations/Sum',A('diqnum'),'Inputs','+--','Position',[780 190 800 270]);
add_block('simulink/Math Operations/Gain',A('giL'),'Gain',num2str(1/L),'Position',[820 210 850 240]);
add_block('simulink/Discrete/Discrete-Time Integrator',A('iqp'),'SampleTime','0.001','InitialCondition','0','Position',[870 210 900 240]);
add_block('simulink/Math Operations/Gain',A('gwe'),'Gain',num2str(PP),'Position',[640 330 670 360]);
add_block('simulink/Math Operations/Product',A('emf'),'Inputs','2','Position',[700 330 730 360]);
add_block('simulink/Math Operations/Gain',A('gkt'),'Gain',num2str(1.5*PP*PSI),'Position',[870 340 900 370]);
add_block('simulink/Sources/Constant',A('tl'),'Value','0.02','SampleTime','0.001','Position',[820 400 860 430]);
add_block('simulink/Math Operations/Sum',A('dw'),'Inputs','+-','Position',[930 350 950 400]);
add_block('simulink/Math Operations/Gain',A('gJ'),'Gain',num2str(1/Jm),'Position',[970 360 1000 390]);
add_block('simulink/Discrete/Discrete-Time Integrator',A('wint'),'SampleTime','0.001','InitialCondition','0','Position',[1020 360 1050 390]);
add_block('simulink/Math Operations/Gain',A('grpm'),'Gain',num2str(30/pi),'Position',[1080 360 1110 390]);
add_block('simulink/Sources/Constant',A('wref'),'Value',num2str(WR),'SampleTime','0.001','Position',[180 400 220 430]);
p('plant blocks ok\n');
% ---------- C Caller ----------
add_block('simulink/User-Defined Functions/MATLAB Function',A('C'),'Position',[700 20 820 180]);
rt2 = sfroot; ch2 = rt2.find('-isa','Stateflow.EMChart','Path',A('C'));
ch2.Script = fileread([srcDir '\b0_ident_m.m']);
p('ML function set\n');
% MATLAB Function: 无 FunctionName 参数
add_block('simulink/Math Operations/Gain',A('giqp'),'Gain',num2str(1/IB),'Position',[560 15 590 45]);
% RCESO 输出端口顺序: 1=u 2=eo_o 3=v_o 4=up_o
nm={'fiq','fu','fom','fe1','fv'}; sg={'giqp/1','RCESO/4','grpm/1','RCESO/2','RCESO/3'};
for i=1:5
    add_block('simulink/Signal Attributes/Data Type Conversion',A(nm{i}),'OutDataTypeStr','single','Position',[620 10+40*(i-1) 660 35+40*(i-1)]);
    add_line(mdl,sg{i},[nm{i} '/1'],'autorouting','on');
    add_line(mdl,[nm{i} '/1'],['C/' num2str(i)],'autorouting','on');
end
% 总线拆分：b0 / du 都是纯输出

add_block('simulink/Signal Attributes/Data Type Conversion',A('b0d'),'OutDataTypeStr','double','Position',[900 40 940 70]);
add_line(mdl,'C/1','b0d/1','autorouting','on');
add_block('simulink/Discrete/Unit Delay',A('b0z'),'SampleTime','0.001','InitialCondition','400','Position',[930 40 960 70]);
add_line(mdl,'b0d/1','b0z/1','autorouting','on');
add_block('simulink/Signal Attributes/Data Type Conversion',A('dup'),'OutDataTypeStr','double','Position',[860 220 900 250]);
add_line(mdl,'C/2','dup/1','autorouting','on');
add_line(mdl,'RCESO/1','sumu/1','autorouting','on');
add_line(mdl,'dup/1','sumu/2','autorouting','on');
% ---------- RCESO 外部接线 ----------
add_line(mdl,'wref/1','RCESO/1','autorouting','on');
add_line(mdl,'wint/1','RCESO/2','autorouting','on');
add_line(mdl,'b0z/1','RCESO/3','autorouting','on');
p('outer wiring ok\n');
% ---------- RCESO 内部接线（以子系统为系统参数，用相对路径） ----------
RCS = [mdl '/RCESO'];
add_line(RCS,'wref1/1','yref/1','autorouting','on');
add_line(RCS,'wref2/1','ypu/1','autorouting','on');
add_line(RCS,'yref/1','en/1','autorouting','on');
add_line(RCS,'z1int/1','en/2','autorouting','on');
add_line(RCS,'en/1','gkpe/1','autorouting','on');
add_line(RCS,'gkpe/1','us/1','autorouting','on');
add_line(RCS,'z2int/1','us/2','autorouting','on');
add_line(RCS,'vint/1','us/3','autorouting','on');
add_line(RCS,'us/1','udiv/1','autorouting','on');
add_line(RCS,'wref3/1','udiv/2','autorouting','on');
add_line(RCS,'udiv/1','u/1','autorouting','on');
add_line(RCS,'udiv/1','uprev/1','autorouting','on');
add_line(RCS,'uprev/1','up_o/1','autorouting','on');
add_line(RCS,'uprev/1','b0u/2','autorouting','on');
add_line(RCS,'wref3/1','b0u/1','autorouting','on');
add_line(RCS,'ypu/1','eo/1','autorouting','on');
add_line(RCS,'z1int/1','eo/2','autorouting','on');
add_line(RCS,'eo/1','eo_o/1','autorouting','on');
add_line(RCS,'eo/1','g2wo/1','autorouting','on');
add_line(RCS,'eo/1','gwo2/1','autorouting','on');
add_line(RCS,'eo/1','g5/1','autorouting','on');
add_line(RCS,'g2wo/1','z1s/4','autorouting','on');
add_line(RCS,'b0u/1','z1s/1','autorouting','on');
add_line(RCS,'vint/1','z1s/2','autorouting','on');
add_line(RCS,'z2int/1','z1s/3','autorouting','on');
add_line(RCS,'z1s/1','z1int/1','autorouting','on');
add_line(RCS,'gwo2/1','z2int/1','autorouting','on');
add_line(RCS,'g5/1','th/1','autorouting','on');
add_line(RCS,'th/1','gb3/1','autorouting','on');
add_line(RCS,'vint/1','td/1','autorouting','on');
add_line(RCS,'td/1','gq/1','autorouting','on');
add_line(RCS,'gb3/1','vchi/1','autorouting','on');
add_line(RCS,'gq/1','vchi/2','autorouting','on');
add_line(RCS,'vchi/1','dv/1','autorouting','on');
add_line(RCS,'vint/1','dv/2','autorouting','on');
add_line(RCS,'dv/1','gka/1','autorouting','on');
add_line(RCS,'gka/1','vint/1','autorouting','on');
add_line(RCS,'vint/1','v_o/1','autorouting','on');
p('inner wiring ok\n');
% ---------- 对象接线 ----------
add_line(mdl,'sumu/1','giqr/1','autorouting','on');
add_line(mdl,'giqr/1','eq/1','autorouting','on');
add_line(mdl,'iqp/1','eq/2','autorouting','on');
add_line(mdl,'eq/1','gkp/1','autorouting','on');
add_line(mdl,'eq/1','iqint/1','autorouting','on');
add_line(mdl,'iqint/1','gki/1','autorouting','on');
add_line(mdl,'gkp/1','vq/1','autorouting','on');
add_line(mdl,'gki/1','vq/2','autorouting','on');
add_line(mdl,'vq/1','diqnum/1','autorouting','on');
add_line(mdl,'iqp/1','gRq/1','autorouting','on');
add_line(mdl,'gRq/1','diqnum/2','autorouting','on');
add_line(mdl,'emf/1','diqnum/3','autorouting','on');
add_line(mdl,'diqnum/1','giL/1','autorouting','on');
add_line(mdl,'giL/1','iqp/1','autorouting','on');
add_line(mdl,'wint/1','gwe/1','autorouting','on');
add_line(mdl,'gwe/1','emf/1','autorouting','on');
add_line(mdl,'iqp/1','gkt/1','autorouting','on');
add_line(mdl,'gkt/1','dw/1','autorouting','on');
add_line(mdl,'tl/1','dw/2','autorouting','on');
add_line(mdl,'dw/1','gJ/1','autorouting','on');
add_line(mdl,'gJ/1','wint/1','autorouting','on');
add_line(mdl,'iqp/1','giqp/1','autorouting','on');
add_line(mdl,'wint/1','grpm/1','autorouting','on');
p('plant wiring ok\n');
% ---------- 记录 ----------
vn={'w_log','b0_log','du_log','iq_log'};
for k=1:4
    add_block('simulink/Sinks/To Workspace',A(['ws' num2str(k)]),'VariableName',vn{k}, ...
        'SaveFormat','Timeseries','SampleTime','0.001','Position',[1150 20+60*(k-1) 1220 50+60*(k-1)]);
end
add_line(mdl,'grpm/1','ws1/1','autorouting','on');
add_line(mdl,'b0d/1','ws2/1','autorouting','on');
add_line(mdl,'C/2','ws3/1','autorouting','on');
add_line(mdl,'iqp/1','ws4/1','autorouting','on');
% 记录辨识器的 5 路输入（供逐点对比回放）
inp = {'log_iq','log_u','log_om','log_e1','log_v'};
src5 = {'giqp/1','RCESO/4','grpm/1','RCESO/2','RCESO/3'};
for k=1:5
    add_block('simulink/Sinks/To Workspace',A(['wi' num2str(k)]),'VariableName',inp{k}, ...
        'SaveFormat','Timeseries','SampleTime','0.001','Position',[1150 300+60*(k-1) 1220 330+60*(k-1)]);
    add_line(mdl,src5{k},['wi' num2str(k) '/1'],'autorouting','on');
end
save('io_src.mat','inp');
save_system(mdl,[srcDir '\b0_foc_m.slx']); p('SAVED\n'); fclose(fid); fprintf('SAVED\n');
try
    out=sim(mdl);
    b=out.b0_log; w=out.w_log; d=out.du_log;
    fid2=fopen('out_f2s.txt','w','n','UTF-8');
    fprintf(fid2,'SIM_OK b0=%.2f w=%.2f du_max=%.4f (真值 536.40)\n', b.Data(end), w.Data(end), max(abs(d.Data)));
    fprintf(fid2,'b0轨迹: ');
    for kk=[20000 40000 60000 80000 100000 120000]
        fprintf(fid2,'%.0f@%ds ', b.Data(kk), round(kk/1000));
    end
    fprintf(fid2,'\n');
    % 保存辨识器的 5 路输入，供 C/ML 逐点对比
    iqd = out.log_iq.Data; ud = out.log_u.Data; omd = out.log_om.Data;
    e1d = out.log_e1.Data; vd = out.log_v.Data;
    save([srcDir '\foc_io.mat'],'iqd','ud','omd','e1d','vd');
    fclose(fid2); fprintf('SIM_OK\n');
catch e
    fprintf('SIM_FAIL: %s\n', e.message);
    for i=1:numel(e.cause), fprintf('  C%d: %s\n', i, e.cause{i}.message); end
end