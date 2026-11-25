function isol_test()
% 把 slx 复制到独立目录，脱离本仓库路径后能否直接运行
src = 'D:\Desktop\RCESO\simulink\scaffold_pmsm\pmsm_foc.slx';
dst = 'D:\tmp_vendor\';
if ~exist(dst, 'dir'), mkdir(dst); end
copyfile(src, fullfile(dst, 'pmsm_foc.slx'));
cd(dst);
% 把仓库路径从 search path 里移除
p = strsplit(path, pathsep);
keep = p(~contains(p, 'RCESO'));
path(strjoin(keep, pathsep));
fprintf('当前目录: %s\n', pwd);
fprintf('路径里还有 RCESO 吗: %d\n', any(contains(strsplit(path,pathsep), 'RCESO')));
try
    load_system('pmsm_foc');
    fprintf('模型载入成功\n');
    % 检查是否有未解析的外部函数依赖
    set_param('pmsm_foc', 'StopTime', '3');
    out = sim('pmsm_foc');
    V = out.flog.signals.values;
    fprintf('仿真成功：3 s，末转速 %.1f rpm\n', V(end,11)*30/pi);
catch e
    fprintf('失败: %s\n', e.message);
end
end
