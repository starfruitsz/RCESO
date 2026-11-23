function probe_variants()
srcDir = 'D:\Desktop\RCESO\simulink';
cd(srcDir);
base = fileread([srcDir '\b0_ident_m.m']);
old  = fileread('D:\Desktop\RCESO\_texbuild\old_script.m');
% V2：删掉顶层的 error() 断言
v2 = strrep(base, ['if abs(cyc*nseg - round(cyc*nseg)) > 1e-6' newline ...
     '    % 该断言在仿真里会显式报错，避免静默失效' newline ...
     '    error(''注入频率 %g Hz 与段长 0.2 s 不相干（cyc*nseg 非整数）'', f_inj);' newline 'end'], '');
names = {'V1 基线（现文件）','V2 去掉 error()','V3 旧脚本（19:51 可用版）'};
scripts = {base, v2, old};
for i = 1:3
    if bdIsLoaded('b0_foc_m'), close_system('b0_foc_m', 0); end
    load_system([srcDir '\b0_foc_m.slx']);
    r = sfroot; ch = r.find('-isa','Stateflow.EMChart','Path','b0_foc_m/C');
    ch.Script = scripts{i};
    try
        set_param('b0_foc_m','SimulationCommand','update');
        fprintf('%s -> UPDATE_OK\n', names{i});
    catch e
        fprintf('%s -> FAIL: %s\n', names{i}, e.message);
        for k=1:numel(e.cause), fprintf('   C%d: %s\n', k, e.cause{k}.message); end
    end
end
close_system('b0_foc_m', 0);
end
