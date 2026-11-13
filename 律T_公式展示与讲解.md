# 律 T（T 自适应 / 锁相 ESC）公式展示与讲解

> **用途**：给 PPT「频率自适应律 T」页做公式展示与口播稿；本文件只负责文字与公式，版面由你粘贴。
>
> **用法**
> 1. **mathtype** 代码块：复制块内单行 LaTeX，到 MathType（Preferences → Workspace Preferences → 勾选 Allow TeX language input）粘贴回车。
> 2. **xml** 代码块：每个“符号”注释行下的一行 m:oMath 元素是 OMML；复制该行到 PPT 文本框/Word，按你的 OMML 流程转成公式。单行字母与短公式都在这里。
> 3. 数值口径：v5.6，真实 J=4.81e-5=2.545J_nom、j_oracle、单种子 20261018；与 rcso_v3.tex §5.5/附录 C 同口径。旧名义-J 数字（27.49/30.20 等）不要再用。
>
> **符号约定**：T 重复周期；δ 周期修正；T_gross 粗周期；ω_f 滤波角频率；A 10 Hz 基波残余；Q 遗忘因子；τ 低通时间常数；κ 碗形曲率；Δ/σ 抖动幅值/步长；P_d 抖动周期；N 每步抖动周期数；δ_max 限幅。

---


## 第 1 页｜为什么需要律 T

**PPT 画面文字**

- 低通重复通道的周期 T 必须对准真实基波周期；T 错 → 延迟线相位错 → 10 Hz 残余 A 变大。
- 律 T 不动增益，只修周期：T = T_gross(1+δ)，T_gross = 2π/ω_f。
- 目标：让内模在 10 Hz 的 |D(jω)| 最小，也就是让 A 最小。
- 关键：最优修正不是 0，而是相位对齐值 δ* = −arctan(ωτ)/(2π)。

**讲解词（口播）**

重复控制的核心是“记住上一个周期”。如果记忆长度 T 和真实基波周期对不上，延迟线回来的波形就转了一个相位，10 Hz 的残余不但压不下去，还可能被放大。

律 T 不动增益，只动周期：T = T_gross(1+δ)。T_gross 由测速滤波后的角频率给出，δ 是周期修正。问题变成：δ 取多少？答案不是 0，而是让内模在 10 Hz 处相位对齐的值。


**MathType 展示公式**

**两层周期**

```mathtype
T=T_{\mathrm{gross}}\,(1+\delta),\quad T_{\mathrm{gross}}=\frac{2\pi}{\omega_f}
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- T（重复周期） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑇</m:t></m:r></m:oMath>
<!-- δ（周期修正） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝛿</m:t></m:r></m:oMath>
<!-- T_gross（粗周期） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑔𝑟𝑜𝑠𝑠</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- ω_f（滤波角频率） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝜔</m:t></m:r></m:e><m:sub><m:r><m:t>𝑓</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- A（10 Hz 残余） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝐴</m:t></m:r></m:oMath>
<!-- T=T_gross(1+δ) -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑇</m:t></m:r><m:r><m:t>=</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑔𝑟𝑜𝑠𝑠</m:t></m:r></m:sub></m:sSub><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>1</m:t></m:r><m:r><m:t>+</m:t></m:r><m:r><m:t>𝛿</m:t></m:r></m:e></m:d></m:oMath>
```

---

## 第 2 页｜相位对齐条件（核心公式）

**PPT 画面文字**

- 内模传递函数：V/W = 1/(1+τs−Qe^(−sT))。
- 在 s=jω 处分母的模平方，用三角配方写成 cos(θ+φ) 形式，θ=ωT、φ=arctan(ωτ)。
- |D| 的唯一极小点：ωT = 2πk − arctan(ωτ)。
- 最优周期修正：δ* = −arctan(ωτ)/(2π)。600 rpm/10 Hz、τ=20 ms 代入约 −14.3%；实测谷 −12%~−12.6%（电流环/测速滤波附加相位）。

**讲解词（口播）**

把低通重复通道写成 V/W = 1/(1+τs−Qe^(−sT))。在 s=jω 处分母的模平方是一个常数减 2Q 乘一个三角组合。

