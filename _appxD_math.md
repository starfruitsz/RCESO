# 附录 D：律 D / J / T 的稳定性与有界性（详细版）

## D.1 符号与模型

被控对象与控制律（程序默认 e = r − z1）：

$$\dot{x}=b_{0}u+d(t),\qquad u=\frac{k_{p}e-z_{2}-v}{\hat{b}},\qquad e=r-z_{1}$$

ESO 观测器（e1 = x − z1 为新息）：

$$\dot{z}_{1}=z_{2}+\hat{b}u+v+2\omega_{o}(x-z_{1}),\qquad \dot{z}_{2}=\omega_{o}^{2}(x-z_{1})$$

重复通道（时滞 T，|Q|<1）：

$$v(t)=Q\,v(t-T)+\varphi(e_{1}),\qquad |\varphi(e_{1})|\le\kappa|e_{1}|,\qquad T=T_{g}(1+\delta)$$

外部输入的能量：

$W(t)=|d(t)|^{2}+|\dot{r}(t)|^{2},\qquad \bar{W}=\sup_{t}W(t)$

## D.2 假设

**假设 A1（对象与输入有界）**：b0 ∈ [b̲0, b̄0] 且 b̲0 > 0；d、r、ṙ 有界，即 W̄ < ∞。

**假设 A2（律D 的增益盒）**：

$$k_{p,\mathrm{eff}}\in[k_{p},\,k_{p}(1+a)],\qquad \omega_{o,\mathrm{eff}}\in[\omega_{o},\,\omega_{o}(1+k_{b})]$$

**假设 A3（律J 的参数盒与速率）**：

$$\hat{b}(t)\in[\underline{b},\,\overline{b}],\qquad |\dot{\hat{b}}|\le L_{J}$$

**假设 A4（律T 的参数盒与速率）**：

$$|\hat{\delta}|\le\delta_{\max},\qquad |\Delta\hat{\delta}|\le\sigma$$

**假设 A5（盒内一致 ISS）**：存在正定、径向无界的 V 与 α, β > 0，使对任意 θ ∈ Θ

$$\dot{V}\le-\alpha V+\beta W$$

**假设 A6（参数灵敏度有界）**：

$$\left|\frac{\partial V}{\partial\theta}\right|\le c_{V}$$

## D.2.1 假设 A5 的证明

**目标**：在参数盒 Θ 上构造公共 Lyapunov 函数 V 与 α, β > 0，使 V̇ ≤ −αV + βW。

**第一步（消去 u，化为三阶线性系统）**：把 u = (k_p e − z2 − v)/b̂ 代入 ESO 的 z1 方程，得

$$\dot{z}_{1}=k_{p}e+2\omega_{o}e_{1}$$

记 ρ = b0/b̂，三条误差方程为

$$\dot{e}=\dot{r}-k_{p}e-2\omega_{o}e_{1}$$

$$\dot{e}_{1}=(\rho-1)k_{p}e-2\omega_{o}e_{1}-\rho z_{2}-\rho v+d$$

$$\dot{z}_{2}=\omega_{o}^{2}e_{1}$$

**第二步（无扰动时的一致性 Hurwitz）**：令 ξ = (e, e1, z2)，在 v=d=ṙ=0 时 ξ̇ = Mξ，

$$M=\begin{bmatrix}-k_{p} & -2\omega_{o} & 0\\ (\rho-1)k_{p} & -2\omega_{o} & -\rho\\ 0 & \omega_{o}^{2} & 0\end{bmatrix}$$

特征多项式为

$$p(s)=\det(sI-M)=s^{3}+(2\omega_{o}+k_{p})s^{2}+\rho\omega_{o}(\omega_{o}+2k_{p})s+k_{p}\rho\omega_{o}^{2}$$

Routh–Hurwitz：三个系数均为正，且

$$a_{1}a_{2}-a_{3}=2\rho\omega_{o}(\omega_{o}+k_{p})^{2}>0$$

故对任意 ρ, kp, ω_o > 0 系统 Hurwitz；Θ 紧致且系数连续 ⇒ Routh 余量有正下界 ⇒ 存在与 θ 无关的衰减率 μ > 0。

