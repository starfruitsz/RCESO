% lic_probe.m
fid=fopen('out_lic.txt','w','n','UTF-8');
for n={'Simscape','Simscape_Electrical','SimPowerSystems','Simulink_Control_Design'}
    try, v=license('test',n{1}); catch, v=-1; end
    fprintf(fid,'%-28s %d\n', n{1}, v);
end
% 找 PMSM / 逆变器 模块
libs = {'Simscape/Electrical/Specialized Power Systems/Electrical Sources', ...
        'sps_lib'};
fprintf(fid,'--- exist sps_lib: %d\n', exist('sps_lib','file'));
try
    load_system('sps_lib');
    b = find_system('sps_lib','SearchDepth',3,'MaskType','PMSM');
    fprintf(fid,'PMSM found: %d\n', numel(b));
    for i=1:min(3,numel(b)), fprintf(fid,'  %s\n', b{i}); end
catch e
    fprintf(fid,'sps_lib err %s\n', e.message);
end
try
    load_system('simscape');
    fprintf(fid,'SIMSCAPE_OK\n');
catch e
    fprintf(fid,'simscape err %s\n', e.message);
end
fclose(fid);
