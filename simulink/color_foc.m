% color_foc.m —— 按功能给块上色，便于手动分组
srcDir='D:\Desktop\RCESO\simulink'; mdl='b0_foc';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system([srcDir '\b0_foc.slx']);
fid=fopen('out_color.txt','w','n','UTF-8');
A=@(n)[mdl '/' n];
sets = { {'gwe','emf','gRq','diqnum','giL','iqp','gkt','tl','dw','gJ','wint'}, 'lightBlue',  'PMSM 本体'; ...
         {'eq','gkp','iqint','gki','vq'},                                    'lightGreen','电流环 PI'; ...
         {'eo','g2wo','gwo2','b0u','z1s','z1int','z2int','g5','th','gb3','td','gq','vchi','dv','gka','vint','uprev'}, 'yellow', '观测器 ESO+重复内模'; ...
         {'en','gkpe','us','udiv','ypu'},                                    'orange',     '控制律'; ...
         {'C'},                                                              'magenta',    'b0 辨识 C Caller' };
for k=1:size(sets,1)
    n_ok = 0;
    for i=1:numel(sets{k,1})
        try
            set_param(A(sets{k,1}{i}),'BackgroundColor',sets{k,2});
            n_ok = n_ok + 1;
        catch e
            fprintf(fid,'fail %s : %s\n', sets{k,1}{i}, e.message);
        end
    end
    fprintf(fid,'%-22s %2d 块 -> %s\n', sets{k,3}, n_ok, sets{k,2});
end
save_system(mdl,[srcDir '\b0_foc.slx']);
fprintf(fid,'SAVED\n'); fclose(fid); fprintf('DONE\n');
