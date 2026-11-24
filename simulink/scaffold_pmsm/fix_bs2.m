function fix_bs2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_cc');
s = get_param('pmsm_cc/BS', 'InputSignals');
fprintf('信号数 %d：\n', numel(s));
for i = 1:numel(s), fprintf('  [%d] %s\n', i, s{i}); end
idxA = find(contains(s, 'angle'), 1);
idxD = find(contains(s, 'is_d'), 1);
idxQ = find(contains(s, 'is_q'), 1);
fprintf('选中: angle=%s  is_d=%s  is_q=%s\n', s{idxA}, s{idxD}, s{idxQ});
% OutputSignals 顺序：thm, id, iq（与 CC 的输入顺序一致）
set_param('pmsm_cc/BS', 'OutputSignals', strjoin({s{idxA}, s{idxD}, s{idxQ}}, ','));
save_system('pmsm_cc');
disp('BS fixed');
end
