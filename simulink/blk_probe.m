% blk_probe.m
fid=fopen('out_blk.txt','w','n','UTF-8');
new_system('bp');
cands = { ...
 'simpowersystems/Electrical Machines/Permanent Magnet Synchronous Machine', ...
 'simscape/Electrical/Specialized Power Systems/Fundamental Blocks/Electrical Machines/Permanent Magnet Synchronous Machine', ...
 'sps_lib/Permanent Magnet Synchronous Machine', ...
 'sps_lib/Electrical Machines/Permanent Magnet Synchronous Machine', ...
 'sps_lib/Universal Bridge'};
for i=1:numel(cands)
    try
        add_block(cands{i}, ['bp/B' num2str(i)]);
        fprintf(fid,'OK   %s\n', cands{i});
    catch e
        fprintf(fid,'FAIL %s\n     %s\n', cands{i}, e.message);
    end
end
% 列出 sps_lib 顶层
try
    load_system('sps_lib');
    top = find_system('sps_lib','SearchDepth',1,'BlockType','SubSystem');
    fprintf(fid,'--- sps_lib 顶层 (%d) ---\n', numel(top));
    for i=1:min(20,numel(top)), fprintf(fid,'  %s\n', top{i}); end
catch e
    fprintf(fid,'lib err %s\n', e.message);
end
bdclose('bp');
fclose(fid);
