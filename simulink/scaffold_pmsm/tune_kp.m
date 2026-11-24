function tune_kp()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
base = fileread('SL.m');
rt = sfroot;
for kp = [0.1 0.2 0.4 0.8]
    s = strrep(base, 'kp = 0.04;', sprintf('kp = %.2f;', kp));
    f = fopen('SL_tmp.m','w'); fwrite(f, s); fclose(f);
    load_system('pmsm_foc');
    ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/SL');
    ch.Script = fileread('SL_tmp.m'); ch.ChartUpdate='DISCRETE'; ch.SampleTime='1e-3';
    set_param('pmsm_foc', 'StopTime', '40');
    out = sim('pmsm_foc');
    V = out.flog.signals.values; wm = V(:,11)*30/pi;
    B = out.blog.signals.values(:);
    tail = round(0.75*numel(wm)):numel(wm);
    fprintf('kp=%.2f : 末值 %.1f 峰值 %.1f 后段均值 %.1f  b0 %.1f\n', ...
        kp, wm(end), max(wm), mean(wm(tail)), B(end));
end
end
