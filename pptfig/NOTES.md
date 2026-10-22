# pptfig/NOTES —— 每张图的一句话讲稿

> 口径：600 rpm、实验室档（3 rpm / 0.1 A / 0.01 N·m）、fci = 500 Hz、类 fal ESO（a=0.75, δ=0.10, λ=10）。
> 所有数字可由根目录脚本复算，见每行"复现"。

## ppt_01_eso_fal_fault.png —— 纯 ESO + 类 fal 应对角度锁相周期负载

- **一句话**：只有 ESO、没有重复通道时，±0.1 N·m 的角度锁相周期负载会把转速打出 **74 rpm RMS（12.4% 额定）**的脉动，ESO 顶不住——这正是需要重复通道（RCESO）的理由。
- **图怎么读**：0–2 s 空载；2 s 故障投入（0.50 额定台阶 + `T(φ)=A[sinφ+0.4sin3φ+0.2sin5φ]`，`T(φ)=T(φ+2π)`，`dφ/dt=ω`，A=0.1 N·m）；第三行看 `i_q*` 与 `i_q` 的跟随（实测电流含采样噪声）。
- **参数**：β₃ = 0（重复通道关）、无律 D、无 F-B；ESO 增益类 fal。
- **复现**：`python run_ppt_fig1.py` → `python plot_ppt_fig1.py`
- **数据**：`_ppt_fig1.npz`、`_ppt_fig1.json`（steady_rms 74.13、iq_std 0.899、iq_max 5.28、Max|iq*| 4.61）

## 起步集（论文级原图，可直接用于细节页）

| 图 | 一句话 |
| --- | --- |
| fig_eso_fal_4cfg.png | 类 fal 默认档让 Base/律 D 全面变好（回声 −32%/−29%），但 F-B 两档要重标定。 |
| fig_eso_fal_gain.png | 类 fal 增益的小信号斜率 = δ^(a−1)：δ 越小、噪声增益越大，这是全部代价的来源。 |
| fig_echo_case.png | 撤除工况的回声只有稳态的 0.44–0.61 倍（不可辨），反相工况 1.26–1.54 倍（可辨）。 |
| fig_fb_retune.png | 方向限定判据把 F-B 的首触发从 12–244 ms 收到 12–68 ms，但窗口仍比线性档宽。 |
| fig_rev2_speed_600.png | 反相工况四档四联图：首拍回声 73 → 40 rpm（D+F-B，α=−1）。 |
