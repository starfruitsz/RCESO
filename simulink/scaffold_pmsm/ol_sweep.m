function ol_sweep()
cd('D:\Desktop\RCESO\simulink');
load_system('pmsm_ol');
for cfg = 1:2
    if cfg == 1, sgn = +1; else, sgn = -1; end
    for k = 1:3
        set_param(sprintf('pmsm_ol/m%d', k), 'Phase', num2str(sgn*(-120)*(k-1)*pi/180), ...
                  'Amplitude', '4.8');
    end
    set_param('pmsm_ol/Tm', 'Value', '0.5');
    out = sim('pmsm_ol');
    T = out.wlog; fn = fieldnames(T);
    wm = T.(fn{find(contains(fn,'speed'),1)}).Data(:);
    iq = T.(fn{find(contains(fn,'is_q'),1)}).Data(:);
    te = T.(fn{find(contains(fn,'torque'),1)}).Data(:);
    fprintf('cfg%d(sgn=%+d): 转速 %.1f rpm   iq %.2f A   转矩 %.3f N·m\n', ...
            cfg, sgn, wm(end)*30/pi, iq(end), te(end));
end
end
