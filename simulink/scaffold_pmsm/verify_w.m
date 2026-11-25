function verify_w()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
B = out.blog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
fprintf('复核：转速 %.1f rpm  b0 %.1f（%+.2f%%） b0 范围 %.1f..%.1f\n', ...
    wm(end), B(end), 100*(B(end)/536.4-1), min(B), max(B));
end
