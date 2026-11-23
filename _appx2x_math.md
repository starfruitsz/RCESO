# 附录 A 补充：2× 分量的来源（OMML 片段）

## 1 现有方程是通用的，2× 由 T(θ) 提供

绕轴转矩方程（对任意谐波成立）：

$$I_{n}\dot{\omega}=T_{e}-T_{L}(\theta)-T_{f}(\theta,\omega)+M_{gZ}(\theta)+T_{mis}(\theta)$$

第 k 次谐波对应的转速纹波：

$$\Delta\omega_{k}\approx\left|S(jk\omega)\right|\frac{T_{k}}{I_{n}k\omega}$$

T(θ) 里只要出现 cos2θ 或 sin2θ，k=2 就是 2× 分量；下面三处会产生这样的项。

## 2 来源一：Hooke / 十字滑块运动学

两轴转角关系：

$$\tan\theta_{2}=\frac{\tan\theta_{1}}{\cos\beta}$$

从动轴角速度比：

$$\frac{\omega_{2}}{\omega_{1}}=\frac{\cos\beta}{1-\sin^{2}\beta\cos^{2}\theta_{1}}$$

小角度展开：

$$\frac{\omega_{2}}{\omega_{1}}\approx1+\frac{\beta^{2}}{2}\cos2\theta_{1}$$

恒功率下的转矩：

$$T_{2}\approx T_{1}\left[1-\frac{\beta^{2}}{2}\cos2\theta_{1}\right]$$

## 3 来源二：联轴器刚度各向异性

偏移 a 在联轴器坐标系中随 θ 旋转，弹性势能：

$$U(\theta)=\frac{1}{2}a^{2}\left(k_{x}\cos^{2}\theta+k_{y}\sin^{2}\theta\right)=\frac{1}{4}a^{2}\left[(k_{x}+k_{y})+(k_{x}-k_{y})\cos2\theta\right]$$

对 θ 的广义力矩：

$$T_{\theta}=-\frac{\partial U}{\partial\theta}=\frac{a^{2}}{2}(k_{x}-k_{y})\sin2\theta$$

角不对中版本（把 a 换成 β）：

$$T_{\theta}=\frac{\beta^{2}}{2}(k_{x}-k_{y})\sin2\theta$$

本质是三角恒等式：

$$\cos\theta\sin\theta=\frac{1}{2}\sin2\theta$$

## 4 来源三：间隙 / 接触非线性

死区特性（分段非线性，傅里叶展开含 2×、3×）：

$$T_{gap}(\varphi)=\begin{cases}k(\varphi-g), & \varphi>g\\ 0, & |\varphi|\le g\\ k(\varphi+g), & \varphi<-g\end{cases}$$

## 5 代回纹波公式

$$\Delta\omega_{2}\approx\left|S(j2\omega)\right|\frac{T_{2}}{2I_{n}\omega}$$

## 6 平行不对中：几何与 2× 转矩（补充）

两轴平行、中心线偏移 e（空间固定矢量，在联轴器坐标系中随 θ 旋转）：

$$\mathbf{e}(\theta)=\left(e\cos\theta,\,-e\sin\theta\right)$$

各向同性联轴器的恒定径向力（空间固定方向）：

$$\mathbf{F}=k\,\mathbf{e}$$

弹性势能（各向异性 k_x、k_y）：

$$U(\theta)=\frac{1}{2}e^{2}\left(k_{x}\cos^{2}\theta+k_{y}\sin^{2}\theta\right)$$

绕轴 2× 转矩（各向同性时为零）：

$$T_{\theta}=\frac{e^{2}}{2}\left(k_{x}-k_{y}\right)\sin2\theta$$
