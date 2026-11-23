% check_blks.m
srcDir='D:\Desktop\RCESO\simulink'; mdl='b0_foc';
fid=fopen('out_chk.txt','w','n','UTF-8');
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system([srcDir '\b0_foc.slx']);
A=@(n)[mdl '/' n];
rceso = {'en','gkpe','us','udiv','uprev','b0u','z1s','z1int','z2int','g2wo', ...
         'gwo2','eo','ypu','g5','th','gb3','td','gq','vchi','dv','gka','vint'};
missing = {};
for i=1:numel(rceso)
    p = A(rceso{i});
    try
        h = get_param(p,'Handle');
        try, bt = get_param(p,'BlockType'); catch, bt='?'; end
        fprintf(fid,'OK   %-8s %s\n', rceso{i}, bt);
    catch
        fprintf(fid,'MISS %-8s\n', rceso{i});
        missing{end+1} = rceso{i};
    end
end
fprintf(fid,'missing=%d\n', numel(missing));
fprintf(fid,'list=[%s]\n', strjoin(setdiff(rceso,missing),' '));
fclose(fid); fprintf('DONE\n');
