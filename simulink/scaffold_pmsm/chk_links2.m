function chk_links2()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc_2018b');
blks = find_system('pmsm_foc_2018b', 'FollowLinks', 'on', 'Type', 'Block');
st = {};
for i = 1:numel(blks)
    try, st{end+1} = get_param(blks{i}, 'LinkStatus'); catch, st{end+1} = 'err'; end
end
u = unique(st);
for i = 1:numel(u)
    fprintf('%-10s : %d\n', u{i}, sum(strcmp(st, u{i})));
end
% SPS 关键块
keys = {'PMSM','powergui','cvs1','cvs2','cvs3'};
for i = 1:numel(keys)
    b = ['pmsm_foc_2018b/' keys{i}];
    try
        fprintf('%-10s LinkStatus=%s  BlockType=%s\n', keys{i}, ...
            get_param(b,'LinkStatus'), get_param(b,'BlockType'));
    catch e
        fprintf('%-10s 读取失败 %s\n', keys{i}, e.message);
    end
end
close_system('pmsm_foc_2018b', 0);
end