把 cosθ−ωτ sinθ 配成 √(1+(ωτ)²)cos(θ+φ)，极小点就在 θ+φ=2πk，即 ωT=2πk−arctan(ωτ)。

所以 δ*=−arctan(ωτ)/(2π)。600 rpm、10 Hz、τ=20 ms 代入是 −14.3%；实测谷在 −12%~−12.6%，差值来自电流环和测速滤波的附加相位。


**MathType 展示公式**

**内模传递函数**

```mathtype
\frac{V(s)}{W(s)}=\frac{1}{1+\tau s-Q\,e^{-sT}}
```

**分母在 jω 的模平方**

```mathtype
\left|D(j\omega)\right|^2=1+(\omega\tau)^2+Q^2-2Q\left[\cos\theta-\omega\tau\sin\theta\right],\quad \theta=\omega T
```

**三角配方**

```mathtype
\cos\theta-\omega\tau\sin\theta=\sqrt{1+(\omega\tau)^2}\,\cos\left(\theta+\varphi\right),\quad \varphi=\arctan(\omega\tau)
```

**相位对齐条件**

```mathtype
\omega T=2\pi k-\arctan(\omega\tau)
```

**最优周期修正**

```mathtype
\delta^{*}(\omega)=-\frac{\arctan(\omega\tau)}{2\pi}
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- ω（角频率） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜔</m:t></m:r></m:oMath>
<!-- τ（低通时间常数） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜏</m:t></m:r></m:oMath>
<!-- Q（遗忘因子） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑄</m:t></m:r></m:oMath>
<!-- θ（角变量） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜃</m:t></m:r></m:oMath>
<!-- φ（相位角） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜑</m:t></m:r></m:oMath>
<!-- δ*（最优修正） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSup><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup></m:oMath>
<!-- k（整数周期） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑘</m:t></m:r></m:oMath>
<!-- θ=ωT -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜃</m:t></m:r><m:r><m:t>=</m:t></m:r><m:r><m:t>𝜔</m:t></m:r><m:r><m:t>𝑇</m:t></m:r></m:oMath>
<!-- φ=arctan(ωτ) -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜑</m:t></m:r><m:r><m:t>=</m:t></m:r><m:func><m:fName><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>arctan</m:t></m:r></m:fName><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>𝜔</m:t></m:r><m:r><m:t>𝜏</m:t></m:r></m:e></m:d></m:e></m:func></m:oMath>
<!-- ωT=2πk−arctan(ωτ) -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜔</m:t></m:r><m:r><m:t>𝑇</m:t></m:r><m:r><m:t>=</m:t></m:r><m:r><m:t>2</m:t></m:r><m:r><m:t>𝜋</m:t></m:r><m:r><m:t>𝑘</m:t></m:r><m:r><m:t>−</m:t></m:r><m:func><m:fName><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>arctan</m:t></m:r></m:fName><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>𝜔</m:t></m:r><m:r><m:t>𝜏</m:t></m:r></m:e></m:d></m:e></m:func></m:oMath>
<!-- δ*=−arctan(ωτ)/(2π) -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSup><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup><m:r><m:t>=</m:t></m:r><m:r><m:t>−</m:t></m:r><m:f><m:num><m:func><m:fName><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>arctan</m:t></m:r></m:fName><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>𝜔</m:t></m:r><m:r><m:t>𝜏</m:t></m:r></m:e></m:d></m:e></m:func></m:num><m:den><m:r><m:t>2</m:t></m:r><m:r><m:t>𝜋</m:t></m:r></m:den></m:f></m:oMath>
```

---

## 第 3 页｜目标函数与搜索抖动

**PPT 画面文字**

- A(δ) 在 δ* 附近是碗形：A ≈ A*[1+κ(δ−δ*)²]。
- 在 δ 上叠加慢正弦：δ(t)=δ̂+Δsin(ω_d t)。
- ESC 不需要对象模型：只利用 A 对抖动的同相响应判断斜率方向。

**讲解词（口播）**

目标函数 A(δ) 在 δ* 附近是一个碗：A≈A*[1+κ(δ−δ*)²]。我们不知道 κ 和 δ* 的精确值，但可以用极值搜索。

