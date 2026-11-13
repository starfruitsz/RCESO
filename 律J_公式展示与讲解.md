# 律 J（自适应 J：辨识 + b0 更新 + 状态 4 回退）公式展示与讲解

> **用途**：给 PPT「自适应 J」页做公式展示与口播稿；本文件只负责文字与公式，版面由你粘贴。
>
> **用法**
> 1. **mathtype** 代码块：复制块内单行 LaTeX，到 MathType（Preferences → Workspace Preferences → 勾选 Allow TeX language input）粘贴回车。
> 2. **xml** 代码块：每个“符号”注释行下的一行 m:oMath 元素是 OMML；复制该行到 PPT 文本框/Word，按你的 OMML 流程转成公式。单行字母与短公式都在这里。
> 3. 数值口径：v5.6；主要结果取 **5.26J_nom 应力测试**（J_true=9.95e-5）、600 rpm、T1=0.057 N·m、10 s、单种子 20261018；定稿台架 2.545J_nom 的差异见报告 C.7。
> 4. 正文里的 $...$ 仅为阅读；实际内联 OMML 在每节末的 xml 块中，按符号复制。
>
> **符号约定**：$J_{nom}$ 电机标称（只进 $b_0$）；$J_{true}$ 传动链真实值（进主循环）；$\hat J$ 辨识值；$b_0$ ESO 输入增益；$b$ 标幺对象增益；$\rho=\hat J/J_{nom}$；其余见正文。

---


## 第 1 页｜为什么需要律 J

**PPT 画面文字**

- 真实传动链惯量 $J_{true}$ 常大于电机标称 $J_{nom}$；$b_0$ 只按 $J_{nom}$ 整定，环路增益 $b k_p/b_0$ 随 $1/J_{true}$ 下降。
- 同一故障下 10 Hz 纹波被放大：固定 $b_0$ 为 33.3 rpm，$b_0$ 校正后为 4.0 rpm（应力测试）。
- 律 J：调试期辨识 $\hat J$，一次性更新 $b_0$，然后冻结；不改 $k_p$，避免双重补偿。
- 目标：把 ESO 输入增益 $b_0$ 调到 $1.2\,b(J_{true})$，恢复设计环路增益。

**讲解词（口播）**

先讲为什么需要律 J。速度环控制律里的 $b_0$ 是 ESO 的输入增益，按电机标称 $J_{nom}$ 整定；真实传动链的 $J_{true}$ 往往大得多，环路增益就按 $1/J_{true}$ 掉下来。

同一个 10 Hz 故障，固定 $b_0$ 时纹波 33.3 rpm，$b_0$ 校正后只有 4.0 rpm。律 J 的做法是：调试期辨识 $\hat J$，一次性把 $b_0$ 改到 $1.2\,b(J_{true})$，然后冻结；只改 $b_0$，不改 $k_p$，否则就是双重补偿。


**MathType 展示公式**

**环路增益**

```mathtype
b=\frac{k_t I_{\mathrm{base}}}{J_{\mathrm{true}}\,\omega_{\mathrm{ref}}},\quad b_0=1.2\,b\left(J_{\mathrm{nom}}\right)
```

**两套惯量的差**

```mathtype
\frac{1}{J_{\mathrm{true}}}-\frac{1}{J_{\mathrm{nom}}}
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- J_nom -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑛𝑜𝑚</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- J_true -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑡𝑟𝑢𝑒</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- b0 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑏</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- b -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑏</m:t></m:r></m:oMath>
<!-- b0=1.2 b(J_nom) -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑏</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub><m:r><m:t>=</m:t></m:r><m:r><m:t>1.2</m:t></m:r><m:r><m:t>𝑏</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑛𝑜𝑚</m:t></m:r></m:sub></m:sSub></m:e></m:d></m:oMath>
```

---

## 第 2 页｜传动链真实惯量

**PPT 画面文字**

- $J_{true}$ = 电机 + 联轴器 + 圆盘/齿轮箱折算 + 轴承折算。
- 均质圆盘 $J_{disc}=\frac12 M_d R_d^2$；薄壁轴承 $J_b\approx\frac12 m_b(r_i^2+r_o^2)$。
- 定稿台架：$J_{true}=4.81\times10^{-5}=2.545J_{nom}$；应力测试：$9.95\times10^{-5}=5.26J_{nom}$。
- 两套只换圆盘；$J_{nom}=1.89\times10^{-5}$ 只进 $b_0$，$J_{true}$ 进主循环机械方程。

