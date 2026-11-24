function [iref_A, u_act, e1] = SL(wref_rpm, wm_rads, b0, du, iq_A)
% 1 kHz 速度环（简化 ADRC）。对象 J=1.89e-5、b0=536.4：kp 需很小
persistent z1 z2 wr
Ts = 1e-3; wo = 500; kp = 0.80; wrf = 62.832; IB = 6.3069;
if isempty(z1), z1 = 0; z2 = 0; wr = 0; end
sl_rpm = 600 * Ts;                       % 0->600 rpm 用 1 s
if wr < wref_rpm, wr = min(wr + sl_rpm, wref_rpm); else, wr = max(wr - sl_rpm, wref_rpm); end
y = wm_rads / wrf;
e = wr/600 - y;
e1 = y - z1;
u = (kp*e - z2) / max(b0, 1);
u = max(min(u, 2.0), -2.0);
u_act = u + du;
z1 = z1 + Ts*(z2 + b0*u_act + 2*wo*e1);
z2 = z2 + Ts*(wo*wo*e1);
iref_A = u_act * IB;
end