在 δ 上叠加一个慢正弦 δ=δ̂+Δsin(ω_d t)，观察 A 的响应。A 对 δ 的斜率符号会体现在与抖动同相的解调量里；ESC 只利用这个符号，不需要对象模型。


**MathType 展示公式**

**碗形近似**

```mathtype
A(\delta)\approx A^{*}\left[1+\kappa\left(\delta-\delta^{*}\right)^2\right]
```

**搜索抖动**

```mathtype
\delta(t)=\hat{\delta}+\Delta\sin(\omega_d t)
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- A（目标函数） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝐴</m:t></m:r></m:oMath>
<!-- A*（谷底） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSup><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup></m:oMath>
<!-- κ（曲率） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜅</m:t></m:r></m:oMath>
<!-- δ（周期修正） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝛿</m:t></m:r></m:oMath>
<!-- δ̂（当前中心） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝛿</m:t></m:r></m:e></m:acc></m:oMath>
<!-- δ*（最优点） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSup><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup></m:oMath>
<!-- Δ（抖动幅值） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝛥</m:t></m:r></m:oMath>
<!-- ω_d（抖动频率） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝜔</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- A≈A*[1+κ(δ−δ*)²] -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝐴</m:t></m:r><m:r><m:t>≈</m:t></m:r><m:sSup><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup><m:d><m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr><m:e><m:r><m:t>1</m:t></m:r><m:r><m:t>+</m:t></m:r><m:r><m:t>𝜅</m:t></m:r><m:sSup><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>𝛿</m:t></m:r><m:r><m:t>−</m:t></m:r><m:sSup><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup></m:e></m:d></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:e></m:d></m:oMath>
<!-- δ(t)=δ̂+Δsin(ω_d t) -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝛿</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>𝑡</m:t></m:r></m:e></m:d><m:r><m:t>=</m:t></m:r><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝛿</m:t></m:r></m:e></m:acc><m:r><m:t>+</m:t></m:r><m:r><m:t>𝛥</m:t></m:r><m:func><m:fName><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>sin</m:t></m:r></m:fName><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:sSub><m:e><m:r><m:t>𝜔</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub><m:r><m:t>𝑡</m:t></m:r></m:e></m:d></m:e></m:func></m:oMath>
```

---

## 第 4 页｜基波幅值观测器与锁相解调

**PPT 画面文字**

- 带通取 10 Hz 基波，取一个周期均方根：A[k] = sqrt(mean(y_bp²))，N_T=T_gross/Δt_s。
- 锁相解调：I_k = (2/(N P_d))∫A(t)sin(ω_d t)dt，在 N 个抖动周期上积分。
- 线性化：I_k ≈ 2κA*(δ̂−δ*)Δ；符号给出 δ̂ 相对 δ* 的方向。
- 更新：δ̂_{k+1}=clip(δ̂_k−σsgn(I_k), ±δ_max)；可分辨条件 2κA*σ|δ̂−δ*|≥η_A。

**讲解词（口播）**

先把 10 Hz 基波取出来：用中心频率跟随转速的带通，取一个周期的均方根作为 A[k]。

锁相解调：把 A(t) 与 sin(ω_d t) 在一个整数抖动周期上积分，得到 I_k。线性化后 I_k≈2κA*(δ̂−δ*)Δ，所以 I_k 的符号就是 δ̂ 相对 δ* 的方向。

更新律是固定步长 σ 的符号下降，并限幅 ±δ_max。可分辨条件是单步调制量大于 A 的噪声 η_A。


**MathType 展示公式**

**基波幅值观测器**

```mathtype
A[k]=\sqrt{\frac{1}{N_T}\sum_{i=0}^{N_T-1}y_{\mathrm{bp}}^2[k-i]},\quad N_T=\frac{T_{\mathrm{gross}}}{\Delta t_s}
```

**锁相解调**

```mathtype
I_k=\frac{2}{N P_d}\int_{(k-1)NP_d}^{kNP_d}A(t)\sin(\omega_d t)\,\mathrm{d}t
```

**解调量线性化**

```mathtype
I_k\approx 2\kappa A^{*}\left(\hat{\delta}_k-\delta^{*}\right)\Delta
```

**极值搜索更新律**

