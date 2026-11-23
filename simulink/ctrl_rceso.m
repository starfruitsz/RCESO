function [u, e1o, vo] = ctrl_rceso(wref, w, b0)
%#codegen
persistent init z1 z2 v vbuf vi uprev
if isempty(init)
    init = 1;
    z1 = 0;
    z2 = 0;
    v = 0;
    vbuf = zeros(1,50);
    vi = 1;
    uprev = 0;
end
dt = 1e-3;
kp = 75.36;
wo = 500;
b3 = 4000;
zeta = 0.2;
tau0 = 20e-3;
Q0 = 0.98;
yref = wref/600;
e1 = yref - z1;
vd = vbuf(vi);
vchi = Q0*vd + b3*tanh(e1/zeta);
vn = vchi + (v - vchi)*exp(-dt/tau0);
vbuf(vi) = v;
vi = vi + 1;
if vi > 50
    vi = 1;
end
z1n = z1 + dt*(z2 + b0*uprev + v + 2*wo*e1);
z2n = z2 + dt*(wo*wo*e1);
en = yref - z1n;
u = (kp*en - z2n - vn)/b0;
z1 = z1n;
z2 = z2n;
v = vn;
uprev = u;
e1o = e1;
vo = vn;
u = single(u);
e1o = single(e1o);
vo = single(vo);
end
