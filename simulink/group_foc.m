% group_foc.m —— 把 b0_foc 整理成三个子系统
srcDir='D:\Desktop\RCESO\simulink';
mdl='b0_foc';
if bdIsLoaded(mdl), close_system(mdl,0); end
load_system([srcDir '\b0_foc.slx']);
fid=fopen('out_grp.txt','w','n','UTF-8');
A=@(n)[mdl '/' n];
% ---- 1) 被控对象 PMSM ----
plant = {A('gwe'),A('emf'),A('gRq'),A('diqnum'),A('giL'),A('iqp'), ...
         A('gkt'),A('tl'),A('dw'),A('gJ'),A('wint')};
try
    b1 = Simulink.BlockDiagram.createSubsystem(plant);
    set_param(b1,'Name','PMSM_Plant');
    fprintf(fid,'plant subsystem OK -> %s\n', b1);
catch e
    fprintf(fid,'plant FAIL %s\n', e.message);
end
% ---- 2) 电流环 ----
cl = {A('eq'),A('gkp'),A('iqint'),A('gki'),A('vq')};
try
    b2 = Simulink.BlockDiagram.createSubsystem(cl);
    set_param(b2,'Name','CurrentLoop_PI');
    fprintf(fid,'current loop OK -> %s\n', b2);
catch e
    fprintf(fid,'cl FAIL %s\n', e.message);
end
% ---- 3) ADRC 外环 ----
adrc = {A('en'),A('gkpe'),A('us'),A('udiv'),A('uprev'),A('b0u'),A('z1s'), ...
        A('z1int'),A('z2int'),A('g2wo'),A('gwo2'),A('eo'),A('ypu'),A('g5'), ...
        A('th'),A('gb3'),A('td'),A('gq'),A('vchi'),A('dv'),A('gka'),A('vint')};
try
    b3 = Simulink.BlockDiagram.createSubsystem(adrc);
    set_param(b3,'Name','ADRC_SpeedLoop');
    fprintf(fid,'adrc OK -> %s\n', b3);
catch e
    fprintf(fid,'adrc FAIL %s\n', e.message);
end
% 加标注
try
    add_block('built-in/Note',[mdl '/note1'],'Position',[40 620 300 660]);
    set_param([mdl '/note1'],'Text','wref: 62.832 rad/s (=600rpm)');
catch, end
save_system(mdl,[srcDir '\b0_foc.slx']);
fprintf(fid,'SAVED\n');
fclose(fid);
fprintf('DONE\n');
