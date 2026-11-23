% build_min.m —— 最小验证模型：C Caller + Scope
mdl = 'b0_min';
srcDir = 'D:\Desktop\RCESO\simulink';
fid = fopen('out_build.txt','w','n','UTF-8');
p = @(varargin) fprintf(fid, varargin{:});

if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl); open_system(mdl);
set_param(mdl,'StopTime','12');
set_param(mdl,'Solver','FixedStepDiscrete');
set_param(mdl,'FixedStep','0.001');
set_param(mdl,'SolverType','Fixed-step');
set_param(mdl,'SimTargetLang','C');

% 关键：把函数原型注入 SimCustomHeaderCode，C Caller 才能识别
set_param(mdl,'SimCustomHeaderCode', ...
    'extern void b0_ident_u(const float in[5], float out[2]);');
set_param(mdl,'SimUserSources', ...
    sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c', srcDir, srcDir));
set_param(mdl,'SimUserIncludeDirs', srcDir);
set_param(mdl,'CustomSource', ...
    sprintf('%s\\b0_ident.c\n%s\\b0_ident_wrap.c', srcDir, srcDir));
p('params set\n');

add_block('simulink/User-Defined Functions/C Caller',[mdl '/C'],'Position',[420 95 540 200]);
set_param([mdl '/C'],'FunctionName','b0_ident_u');
p('PORTS=%s\n', mat2str(get_param([mdl '/C'],'Ports')));

add_block('simulink/Sources/Sine Wave',[mdl '/u'],'Amplitude','0.118', ...
    'Frequency','2*pi*65','SampleTime','0.001','Position',[60 62 100 88]);
add_block('simulink/Math Operations/Gain',[mdl '/iq'],'Gain','1','Position',[150 62 190 88]);
add_block('simulink/Sources/Constant',[mdl '/omega'],'Value','600', ...
    'SampleTime','0.001','Position',[60 122 100 148]);
add_block('simulink/Sources/Constant',[mdl '/e1'],'Value','0', ...
    'SampleTime','0.001','Position',[60 182 100 208]);
add_block('simulink/Sources/Constant',[mdl '/v'],'Value','0', ...
    'SampleTime','0.001','Position',[60 242 100 268]);
add_block('simulink/Signal Routing/Mux',[mdl '/Mux'],'Inputs','5','Position',[300 58 305 272]);
add_block('simulink/Signal Routing/Demux',[mdl '/Demux'],'Outputs','2','Position',[600 110 605 190]);
add_block('simulink/Sinks/Scope',[mdl '/Scope'],'NumInputPorts','2','Position',[730 90 790 170]);
add_block('simulink/Sinks/To Workspace',[mdl '/b0_ws'],'VariableName','b0_log', ...
    'SaveFormat','Timeseries','SampleTime','0.001','Position',[690 30 760 60]);
add_block('simulink/Sinks/To Workspace',[mdl '/du_ws'],'VariableName','du_log', ...
    'SaveFormat','Timeseries','SampleTime','0.001','Position',[690 220 760 250]);

add_line(mdl,'u/1','iq/1','autorouting','on');
add_line(mdl,'u/1','Mux/1','autorouting','on');
add_line(mdl,'iq/1','Mux/2','autorouting','on');
add_line(mdl,'omega/1','Mux/3','autorouting','on');
add_line(mdl,'e1/1','Mux/4','autorouting','on');
add_line(mdl,'v/1','Mux/5','autorouting','on');
add_line(mdl,'Mux/1','C/1','autorouting','on');
add_line(mdl,'C/1','Demux/1','autorouting','on');
add_line(mdl,'Demux/1','Scope/1','autorouting','on');
add_line(mdl,'Demux/2','Scope/2','autorouting','on');
add_line(mdl,'Demux/1','b0_ws/1','autorouting','on');
add_line(mdl,'Demux/2','du_ws/1','autorouting','on');

save_system(mdl,[srcDir '\b0_min.slx']);
p('MODEL_SAVED\n');
fclose(fid);
fprintf('SAVED\n');

try
    out = sim(mdl);
    fid = fopen('out_sim.txt','w','n','UTF-8');
    p2 = @(varargin) fprintf(fid, varargin{:});
    p2('SIM_OK\n');
    b = out.b0_log; d = out.du_log;
    p2('b0 n=%d min=%.2f max=%.2f last=%.2f\n', numel(b.Data), min(b.Data), max(b.Data), b.Data(end));
    p2('du min=%.4f max=%.4f\n', min(d.Data), max(d.Data));
    nz = d.Data ~= 0;
    p2('du nonzero=%.2f%%\n', 100*sum(nz)/numel(nz));
    figure('Visible','off');
    subplot(2,1,1); plot(b.Time,b.Data,'LineWidth',1.2); grid on; ylabel('b0');
    title('b0 identification (minimal model)');
    subplot(2,1,2); plot(d.Time,d.Data); grid on; ylabel('deltau'); xlabel('t / s');
    print('-dpng','-r110',[srcDir '\fig_min_model.png']);
    p2('FIG_SAVED\n');
    fclose(fid);
    fprintf('SIM_OK\n');
catch e
    fprintf('SIM_FAIL: %s\n', e.message);
end
