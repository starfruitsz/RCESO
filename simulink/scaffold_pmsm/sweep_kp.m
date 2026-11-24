function sweep_kp()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
base = fileread('SL.m');
kps = [0.3 0.6 1.0 2.0];
for k = 1:numel(kps)
    s = strrep(base, 'kp = 1.0;', sprintf('kp = %.2f;', kps(k)));
    f = fopen('SL_tmp.m','w'); fwrite(f, s); fclose(f);
    load_system('pmsm_foc');
    rt = sfroot; ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/SL');
    ch.Script = fileread('SL_tmp.m');
    out = sim('pmsm_foc');
    V = out.flog.signals.values; wm = V(:,11)*30/pi;
    fprintf('kp=%.2f : 末值 %.1f  峰值 %.1f  超调 %+.1f%%\n', kps(k), wm(end), max(wm), 100*(max(wm)/600-1));
end
end
