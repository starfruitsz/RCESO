# -*- coding: utf-8 -*-
"""_adrc_sweep.py —— 扫 k1（k2,k3 按论文比例 3e-4,1e-6 缩放），看是否存在"调好了就有用"的增益。"""
import math, numpy as np, importlib.util
spec=importlib.util.spec_from_file_location("lab","_adrc_lab.py")
lab=importlib.util.module_from_spec(spec); spec.loader.exec_module(lab)

def met(d,tstep=0.5):
    t=d["t"]; ref=1000.0 if d["wref"]==lab.W_HI else 500.0
    m=t>=tstep; seg=d["w"][m]; ts=t[m]
    dip=seg.min()-ref; over=(seg.max()/ref-1)*100
    tr=(t>=tstep)&(t<=tstep+0.6)
    e1tr=float(np.sqrt(np.mean(d["e1"][tr]**2)))
    return dip,over,e1tr,d["bh"].min(),d["bh"].max(),d["bh"][-1],float(seg.max())

base_speed=lab.sim("speed",1.0,False); base_load=lab.sim("load",4.0,False)
bs=met(base_speed); bl=met(base_load)
print("baseline conv speed: over %.2f%%  e1tr %.2f  max %.0f"%(bs[1],bs[2],bs[6]))
print("baseline conv load J4: dip %.1f  e1tr %.2f  max %.0f"%(bl[0],bl[2],bl[6]))
print("k1      speed(J1): over%  e1tr   maxW | load(J4): dip    e1tr   bh_end  bh_min")
for k1 in (0.003,0.01,0.03,0.1,0.3,1.0,3.0,12.0):
    k2=k1*3e-4; k3=k1*1e-6
    ds=lab.sim("speed",1.0,True,k1=k1,k2=k2,k3=k3)
    dl=lab.sim("load",4.0,True,k1=k1,k2=k2,k3=k3)
    ms=met(ds); ml=met(dl)
    print("%-7g %7.2f %6.2f %7.0f | %8.1f %6.2f %8.1f %8.1f"%(
        k1, ms[1], ms[2], ms[6], ml[0], ml[2], ml[5], ml[3]))
