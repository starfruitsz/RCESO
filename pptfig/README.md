# pptfig —— PPT 用仿真图

本目录专门存放**汇报/答辩 PPT 用的仿真图**。仓库根目录的 `fig_*.png` 仍是论文/正文用图（口径唯一来源），
这里只放**面向投屏重新排版**的版本：图更大、字号更大、去掉细网格、白底。

## 规格约定

| 项 | 约定 |
| --- | --- |
| 画布 | 16:9（如 12.8 × 7.2 in），单栏图至少 9 × 5 in |
| 字号 | 轴标签 ≥ 14 pt、刻度 ≥ 12 pt、图例 ≥ 11 pt、标题 ≥ 16 pt |
| DPI | 300（投屏够用，体积仍在几 MB 内） |
| 背景 | 纯白不透明；只保留主网格（alpha ≤ 0.15） |
| 颜色 | 沿用正文色：线性/无律 #1f4e79、类 fal #c0392b、律 D #e67e22、F-B #16a085、D+F-B #8e44ad |
| 命名 | `ppt_<序号>_<主题>_<变量>.png`，如 `ppt_03_echo_rev_600.png`；需要矢量时同名再存 .pdf |
| 图注 | 图内不写长说明（放 PPT 备注），只保留必要的 (a)(b) 标号 |

## 起步集（已复制，可直接用；原图在仓库根目录）

| 文件 | 内容 | 生成脚本 |
| --- | --- | --- |
| fig_eso_fal_4cfg.png | 四档算法 × 线性/类 fal（8 种子柱状） | run_eso_fal_4cfg.py → plot_eso_fal.py |
| fig_eso_fal_gain.png | 类 fal 增益形状 + 小信号斜率 | plot_eso_fal.py |
| fig_echo_case.png | 回声工况筛选：撤除 vs 反相 | run_echo_case_screen.py / run_echo_reversal.py → plot_echo_case.py |
| fig_fb_retune.png | F-B 重标定：oracle 曲线 + 触发时刻 + 指标 | run_fb_oracle.py / run_fb_retune.py → plot_fb_retune.py |
| fig_rev2_speed_600.png | 反相工况四联图（600 rpm） | run_echo_rev2_wave.py → plot_echo_rev2_case.py 600 10 |

## 待办

- [ ] 按上表规格把起步集重画成 PPT 版（大字号 / 16:9），输出 `ppt_*.png`
- [ ] 每张图配一行"一句话结论"，存进 `pptfig/NOTES.md`（供写讲稿）
- [ ] 需要动画时，从同名 `_wave_*.npz` 直接导出 GIF/MP4

## 纪律

- 本目录**只放展示用图**，任何数字都必须能由根目录的 `run_*.py` + `_*.json` 复算；不得手工改图。
- 换口径（ESO 默认档、事件类型）时，本目录的图与根目录的图必须同批重出。
