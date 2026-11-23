% check_ports.m
fid=fopen('out_pt.txt','w','n','UTF-8');
mdl='b0_foc2';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system(['D:\Desktop\RCESO\simulink\' mdl '.slx']);
fprintf(fid,'C 端口 = %s   (应为 5 进 1 出)\n', mat2str(get_param([mdl '/C'],'Ports')));
fprintf(fid,'C 函数 = %s\n', get_param([mdl '/C'],'FunctionName'));
fprintf(fid,'BS 输出 = %s\n', get_param([mdl '/BS'],'OutputSignals'));
fprintf(fid,'BS 端口 = %s\n', get_param([mdl '/BS'],'Ports') == get_param([mdl '/BS'],'Ports'));
% 顶层还有没有 ic1/ic2
r = find_system(mdl,'SearchDepth',1,'Name','ic1');
fprintf(fid,'ic1 存在 = %d\n', numel(r));
r2 = find_system(mdl,'SearchDepth',1,'Name','ic2');
fprintf(fid,'ic2 存在 = %d\n', numel(r2));
% RCESO
fprintf(fid,'RCESO 端口 = %s\n', mat2str(get_param([mdl '/RCESO'],'Ports')));
fclose(fid); fprintf('DONE\n');
