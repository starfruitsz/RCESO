function final_check()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
B = out.blog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
fprintf('冻结循环修改后：转速 %.1f rpm   b0 %.1f（%+.2f%%）\n', wm(end), B(end), 100*(B(end)/536.4-1));
end
