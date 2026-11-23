# 附录 A 补充：轴承反力、摩擦转矩、转矩方程与转速纹波

## 1 轴承反力（力平衡 + 力矩平衡）

质心向心加速度：

$$a_{\mathrm{CM}}=-\omega^{2}r_{\perp}$$

力平衡：

$$m a_{\mathrm{CM}}=R_{A}+R_{B}+F_{g}+F_{\mathrm{coup}}\quad\Longrightarrow\quad R_{A}+R_{B}=-m\omega^{2}r_{\perp}-F_{g}-F_{\mathrm{coup}}\equiv F$$

对 O 点力矩平衡（两轴承 r_A = −aẐ、r_B = +bẐ）：

$$r_{A}\times R_{A}+r_{B}\times R_{B}=\omega\times\left(J_{O}\omega\right)-M_{g}-M_{\mathrm{coup}}\equiv N$$

投影到 ⊥Z 平面：

$$aR_{A}-bR_{B}=\hat{Z}\times N$$

解得两轴承径向反力：

$$R_{A}=\frac{bF+\hat{Z}\times N}{a+b},\qquad R_{B}=\frac{aF-\hat{Z}\times N}{a+b}$$

## 2 轴承摩擦转矩

$$T_{f}(\theta,\omega)=T_{f0}+\mu_{b}r_{b}\left(\left|R_{A}\right|+\left|R_{B}\right|\right)+c_{v}\omega+T_{\mathrm{cage}}(\theta)$$

载荷相关项的一阶展开：

$$\left|R\right|\approx R_{0}+R_{1}\cos(\theta-\varphi)\quad\Longrightarrow\quad T_{f1}\approx\mu_{b}r_{b}R_{1}\cos(\theta-\varphi)$$

## 3 绕轴转矩方程与转速纹波

实际轴等效惯量：

$$I_{n}=I_{t}\sin^{2}\beta+I_{p}\cos^{2}\beta$$

绕轴转矩方程：

$$I_{n}\dot{\omega}=T_{e}-T_{L}(\theta)-T_{f}(\theta,\omega)+M_{gZ}(\theta)+T_{\mathrm{mis}}(\theta)$$

第 k 次转矩谐波的开环机械响应：

$$\Delta\omega_{k}\approx-\frac{T_{k}}{I_{n}k\omega}\sin(k\theta-\psi_{k})$$

计入速度环灵敏度 S(s) 后：

$$\Delta\omega_{k}\approx\left|S(jk\omega)\right|\frac{T_{k}}{I_{n}k\omega}$$
