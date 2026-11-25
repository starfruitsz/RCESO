function chk_links()
cd('D:\Desktop\RCESO\simulink\scaffold_pmsm');
load_system('pmsm_foc_2018b');
blks = find_system('pmsm_foc_2018b', 'LookUnderMasks', 'all', 'FollowLinks', 'on', 'Type', 'Block');
bad = {};
for i = 1:numel(blks)
    try
        st = get_param(blks{i}, 'LinkStatus');
        if ~strcmp(st, 'resolved')
            bad{end+1} = sprintf('%s [%s]', blks{i}, st); %#ok
        end
    catch
    end
end
fprintf('未解析链接 %d 个：\n', numel(bad));
for i = 1:min(numel(bad), 8), fprintf('  %s\n', bad{i}); end
close_system('pmsm_foc_2018b', 0);
end