**第三步（二次 Lyapunov 函数）**：对每个 θ 解 Lyapunov 方程

$$A^{\top}P+PA=-I$$

P(θ) 连续，Θ 紧致 ⇒ p1I ≤ P ≤ p2I；V0 = ξᵀPξ 满足

$$\dot{V}_{0}\le-\|\xi\|^{2}+2\xi^{\top}P\left(B_{v}v+B_{d}d+B_{r}\dot{r}\right)$$

**第四步（a）：线性系统的 L∞ 增益**。由第二步，A 在 Θ 上一致 Hurwitz，故存在 K, μ > 0 使

$$\|e^{At}\|\le K e^{-\mu t}$$

系统输入为 (v, d, ṙ)，输出 y = e1 = Cξ，零状态解为

$$e_{1}(t)=C\int_{0}^{t}e^{A(t-s)}\left(B_{v}v(s)+B_{d}d(s)+B_{r}\dot{r}(s)\right)ds$$

取绝对值并对 t 取上确界：

$$\|e_{1}\|_{\infty}\le\frac{\|C\|K}{\mu}\left(\|B_{v}\|\|v\|_{\infty}+\|B_{d}\|\|d\|_{\infty}+\|B_{r}\|\|\dot{r}\|_{\infty}\right)$$

记增益

$$c_{v}=\frac{\|C\|K\|B_{v}\|}{\mu},\qquad c_{d}=\frac{\|C\|K\|B_{d}\|}{\mu},\qquad c_{r}=\frac{\|C\|K\|B_{r}\|}{\mu}$$

并利用 |d|、|ṙ| ≤ √W，得

$\|e_{1}\|_{\infty}\le c_{v}\|v\|_{\infty}+c_{w}\|\sqrt{W}\|_{\infty},\qquad c_{w}=c_{d}+c_{r}$

这就是“线性系统给出”的那一行的具体来源：增益是脉冲响应的 L1 范数（∫|h|dt ≤ K/μ），有限性来自 A 的指数稳定。初值项 e^{At}ξ(0) 按 e^{−μt} 衰减，只贡献有界常数。

**第四步（b）：RC 通道的小增益闭合**。由 v(t) = Qv(t−T) + φ(e1)、|φ| ≤ κ|e1|，

$$|v(t)|\le Q|v(t-T)|+\kappa|e_{1}(t)|\ \Longrightarrow\ \|v\|_{\infty}\le\frac{\kappa}{1-Q}\|e_{1}\|_{\infty}\equiv\bar{\kappa}\|e_{1}\|_{\infty}$$

把 v 当作有界输入，线性系统给出 ||e1||∞ ≤ c_v||v||∞ + c_w||√W||∞，代入得

$\left(1-c_{v}\bar{\kappa}\right)\|e_{1}\|_{\infty}\le c_{w}\|\sqrt{W}\|_{\infty}$

若小增益条件 c_v·κ̄ < 1（即报告里的 γ0 < 1），则 e1 与 v 都被 W 界住。

**第五步（合成）**：把第四步代回第三步，

$$\dot{V}\le-\alpha V+\beta W$$

其中 α, β 只依赖盒内参数的界（P、c_v、c_w 连续 + Θ 紧致），与 θ(t) 无关——这就是假设 A5。

**说明**：Routh 余量、P 的一致性和 Lyapunov 方程解都是解析的；唯一需要数值核验的是小增益 c_v·κ̄ < 1，本文用频域裕度与仿真包络确认。

## D.3 引理 1（参数紧致 + 速率有界）

**引理 1**：在 A2–A4 下，θ(t) 始终落在紧致盒 Θ 内，且 |θ̇| ≤ L。

**证明（分三条）**：

（1）**律D（用 A2）**：门控是饱和函数，

$$g=\frac{e_{1m}^{2}}{e_{1m}^{2}+\varepsilon^{2}}\in[0,1]$$

代入 k_p,eff = k_p(1+ag)、ω_o,eff = ω_o(1+k_b g)，直接得到 A2 的增益盒；g 连续，无跳变。

（2）**律J（用 A3）**：限幅更新保证 b̂ ∈ [b̲,b̄]；低通切换的解析解为

