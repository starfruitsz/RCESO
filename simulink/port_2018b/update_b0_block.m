function update_b0_block(model, blkPath, mfile)
% UPDATE_B0_BLOCK  把 b0_ident_m.m 的全文写进目标机模型里的 MATLAB Function 块
%
% 用法（在目标机的 MATLAB 命令窗口）：
%   update_b0_block('PMSM_2Loop_ADRC', ...
%                   'PMSM_2Loop_ADRC/ADRC Speed Control1/ID1', ...
%                   'b0_ident_m.m')
%
% 说明：
%   - 写入后块的输入端口数会由 5 变成 7（新增 w、wref），
%     需要手动把这两个新端口接上（w=实测转速，wref=参考转速，单位一致）。
%   - 采样时间统一设为 1 ms（ChartUpdate='DISCRETE', SampleTime='1e-3'）。
%   - 不会修改模型里其它任何东西。

if nargin < 3, mfile = 'b0_ident_m.m'; end
if exist(mfile, 'file') ~= 2
    error('找不到 %s，请把它和本脚本放在同一目录', mfile);
end
load_system(model);
rt = sfroot;
ch = rt.find('-isa', 'Stateflow.EMChart', 'Path', blkPath);
if isempty(ch)
    error('找不到 MATLAB Function 块：%s', blkPath);
end
ch.Script = fileread(mfile);
ch.ChartUpdate = 'DISCRETE';
ch.SampleTime  = '1e-3';
save_system(model);

% 报告端口数
blk = get_param(blkPath, 'Handle');
ph  = get_param(blk, 'PortHandles');
nIn = numel(ph.Inport);
fprintf('已更新：%s\n', blkPath);
fprintf('当前输入端口数 = %d（应为 7：iq, u, ge1, e1, v, w, wref）\n', nIn);
if nIn > 5
    fprintf('请把第 6、7 个输入接上：w = 实测转速, wref = 参考转速（单位一致）\n');
end
fprintf('下一步：Ctrl+D 更新框图，确认代数环消失、无未接线端口\n');
end