**讲解词（口播）**

$J_{true}$ 不是电机转子惯量，而是整条传动链折算到电机轴：电机 + 联轴器 + 圆盘除以速比平方 + 轴承。

定稿台架是小圆盘，$4.81\times10^{-5}=2.545J_{nom}$；应力测试用大圆盘，$9.95\times10^{-5}=5.26J_{nom}$。两套只换圆盘。$J_{nom}$ 只用于 $b_0$，$J_{true}$ 只用于主循环机械方程。


**MathType 展示公式**

**传动链折算**

```mathtype
J_{\mathrm{true}}=J_{\mathrm{motor}}+J_{\mathrm{cpl}}+\frac{J_{\mathrm{disc}}}{n_g^2}+\frac{n_b J_b}{n_g^2}
```

**圆盘与轴承**

```mathtype
J_{\mathrm{disc}}=\frac{1}{2}M_dR_d^2,\quad J_b\approx\frac{1}{2}m_b\left(r_i^2+r_o^2\right)
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- J_motor -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑚𝑜𝑡𝑜𝑟</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- J_cpl -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑐𝑝𝑙</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- J_disc -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑𝑖𝑠𝑐</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- J_b -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑏</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- n_g -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑛</m:t></m:r></m:e><m:sub><m:r><m:t>𝑔</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- M_d -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑀</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- R_d -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑅</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- m_b -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑚</m:t></m:r></m:e><m:sub><m:r><m:t>𝑏</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- r_i -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑟</m:t></m:r></m:e><m:sub><m:r><m:t>𝑖</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- r_o -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑟</m:t></m:r></m:e><m:sub><m:r><m:t>𝑜</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- J_true 折算 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑡𝑟𝑢𝑒</m:t></m:r></m:sub></m:sSub><m:r><m:t>=</m:t></m:r><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑚𝑜𝑡𝑜𝑟</m:t></m:r></m:sub></m:sSub><m:r><m:t>+</m:t></m:r><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑐𝑝𝑙</m:t></m:r></m:sub></m:sSub><m:r><m:t>+</m:t></m:r><m:f><m:num><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑𝑖𝑠𝑐</m:t></m:r></m:sub></m:sSub></m:num><m:den><m:sSup><m:e><m:sSub><m:e><m:r><m:t>𝑛</m:t></m:r></m:e><m:sub><m:r><m:t>𝑔</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:den></m:f><m:r><m:t>+</m:t></m:r><m:f><m:num><m:sSub><m:e><m:r><m:t>𝑛</m:t></m:r></m:e><m:sub><m:r><m:t>𝑏</m:t></m:r></m:sub></m:sSub><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑏</m:t></m:r></m:sub></m:sSub></m:num><m:den><m:sSup><m:e><m:sSub><m:e><m:r><m:t>𝑛</m:t></m:r></m:e><m:sub><m:r><m:t>𝑔</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:den></m:f></m:oMath>
<!-- J_disc -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑𝑖𝑠𝑐</m:t></m:r></m:sub></m:sSub><m:r><m:t>=</m:t></m:r><m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>2</m:t></m:r></m:den></m:f><m:sSub><m:e><m:r><m:t>𝑀</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub><m:sSup><m:e><m:sSub><m:e><m:r><m:t>𝑅</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:oMath>
```

---

## 第 3 页｜控制律与 b0 更新

**PPT 画面文字**

- 控制律 $u=\frac{1}{b_0}[k_p^{eff}(r-z_1)-z_2-v]$；环路增益正比于 $b/b_0$。
- 把 $b_0$ 调到 $1.2\,b(J_{true})$ 即恢复设计增益；$b_0$ 同时是 ESO 的输入增益。
- 更新式 $b_0\leftarrow b_0 J_{nom}/\hat J$，$k_p$ 不变，$\hat J\in[0.5,50]J_{nom}$。
- 为什么不同时放大 $k_p$：双重补偿实测 $i_q$ 冲到 19–45 A，已弃用。

