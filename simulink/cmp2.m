% cmp2.m —— 用真实闭环输入回放，逐点对比 C 与 MATLAB 实现
srcDir='D:\Desktop\RCESO\simulink'; cd(srcDir);
fid=fopen('out_cmp2.txt','w','n','UTF-8');
load('foc_io.mat');           % iqd, ud, omd, e1d, vd
N = numel(iqd);
try
    mex('-O','b0_ident_mex.c','b0_ident.c','b0_ident_wrap.c');
    fprintf(fid,'MEX_OK (重编译)\n');
catch e
    fprintf(fid,'MEX_FAIL %s\n', e.message); fclose(fid); return;
end
clear b0_ident_m;             % 清 persistent
b0c=zeros(N,1); duc=zeros(N,1); b0m=zeros(N,1); dum=zeros(N,1);
tic;
for k=1:N
    [b0c(k),duc(k)] = b0_ident_mex(iqd(k),ud(k),omd(k),e1d(k),vd(k));
    [b0m(k),dum(k)] = b0_ident_m(iqd(k),ud(k),omd(k),e1d(k),vd(k));
end
el=toc;
d0=abs(b0c-b0m); dd=abs(duc-dum);
fprintf(fid,'N=%d  用时 %.1f s\n',N,el);
fprintf(fid,'b0 终值: C=%.6f  ML=%.6f  差=%.2e\n',b0c(end),b0m(end),d0(end));
fprintf(fid,'b0 最大差=%.3e  平均差=%.3e\n',max(d0),mean(d0));
fprintf(fid,'du 最大差=%.3e  du 非零: C=%d ML=%d\n',max(dd),sum(duc~=0),sum(dum~=0));
first = find(d0>1e-6,1);
if isempty(first), fprintf(fid,'首次超 1e-6 的点: 无（全程一致）\n');
else, fprintf(fid,'首次超 1e-6 的点: %d (t=%.3fs)  该处 C=%.6f ML=%.6f\n',first,(first-1)*1e-3,b0c(first),b0m(first)); end
first2 = find(d0>0.01,1);
if ~isempty(first2), fprintf(fid,'首次超 0.01 的点: %d (t=%.3fs)\n',first2,(first2-1)*1e-3); end
fprintf(fid,'相对误差 b0: max=%.3e  mean=%.3e\n', max(d0./max(abs(b0c),1e-9)), mean(d0./max(abs(b0c),1e-9)));
save('cmp2.mat','b0c','b0m','duc','dum','d0','dd');
figure('Visible','off');
subplot(2,1,1); plot((0:N-1)*1e-3,b0c,'b',(0:N-1)*1e-3,b0m,'r--'); grid on;
ylabel('b0'); legend('C','MATLAB'); title('b0: C vs MATLAB (同一输入回放)');
subplot(2,1,2); semilogy((0:N-1)*1e-3,max(d0,1e-12)); grid on; ylabel('|dB0|'); xlabel('t/s');
print('-dpng','-r110','fig_cmp_cm.png');
fprintf(fid,'FIG_OK\n'); fclose(fid); fprintf('DONE\n');
