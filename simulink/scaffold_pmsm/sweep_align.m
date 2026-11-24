function sweep_align()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
V = 1.0;
phases = [0 90 180 -90];
for i = 1:numel(phases)
    ph = phases(i)*pi/180;
    set_param('pmsm_align/v1', 'Value', num2str(V*cos(ph)));
    set_param('pmsm_align/v2', 'Value', num2str(V*cos(ph - 2*pi/3)));
    set_param('pmsm_align/v3', 'Value', num2str(V*cos(ph + 2*pi/3)));
    out = sim('pmsm_align');
    M = out.alog.signals.values;
    id = M(:,5); iq = M(:,4);
    n = size(M,1); tail = round(n*0.8):n;
    fprintf('phi=%4d deg :  id 均值 %6.2f A   iq 均值 %6.2f A   (id 峰值 %.1f)\n', ...
        phases(i), mean(id(tail)), mean(iq(tail)), max(abs(id)));
end
end
