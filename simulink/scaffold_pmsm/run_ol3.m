function run_ol3()
cd('D:\Desktop\RCESO\simulink');
out = sim('pmsm_ol');
w = out.wlog;
fprintf('class = %s\n', class(w));
try, disp(fieldnames(w)); catch, end
try, disp(w.Properties.VariableNames); catch, end
try, d = w{:, 1}; fprintf('末值 %.1f rpm\n', d(end)*30/pi); catch e, fprintf('取值失败: %s\n', e.message); end
end
