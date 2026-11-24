function fix_bs()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_cc');
s = get_param('pmsm_cc/BS', 'InputSignals');
fprintf('可用信号（前 400 字符）：\n%s\n', s(1:min(numel(s),400)));
end
