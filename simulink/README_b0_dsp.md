# b0 在线辨识模块 —— Simulink / F28335 移植说明

## 1. 文件清单

| 文件 | 说明 |
|---|---|
| `b0_ident.h` | 参数结构体 `b0_ident_P`、状态结构体 `b0_ident_DW`、接口声明 |
| `b0_ident.c` | 算法实现（段机 + 相干解调 + 代数反解 + 门控 + 低通 + 冻结） |
| `b0_ident_wrap.h/.c` | Simulink C Caller 入口 `b0_ident_u(in[5], out[2])`，含硬件可调宏 |
| `test_b0.c` | 解析自洽测试（gcc 可编，5 个用例） |

## 2. 端口规格（全部 1 ms 离散，`[0.001 0]`）

| 端口 | 方向 | 类型 | 单位 | 范围 | 备注 |
|---|---|---|---|---|---|
| `in[0]` iq | in | single | pu | ±4.5 | 实测 q 轴电流 |
| `in[1]` u | in | single | pu | ±4.5 | 转速环输出，**不含**注入 |
| `in[2]` omega | in | single | rpm | ±3000 | 实测转速 |
| `in[3]` e1 | in | single | pu | ±0.05 | 观测器误差 $e_1=\omega_{ref}-z_1$ |
| `in[4]` v | in | single | pu/s | ±20 | 重复内模状态 |
| `out[0]` b0 | out | single | 控制器标幺 | 200~800 | 辨识结果，初值 400 |
| `out[1]` deltau | out | single | pu | ±0.25 | 注入增量，叠加到控制量 |

> iq 与 u 必须同标幺、同量纲；e1 与 v 必须与观测器内部一致。**模块内部不做任何单位换算。**

## 3. 参数

### 3.1 硬件侧可调（改 `b0_ident_wrap.c` 顶部宏即可）

| 宏 | 默认 | 说明 |
|---|---|---|
| `CFG_WH_HZ` | 65.0 | 注入频率 [Hz]，**必须 5 Hz 整数倍**（保证 0.2 s 段内整数周期） |
| `CFG_AMP` | 0.118 | 注入幅值 [pu] |
| `CFG_WAVE` | `B0_WAVE_SINE` | `SINE` / `SQUARE` / `TRI` |
| `CFG_B0_INIT` | 400 | 初值（控制器标称） |
| `CFG_B0_LO/HI` | 200 / 800 | 硬限幅 |
| `CFG_KP` | 75.36 | 转速环 kp |
| `CFG_LP_DIV` | 50 | 低通带宽 = kp/50，$tau=0.663$ s |
| `CFG_WO` | 500 | 观测器带宽 [rad/s] |

### 3.2 算法固定项（已按仿真整定）

`d1=0.10, d2=0.20, dmax=0.50, alpha_base=0.30, mu=0.35, n_seg=200, n_warm=3, n_ident=24, n_freeze=4, period_run=5 s, period_idle=3600 s`

## 4. Simulink 接线

1. 把 3 个 `.c/.h` 加进 **Configuration Parameters → Code Generation → Custom Code**（Include directories 与 Source files）。
2. 放置 **C Caller** 块，函数名选 `b0_ident_u`。
3. 输入端改成一个 **5×1 的 single 向量**（用 Mux 把 iq/u/omega/e1/v 合起来）；输出是一个 **2×1 向量**（用 Demux 拆成 b0 与 deltau）。
4. 采样时间设为 **1 ms**（继承模型基速率）。
5. **不需要**额外初始化块——`b0_ident_u()` 首次调用会自动执行 `b0_ident_setup()`。

在控制回路里：

```
u_loop = 转速环输出
u_cmd  = u_loop + deltau        // 送到电流环
b0_fb  = b0                     // 回写观测器/控制律的 b0
```

## 5. 代码生成配置

| 项 | 值 |
|---|---|
| System target file | `ert.tlc` |
| 数据类型 | 全 `single`（`real32_T`） |
| 动态内存 | 无（状态全在静态 `s_DW`） |
| 浮点 | 单精度；已避开 `math.h`（级数展开 + LUT） |
| 子步 | 无，1 ms 单速率 |

## 6. F28335 注意事项

- **C28x 无硬件 FPU**，单精度走软件模拟。本模块每拍约 40~60 次浮点运算，折算 **约 2000 周期 / 1 ms ≈ 1.3% CPU**（150 MHz），可接受。
- 相位用 **256 点 LUT**（1 KB RAM），运行期无 `sinf/cosf`。
- `expf` 已换成 5 阶级数（误差 <2e-4），只在门控里每 burst 用一次。
- 若 RAM 紧张，`B0_LUT_BITS` 可降到 7（512 B），频率精度略降。

## 7. 上板验证流程（重要）

干净模型上的 5 个自洽测试：

| 用例 | 误差 |
|---|---|
| 正弦 T=1 | −0.031% |
| 正弦 T=0.95∠5°，**T 修正关** | **−0.033%** |
| 正弦 T=0.95∠5°，**T 修正开** | **+3.52%** |
| 方波 T=1 | −0.031% |
| 三角 T=1 | −0.031% |

