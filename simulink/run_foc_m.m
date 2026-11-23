% run_foc_m.m —— 单独跑 b0_foc_m（MATLAB Function 版）取闭环终值
srcDir = 'D:\Desktop\RCESO\simulink'; cd(srcDir);
load_system([srcDir '\b0_foc_m.slx']);
set_param('b0_foc_m','StopTime','130');
out = sim('b0_foc_m');
fid = fopen('out_fm.txt','w','n','UTF-8');
fprintf(fid,'SIM_OK b0=%.2f w=%.2f (真值 536.40)\n', out.b0_log.Data(end), out.w_log.Data(end));
fprintf(fid,'b0轨迹: ');
for kk = [20000 40000 60000 80000 100000 120000]
    fprintf(fid,'%.0f@%ds ', out.b0_log.Data(kk), round(kk/1000));
end
fprintf(fid,'\n'); fclose(fid);
fprintf('FOC_M b0=%.3f\n', out.b0_log.Data(end));
