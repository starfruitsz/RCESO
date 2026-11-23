% probe3.m —— 摸清模型参数名与工具链
mdl = 'p3';
if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl);
fprintf('=== 相关模型参数 ===\n');
p = get_param(mdl,'ObjectParameters'); f = fieldnames(p);
for i=1:numel(f)
    nm = f{i};
    if ~isempty(regexpi(nm,'toolchain|includedir|customsource|custominclude|simuser|simtargetlang'))
        try
            v = get_param(mdl,nm);
            if ~ischar(v), v = mat2str(v); end
            fprintf('%-28s = %s\n', nm, v);
        catch
            fprintf('%-28s = <read err>\n', nm);
        end
    end
end
fprintf('=== 编译器 ===\n');
c = mex.getCompilerConfigurations('C','Installed');
for i=1:numel(c)
    fprintf('%-40s ver=%s loc=%s\n', c(i).Name, c(i).Version, c(i).Location);
end
sel = mex.getCompilerConfigurations('C','Selected');
if ~isempty(sel)
    fprintf('SELECTED=%s\n', sel(1).Name);
    fprintf('SEL_LOC=%s\n', sel(1).Location);
end
bdclose(mdl);
fprintf('=== DONE ===\n');