**讲解词（口播）**

控制律是 $u=(1/b_0)[k_p^{eff}(r-z_1)-z_2-v]$，环路增益正比于 $b/b_0$。把 $b_0$ 调到真实 $b$ 的 1.2 倍，就恢复设计增益。

更新式是 $b_0\leftarrow b_0 J_{nom}/\hat J$，只改 $b_0$，$k_p$ 不变。为什么不同时放大 $k_p$？那是双重补偿，实测 $i_q$ 会冲到 19–45 A，所以弃用。


**MathType 展示公式**

**控制律**

```mathtype
u=\frac{1}{b_0}\left[k_p^{\mathrm{eff}}\left(r-z_1\right)-z_2-v\right],\quad k_p^{\mathrm{eff}}=k_p\left(1+k_{p,\mathrm{boost}}g\right)
```

**b0 更新**

```mathtype
b_0\leftarrow b_0\frac{J_{\mathrm{nom}}}{\hat J},\quad \hat J\in\left[0.5,50\right]J_{\mathrm{nom}}
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- u -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑢</m:t></m:r></m:oMath>
<!-- k_p -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑘</m:t></m:r></m:e><m:sub><m:r><m:t>𝑝</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- k_p_eff -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑘</m:t></m:r></m:e><m:sub><m:r><m:t>𝑝</m:t></m:r></m:sub></m:sSub><m:r><m:t>𝑒𝑓𝑓</m:t></m:r></m:oMath>
<!-- z_1 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑧</m:t></m:r></m:e><m:sub><m:r><m:t>1</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- z_2 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑧</m:t></m:r></m:e><m:sub><m:r><m:t>2</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- v -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑣</m:t></m:r></m:oMath>
<!-- g -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑔</m:t></m:r></m:oMath>
<!-- b0 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑏</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- b -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑏</m:t></m:r></m:oMath>
<!-- k_t -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑘</m:t></m:r></m:e><m:sub><m:r><m:t>𝑡</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- I_base -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐼</m:t></m:r></m:e><m:sub><m:r><m:t>𝑏𝑎𝑠𝑒</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- ω_ref -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝜔</m:t></m:r></m:e><m:sub><m:r><m:t>𝑟𝑒𝑓</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- u 控制律 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑢</m:t></m:r><m:r><m:t>=</m:t></m:r><m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:sSub><m:e><m:r><m:t>𝑏</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub></m:den></m:f><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:sSub><m:e><m:r><m:t>𝑘</m:t></m:r></m:e><m:sub><m:r><m:t>𝑝</m:t></m:r></m:sub></m:sSub><m:r><m:t>𝑒𝑓𝑓</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>𝑟</m:t></m:r><m:r><m:t>−</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑧</m:t></m:r></m:e><m:sub><m:r><m:t>1</m:t></m:r></m:sub></m:sSub></m:e></m:d><m:r><m:t>−</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑧</m:t></m:r></m:e><m:sub><m:r><m:t>2</m:t></m:r></m:sub></m:sSub><m:r><m:t>−</m:t></m:r><m:r><m:t>𝑣</m:t></m:r></m:e></m:d></m:oMath>
<!-- b0 更新 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑏</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub><m:r><m:t>←</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑏</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub><m:f><m:num><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑛𝑜𝑚</m:t></m:r></m:sub></m:sSub></m:num><m:den><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝐽</m:t></m:r></m:e></m:acc></m:den></m:f></m:oMath>
```

---

## 第 4 页｜调试期 dither 与频域比值辨识

**PPT 画面文字**

- 在电流指令上叠加 100 Hz 小转矩 dither：$T_d=A\sin(2\pi f_d t)$，$A=0.1$ N·m，$f_d=100$ Hz。
- 归一化幅值 $a_d=0.157$；取 0.2 s 窗（20 个 dither 周期、2 个 10 Hz 周期）。
- 对 $T_e$ 与 $\omega$ 做单频正交解调，比值给出 $\hat J=|T_{e,f_d}|/(2\pi f_d|\omega_{f_d}|)$。
- 闭环保真：$\omega=T_e/(J_{true}s)$；控制器反作用已含在实测 $T_e$ 中。

**讲解词（口播）**