```mathtype
\hat{\delta}_{k+1}=\mathrm{clip}\left(\hat{\delta}_k-\sigma\,\mathrm{sgn}(I_k),\,-\delta_{\max},\,\delta_{\max}\right)
```

**可分辨条件**

```mathtype
2\kappa A^{*}\sigma\left|\hat{\delta}-\delta^{*}\right|\ge\eta_A
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- A[k]（离散幅值） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝐴</m:t></m:r><m:r><m:t>[</m:t></m:r><m:r><m:t>𝑘</m:t></m:r><m:r><m:t>]</m:t></m:r></m:oMath>
<!-- N_T（周期点数） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑁</m:t></m:r></m:e><m:sub><m:r><m:t>𝑇</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- y_bp（带通输出） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑦</m:t></m:r></m:e><m:sub><m:r><m:t>𝑏𝑝</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- Δt_s（采样周期） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝛥</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑡</m:t></m:r></m:e><m:sub><m:r><m:t>𝑠</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- I_k（解调量） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐼</m:t></m:r></m:e><m:sub><m:r><m:t>𝑘</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- N（抖动周期数） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑁</m:t></m:r></m:oMath>
<!-- P_d（抖动周期） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑃</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- σ（步长） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜎</m:t></m:r></m:oMath>
<!-- δ_max（限幅） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sub><m:r><m:t>𝑚𝑎𝑥</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- η_A（A 噪声） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝜂</m:t></m:r></m:e><m:sub><m:r><m:t>𝐴</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- I_k≈2κA*(δ̂−δ*)Δ -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐼</m:t></m:r></m:e><m:sub><m:r><m:t>𝑘</m:t></m:r></m:sub></m:sSub><m:r><m:t>≈</m:t></m:r><m:r><m:t>2</m:t></m:r><m:r><m:t>𝜅</m:t></m:r><m:sSup><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝛿</m:t></m:r></m:e></m:acc><m:r><m:t>−</m:t></m:r><m:sSup><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup></m:e></m:d><m:r><m:t>𝛥</m:t></m:r></m:oMath>
<!-- δ̂_{k+1}=clip(δ̂_k−σsgn(I_k),±δ_max) -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝛿</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:t>𝑘+1</m:t></m:r></m:sub></m:sSub><m:r><m:t>=</m:t></m:r><m:func><m:fName><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>clip</m:t></m:r></m:fName><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:sSub><m:e><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝛿</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:t>𝑘</m:t></m:r></m:sub></m:sSub><m:r><m:t>−</m:t></m:r><m:r><m:t>𝜎</m:t></m:r><m:func><m:fName><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>sgn</m:t></m:r></m:fName><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:sSub><m:e><m:r><m:t>𝐼</m:t></m:r></m:e><m:sub><m:r><m:t>𝑘</m:t></m:r></m:sub></m:sSub></m:e></m:d></m:e></m:func><m:r><m:t>,</m:t></m:r><m:r><m:t>±</m:t></m:r><m:sSub><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sub><m:r><m:t>𝑚𝑎𝑥</m:t></m:r></m:sub></m:sSub></m:e></m:d></m:e></m:func></m:oMath>
<!-- 2κA*σ|δ̂−δ*|≥η_A -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>2</m:t></m:r><m:r><m:t>𝜅</m:t></m:r><m:sSup><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup><m:r><m:t>𝜎</m:t></m:r><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝛿</m:t></m:r></m:e></m:acc><m:r><m:t>−</m:t></m:r><m:sSup><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup></m:e></m:d><m:r><m:t>≥</m:t></m:r><m:sSub><m:e><m:r><m:t>𝜂</m:t></m:r></m:e><m:sub><m:r><m:t>𝐴</m:t></m:r></m:sub></m:sSub></m:oMath>
```

---

## 第 5 页｜离散实现：分数延迟、冻结与前馈

**PPT 画面文字**

- T 不是采样周期整数倍：分数延迟线性插值。
- 换速时 T_gross 突变：冻结搜索；判据 |ΔT_gross/T_gross|>5% 或 |1−y|>0.1。
- 稳定后用理论值前馈重置：δ_ff=−arctan(ω_fτ)/(2π)。
- 终版：Δ=0.5%、σ=1%、P_d=1.5 s、N=3、δ0=−14.3%、δ_max=20%。