**结论：T 修正在精确模型下有害。** 它在 Simulink 全系统仿真里是必需的（补偿 u 与 iq 的采样错位），但上板后是否存在同样的错位取决于你的采样时序。所以：

1. **首轮上板先关**（`s_P.tcorr_en = 0`，默认）；
2. 若测得 b0 系统性偏低约 5%（对应 T≈0.95），再打开；
3. 判据：与离线 $b=k_t I_{BASE}/(J\omega_{ref})$ 比对，误差 >3% 才考虑开启。

## 8. 已知限制

- **注入频率必须是 5 Hz 整数倍**：段长固定 200 拍 = 0.2 s，要求 $0.2f_h$ 为整数。若转速大幅变化需改 $f_h$，应在 burst 边界改，段内不得改。
- **辨识窗口固定 120 s**（24 个 burst）。仿真：20 s 进入 ±3%，120 s 时仍在缓慢爬升（增量约 0.4/20 s），120 s 冻结已够。
- **冻结后不再更新**，周期 60 min。若负载惯量会变（联轴、换挡），需缩短 `period_idle` 或改为周期重辨识。
- **门控基线是移动量**（指数滑动），不是固定中位数——这是避免自锁的关键，勿改回中位数。
---

## 附：Simulink C Caller 环境修复记录（2026-11-23）

本机 MATLAB R2023b 原先**无法编译任何自定义代码**，报"未检测到支持的编译器"。三步修复：

### 1. 强制 MinGW 编译器配置

MATLAB 自带的模板 `matlabroot/bin/win64/mexopts/mingw64.xml` 可用，但需手动指定：

```bash
cp "$MATLABROOT/bin/win64/mexopts/mingw64.xml" \
   "$APPDATA/MathWorks/MATLAB/R2023b/mex_C_win64.xml"
```

（原 MSVC 配置已备份为 `mex_C_win64.xml.msvc.bak`）

### 2. 环境变量指向**无空格**路径

模板的 `locationFinder` 要求 `MW_MINGW64_LOC` 且其下存在 `bin\gcc.exe`。
**关键**：路径不能含空格，否则 mex 拼命令行时不加引号会失败。

```bat
:: 建联接，避开 "C:\Program Files\..." 的空格
mklink /J "D:\Matlab2023\bin\win64\mingw64" "C:\Program Files\x86_64-8.1.0-...\mingw64"
set MW_MINGW64_LOC=D:\Matlab2023\bin\win64\mingw64
```

注意：该变量必须出现在 **MATLAB 进程的环境**里。命令行批处理时要显式带上，否则 `mex`
仍会报“未检测到支持的编译器”：

```bash
MW_MINGW64_LOC=D:\Matlab2023\bin\win64\mingw64 matlab -batch "cd('...\\simulink'); cmp2"
```

建议写进用户环境变量（`setx MW_MINGW64_LOC ...`），一劳永逸。

### 2b. 时基必须用整数拍计数（2026-11-23 修正）

调度原来用 `t_now += P->dT`（float32 秒）计时，130 s 会累积 −45 ms 漂移
（约 0.042%，合 1.5 s/h）。在闭环里看不出来（注入与段边界同源于一个时钟），
但在“记录—回放”类测试里会让段边界相对记录流滑动，末端错开 52 拍，
使“无注入参考段”被 26% 的注入污染，回放终值从 531.7 漂到 573.2。

现已改为 `uint32_t tick` 拍计数：`tick++`、`next_tick = tick + b0_ticks(period, dT)`。
换回浮点秒时基可复现旧的漂移（`replay_variants.py` 已含四种变体）。

注意：uint32 拍计数在 1 kHz 下约 49.7 天回绕。辨识窗口只有 120 s，
回绕至多让一次 burst 提前/推迟一拍，无需处理；若将来改成高频流式运行再说。

### 3. 信号源必须是 single

C Caller 端口默认 `single`，Sine/Constant 默认 `double`，需加
**Data Type Conversion** 块（`OutDataTypeStr = single`）。

修复后验证：`MEX_C_OK` → C Caller 模型 `SIM_OK`。

### 已知问题的结论（已修，2026-11-23）

`du` 从第 13 拍发散到 1.344 的**根因不是 inout 指针，而是 LUT 建表**：
`b0_build_tab()` 原先在 [0, 2*pi) 上直接展开 Taylor，a≈2*pi 时末项 a^9/9!≈44，
LUT 输出远大于 1，注入量被放大 11 倍（应为 0.118，实测 1.344）。
修复：**先按象限折叠到 [0, pi/2] 再展开级数**，LUT 输出回到 |·|<=1。

同时把接口改成结构体返回值（`b0_ident_res`，5 进 1 出），顺带消除指针歧义：

```c
typedef struct { float b0; float du; } b0_res_t;
b0_res_t b0_ident_res(float iq, float u, float omega, float e1, float v);
```

`b0_foc2` 即用此接口，闭环误差 −0.90%。教训：**自洽测试看不出的缺陷，跑一遍实际波形就露出来**——
这也是 `cmp2.m`（C vs MATLAB 逐点回放）存在的理由。
