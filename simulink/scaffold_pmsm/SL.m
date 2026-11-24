function [iref_A, u_act, e1] = SL(wref_rpm, wm_rads, b0, du, iq_A)
% 1 kHz 速度环：ESO 的 u 必须用【注入后】的实际指令（幅频特性看的是输入 u）
persistent z1 z2 wr
Ts = 1e-3; wo = 500; kp = 1.0; wrf = 62.832; IB = 6.3069;
if isempty(z1), z1 = 0; z2 = 0; wr = 0; end
sl_rpm = 2000 * Ts;
if wr < wref_rpm, wr = min(wr + sl_rpm, wref_rpm); else, wr = max(wr - sl_rpm, wref_rpm); end
y = wm_rads / wrf;
e = wr/600 - y;
e1 = y - z1;
u = (kp*e - z2) / max(b0, 1);
u = max(min(u, 2.0), -2.0);
u_act = u + du;                                  % 注入后的实际电流指令（pu）
z1 = z1 + Ts*(z2 + b0*u_act + 2*wo*e1);          % ESO 用 u_act
z2 = z2 + Ts*(wo*wo*e1);
iref_A = u_act * IB;
end