**讲解词（口播）**

离散实现有两件事要小心：一是 T 不是采样周期的整数倍，延迟线要做分数延迟插值；二是换速时 T_gross 突变，搜索要冻结，等转速稳定后用理论值前馈重置 δ̂。

冻结判据是 T_gross 相对变化 >5% 或 |1−y|>0.1；前馈值就是 δ_ff=−arctan(ω_fτ)/(2π)。终版参数：Δ=0.5%、σ=1%、P_d=1.5 s、N=3、δ0=−14.3%、δ_max=20%。


**MathType 展示公式**

**分数延迟插值**

```mathtype
v[k-n_d]\approx(1-\lambda)\,v[k-i_0]+\lambda\,v[k-i_0-1],\quad n_d=\frac{T}{\Delta t_s},\ i_0=\lfloor n_d\rfloor,\ \lambda=n_d-i_0
```

**换速冻结判据**

```mathtype
\left|\frac{T_{\mathrm{gross}}[k]-T_{\mathrm{gross}}[k-1]}{T_{\mathrm{gross}}[k-1]}\right|>0.05\quad\mathrm{or}\quad\left|1-y\right|>0.1
```

**前馈重置**

```mathtype
\hat{\delta}\leftarrow\mathrm{clip}\left(-\frac{\arctan(\omega_f\tau)}{2\pi},\,-\delta_{\max},\,\delta_{\max}\right)
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- n_d（延迟拍数） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑛</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- i_0（整数部分） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑖</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- λ（插值系数） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜆</m:t></m:r></m:oMath>
<!-- y（标幺转速） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑦</m:t></m:r></m:oMath>
<!-- δ_max（限幅） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sub><m:r><m:t>𝑚𝑎𝑥</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- n_d=T/Δt_s -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑛</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub><m:r><m:t>=</m:t></m:r><m:f><m:num><m:r><m:t>𝑇</m:t></m:r></m:num><m:den><m:r><m:t>𝛥</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑡</m:t></m:r></m:e><m:sub><m:r><m:t>𝑠</m:t></m:r></m:sub></m:sSub></m:den></m:f></m:oMath>
<!-- 冻结判据 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e><m:f><m:num><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑔𝑟𝑜𝑠𝑠</m:t></m:r></m:sub></m:sSub><m:r><m:t>[𝑘]</m:t></m:r><m:r><m:t>−</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑔𝑟𝑜𝑠𝑠</m:t></m:r></m:sub></m:sSub><m:r><m:t>[𝑘−1]</m:t></m:r></m:num><m:den><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑔𝑟𝑜𝑠𝑠</m:t></m:r></m:sub></m:sSub><m:r><m:t>[𝑘−1]</m:t></m:r></m:den></m:f></m:e></m:d><m:r><m:t>&gt;</m:t></m:r><m:r><m:t>0.05</m:t></m:r></m:oMath>
<!-- δ_ff=−arctan(ω_fτ)/(2π) -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sub><m:r><m:t>𝑓𝑓</m:t></m:r></m:sub></m:sSub><m:r><m:t>=</m:t></m:r><m:r><m:t>−</m:t></m:r><m:f><m:num><m:func><m:fName><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>arctan</m:t></m:r></m:fName><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:sSub><m:e><m:r><m:t>𝜔</m:t></m:r></m:e><m:sub><m:r><m:t>𝑓</m:t></m:r></m:sub></m:sSub><m:r><m:t>𝜏</m:t></m:r></m:e></m:d></m:e></m:func></m:num><m:den><m:r><m:t>2</m:t></m:r><m:r><m:t>𝜋</m:t></m:r></m:den></m:f></m:oMath>
```

---

## 第 6 页｜实测结果与边界（真实 J=2.545J_nom）

**PPT 画面文字**

- 600 rpm：不整定 RMS 13.43；固定 −12% 12.37；ESC 由 −14.3% 收敛到 −11.57%（12.41），由 −5% 收敛到 −10.27%（12.28）。
- 收益 −7.6%~−8.6%；抖动峰峰 3.0%→1.5%。
- 真实 J 下五种抖动配置 RMS 只在 12.37~12.58 内，Δ/σ 的 RMS 差异已不可分辨；终版是保守选择，不是显著最优。
- 边界：A 噪声底约 7.7×10⁻⁴，δ 分辨率约 ±2 个百分点；A 随 1/J 缩放但 3 rpm 传感器噪声不缩放；目前单种子。

