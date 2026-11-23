% check_foc2.m
fid=fopen('out_c2.txt','w','n','UTF-8');
mdl='b0_foc2';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system(['D:\Desktop\RCESO\simulink\' mdl '.slx']);
% 顶层块
top = find_system(mdl,'SearchDepth',1,'Type','Block');
fprintf(fid,'顶层块 %d 个:\n', numel(top));
for i=1:numel(top)
    [~,nm]=fileparts(top{i});
    bt=get_param(top{i},'BlockType');
    fprintf(fid,'  %-10s %s\n', nm, bt);
end
% RCESO 端口
try
    ph=get_param([mdl '/RCESO'],'Ports');
    fprintf(fid,'RCESO Ports = %s\n', mat2str(ph));
    in = find_system([mdl '/RCESO'],'SearchDepth',1,'BlockType','Inport');
    ot = find_system([mdl '/RCESO'],'SearchDepth',1,'BlockType','Outport');
    nb = find_system([mdl '/RCESO'],'SearchDepth',1,'Type','Block');
    fprintf(fid,'RCESO 内部: %d 块, %d 输入端口, %d 输出端口\n', numel(nb), numel(in), numel(ot));
catch e
    fprintf(fid,'RCESO err %s\n', e.message);
end
fclose(fid); fprintf('DONE\n');
