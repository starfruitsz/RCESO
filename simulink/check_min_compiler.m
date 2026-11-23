% check_min_compiler.m
fid = fopen('out_min.txt','w','n','UTF-8');
p = @(varargin) fprintf(fid, varargin{:});
p('MW_MINGW64_LOC=%s\n', getenv('MW_MINGW64_LOC'));
s = mex.getCompilerConfigurations('C','Selected');
if isempty(s)
    p('SELECTED=none\n');
else
    p('SELECTED=%s\n  loc=%s\n', s(1).Name, s(1).Location);
end
try
    eval('mex -c b0_ident.c');
    p('MEX_C_OK\n');
catch e
    p('MEX_C_FAIL: %s\n', e.message);
end
fclose(fid);
