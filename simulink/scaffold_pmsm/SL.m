function [iref_A, u_pu, e1] = SL(wref_rpm, wm_rads, b0, du, iq_A)
% 1 kHz 速度环（简化 ADRC：线性 ESO + PD + b0 归一化）
% 归一化：y = w/wref，u = iq/IB（pu），b0 = kt*IB/(J*wref)
persistent z1 z2
Ts = 1e-3; wo = 500; kp = 75.36; wr = 62.832; IB = 6.3069;
y = wm_rads / wr;
if isempty(z1), z1 = y; z2 = 0; end
e = wref_rpm/600 - y;
e1 = y - z1;
u = (kp*e - z2) / max(b0, 1);
z1 = z1 + Ts*(z2 + b0*u + 2*wo*e1);
z2 = z2 + Ts*(wo*wo*e1);
u_pu = u;
iref_A = (u + du) * IB;
end
