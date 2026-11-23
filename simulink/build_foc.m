% build_foc.m —— PMSM dq(简化 id=0) FOC + ADRC + C Caller 辨识，全 1 ms
mdl='b0_foc'; srcDir='D:\Desktop\RCESO\simulink';
fid=fopen('out_foc.txt','w','n','UTF-8'); p=@(varargin) fprintf(fid,varargin{:});
R=0.175; L=0.57e-3; PSI=0.016833; PP=4; Jm=1.89e-5; IB=6.3069;
wci=2*pi*150; kpi=L*wci; kii=R*wci;
kp=75.36; wo=500; q0=0.98; ka=1-exp(-1e-3/20e-3);
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl); open_system(mdl);
set_param(mdl,'StopTime','150','Solver','FixedStepDiscrete','FixedStep','0.001','SimTargetLang','C');
set_param(mdl,'SimCustomHeaderCode','extern void b0_ident_sim(float iq, float u, float omega, float e1, float v, float *b0, float *du);');
set_param(mdl,'SimUserSources',sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c',srcDir,srcDir));
set_param(mdl,'SimUserIncludeDirs',srcDir);
A=@(n) [mdl '/' n];
% ---------- ADRC 外环 ----------
add_block('simulink/Sources/Constant',A('wref'),'Value','62.832','SampleTime','0.001','Position',[20 20 60 50]);
add_block('simulink/Math Operations/Gain',A('yref'),'Gain',num2str(1/62.832),'Position',[80 20 120 50]);  % 600rpm=62.83rad/s
add_block('simulink/Math Operations/Sum',A('en'),'Inputs','+-','Position',[160 60 180 100]);
add_block('simulink/Math Operations/Gain',A('gkpe'),'Gain',num2str(kp),'Position',[200 65 230 95]);
add_block('simulink/Math Operations/Sum',A('us'),'Inputs','+--','Position',[260 70 280 120]);
add_block('simulink/Math Operations/Divide',A('udiv'),'Position',[310 80 340 120]);
add_block('simulink/Discrete/Unit Delay',A('uprev'),'SampleTime','0.001','InitialCondition','0','Position',[360 100 390 130]);
add_block('simulink/Math Operations/Sum',A('eo'),'Inputs','+-','Position',[160 300 180 340]);
add_block('simulink/Math Operations/Gain',A('g2wo'),'Gain',num2str(2*wo),'Position',[200 250 230 280]);
add_block('simulink/Math Operations/Gain',A('gwo2'),'Gain',num2str(wo*wo),'Position',[200 340 230 370]);
add_block('simulink/Math Operations/Product',A('b0u'),'Inputs','2','Position',[200 190 230 220]);
add_block('simulink/Math Operations/Sum',A('z1s'),'Inputs','++++','Position',[260 200 280 290]);
add_block('simulink/Math Operations/Gain',A('ypu'),'Gain',num2str(1/62.832),'Position',[120 300 150 330]);
add_block('simulink/Discrete/Discrete-Time Integrator',A('z1int'),'SampleTime','0.001','InitialCondition','0','Position',[310 230 340 270]);
add_block('simulink/Discrete/Discrete-Time Integrator',A('z2int'),'SampleTime','0.001','InitialCondition','0','Position',[260 340 290 370]);
add_block('simulink/Math Operations/Gain',A('g5'),'Gain',num2str(1/0.2),'Position',[200 400 230 430]);
add_block('simulink/Math Operations/Trigonometric Function',A('th'),'Operator','tanh','Position',[250 400 280 430]);
add_block('simulink/Math Operations/Gain',A('gb3'),'Gain','4000','Position',[300 400 330 430]);
add_block('simulink/Discrete/Discrete Transfer Fcn',A('td'),'Numerator','1','Denominator','[1 zeros(1,100)]','SampleTime','0.001','Position',[360 440 400 480]);
add_block('simulink/Math Operations/Gain',A('gq'),'Gain',num2str(q0),'Position',[420 440 450 470]);
add_block('simulink/Math Operations/Sum',A('vchi'),'Inputs','++','Position',[470 400 490 460]);
add_block('simulink/Math Operations/Sum',A('dv'),'Inputs','+-','Position',[510 410 530 450]);
add_block('simulink/Math Operations/Gain',A('gka'),'Gain',num2str(ka,10),'Position',[550 415 580 445]);
add_block('simulink/Discrete/Discrete-Time Integrator',A('vint'),'SampleTime','0.001','InitialCondition','0','Position',[600 415 630 445]);
% ---------- FOC 电流环 ----------
add_block('simulink/Math Operations/Gain',A('giqr'),'Gain',num2str(IB),'Position',[400 85 430 115]);
add_block('simulink/Math Operations/Sum',A('eq'),'Inputs','+-','Position',[470 80 490 120]);
add_block('simulink/Math Operations/Gain',A('gkp'),'Gain',num2str(kpi),'Position',[520 60 550 90]);
add_block('simulink/Discrete/Discrete-Time Integrator',A('iqint'),'SampleTime','0.001','InitialCondition','0','Position',[520 110 550 140]);
add_block('simulink/Math Operations/Gain',A('gki'),'Gain',num2str(kii),'Position',[570 110 600 140]);
add_block('simulink/Math Operations/Sum',A('vq'),'Inputs','++','Position',[630 70 650 130]);
% ---------- PMSM dq(简化) ----------
add_block('simulink/Math Operations/Gain',A('gwe'),'Gain',num2str(PP),'Position',[520 330 550 360]);
add_block('simulink/Math Operations/Product',A('emf'),'Inputs','2','Position',[580 330 610 360]);
add_block('simulink/Math Operations/Gain',A('gRq'),'Gain',num2str(R),'Position',[580 220 610 250]);
add_block('simulink/Math Operations/Sum',A('diqnum'),'Inputs','+--','Position',[660 200 680 280]);
add_block('simulink/Math Operations/Gain',A('giL'),'Gain',num2str(1/L),'Position',[700 220 730 250]);
add_block('simulink/Discrete/Discrete-Time Integrator',A('iqp'),'SampleTime','0.001','InitialCondition','0','Position',[750 220 780 250]);
add_block('simulink/Math Operations/Gain',A('gkt'),'Gain',num2str(1.5*PP*PSI),'Position',[750 350 780 380]);
add_block('simulink/Sources/Constant',A('tl'),'Value','0.02','SampleTime','0.001','Position',[700 400 740 430]);
add_block('simulink/Math Operations/Sum',A('dw'),'Inputs','+-','Position',[810 360 830 410]);
add_block('simulink/Math Operations/Gain',A('gJ'),'Gain',num2str(1/Jm),'Position',[850 370 880 400]);
add_block('simulink/Discrete/Discrete-Time Integrator',A('wint'),'SampleTime','0.001','InitialCondition','0','Position',[900 370 930 400]);
add_block('simulink/Math Operations/Gain',A('grpm'),'Gain',num2str(30/pi),'Position',[960 370 990 400]);
% ---------- C Caller ----------
add_block('simulink/User-Defined Functions/C Caller',A('C'),'Position',[700 20 820 180]);
set_param(A('C'),'FunctionName','b0_ident_sim');
add_block('simulink/Math Operations/Gain',A('giqp'),'Gain',num2str(1/IB),'Position',[560 15 590 45]);
nm={'fiq','fu','fom','fe1','fv'}; sg={'giqp/1','uprev/1','grpm/1','eo/1','vint/1'};  % u 用延迟版，与 iq 同刻
for i=1:5
    add_block('simulink/Signal Attributes/Data Type Conversion',A(nm{i}),'OutDataTypeStr','single','Position',[620 10+40*(i-1) 660 35+40*(i-1)]);
    add_line(mdl,sg{i},[nm{i} '/1'],'autorouting','on');
    add_line(mdl,[nm{i} '/1'],['C/' num2str(i)],'autorouting','on');
end
add_block('simulink/Sources/Constant',A('ic1'),'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[620 220 660 240]);
add_block('simulink/Sources/Constant',A('ic2'),'Value','0','SampleTime','0.001','OutDataTypeStr','single','Position',[620 260 660 280]);
add_line(mdl,'ic1/1','C/6','autorouting','on');
add_line(mdl,'ic2/1','C/7','autorouting','on');
add_block('simulink/Signal Attributes/Data Type Conversion',A('b0d'),'OutDataTypeStr','double','Position',[860 40 900 70]);
add_line(mdl,'C/1','b0d/1','autorouting','on');
add_block('simulink/Discrete/Unit Delay',A('b0z'),'SampleTime','0.001','InitialCondition','400','Position',[930 40 960 70]);
add_line(mdl,'b0d/1','b0z/1','autorouting','on');
% 注入：u_cmd = u + du
add_block('simulink/Signal Attributes/Data Type Conversion',A('dup'),'OutDataTypeStr','double','Position',[860 220 900 250]);
add_line(mdl,'C/2','dup/1','autorouting','on');
add_block('simulink/Math Operations/Sum',A('sumu'),'Inputs','++','Position',[370 40 390 90]);
add_line(mdl,'udiv/1','sumu/1','autorouting','on');
add_line(mdl,'dup/1','sumu/2','autorouting','on');
p('blocks ok\n');
% ---------- 记录 ----------
vn={'w_log','b0_log','du_log','iq_log'};
for k=1:4
    add_block('simulink/Sinks/To Workspace',A(['ws' num2str(k)]),'VariableName',vn{k}, ...
        'SaveFormat','Timeseries','SampleTime','0.001','Position',[1050 20+60*(k-1) 1120 50+60*(k-1)]);
end
add_line(mdl,'grpm/1','ws1/1','autorouting','on');
add_line(mdl,'b0d/1','ws2/1','autorouting','on');
add_line(mdl,'C/2','ws3/1','autorouting','on');
add_line(mdl,'iqp/1','ws4/1','autorouting','on');
% ---------- 接线 ----------
add_line(mdl,'wref/1','yref/1','autorouting','on');
add_line(mdl,'yref/1','en/1','autorouting','on');
add_line(mdl,'z1int/1','en/2','autorouting','on');
add_line(mdl,'en/1','gkpe/1','autorouting','on');
add_line(mdl,'gkpe/1','us/1','autorouting','on');
add_line(mdl,'z2int/1','us/2','autorouting','on');
add_line(mdl,'vint/1','us/3','autorouting','on');
add_line(mdl,'us/1','udiv/1','autorouting','on');
add_line(mdl,'b0z/1','udiv/2','autorouting','on');
add_line(mdl,'udiv/1','uprev/1','autorouting','on');
add_line(mdl,'uprev/1','b0u/2','autorouting','on');
add_line(mdl,'b0z/1','b0u/1','autorouting','on');
add_line(mdl,'wint/1','grpm/1','autorouting','on');
add_line(mdl,'z1int/1','eo/2','autorouting','on');
add_line(mdl,'wint/1','ypu/1','autorouting','on');
add_line(mdl,'ypu/1','eo/1','autorouting','on');
add_line(mdl,'eo/1','g2wo/1','autorouting','on');
add_line(mdl,'eo/1','gwo2/1','autorouting','on');
add_line(mdl,'eo/1','g5/1','autorouting','on');
add_line(mdl,'g5/1','th/1','autorouting','on');
add_line(mdl,'th/1','gb3/1','autorouting','on');
add_line(mdl,'vint/1','td/1','autorouting','on');
add_line(mdl,'td/1','gq/1','autorouting','on');
add_line(mdl,'gb3/1','vchi/1','autorouting','on');
add_line(mdl,'gq/1','vchi/2','autorouting','on');
add_line(mdl,'vchi/1','dv/1','autorouting','on');
add_line(mdl,'vint/1','dv/2','autorouting','on');
add_line(mdl,'dv/1','gka/1','autorouting','on');
add_line(mdl,'gka/1','vint/1','autorouting','on');
add_line(mdl,'g2wo/1','z1s/4','autorouting','on');
add_line(mdl,'b0u/1','z1s/1','autorouting','on');
add_line(mdl,'vint/1','z1s/2','autorouting','on');
add_line(mdl,'z2int/1','z1s/3','autorouting','on');
add_line(mdl,'z1s/1','z1int/1','autorouting','on');
add_line(mdl,'gwo2/1','z2int/1','autorouting','on');
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
p('wiring ok\n');
save_system(mdl,[srcDir '\b0_foc.slx']); p('SAVED\n'); fclose(fid); fprintf('SAVED\n');
try
    out=sim(mdl);
    b=out.b0_log; w=out.w_log; d=out.du_log; iq=out.iq_log;
    fid2=fopen('out_focs.txt','w','n','UTF-8');
    fprintf(fid2,'SIM_OK b0_end=%.2f b0_20_40=%.2f w_end=%.2f iq_end=%.3f du_max=%.4f\n', ...
      b.Data(end), mean(b.Data(20000:40000)), w.Data(end), iq.Data(end), max(abs(d.Data)));
    fprintf(fid2,'理论 b = %.2f\n', 1.5*PP*PSI*IB/(Jm*62.832));
    ii=[20000 40000 60000 80000 100000 120000 140000];
    fprintf(fid2,'b0 轨迹: ');
    for kk=ii, fprintf(fid2,'%.0f@%ds ', b.Data(kk), round(kk/1000)); end
    fprintf(fid2,'\n');
    figure('Visible','off');
    subplot(2,1,1); plot(w.Time,w.Data); grid on; ylabel('w/rpm'); title('PMSM dq FOC + b0 ident');
    subplot(2,1,2); plot(b.Time,b.Data,'LineWidth',1.3); grid on; ylabel('b0'); xlabel('t/s');
    print('-dpng','-r110',[srcDir '\fig_foc.png']); fprintf(fid2,'FIG_OK\n'); fclose(fid2);
    fprintf('SIM_OK\n');
catch e
    fprintf('SIM_FAIL: %s\n', e.message);
    for i=1:numel(e.cause), fprintf('  C%d: %s\n', i, e.cause{i}.message); end
end