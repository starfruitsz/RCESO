% diag_du.m
mdl='b0_caller';
if ~bdIsLoaded(mdl), load_system(mdl); end
set_param(mdl,'StopTime','1');
out = sim(mdl);
d = out.du_log;
fid=fopen('out_diag.txt','w','n','UTF-8');
fprintf(fid,'n=%d\n', numel(d.Data));
idx = 195:215;
for i=idx
    fprintf(fid,'t=%.3f du=%+.5f\n', d.Time(i), d.Data(i));
end
fprintf(fid,'--- burst 内最大 ---\n');
seg = d.Time>=0.2 & d.Time<=0.42;
fprintf(fid,'max|du|=%.5f  min=%.5f max=%.5f\n', max(abs(d.Data(seg))), min(d.Data(seg)), max(d.Data(seg)));
fclose(fid);
