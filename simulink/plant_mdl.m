function [w, y, iq] = plant_mdl(ucmd)
%#codegen
persistent init y iq2 tl
if isempty(init)
    init = 1; y = 0; iq2 = 0; tl = 0;
end
dt = 1e-3; b_true = 380;
if tl == 0
    % 2 s 后加扰动
end
f = -0.05;
iqi = iq2;
y = y + dt*(b_true*iqi + f);
iq2 = ucmd;
w = y*600;
iq = iqi;
