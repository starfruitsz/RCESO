function run_matrix()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
base = fileread('../b0_ident_m.m');
rt = sfroot;
names = {'正弦','方波','三角'};
res = [];
for w = 0:2
    for upd = [1 0]
        txt = regexprep(base, 'amp\s*=\s*[0-9.]+;', 'amp    = 0.05;');
        txt = regexprep(txt, 'wave\s*=\s*[0-2];', sprintf('wave   = %d;', w));
        txt = regexprep(txt, 'b0_init=\s*[0-9.]+;', 'b0_init= 800;');
        txt = regexprep(txt, 'b0lo\s*=\s*[0-9.]+;', 'b0lo   = 300;');
        txt = regexprep(txt, 'b0hi\s*=\s*[0-9.]+;', 'b0hi   = 1500;');
        txt = regexprep(txt, 'upd_on\s*=\s*[01];', sprintf('upd_on  = %d;', upd));
        f = fopen('ID_tmp.m','w'); fwrite(f, txt); fclose(f);
        load_system('pmsm_foc');
        ch = rt.find('-isa','Stateflow.EMChart','Path','pmsm_foc/ID');
        ch.Script = fileread('ID_tmp.m'); ch.ChartUpdate='DISCRETE'; ch.SampleTime='1e-3';
        set_param('pmsm_foc', 'StopTime', '130');
        out = sim('pmsm_foc');
        V = out.flog.signals.values; t = out.flog.time(:);
        wm = V(:,11)*30/pi; iq = V(:,4);
        B = out.blog.signals.values(:);
        tail = t > 60;
        x = wm(tail) - mean(wm(tail));
        X = np_fft(x, t);
        r.name = names{w+1}; r.upd = upd; r.b0 = B(end);
        r.err = 100*(B(end)/536.4 - 1);
        r.rms = std(wm(tail)); r.a10 = X;
        r.iqrms = std(iq(tail));
        res = [res, r];
        fprintf('%-3s upd=%d : b0 %.1f (%+.1f%%)  rms %.2f  10Hz %.2f  iq_rms %.3f\n', ...
            names{w+1}, upd, B(end), r.err, r.rms, r.a10, r.iqrms);
    end
end
save('matrix_res.mat', 'res');
end
function a = np_fft(x, t)
    X = fft(x); fr = (0:numel(x)-1)/(t(end)-t(1))*numel(x)/numel(x);
    Ts = mean(diff(t)); N = numel(x);
    f = (0:N-1)/(N*Ts);
    k = round(10*N*Ts)+1;
    a = 2*abs(X(k))/N;
end
