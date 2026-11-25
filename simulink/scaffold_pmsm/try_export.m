function try_export()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
try
    Simulink.ExportToVersion('pmsm_foc', 'pmsm_foc_2018b', 'R2018b');
    fprintf('导出成功\n');
catch e
    fprintf('导出失败: %s\n', e.identifier);
    fprintf('%s\n', e.message);
end
% 看看本版支持导出到哪些版本
try
    v = Simulink.ExportToVersion;   %#ok
catch
end
end
