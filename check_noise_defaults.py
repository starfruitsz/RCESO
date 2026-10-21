# -*- coding: utf-8 -*-
"""噪声口径默认值自检：0.025 N·m / 6 rpm（1%） / 0.2 A"""
from noise_cfg import NOISE, NOISE_LAB, NOISE_STD, NOISE_HARSH

EXP = {"sig_T_nm": 0.025, "sig_n_rpm": 6.0, "i_noise_peak": 0.2}
for k, v in EXP.items():
    got = float(NOISE[k])
    assert abs(got - v) < 1e-12, (k, got, v)
print("NOISE defaults OK:", {k: NOISE[k] for k in EXP})
for name, prof in [("lab", NOISE_LAB), ("std", NOISE_STD), ("harsh", NOISE_HARSH)]:
    print(name, prof)