调试期在电流指令上叠加 100 Hz 小转矩 dither，幅值 0.1 N·m，归一化后 $a_d=0.157$。取 0.2 s 窗，正好是 20 个 dither 周期、2 个 10 Hz 周期。

对 $T_e$ 和 $\omega$ 做单频正交解调，比值就是惯量：$\hat J=|T_{e,f_d}|/(2\pi f_d|\omega_{f_d}|)$。闭环下这个式子仍然成立，因为负载在 100 Hz 没有分量，控制器的反作用已经包含在实测 $T_e$ 里。


**MathType 展示公式**

**dither 注入**

```mathtype
T_d\left(t\right)=A\sin\left(2\pi f_dt\right),\quad A=0.1\ \mathrm{N\cdot m},\ f_d=100\ \mathrm{Hz}
```

**归一化幅值**

```mathtype
u\leftarrow u+a_d\sin\left(2\pi f_dt\right),\quad a_d=\frac{A}{k_tI_{\mathrm{base}}}\approx0.157
```

**DFT 解调**

```mathtype
T_{e,f_d}=\frac{2}{N}\sum_{k=0}^{N-1}T_e\left(t_k\right)e^{-j\omega_dt_k},\quad \omega_{f_d}=\frac{2}{N}\sum_{k=0}^{N-1}\omega\left(t_k\right)e^{-j\omega_dt_k}
```

**惯量估计**

```mathtype
\hat J=\frac{\left|T_{e,f_d}\right|}{\omega_d\left|\omega_{f_d}\right|},\quad \omega_d=2\pi f_d
```

**闭环保真**

```mathtype
\left|\omega_{f_d}\right|=\frac{\left|T_{e,f_d}\right|}{J_{\mathrm{true}}\omega_d}\quad\Longrightarrow\quad\hat J=J_{\mathrm{true}}
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- T_d -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- A -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝐴</m:t></m:r></m:oMath>
<!-- f_d -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑓</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- a_d -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑎</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- T_e -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑒</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- ω -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜔</m:t></m:r></m:oMath>
<!-- ω_d -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝜔</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- N -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝑁</m:t></m:r></m:oMath>
<!-- T_w -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑤</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- Jhat -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝐽</m:t></m:r></m:e></m:acc></m:oMath>
<!-- T_d 注入 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>𝑡</m:t></m:r></m:e></m:d><m:r><m:t>=</m:t></m:r><m:r><m:t>𝐴</m:t></m:r><m:func><m:fName><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>sin</m:t></m:r></m:fName><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>2</m:t></m:r><m:r><m:t>𝜋</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑓</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub><m:r><m:t>𝑡</m:t></m:r></m:e></m:d></m:e></m:func></m:oMath>
<!-- Jhat 估计 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝐽</m:t></m:r></m:e></m:acc><m:r><m:t>=</m:t></m:r><m:f><m:num><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e><m:sSub><m:e><m:r><m:t>𝑇</m:t></m:r></m:e><m:sub><m:r><m:t>𝑒,𝑓_𝑑</m:t></m:r></m:sub></m:sSub></m:e></m:d></m:num><m:den><m:sSub><m:e><m:r><m:t>𝜔</m:t></m:r></m:e><m:sub><m:r><m:t>𝑑</m:t></m:r></m:sub></m:sSub><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e><m:sSub><m:e><m:r><m:t>𝜔</m:t></m:r></m:e><m:sub><m:r><m:t>𝑓_𝑑</m:t></m:r></m:sub></m:sSub></m:e></m:d></m:den></m:f></m:oMath>
```

---

## 第 5 页｜上电状态机 0–5 与应用后校验/回退

**PPT 画面文字**

- 状态 0 空闲 → 1 辨识（$t_0=0.5$–$1.0$ s 起，最长 3 s）→ 2 已应用 / 3 超时回退 / 4 校验回退 / 5 死区。
- 有效窗：dither 转速幅值 $\ge2$ rpm、窗数 $\ge3$–$5$、窗间标准差 $\le15\%\bar{\hat J}$、$\hat J\in[0.5,50]J_{nom}$。
- 死区：$\rho=\hat J/J_{nom}$，$|\rho-1|\le0.20$ → 状态 5，不更新、不校验。
- 应用后校验：dither 关、标称 $b_0$ 采基线；应用后 0.5 s 取后窗；$i_q$ AC-RMS 或 10 Hz 恶化 $>20\%$ → 回退（状态 4）。

