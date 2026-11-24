function save_traces()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
base = fileread('../b0_ident_m.m');
rt = sfroot;
for upd = [1 0]
    txt = regexprep(base, 'amp\s*=\s*[0-9.]+;', 'amp    = 0.05;');
    txt = regexprep(txt, 'wave\s*=\s*[0-2];', 'wave   = 0;');
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
    t = out.flog.time(:); V = out.flog.signals.values;
    b0 = out.blog.signals.values(:);
    tag = sprintf('upd%d', upd);
    save(sprintf('_tr_%s.mat', tag), 't', 'V', 'b0');
    fprintf('%s: b0 末值 %.1f, 保存 %d 点\n', tag, b0(end), numel(t));
end
end
