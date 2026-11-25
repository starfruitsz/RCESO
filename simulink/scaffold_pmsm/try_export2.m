function try_export2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc');
names = {'Simulink.exportToVersion', 'exportToVersion'};
for i = 1:numel(names)
    try
        feval(names{i}, 'pmsm_foc', 'pmsm_foc_2018b', 'R2018b');
        fprintf('%s 成功\n', names{i});
        return;
    catch e
        fprintf('%s 失败: %s | %s\n', names{i}, e.identifier, e.message);
    end
end
end