**讲解词（口播）**

把辨识做成上电流程：状态 0 空闲，1 辨识，然后分岔到 2 已应用、3 超时回退、4 校验回退、5 死区。

辨识段的有效窗要求：dither 转速幅值 ≥2 rpm、窗数 3–5、窗间标准差 ≤15%、$\hat J$ 限幅 0.5–50 $J_{nom}$。如果 $|\rho-1|\le0.20$，进死区，不更新。

应用后做一次 0.5 s 校验：先用“dither 关、标称 $b_0$”采基线，更新后取后窗，比较 $i_q$ 的 AC-RMS 和 10 Hz 幅值；任一恶化 >20% 就回退到标称 $b_0$，状态 4。


**MathType 展示公式**

**死区**

```mathtype
\rho=\frac{\hat J}{J_{\mathrm{nom}}},\quad\left|\rho-1\right|\le0.20
```

**iq AC-RMS**

```mathtype
i_{q,\mathrm{AC}}=\sqrt{\frac{1}{N}\sum_{k=1}^{N}i_{q,k}^2-\left(\frac{1}{N}\sum_{k=1}^{N}i_{q,k}\right)^2}
```

**10 Hz 幅值**

```mathtype
A_{10}=\frac{2}{N}\left|\sum_{k=1}^{N}e_ke^{-j2\pi10t_k}\right|,\quad e_k=n\left(t_k\right)-n_{\mathrm{ref}}
```

**回退判据**

