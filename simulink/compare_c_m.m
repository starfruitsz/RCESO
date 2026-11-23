% compare_c_m.m —— C 版 vs MATLAB 版逐点对比
srcDir = 'D:\Desktop\RCESO\simulink';
cd(srcDir);
fid = fopen('out_cmp.txt','w','n','UTF-8');
try
    mex('-O','b0_ident_mex.c','b0_ident.c','b0_ident_wrap.c');
    fprintf(fid,'MEX_BUILD_OK\n');
catch e
    fprintf(fid,'MEX_BUILD_FAIL %s\n', e.message);
    fclose(fid); return;
end
N = 130000; t = (0:N-1)'*1e-3;
rng(42);
u  = 0.05*sin(2*pi*0.3*t) + 0.01*randn(N,1);
iq = 0.118*sin(2*pi*65*t) + 0.20*sin(2*pi*0.3*t) + 0.005*randn(N,1);
om = 600 + 5*sin(2*pi*0.1*t);
e1 = 0.002*randn(N,1) + 0.001*sin(2*pi*65*t);
v  = 0.01*sin(2*pi*0.05*t) + 0.001*randn(N,1);
b0c = zeros(N,1); duc = zeros(N,1);
b0m = zeros(N,1); dum = zeros(N,1);
tic;
for k = 1:N
    [b0c(k), duc(k)] = b0_ident_mex(iq(k), u(k), om(k), e1(k), v(k));
    [b0m(k), dum(k)] = b0_ident_m(iq(k), u(k), om(k), e1(k), v(k));
end
el = toc;
d0 = abs(b0c - b0m); dd = abs(duc - dum);
fprintf(fid,'N=%d  用时 %.1f s\n', N, el);
fprintf(fid,'b0 终值: C=%.6f  ML=%.6f  差=%.3e\n', b0c(end), b0m(end), abs(b0c(end)-b0m(end)));
fprintf(fid,'b0 最大绝对差 = %.3e  (相对 %.3e)\n', max(d0), max(d0./max(abs(b0c),1e-9)));
fprintf(fid,'du 最大绝对差 = %.3e  (相对 %.3e)\n', max(dd), max(dd./max(abs(duc),1e-9)));
fprintf(fid,'du 非零点数: C=%d  ML=%d\n', sum(duc~=0), sum(dum~=0));
fprintf(fid,'逐点比较点数 = %d\n', N);
save('cmp_result.mat','t','b0c','b0m','duc','dum','d0','dd');
fclose(fid); fprintf('DONE\n');
