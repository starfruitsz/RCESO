% scope_foc2.m —— 跑 ADRC 闭环，把波形存成 foc2_log.mat（供 plot_scope_foc2.py 出图）
% 模型里已带 5 个 Scope（du / iq / w / b0 / u），GUI 下可直接双击看波形；
% 批处理模式下用本脚本导出数据，由 Python 画成图。
srcDir = 'D:\Desktop\RCESO\simulink';
cd(srcDir); mdl = 'b0_foc2';
if bdIsLoaded(mdl), close_system(mdl,0); end
% 注册总线类型（C Caller 的结构体返回值），否则 C 块的输出类型无法解析
bs = Simulink.Bus;
ea = Simulink.BusElement; ea.Name='b0'; ea.DataType='single';
eb = Simulink.BusElement; eb.Name='du'; eb.DataType='single';
bs.Elements=[ea eb]; assignin('base','b0_res_t',bs);
load_system([srcDir '\b0_foc2.slx']);
set_param(mdl,'StopTime','150');
out = sim(mdl);
W = out.w_log; B = out.b0_log; D = out.du_log; Q = out.iq_log; U = out.u_log;
E = out.e1_log; V = out.v_log;
% 存成纯 double 数组（timeseries 对象在 scipy 里读不出）
tw = W.Time; wv = W.Data;  tb = B.Time; bv = B.Data;
td = D.Time; dv = D.Data;  tq = Q.Time; qv = Q.Data;  tu = U.Time; uv = U.Data;
te = E.Time; ev = E.Data;  tv = V.Time; vv = V.Data;
save([srcDir '\foc2_log.mat'],'tw','wv','tb','bv','td','dv','tq','qv','tu','uv','te','ev','tv','vv','-v7');
fprintf('SAVED b0=%.2f du_max=%.4f w_end=%.2f\n', B.Data(end), max(abs(D.Data)), W.Data(end));
close_system(mdl,0);
