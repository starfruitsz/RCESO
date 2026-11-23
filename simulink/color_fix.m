% color_fix.m
srcDir='D:\Desktop\RCESO\simulink'; mdl='b0_foc';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system([srcDir '\b0_foc.slx']);
fid=fopen('out_color2.txt','w','n','UTF-8');
A=@(n)[mdl '/' n];
cl = {'eq','gkp','iqint','gki','vq'};
cols = {'green','darkGreen','cyan'};
n=0;
for i=1:numel(cl)
    for c=1:numel(cols)
        try
            set_param(A(cl{i}),'BackgroundColor',cols{c});
            n=n+1; break;
        catch
        end
    end
end
fprintf(fid,'current loop colored: %d / %d\n', n, numel(cl));
save_system(mdl,[srcDir '\b0_foc.slx']);
fprintf(fid,'SAVED\n'); fclose(fid); fprintf('DONE\n');
