% fix_and_build.m
fid = fopen('out_fix.txt','w','n','UTF-8');
c = mex.getCompilerConfigurations('C','Installed');
fprintf(fid,'installed=%d\n', numel(c));
for i=1:numel(c)
    fprintf(fid,'  %s | %s | %s\n', c(i).Name, c(i).Version, c(i).Location);
end
if ~isempty(c)
    try
        evalc('mex -setup C');
        fprintf(fid,'setup_ok\n');
    catch e
        fprintf(fid,'setup_err %s\n', e.message);
    end
    s = mex.getCompilerConfigurations('C','Selected');
    if ~isempty(s), fprintf(fid,'selected=%s\n', s(1).Name); end
end
fclose(fid);
fprintf('STEP1_DONE\n');
if ~isempty(c)
    run('build_min4');
end
