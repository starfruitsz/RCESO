function [va, vb, vc] = CC(idr, iqr, id, iq, thm)
% 电流环 20 kHz（Ts=5e-5）+ 反 Park，输出三相电压给平均逆变器
% 电机约定：电角度 θe = p·θm；采用幅值不变 Park 变换
persistent xi xq
Ts = 5e-5; p = 4;
Kp = 7.2; Ki = 2200;          % L*wc, R*wc（wc≈2 kHz）
if isempty(xi), xi = 0; xq = 0; end
ed = idr - id;
eq = iqr - iq;
xi = xi + Ki*Ts*ed;
xq = xq + Ki*Ts*eq;
vd = Kp*ed + xi;
vq = Kp*eq + xq;
th = p*thm;
va = vd*cos(th) - vq*sin(th);
vb = vd*cos(th - 2*pi/3) - vq*sin(th - 2*pi/3);
vc = vd*cos(th + 2*pi/3) - vq*sin(th + 2*pi/3);
end
