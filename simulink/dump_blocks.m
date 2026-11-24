function dump_blocks()
cd('D:\Desktop\RCESO\simulink');
load_system('b0_foc_m');
blks = find_system('b0_foc_m', 'SearchDepth', 1, 'Type', 'Block');
fprintf('顶层块 %d 个：\n', numel(blks));
for i = 1:numel(blks)
    [~, nm] = fileparts(blks{i});
    bt = get_param(blks{i}, 'BlockType');
    fprintf('  %-16s [%s]\n', nm, bt);
end
close_system('b0_foc_m', 0);
end
