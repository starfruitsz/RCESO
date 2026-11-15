# RCESO

重复控制 + 扩张状态观测器（RC-ESO）的 PMSM 逆变器侧自适应抑制：技术报告、PPT、公式与仿真代码。

## 先读

- [交接_2026-11-14.md](交接_2026-11-14.md)：当前口径、已完成/未完成项、复现命令与文件地图（最新 2026-11-15 追加见 §9/§10）。

## 交付物

| 类别 | 文件 |
|---|---|
| 技术报告 | `rcso_v3.tex` / `rcso_v3.pdf`（42 页）/ `rcso_v3.html`（自包含） |
| 报告配图 | `fig_qmode.png`、`fig_qmode_c.png`、`fig_inv_demo.png`、`fig_lawd_cmp_600.png`、`fig_t_es3.png`、`fig_t_es4.png`、`fig_t_es_rt.png`、`fig_j_adapt.png`、`fig_fault_sweep.png`、`fig_t_dft_report.png` |
| 关节报告 PPT | `2026.10--2_b0combined.pptx`（图源 `ppt_s*_combined.png`、`fig_b0_adaptive_ppt.png`） |
| 公式与讲解 | `j_recheck_formulas.pdf`、`j_adapt_formulas.pdf`、`律J_*`、`律T_公式展示与讲解.md` |
| 仿真 | `pmsm_inv_sim.py`（三相 PWM + PMSM + ESO/RC + 律 D/T/J）、`noise_cfg.py` |
| 出图脚本 | `run_ppt5.py`/`plot_ppt5.py`、`run_b0_ppt.py`/`plot_b0_adaptive_ppt.py` |
| 律T 幅值 DFT | `run_t_dft.py`、`_t_dft_cmp.py`、`_t_svf_gain.py`、`_t_dft_report_fig.py`；图 `fig_t_dft.png`、`fig_t_dft_report.png` |

## 编译报告

```bash
xelatex rcso_v3.tex   # 两遍
python _mkhtml.py rcso_v3.tex   # 可选：重建自包含 HTML
```

> 旧实验脚本/数据/中间图已从当前版本移除（仍在 git 历史中）；未跟踪的原始数据在仓库外的 `RCESO_archive_20261115/`。