function dump_mlog()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
out = sim('pmsm_cc');
T = out.mlog;
disp(class(T));
fn = fieldnames(T.signals);
fprintf('字段 %d：\n', numel(fn));
for i = 1:numel(fn), fprintf('  %s\n', fn{i}); end
end
