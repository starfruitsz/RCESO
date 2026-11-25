function ver_export()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
% 检查导出的模型能否在本机（R2023b）打开并运行
load_system('pmsm_foc_2018b');
set_param('pmsm_foc_2018b', 'StopTime', '3');
out = sim('pmsm_foc_2018b');
V = out.flog.signals.values;
fprintf('导出模型可运行：3 s 末转速 %.1f rpm\n', V(end,11)*30/pi);
save_system('pmsm_foc_2018b');
close_system('pmsm_foc_2018b', 1);
end
