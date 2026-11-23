% probe4.m
fid = fopen('out4.txt','w','n','UTF-8');
p = @(varargin) fprintf(fid, varargin{:});
try
    tc = RTW.getToolchains();
    p('=== Toolchains (%d) ===\n', numel(tc));
    for i=1:numel(tc)
        p('%s\n', tc(i).Name);
    end
catch e
    p('TC_ERR %s\n', e.message);
end
try
    p('\n=== mex -setup 结果 ===\n');
    s = mex.getCompilerConfigurations('C','Selected');
    p('Selected: %s\\n', s(1).Name);
    p('Location: %s\n', s(1).Location);
    p('MexOpt:   %s\n', s(1).MexOpt);
catch e
    p('MEX_ERR %s\n', e.message);
end
fclose(fid);