```mathtype
\frac{i_{q,\mathrm{AC}}^{\mathrm{post}}}{i_{q,\mathrm{AC}}^{\mathrm{base}}}>1.20\quad\mathrm{or}\quad\left(A_{10}^{\mathrm{base}}\ge2\ \mathrm{rpm}\ \mathrm{and}\ \frac{A_{10}^{\mathrm{post}}}{A_{10}^{\mathrm{base}}}>1.20\right)
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- ρ -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜌</m:t></m:r></m:oMath>
<!-- Jhat -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝐽</m:t></m:r></m:e></m:acc></m:oMath>
<!-- J_nom -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑛𝑜𝑚</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- iq -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑖</m:t></m:r></m:e><m:sub><m:r><m:t>𝑞</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- iq_AC -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑖</m:t></m:r></m:e><m:sub><m:r><m:t>𝑞</m:t></m:r></m:sub></m:sSub><m:r><m:t>𝐴𝐶</m:t></m:r></m:oMath>
<!-- A10 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sub><m:r><m:t>10</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- ρ=Jhat/J_nom -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜌</m:t></m:r><m:r><m:t>=</m:t></m:r><m:f><m:num><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝐽</m:t></m:r></m:e></m:acc></m:num><m:den><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑛𝑜𝑚</m:t></m:r></m:sub></m:sSub></m:den></m:f></m:oMath>
<!-- 死区 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e><m:r><m:t>𝜌</m:t></m:r><m:r><m:t>−</m:t></m:r><m:r><m:t>1</m:t></m:r></m:e></m:d><m:r><m:t>≤</m:t></m:r><m:r><m:t>0.20</m:t></m:r></m:oMath>
<!-- iq AC-RMS -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑖</m:t></m:r></m:e><m:sub><m:r><m:t>𝑞</m:t></m:r></m:sub></m:sSub><m:r><m:t>𝐴𝐶</m:t></m:r><m:r><m:t>=</m:t></m:r><m:r><m:t>√</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>𝑁</m:t></m:r></m:den></m:f><m:r><m:t>𝛴</m:t></m:r><m:sSup><m:e><m:sSub><m:e><m:r><m:t>𝑖</m:t></m:r></m:e><m:sub><m:r><m:t>𝑞</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup><m:r><m:t>−</m:t></m:r><m:sSup><m:e><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>𝑁</m:t></m:r></m:den></m:f><m:r><m:t>𝛴</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑖</m:t></m:r></m:e><m:sub><m:r><m:t>𝑞</m:t></m:r></m:sub></m:sSub></m:e></m:d></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:e></m:d></m:oMath>
<!-- 10 Hz 幅值 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sub><m:r><m:t>10</m:t></m:r></m:sub></m:sSub><m:r><m:t>=</m:t></m:r><m:f><m:num><m:r><m:t>2</m:t></m:r></m:num><m:den><m:r><m:t>𝑁</m:t></m:r></m:den></m:f><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e><m:r><m:t>𝛴</m:t></m:r><m:sSub><m:e><m:r><m:t>𝑒</m:t></m:r></m:e><m:sub><m:r><m:t>𝑘</m:t></m:r></m:sub></m:sSub><m:sSup><m:e><m:r><m:t>𝑒</m:t></m:r></m:e><m:sup><m:r><m:t>−𝑗2𝜋10𝑡_𝑘</m:t></m:r></m:sup></m:sSup></m:e></m:d></m:oMath>
<!-- 回退判据 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:f><m:num><m:sSup><m:e><m:sSub><m:e><m:r><m:t>𝑖</m:t></m:r></m:e><m:sub><m:r><m:t>𝑞</m:t></m:r></m:sub></m:sSub><m:r><m:t>𝐴𝐶</m:t></m:r></m:e><m:sup><m:r><m:t>𝑝𝑜𝑠𝑡</m:t></m:r></m:sup></m:sSup></m:num><m:den><m:sSup><m:e><m:sSub><m:e><m:r><m:t>𝑖</m:t></m:r></m:e><m:sub><m:r><m:t>𝑞</m:t></m:r></m:sub></m:sSub><m:r><m:t>𝐴𝐶</m:t></m:r></m:e><m:sup><m:r><m:t>𝑏𝑎𝑠𝑒</m:t></m:r></m:sup></m:sSup></m:den></m:f><m:r><m:t>&gt;</m:t></m:r><m:r><m:t>1.20</m:t></m:r><m:r><m:t> 𝑜𝑟 </m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:sSup><m:e><m:sSub><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sub><m:r><m:t>10</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>𝑏𝑎𝑠𝑒</m:t></m:r></m:sup></m:sSup><m:r><m:t>≥</m:t></m:r><m:r><m:t>2 𝑟𝑝𝑚</m:t></m:r><m:r><m:t> 𝑎𝑛𝑑 </m:t></m:r><m:f><m:num><m:sSup><m:e><m:sSub><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sub><m:r><m:t>10</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>𝑝𝑜𝑠𝑡</m:t></m:r></m:sup></m:sSup></m:num><m:den><m:sSup><m:e><m:sSub><m:e><m:r><m:t>𝐴</m:t></m:r></m:e><m:sub><m:r><m:t>10</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>𝑏𝑎𝑠𝑒</m:t></m:r></m:sup></m:sSup></m:den></m:f><m:r><m:t>&gt;</m:t></m:r><m:r><m:t>1.20</m:t></m:r></m:e></m:d></m:oMath>
```

---

## 第 6 页｜实测结果与边界（应力测试 J_true=5.26J_nom）

**PPT 画面文字**

- $\hat J$ 终值 +9.1%（报告 C.4 表为 +9.5%，另一组调试参数/舍入；本图数据 +9.1%）。
- $b_0$ 更新为 $0.174b_0$；10 Hz 残差 33.3 → 4.0 rpm（−88%）。
- dither 代价只在辨识期：100 Hz 转速分量 18.15 → 0.16 rpm。
- 状态 4：无校验 $i_q$ 峰值 6.40/12.32 A → 回退 3.97/4.88 A；代价是回到标称 $b_0$ 的稳态误差。
- 边界：编码器量化约 6 rpm；无故障时 $\hat J$ 偏高约 15%；$J_{true}/J_{nom}>5$ 需复核 $k_p,\omega_o$；连续在线自适应会发散。

**讲解词（口播）**

在 5.26$J_{nom}$ 应力测试下，$\hat J$ 终值 +9.1%，$b_0$ 更新到 0.174$b_0$；10 Hz 残差从 33.3 降到 4.0 rpm，降了 88%。

dither 代价只在辨识期：100 Hz 转速分量 18.15 rpm，运行段只有 0.16 rpm。

