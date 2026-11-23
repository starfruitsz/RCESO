% probe5.m
fid = fopen('out7.txt','w','n','UTF-8');
p = @(varargin) fprintf(fid, varargin{:});
p('MW_MINGW64_LOC = %s\n', getenv('MW_MINGW64_LOC'));
c = mex.getCompilerConfigurations('C','Installed');
p('installed C compilers: %d\n', numel(c));
for i=1:numel(c)
    p('  [%d] %s | ver %s | %s\n', i, c(i).Name, c(i).Version, c(i).Location);
end
s = mex.getCompilerConfigurations('C','Selected');
if ~isempty(s)
    p('selected: %s\n', s(1).Name);
    p('  location exists = %d\n', exist(s(1).Location,'dir') ~= 0);
end
fclose(fid);