**讲解词（口播）**

在真实 J=2.545J_nom 下，600 rpm 的 A 扫描最小值在 −15% 附近，但平台落在噪声底内；拟合碗中心 −12.6%，RMS 最小 −11%。

ESC 从 −14.3% 收敛到 −11.57%，从 −5% 收敛到 −10.27%；稳态 RMS 从不整定的 13.43 降到 12.28~12.41，收益 −7.6%~−8.6%。

抖动从 3.0% 压到 1.5%，但五种抖动配置的 RMS 只在 12.37~12.58 内，真实 J 下 Δ/σ 的 RMS 差异已不可分辨；终版 Δ=0.5%/σ=1% 是保守选择，不是显著最优。

边界：A 的噪声底约 7.7×10⁻⁴，δ 分辨率约 ±2 个百分点；A 随 1/J 缩放，但 3 rpm 传感器噪声不缩放，所以 RMS 收益会缩水；目前是单种子。


**MathType 展示公式**

**拟合碗形（实测）**

```mathtype
A(\delta)\approx A^{*}\left[1+\kappa\left(\delta-\delta^{*}\right)^2\right],\quad \delta^{*}\approx-12.6\%,\ \kappa\approx26
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- δ*（拟合最优点） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSup><m:e><m:r><m:t>𝛿</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup></m:oMath>
<!-- A*（拟合谷底） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSup><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sup><m:r><m:t>∗</m:t></m:r></m:sup></m:sSup></m:oMath>
<!-- κ（拟合曲率） -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜅</m:t></m:r></m:oMath>
```

---

## 口播顺序建议（约 6–8 分钟）

1. 第 1 页：30 s，讲“周期错 → 相位错 → 残余变大”，给出 T=T_gross(1+δ)。
2. 第 2 页：2 min，板书内模频响 → 三角配方 → 相位对齐 → δ*；代入 −14.3%，解释实测 −12%~−12.6%。
3. 第 3 页：1 min，讲碗形目标函数与 dither，强调 ESC 不用对象模型。
4. 第 4 页：2 min，讲 A[k] 观测器、锁相解调 I_k、更新律与可分辨条件。
5. 第 5 页：1 min，讲分数延迟、冻结、前馈与终版参数。
6. 第 6 页：1 min，给真实 J 的收敛/RMS 数字与边界，强调“平台内不可分辨、终版是保守选择”。

## 常见追问（备用）

- **为什么 δ* 不是 0？** 低通 τ 在 10 Hz 产生相位滞后，延迟线必须提前一个角度才能对齐；δ*=−arctan(ωτ)/(2π)。
- **为什么实测比理论浅？** 电流环、测速滤波、离散化又加了 2~3 个百分点相位；理论值只含 τ。
- **为什么用 sin 而不是 cos 解调？** 抖动是 sin；与抖动同相的分量才对应 A 对 δ 的斜率。
- **为什么换速要冻结？** T_gross 突变时 A 的“碗”在移动，继续搜索会把转速瞬态误当成 δ 失配；冻结后用理论值前馈定位，再解冻。
- **为什么真实 J 下 Δ/σ 看不出差别？** A 随 1/J 缩小，3 rpm 传感器噪声不缩小；A 的平台已接近噪声底，δ 分辨率约 ±2 个百分点。

## 附录：补充单字母 OMML

```xml
<!-- V -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑉</m:t></m:r></m:oMath>
<!-- W -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑊</m:t></m:r></m:oMath>
<!-- s -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑠</m:t></m:r></m:oMath>
<!-- j -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑗</m:t></m:r></m:oMath>
<!-- D -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝐷</m:t></m:r></m:oMath>
<!-- v -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑣</m:t></m:r></m:oMath>
<!-- t -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑡</m:t></m:r></m:oMath>
<!-- i -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑖</m:t></m:r></m:oMath>
<!-- π -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜋</m:t></m:r></m:oMath>
```