状态 4 把无校验时的 $i_q$ 峰值 6.40/12.32 A 压到 3.97/4.88 A；代价是回到标称 $b_0$ 的稳态误差。

边界：编码器约 6 rpm 量化；无故障时 $\hat J$ 偏高约 15%；$J_{true}/J_{nom}>5$ 时除 $b_0$ 外还要复核 $k_p,\omega_o$；连续在线自适应会发散，所以只在调试期辨识一次。


**MathType 展示公式**

**b0 更新比例**

```mathtype
\frac{b_0^{\mathrm{e}}}{b_0}=\frac{J_{\mathrm{nom}}}{\hat J}=0.174
```

**估计偏差**

```mathtype
\hat J\approx1.091\,J_{\mathrm{true}}
```

**本节 OMML（内联符号/短式，复制对应行）**

```xml
<!-- Jhat -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:acc><m:accPr><m:chr m:val="̂"/></m:accPr><m:e><m:r><m:t>𝐽</m:t></m:r></m:e></m:acc></m:oMath>
<!-- b0 -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝑏</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub></m:oMath>
<!-- ρ -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>𝜌</m:t></m:r></m:oMath>
<!-- J_nom -->
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>𝐽</m:t></m:r></m:e><m:sub><m:r><m:t>𝑛𝑜𝑚</m:t></m:r></m:sub></m:sSub></m:oMath>
```

---

## 附：定稿参数

| 参数 | 取值 | 说明 |
|---|---|---|
| dither 频率 / 转矩 | 100 Hz / 0.1 N·m | 归一化幅值 0.157 |
| 辨识窗 / 点数 | 0.2 s / N=200 | 20 个 100 Hz 周期、2 个 10 Hz 周期 |
| 辨识起始 / 截止 | 0.5–1.0 s / 3.0 s | 上电调试期 |
| 有效窗数 / 标准差 | 3–5 / 0.15 | 提前决策 |
| SNR 门限 | ≥2 rpm | 编码器量化约 6 rpm |
| 限幅 | [0.5, 50] J_nom | 防异常值 |
| 死区 | 0.20 | abs(ρ−1)≤0.20，状态 5 |
| 校验静置 / 基线窗 | 0.2 s / 0.5 s | dither 关、标称 b0 |
| 应用后等待 / 后窗 | 0.5 s / 0.5 s | 更新后 |
| 恶化门限 | 0.20 | iq AC-RMS 或 10 Hz |
| 10 Hz 基线门限 | 2.0 rpm | 低于此值只用 iq 判据 |
| 额定电流 | 6.31 A（1 ms 包络） | 10 µs 原始峰值含 PWM 纹波 |

## 口播顺序建议（约 6–8 分钟）

1. 第 1 页：30 s，讲 $J_{true}>J_{nom}$ → $b_0$ 失配 → 10 Hz 纹波变大。
2. 第 2 页：1 min，讲传动链折算与两套台架。
3. 第 3 页：1.5 min，讲控制律、环路增益、只改 $b_0$ 的理由与限幅。
4. 第 4 页：2 min，讲 100 Hz dither、DFT 比值、闭环保真。
5. 第 5 页：1.5 min，讲状态机 0–5、死区、应用后 0.5 s 校验/回退。
6. 第 6 页：1 min，给 +9.1%、33.3→4.0、18.15→0.16、状态 4 的 6.40→3.97/12.32→4.88，以及边界。

## 常见追问（备用）

- **为什么不直接改 $k_p$？** 环路增益是 $b k_p/b_0$，同时改 $b_0$ 和 $k_p$ 会双重补偿；实测 $i_q$ 冲到 19–45 A。
- **为什么只在上电时辨识？** 编码器量化约 6 rpm，连续在线辨识会让 $\hat J$ 抖动、增益抖动，实测 $i_q$ 发散。
- **为什么无故障时会回退？** 无故障基线 $i_q$ 纹波很小；把 $b_0$ 改小、环路增益抬高后纹波反而变大，校验判据把它拦下。
- **$J_{true}/J_{nom}>5$ 怎么办？** 除 $b_0$ 外还要复核 $k_p,\omega_o$；本文 5.26 倍是应力测试上限。
