function baseline_model()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
set_param('pmsm_foc/dB0', 'InitialCondition', '536.4');
set_param('pmsm_foc/TLf', 'Amplitude', '0');        % 默认关故障；改成 0.1 即 10 Hz 扰动
save_system('pmsm_foc');
set_param('pmsm_foc', 'StopTime', '130');
out = sim('pmsm_foc');
B = out.blog.signals.values(:);
V = out.flog.signals.values; wm = V(:,11)*30/pi;
fprintf('转速 末值 %.1f  后段均值 %.1f   b0 %.1f（%+.2f%%）\n', ...
    wm(end), mean(wm(round(0.8*numel(wm)):end)), B(end), 100*(B(end)/536.4-1));
end
