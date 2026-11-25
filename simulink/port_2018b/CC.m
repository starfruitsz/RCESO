function [va, vb, vc] = CC(idr, iqr, id, iq, thm)
% 电流环 20 kHz（Ts=5e-5）+ 反 Park
% 标定结果（2026-11-24，静止注入扫描）：机器 d 轴在 phase-A 轴 +90° 处
%   phi=90° 时 id=V/R、iq≈0  =>  theta_e = p*thm + pi/2
persistent xi xq
Ts = 5e-5; p = 4;
Kp = 7.2; Ki = 2200;
if isempty(xi), xi = 0; xq = 0; end
ed = idr - id;
eq = iqr - iq;
xi = xi + Ki*Ts*ed;
xq = xq + Ki*Ts*eq;
vd = Kp*ed + xi;
vq = Kp*eq + xq;
th = p*thm + pi/2;
va = vd*cos(th) - vq*sin(th);
vb = vd*cos(th - 2*pi/3) - vq*sin(th - 2*pi/3);
vc = vd*cos(th + 2*pi/3) - vq*sin(th + 2*pi/3);
end
