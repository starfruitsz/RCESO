function sweep_align2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
% 标定用：加大转动惯量让转子在 50 ms 内几乎不动；负载 0
set_param('pmsm_align/PMSM', 'Mechanical', '[1 0 4 0]');
set_param('pmsm_align/Tm', 'Value', '0');
V = 1.0;
phases = [0 45 90 135 180 225 270 315];
for i = 1:numel(phases)
    ph = phases(i)*pi/180;
    set_param('pmsm_align/v1', 'Value', num2str(V*cos(ph)));
    set_param('pmsm_align/v2', 'Value', num2str(V*cos(ph - 2*pi/3)));
    set_param('pmsm_align/v3', 'Value', num2str(V*cos(ph + 2*pi/3)));
    out = sim('pmsm_align');
    M = out.alog.signals.values;
    id = M(:,5); iq = M(:,4);
    n = size(M,1); tail = round(n*0.8):n;
    fprintf('phi=%4d :  id %6.2f   iq %6.2f   |I| %6.2f A\n', ...
        phases(i), mean(id(tail)), mean(iq(tail)), hypot(mean(id(tail)), mean(iq(tail))));
end
end
