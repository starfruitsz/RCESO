function run_wave_full(ampOverride, tag)
% run_wave_full —— 三波闭环全信号记录（b0 / u / iq / 转速），供出图
% 用法： run_wave_full()            正常（识别开启，amp=0.118）
%        run_wave_full(0, 'off')    关闭识别（amp=0，b0 停在标称 400）
srcDir = fileparts(mfilename('fullpath'));
if isempty(srcDir), srcDir = pwd; end
cd(srcDir);
if nargin < 1 || isempty(ampOverride), ampOverride = -1; end
if nargin < 2 || isempty(tag), tag = 'on'; end
fid0 = fopen('b0_ident_m.m', 'r'); orig = fread(fid0, inf, 'char=>char').'; fclose(fid0);
names = {'正弦', '方波', '三角'};
res = [];
for wi = 0:2
    txt = regexprep(orig, 'wave\s*=\s*0;', sprintf('wave   = %d;', wi));
    if ampOverride >= 0
        txt = regexprep(txt, 'amp\s*=\s*[0-9.]+;', sprintf('amp    = %g;', ampOverride));
    end
    if strcmp(tag, 'off')
        txt = regexprep(txt, 'upd_on\s*=\s*1;', 'upd_on  = 0;');
    end
    fid = fopen('b0_ident_m.m', 'w'); fwrite(fid, txt); fclose(fid);
    fprintf('--- %s 波 (wave=%d, amp=%.3f) ---\n', names{wi+1}, wi, ampOverride);
    build_foc_m;
    L = load('foc_m_log.mat');
    r = struct();
    r.name = names{wi+1};
    r.t   = L.b0_log.Time(:);
    r.b0  = L.b0_log.Data(:);
    r.w   = L.w_log.Data(:);
    r.iq  = L.iq_log.Data(:);
    r.u   = L.du_log.Data(:);
    res = [res, r];
end
fid = fopen('b0_ident_m.m', 'w'); fwrite(fid, orig); fclose(fid);
save(sprintf('wave_full_%s.mat', tag), 'res');
fprintf('saved wave_full_%s.mat\n', tag);
end
