# 电机不对中故障的转矩与受力：修正版完整推导

> 对共享对话《β₀=0 重写》的核对与重写。原稿的坐标分解、平行轴定理、$I_n$ 公式、陀螺力矩形式、重力矩幅值都是对的；但“离心力对 O 点力矩为零”“三个力直接取模当轴承载荷”“重力矩是 1× 转矩主源”等处有误，且 $\hat Z^{(r)}$ 的符号与重力表达式不闭合。下面给出自洽推导（所有符号可由文中姿态矩阵复核），第 12 节逐条列出纠正。

---

## 0. 结论速览

| 量 | 结果 |
|---|---|
| 绕实际轴转动惯量 | $I_n=I_t\sin^2\beta+I_p\cos^2\beta+m d^2$，$d=l\sin\beta$ |
| 体固系角速度 | $\vec\omega^{(r)}=\omega(-\sin\beta,\,0,\,\cos\beta)$ |
| 横向陀螺力矩 | $\tau_y=\omega^2(I_p-I_t')\sin\beta\cos\beta$，$I_t'=I_t+ml^2$ |
| 绕轴方程 | $T_e-T_L-T_f+M_{gZ}+T_{mis}=I_n\dot\omega$ |
| 轴承反力 | $R_A=\dfrac{bF+\hat Z\times N}{a+b},\quad R_B=\dfrac{aF-\hat Z\times N}{a+b}$ |
| 离心力矩 | $M_c=m\omega^2l^2\sin\beta\cos\beta\ \neq 0$（已含在欧拉项内） |
| 重力矩 | $M_{gZ}=-mgd\cos\theta$，幅值 $mgd$，1× |
| 转速纹波 | $\Delta\omega_k=|S(jk\omega)|\,T_k/(I_n k\omega)$ |

---

## 1. 坐标、姿态与符号（先固定约定）

惯性系 $S_0=(X,Y,Z)$：$Z$ 为实际旋转轴（水平），重力 $\vec g=-g\hat Y$。

体固系 $S_r=(x,y,z)$：$z$ 为几何对称轴，原点 $O$ 为两轴交点。取 $\theta=0$ 时的姿态矩阵
$$
e_x=(c,0,-s),\qquad e_y=(0,1,0),\qquad e_z=(s,0,c),\qquad s=\sin\beta,\ c=\cos\beta,
$$
（右手系，$e_x\times e_y=e_z$）。于是实际轴在体固系中的坐标
$$
\boxed{\ \hat Z^{(r)}=(-\sin\beta,\ 0,\ \cos\beta)\ }
$$
且 $\hat Z$ 在体固系中为常矢量（因为 $Z$ 是旋转轴）。$\beta=0$ 时 $\hat Z^{(r)}=(0,0,1)$。

> **约定说明**：若改用 $\beta\to-\beta$，则 $\hat Z^{(r)}=(+\sin\beta,0,\cos\beta)$，本文所有横向分量整体反号，模值不变。下面全部按上式推导，可逐项复核。

转子质心（静平衡情形）：$r_C^{(r)}=(0,0,l)$，$l$ 为质心到 $O$ 的轴向距离；
质心到实际轴距离 $d=|r_C-(r_C\cdot\hat Z)\hat Z|=l\sin\beta$。

## 2. 运动学

$$
\vec\omega^{(r)}=\omega\hat Z^{(r)}=\omega(-\sin\beta,\,0,\,\cos\beta),\qquad
\omega_x=-\omega\sin\beta,\quad\omega_y=0,\quad\omega_z=\omega\cos\beta .
$$

$\omega_x\neq0$ 是角不对中的运动学标志：几何轴“斜着”绕实际轴转。

## 3. 惯量与绕轴转动惯量

绕质心 $J_C=\mathrm{diag}(I_t,I_t,I_p)$。绕固定点 $O$（平行轴定理）：
$$
J_O=J_C+m(l^2E-r_Cr_C^{\mathsf T})
=\mathrm{diag}(I_t+ml^2,\,I_t+ml^2,\,I_p)\equiv\mathrm{diag}(I_t',I_t',I_p).
$$
绕实际轴：
$$
I_n=\hat Z^{\mathsf T}J_O\hat Z=I_t\sin^2\beta+I_p\cos^2\beta+m d^2 .
$$
极限：$\beta=0\Rightarrow I_n=I_p$；$\beta=\pi/2\Rightarrow I_n=I_t+ml^2$。

## 4. 欧拉方程与横向力矩

对固定点 $O$：$\vec\tau_{ext}=J_O\dot{\vec\omega}+\vec\omega\times(J_O\vec\omega)$。体固系中 $J_O,\hat Z$ 均为常矢量，代入 $\vec\omega=\omega\hat Z$：
$$
J_O\vec\omega=\omega(-I_t's,\,0,\,I_pc),\qquad
\vec\omega\times(J_O\vec\omega)=\omega^2(I_p-I_t')\,sc\ \hat e_y,
$$
故
$$
\boxed{\ \tau_x=-I_t'\dot\omega\sin\beta,\qquad
\tau_y=\omega^2(I_p-I_t')\sin\beta\cos\beta,\qquad
\tau_z=I_p\dot\omega\cos\beta\ }
$$
绕轴分量：
$$
\tau_Z=\hat Z\cdot\vec\tau=(-\sin\beta)\tau_x+\cos\beta\,\tau_z
=I_t'\dot\omega\sin^2\beta+I_p\dot\omega\cos^2\beta=I_n\dot\omega .
$$

要点：
1. 匀速（$\dot\omega=0$）时 $\tau_x=0$，只剩横向力矩 $\tau_y$（1× 旋转矢量），由轴承弯矩承担；
2. $\tau_y$ 垂直于 $Z$，**不进入绕轴转矩方程**——所以理想刚性、匀速的角不对中**不产生 1× 转矩纹波**，只产生 1× 振动/弯矩；
3. $\tau_y$ 是“轴承对转子”的力矩；转子对轴承反号。

## 5. 离心力及其力矩（原稿的关键错误）

$$
r_\perp=r_C-(r_C\cdot\hat Z)\hat Z=(lsc,\,0,\,ls^2),\qquad |r_\perp|=ls=d,
$$
$$
\vec F_c=m\omega^2r_\perp=m\omega^2(lsc,\,0,\,ls^2).
$$
对 $O$ 点力矩：
$$
\vec M_c=r_C\times\vec F_c=(0,\;m\omega^2l^2sc,\;0)\ \neq 0 .
$$

**离心力对 $O$ 点的力矩不是零**。且与欧拉项对照：
$$
\vec\omega\times(J_O\vec\omega)=\omega^2(I_p-I_t')sc\ \hat e_y
=\underbrace{\omega^2(I_p-I_t)sc\ \hat e_y}_{\text{惯量各向异性}}
-\underbrace{\vec M_c}_{\text{离心力矩}} .
$$
即离心力矩与 $J_O$ 中 $ml^2$ 部分**等值反号**，已包含在欧拉项里。因此轴承力矩只能二选一：
- 用 $\vec\omega\times(J_O\vec\omega)$（推荐，本文做法）；或
- 用“各向异性力矩 $-$ 离心力矩”；
**不能两者相加**，否则重复计入。

## 6. 重力

重力在体固系：
$$
\vec F_g^{(r)}=\bigl(-mg\cos\beta\sin\theta,\;-mg\cos\theta,\;-mg\sin\beta\sin\theta\bigr),\qquad\theta=\omega t .
$$
对 $O$ 点力矩：
$$
\vec M_g=r_C\times\vec F_g=\bigl(mgl\cos\theta,\;-mgl\cos\beta\sin\theta,\;0\bigr),
$$
绕轴分量：
$$
M_{gZ}=\hat Z\cdot\vec M_g=-mg\,l\sin\beta\cos\theta=-mg\,d\cos\theta .
$$
幅值 $mgd$、频率 1×。符号取决于 $\theta$ 的相位定义；物理上有意义的是幅值与阶次。

## 7. 轴承反力（力平衡 + 力矩平衡）

轴承 $A,B$ 位于 $z_A=-a,\ z_B=+b$，跨距 $L=a+b$，径向反力 $R_A,R_B\perp Z$。

**力平衡**（质心仅作圆周运动，$a_{CM}=-\omega^2r_\perp$）：
$$
R_A+R_B=\underbrace{-m\omega^2r_\perp}_{F}-F_g-F_{coup}.
$$
**对 $O$ 点力矩平衡**：
$$
r_A\times R_A+r_B\times R_B=\vec\omega\times J_O\vec\omega-M_g-M_{coup}\equiv N,
\qquad r_A=-a\hat Z,\ r_B=b\hat Z .
$$
投影到 $\perp Z$ 平面并对 $\hat Z$ 叉乘（用 $\hat Z\times(\hat Z\times R)=-R$）：
$$
aR_A-bR_B=\hat Z\times N,
$$
解得
$$
\boxed{\ R_A=\frac{bF+\hat Z\times N}{a+b},\qquad
R_B=\frac{aF-\hat Z\times N}{a+b}\ }
$$
（以上均为 $\perp Z$ 平面内的二维矢量；轴向分量单独由轴向力平衡处理。）

**物理解读**：陀螺力矩以力偶 $\pm\tau_y/L$ 分配到两轴承；重力、联轴器弹性力按杠杆比 $b/L$、$a/L$ 分配。原稿把 $|F_{mis}+F_g+F_c|$ 直接当轴承载荷，既没有杠杆分配，又可能把离心力矩与陀螺力矩重复计入。

## 8. 轴承摩擦转矩

$$
T_f(\theta,\omega)=T_{f0}+\mu_b r_b\bigl(|R_A|+|R_B|\bigr)+c_v\omega+T_{cage}(\theta).
$$
$|R_A|,|R_B|$ 含 1×（重力/弯矩）与 2×（联轴器/间隙）分量，故 $T_f$ 也含 1×、2× 纹波。

## 9. 绕轴转矩方程与转速纹波

$$
\boxed{\ I_n\dot\omega=T_e-T_L(\theta)-T_f(\theta,\omega)+M_{gZ}(\theta)+T_{mis}(\theta)\ }
$$
- $T_e$ 电磁转矩；$T_L$ 负载（含不对中/偏心等效）；$T_{mis}$ 为联轴器角刚度各向异性给出的绕轴分量（理想刚性联轴器为 0）；
- $M_{gZ}=-mgd\cos\theta$，1×，幅值 $mgd$。

对第 $k$ 次转矩谐波 $T_k\cos(k\theta-\psi_k)$，开环机械响应
$$
\Delta\omega_k\approx-\frac{T_k}{I_nk\omega}\sin(k\theta-\psi_k)\quad(\text{开环}),
$$
含速度环灵敏度 $S(s)$ 时
$$
\boxed{\ \Delta\omega_k\approx|S(jk\omega)|\,\frac{T_k}{I_nk\omega}\ }.
$$

## 10. 谐波来源

| 阶次 | 来源 | 备注 |
|---|---|---|
| 1× | 静不平衡 $me\omega^2$、角不对中弯矩 $\tau_y$、重力 $mgd$、联轴器/摩擦调制 | 随转子旋转的空间固定矢量 |
| 2× | 十字滑块/Hooke 联轴器运动学（幅值 $\sim\beta^2/2$）、平行不对中柔性联轴器、间隙 | 运动学/几何非线性 |
| 高阶 | 盘面偏摆、齿式联轴器、滚动体通过、间隙碰撞 | 非线性接触 |

刚性角不对中本身只给 1× **弯矩**；2× 必须由联轴器运动学或几何非线性解释。

## 11. 与台架 $T(\theta)$ 的数值对应（600 rpm，$I_n\approx1.89\times10^{-5}$ kg·m²）

- 型线 V2 峰值 0.095 N·m，基波 $T_1\approx0.095/1.664=0.0571$ N·m；
- 开环 10 Hz 纹波：$\Delta\omega_1=T_1/(I_n\omega)=0.0571/(1.89\times10^{-5}\times62.83)\approx459$ rpm；
- 实测 $\sim22$ rpm $\Rightarrow |S(j2\pi10)|\approx0.048$——速度环把机械纹波压到 5% 左右；
- 重力矩（$m=0.1$ kg、$d=0.1$ mm）：$mgd\approx9.8\times10^{-5}$ N·m（额定的 $1.5\times10^{-4}$）；
- 陀螺力矩（$\beta=1^\circ$、$I_t'-I_p\approx-0.94\times10^{-5}$）：$\approx6.5\times10^{-4}$ N·m；
- 离心力（$l=50$ mm、$\beta=1^\circ$）：$F_c\approx0.34$ N。

可见：物理不对中在**轴承载荷**上是 N 级可见量，在**绕轴转矩**上很小；台架 0.095 N·m 是程序注入的等效故障，不能把两类量混为一谈。

## 12. 对共享稿的逐条纠正

1. **“离心力对 O 点力矩 = 0”**：错。$M_c=m\omega^2l^2\sin\beta\cos\beta$；它已含在欧拉项中，不能再叠加。
2. **“轴承载荷 = |F_mis+F_g+F_c|”**：错。须做力/力矩平衡，陀螺力矩按 $\pm\tau_y/L$ 分配，重力/弹性力按杠杆比分配。
3. **“重力矩是 1× 故障转矩主源”**：量级不对。$mgd\sim10^{-4}$ N·m，远小于负载/摩擦调制；仅在低速、大偏心时显著。
4. **$\hat Z^{(r)}$ 与重力表达式不闭合**：原稿写 $\hat Z^{(r)}=(\sin\beta,0,\cos\beta)$，但其 $F_g$、$M_g$ 对应的是 $\hat Z^{(r)}=(-\sin\beta,0,\cos\beta)$；两处符号需统一（本文取后者）。模值不受影响，但符号链必须闭合。
5. **平行不对中合成**：不能写 $d=\sqrt{\delta^2+(l\sin\beta)^2}$；$e$、$\delta$、$l\sin\beta$ 是矢量，应先矢量合成再取模。
6. **转速纹波**：只给开环 $T_k/(I_nk\omega)$；台架开环 459 rpm 对实测 22 rpm，必须乘 $|S(jk\omega)|$。
7. **2× 来源**：未说明。刚性角不对中不产生 2× 转矩；2× 来自联轴器运动学/平行不对中/间隙。
8. **符号**：$\tau_y$ 的符号随姿态取向变化；“轴承对转子”与“转子对轴承”反号，原稿未区分。

**原稿正确的部分**：坐标分解思路、$J_C$ 对角、平行轴定理、$I_n=I_t\sin^2\beta+I_p\cos^2\beta+md^2$、陀螺力矩的形式与 $I_t'=I_t+ml^2$、$M_{gZ}$ 的幅值 $mgd$ 与 1× 阶次、摩擦模型的形式。

---

## 附录：符号表

| 符号 | 含义 |
|---|---|
| $\beta$ | 角不对中（几何轴与实际轴夹角） |
| $l$ | 质心沿几何轴到交点 $O$ 的距离 |
| $d=l\sin\beta$ | 质心到实际轴距离 |
| $I_p,I_t$ | 极/横向转动惯量（绕质心） |
| $I_t'=I_t+ml^2$ | 绕 $O$ 的横向惯量 |
| $I_n$ | 绕实际轴等效转动惯量 |
| $a,b,L$ | 两轴承到 $O$ 的距离与跨距 |
| $S(s)$ | 速度环灵敏度 |
| $T_k,\psi_k$ | 第 $k$ 次转矩谐波幅值与相位 |