$$\hat{b}(t)=b_{\mathrm{goal}}+\left(\hat{b}(t_{k})-b_{\mathrm{goal}}\right)e^{-(t-t_{k})/\tau}$$

对 t 求导得

$$|\dot{\hat{b}}|=\frac{|b_{\mathrm{goal}}-\hat{b}(t)|}{\tau}\le\frac{\overline{b}-\underline{b}}{\tau}=L_{J}$$

（3）**律T（用 A4）**：限幅更新 ⇒ |δ̂| ≤ δ_max、每窗 |Δδ̂| ≤ σ；叠加抖动后

$$\delta=\hat{\delta}+\Delta\sin(\omega_{d}t)\ \Longrightarrow\ |\delta|\le\delta_{\max}+\Delta$$

时滞落在紧致区间：

$$T=T_{g}(1+\delta)\in\left[T_{g}(1-\delta_{\max}-\Delta),\,T_{g}(1+\delta_{\max}+\Delta)\right]$$

（4）合并三条，总速率上界为

$$L=L_{J}+\frac{\sigma}{N P_{d}}+\frac{2\pi\Delta}{P_{d}}$$

## D.4 引理 2（慢变参数 Lyapunov 界）

**引理 2**：在 A5、A6 下，若 θ(t) ∈ Θ 且 |θ̇| ≤ L，则

$$V(t)\le e^{-\alpha t}V(0)+\frac{\beta\bar{W}+c_{V}L}{\alpha}$$

**证明**：沿闭环轨迹对 V 用链式法则，并代入 A5、A6：

$$\dot{V}=\nabla_{x}V\cdot f(x,\theta)+\frac{\partial V}{\partial\theta}\dot{\theta}\le-\alpha V+\beta W+c_{V}L$$

由 Gronwall 不等式（常数强制项）：

$$V(t)\le e^{-\alpha t}V(0)+\left(\beta\bar{W}+c_{V}L\right)\frac{1-e^{-\alpha t}}{\alpha}$$

于是 sup_t V(t) ≤ max{V(0), (βW̄ + c_V L)/α}。

## D.5 定理（三律联立有界性）

**定理**：在 A1–A6 下，闭环所有信号有界，且存在 c0 > 0 使

$$|e(t)|\le\sqrt{\frac{\beta\bar{W}+c_{V}L}{\alpha c_{0}}}$$

**证明（逐条对应假设/引理）**：

**第 1 步（参数界）**：由**引理 1**（其中律D 用 A2、律J 用 A3、律T 用 A4）得 θ(t) ∈ Θ 且 |θ̇| ≤ L。

**第 2 步（状态界）**：由**引理 2**（用 A5、A6）得

$$\sup_{t}V(t)\le\max\left\{V(0),\ \frac{\beta\bar{W}+c_{V}L}{\alpha}\right\}$$

**第 3 步（误差界）**：V 正定 ⇒ 存在 c0 > 0 使 V ≥ c0|e|²，代入第 2 步即得定理的误差界。

**第 4 步（其余状态）**：V 径向无界 ⇒ x、z1、z2、v 以及在 Θ 内的参数均有界。

## D.6 注记

（1）A5 的可检验形式是底层速度环 + 重复通道的小增益条件：

$$\gamma_{0}=\left\|Q\,e^{-sT}S_{0}(s)\right\|_{\infty}<1$$

|Q| < 1 保证内模对任意有界 T 稳定；小增益只与增益有关，时滞扰动只移动陷波相位。Θ 上逐点验证 + 紧致性 ⇒ 一致裕度 ⇒ A5 成立（本文用频域裕度与全工况仿真包络数值验证）。

（2）**证了什么**：三个自适应参数被限制在紧致盒内、变化率有界（引理 1）；由此闭环状态有界、误差有显式界（引理 2 + 定理）。

（3）**没证什么**：δ̂ → δ* 的渐近收敛（σ 步长与噪声决定极限环大小）；A5 本身是假设，靠数值验证而非解析证明。

（4）律D 的增益必须饱和（g ≤ 1）才能保证 A2 的盒紧致；无界门控会使 A5 失效。