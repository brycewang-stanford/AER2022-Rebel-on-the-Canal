# 交叠DID（DID in Staggered Adoption Design）Stata 命令详解

> 本文档对应推文《交叠DID方法太多，实证时到底怎么选？》，整理了 6 个 Stata 命令包的语法、核心选项及适用场景。所有命令均可在 GitHub 上找到对应仓库。

---

## 目录

1. [csdid](#1-csdid) — Callaway & Sant'Anna（2021）
2. [did_imputation](#2-did_imputation) — Borusyak, Jaravel & Spiess（2023）
3. [eventstudyinteract](#3-eventstudyinteract) — Sun & Abraham（2021）
4. [did_multiplegt](#4-did_multiplegt) — de Chaisemartin & D'Haultfœuille（2020）
5. [did_had](#5-did_had) — de Chaisemartin & D'Haultfœuille（2025）
6. [ddtiming](#6-ddtiming) — Bacon 分解（诊断 TWFE）

---

## 1. csdid

**功能：** 实现了 Callaway & Sant'Anna（2021）的 DID 估计量，支持 **聚类稳健 wild bootstrap**（WBoot），可处理处理效应的异质性。

**GitHub：** [pedrohcgs/csdid-stata](https://github.com/pedrohcgs/csdid-stata)

### 基本语法

```stata
csdid Y [xvar] [if] [in] [weight]                          ///
    , ivar(panelvar) time(timevar) gvar(cohortvar)         ///
    [notyet]                                                ///
    [method(dripw|drimp|aipw|reg|stdipw)]                  ///
    [agg(attgt|simple|group|calendar|event)]               ///
    [cluster(varname)]                                      ///
    [wboot | wboot1]                                        ///
    [reps(integer 999) rseed(string) wbtype(mammen|rademacher)] ///
    [level(int 95)]                                         ///
    [covariates(varlist)]                                   ///
    [saverif(filename) replace]                             ///
    [notyet long long2 asinr]
```

### 核心选项详解

| 选项 | 说明 | 备注 |
|------|------|------|
| `ivar(panelvar)` | 个体/面板 ID | **必选** |
| `time(timevar)` | 时间变量 | **必选** |
| `gvar(cohortvar)` | 处理组 cohort（首次被处理的时期） | **必选** |
| `notyet` | 使用 **not-yet-treated** 作为对照组 | 当没有 never-treated 组时使用 |
| `method(dripw)` | 估计方法，默认 `dripw`（逆概率加权） | `drimp`（带倾斜）、`aipw`（双重稳健）、`reg`（仅回归）、`stdipw`（稳定IPW） |
| `agg(attgt)` | 聚合方式，默认 `attgt`（各 cohort×time ATT） | `simple`（总体 ATT）、`group`（按 cohort 聚合）、`calendar`（按日历期聚合）、`event`（事件研究图） |
| `cluster(varname)` | 聚类标准误的聚类变量 | 建议使用 |
| `wboot` / `wboot1` | 开启 **wild bootstrap** | 推荐用于小样本，聚类稳健 |
| `reps(999)` | bootstrap 重复次数 | 默认 999 |
| `rseed(#)` | 随机数种子 | 确保可复现 |
| `wbtype(mammen)` | bootstrap 类型 | `mammen`（默认）或 `rademacher` |
| `pointwise` | 使用逐点置信区间（而非 uniform） | 与 `wboot` 联用 |
| `level(95)` | 置信水平，默认 95% | |
| `covariates(varlist)` | 加入协变量 | 仅与 `dripw`/`drimp`/`aipw` 联用 |
| `saverif(filename)` | 保存所有 RIF（recentered influence function） | 用于后续自定义聚合 |
| `replace` | 覆盖已存在的 saverif 文件 | |
| `long` / `long2` | 允许时间序列中存在缺失期 | 处理非平行时间窗口 |
| `asinr` | 预趋势检验专用选项 | 用于 as-if 随机假设检验 |

### agg 选项详细说明

- **`agg(attgt)`**（默认）：输出所有 cohort×time 组合的 ATT(g,t)，即 ATT(g=处理 cohort, t=相对时间)
- **`agg(simple)`**：加权平均，得到总体平均处理效应 E[ATT]
- **`agg(group)`**：按 cohort 分组聚合
- **`agg(calendar)`**：按日历期（cohort 间平均）聚合
- **`agg(event)`**：生成事件研究图格式的估计量

### 输出结果

`csdid` 会自动输出回归表，并存储以下 e 类结果供后续使用：

```stata
ereturn list
// 关键存储项：
// e(b)          — 估计系数矩阵
// e(V)          — 方差-协方差矩阵
// e(gtt)        — 样本信息（cohort、t0、t1、样本量）
// e(agg)        — 聚合方式
// e(glev)       — 各 cohort 取值
// e(tlev)       — 各时间取值
// e(method)     — 使用的估计方法
// e(control_group) — 对照组类型（Never Treated / Not yet Treated）
```

### 完整示例

```stata
* 基本用法（总体 ATT）
csdid y, ivar(id) time(year) gvar(cohort)

* 事件研究图
csdid y, ivar(id) time(year) gvar(cohort) agg(event)

* 带协变量 + wild bootstrap
csdid y x1 x2, ivar(id) time(year) gvar(cohort) ///
    covariates(x1 x2) method(dripw) wboot reps(999) rseed(12345)

* 使用 not-yet-treated 作为对照组
csdid y, ivar(id) time(year) gvar(cohort) notyet agg(group)

* 保存 RIF 后自定义聚合
csdid y, ivar(id) time(year) gvar(cohort) saverif(myrif) replace
```

---

## 2. did_imputation

**功能：** 实现了 Borusyak, Jaravel & Spiess（2023）的**插补（imputation）估计量**。先利用未处理组（或 not-yet-treated）估计反事实结果，再计算处理效应。

**GitHub：** [borusyak/did_imputation](https://github.com/borusyak/did_imputation)

### 基本语法

```stata
did_imputation Y i t ei [if] [in] [aw iw]           ///
    [, sum]                                         ///
    [horizons(numlist)] [allhorizons] [hbalance]   ///
    [cluster(varname)]                              ///
    [controls(varlist)]                             ///
    [unitcontrols(varlist)]                         ///
    [timecontrols(varlist)]                         ///
    [fe(string)]                                    ///
    [autosample]                                    ///
    [wtr(varlist)]                                  ///
    [project(varlist)]                              ///
    [hetby(varname)]                                ///
    [minn(integer 30)]                              ///
    [pretrends(integer 0)]                          ///
    [delta(integer 0)]                              ///
    [alpha(real 0.05)]                              ///
    [nose]                                          ///
    [verbose]                                       ///
    [saveestimates(varname)]                        ///
    [saveweights(varlist)]                          ///
    [loadweights(varlist)]                          ///
    [saveresid(name)]
```

### 核心选项详解

| 选项 | 说明 | 备注 |
|------|------|------|
| `Y` | 结果变量 | **必选，第1个变量** |
| `i` | 个体 ID | **必选，第2个变量** |
| `t` | 时间变量 | **必选，第3个变量** |
| `ei` | **处理开始时间**（首次被处理的时间） | **必选，第4个变量**；never-treated 设为缺失（`.`） |
| `sum` | 报告加权 sum 而非 weighted mean | |
| `horizons(numlist)` | 指定要估计的期数（相对时间） | 例如 `horizons(0 1 2 3 4)` |
| `allhorizons` | 估计所有出现的期数 | |
| `hbalance` | 仅保留在所有 horizon 都有数据的单位（平衡面板） | 与 horizons/allhorizons 联用 |
| `cluster(varname)` | 聚类标准误，默认聚类到个体 i | **建议使用** |
| `controls(varlist)` | 时不变协变量（控制组和处理组均可用） | |
| `unitcontrols(varlist)` | 个体层面时变协变量 | 会与个体固定效应交互 |
| `timecontrols(varlist)` | 时间层面协变量 | 会与时间固定效应交互 |
| `fe(string)` | 固定效应，默认 `i t`（个体+时间 FE） | 可改为 `.`（仅常数）、或指定交互项 |
| `autosample` | **自动删除无法插补的观测** | 重要选项，防止报错 |
| `wtr(varlist)` | 处理权重的变量列表 | 默认每个 horizon 权重为1 |
| `project(varlist)` | 投影变量（用于构建稳健权重） | 与 hetby 不兼容 |
| `hetby(varname)` | 按变量分组估计异质性 ATT | 最多30个组 |
| `minn(integer 30)` | 最小有效样本量阈值（HHI 倒数） | 太小则抑制该系数估计 |
| `pretrends(integer k)` | 估计前 k 期 pre-trend 系数并联合检验 | 输出 `e(pre_F)` 和 `e(pre_p)` |
| `delta(integer 0/1)` | 时间间隔，默认自动检测 | 手动指定如 `delta(1)` |
| `nose` | 仅报告点估计，不计算标准误 | 加速调试 |
| `saveestimates(varname)` | 将估计的处理效应保存为新变量 | |
| `saveweights(varlist)` | 保存估计权重到变量 | 用于诊断 |
| `verbose` | 输出详细迭代信息 | |

### 核心逻辑

1. **第一步**：利用处理组在处理前的数据，插补（impute）反事实结果 `Y0`
2. **第二步**：计算处理效应 `ATT = Y - Y0`（仅对处理组）
3. **第三步**：加权平均得到各 horizon 的 ATT

### 事件研究图配套命令

`did_imputation` 配套提供了 `event_plot` 命令用于绘图：

```stata
event_plot, estfile(filename) name(graph_name) [...]
```

### 完整示例

```stata
* 基本用法
did_imputation y id year first_treated, cluster(id)

* 事件研究图（所有 horizon）
did_imputation y id year first_treated, cluster(id) allhorizons

* 带协变量和 pre-trend 检验
did_imputation y id year first_treated,               ///
    cluster(id) controls(x1 x2) pretrends(2)

* 平衡面板 + 指定 horizon
did_imputation y id year first_treated,               ///
    horizons(0 1 2 3 4) hbalance cluster(id)

* 异质性分析
did_imputation y id year first_treated,               ///
    cluster(id) hetby(group_var)

* 自动删除无法插补的观测
did_imputation y id year first_treated, cluster(id) autosample
```

---

## 3. eventstudyinteract

**功能：** 实现了 Sun & Abraham（2021）的事件研究交互估计量（Interaction-weighted Estimator），用于稳健地估计动态处理效应并画事件研究图。

**GitHub：** [lsun20/EventStudyInteract](https://github.com/lsun20/EventStudyInteract)

### 基本语法

```stata
eventstudyinteract Y varlist                                    ///
    [if] [in] [weight]                                          ///
    , absorb(absorbvar) cohort(cohortvar)                       ///
    [control_cohort(cohortvar)]                                 ///
    [covariates(varlist)]                                       ///
    [vce(vcetype)]
```

### 核心选项详解

| 选项 | 说明 | 备注 |
|------|------|------|
| `Y` | 结果变量 | **在 varlist 中第一个** |
| `varlist` | **相对时间虚拟变量列表**（leads and lags） | 例如 `rel_time_m4 rel_time_m3 ... rel_time_p4`，**必选** |
| `absorb(absorbvar)` | 固定效应（支持交互固定效应，如 `i.t`） | **必选**；通常用 `reghdfe` 语法 |
| `cohort(cohortvar)` | 处理 cohort 变量 | **必选** |
| `control_cohort(varname)` | 对照 cohort（通常设为 never-treated=1） | 若不指定，默认控制 cohort 权重为0 |
| `covariates(varlist)` | 协变量 | |
| `vce(vcetype)` | 标准误类型，默认 `robust` | 可用 `cluster(clustervar)` |

### 相对时间变量构建

需要手动构建相对时间变量 `rel_time = t - cohort`（cohort 为处理开始期），然后生成各期的虚拟变量：

```stata
gen rel_time = year - cohort
forvalues k = -4/4 {
    gen rel_time_`k' = (rel_time == `k')
}
```

### 关键返回值

`eventstudyinteract` 将结果存在以下矩阵中：

```stata
ereturn matrix b_iw     // Interaction-weighted 平均处理效应（聚合后）
ereturn matrix V_iw     // 对应方差矩阵
ereturn matrix b_interact // 各 cohort×relative_time 的原始估计
ereturn matrix ff_w     // 各 cohort 的权重（份额）
```

### 完整示例

```stata
* 构建相对时间变量
gen rel_time = year - cohort
forvalues k = -4/4 {
    gen rel_`k' = (rel_time == `k')
}

* 基本事件研究图
eventstudyinteract y rel_*-4 -3 -2 -1 0 1 2 3 4    ///
    , absorb(i.id i.year) cohort(cohort)           ///
    control_cohort(never_treated)

* 带协变量 + 聚类标准误
eventstudyinteract y rel_*-4 -3 -2 -1 0 1 2 3 4      ///
    , absorb(i.id i.year) cohort(cohort)           ///
    control_cohort(never_treated)                  ///
    covariates(x1 x2) vce(cluster county)
```

---

## 4. did_multiplegt

**功能：** 实现了 de Chaisemartin & D'Haultfœuille（2020）的**多期 DID 估计量**，特别适合处理状态可能**反复切换**（go on/off treatment）的情形。

**注意：** `did_multiplegt` 是一个**包装命令**，通过 `mode` 参数调用四个不同的子命令。

**GitHub：** [Credible-Answers/did_multiplegt](https://github.com/Credible-Answers/did_multiplegt)

### 基本语法

```stata
did_multiplegt (mode) Y G T D [if] [in] [, options]
```

### mode 参数

| mode | 调用命令 | 适用场景 |
|------|---------|---------|
| `(old)` | `did_multiplegt_old` | 旧版（2020）简单版 |
| `(dyn)` | `did_multiplegt_dyn` | **动态处理效应**（事件研究图） |
| `(had)` | `did_had` | de Chaisemartin & D'Haultfœuille（2025）新方法 |
| `(stat)` | `did_multiplegt_stat` | 静态平均处理效应 |

### 核心通用选项（子命令层面）

| 选项 | 说明 |
|------|------|
| `robust` | 稳健标准误 |
| `cluster(varname)` | 聚类标准误 |
| `diff>` | 允许处理效应在组内不同 |
| `saveplot(filename)` | 保存图片 |
| `table` | 输出汇总表格 |

### 动态估计（dyn 模式）示例

```stata
did_multiplegt (dyn) y group time treatment, cluster(group)
```

### 静态估计（stat 模式）示例

```stata
did_multiplegt (stat) y group time treatment, cluster(group)
```

### 注意事项

- `did_multiplegt` 依赖 `reghdfe`（`ssc install reghdfe, replace`）和 `ftools`
- 如果子命令未安装会自动从 SSC 安装
- 该包**不**提供直接的事件研究图命令，需配合手动绘图

---

## 5. did_had

**功能：** 实现了 de Chaisemartin & D'Haultfœuille（2025）的**异质性 adoption design 估计量**，使用局部多项式（local polynomial）方法，支持动态效应、线性趋势调整和 QUG（quasi-untreated group）诊断检验。

**GitHub：** [chaisemartinPackages/did_had](https://github.com/chaisemartinPackages/did_had)

### 基本语法

```stata
did_had Y G T D [if] [in]                            ///
    [, effects(integer 1) placebo(integer 0)        ///
       level(real 0.05)                              ///
       kernel(string) bw_method(string)              ///
       graph_off dynamic trends_lin yatchew          ///
       _no_updates graph_opts(string)]
```

### 核心选项详解

| 选项 | 说明 | 备注 |
|------|------|------|
| `Y` | 结果变量 | **必选，第1个位置** |
| `G` | 个体/群体 ID | **必选，第2个位置** |
| `T` | 时间变量 | **必选，第3个位置** |
| `D` | 处理变量（二值，处理强度连续均可） | **必选，第4个位置** |
| `effects(integer 1)` | 估计多少期**事后**处理效应 | 默认1（即处理当期） |
| `placebo(integer 0)` | 估计多少期**事前**伪处理效应 | 用于安慰剂检验 |
| `level(real 0.05)` | 显著性水平，默认 5% | |
| `kernel(epa)` | 核函数，默认 `epa`（epanechnikov） | 可选 `uniform`、`triangular` 等 |
| `bw_method(mse-dpi)` | 带宽选择方法，默认 MSE-DPI | 可选 `mse`、`cc` 等 |
| `graph_off` | **不画图** | 仅输出表格 |
| `dynamic` | 使用累积处理变化（而非水平处理） | 处理强度变化时使用 |
| `trends_lin` | 控制线性时间趋势 | 需要至少3期预处理数据 |
| `yatchew` | 执行 Yatchew 异方差稳健检验 | 需要安装 `yatchew_test` |
| `_no_updates` | 禁止自动检查更新 | |
| `graph_opts(string)` | 传给 `twoway` 绘图的其他选项 | |

### 估计量逻辑

`did_had` 的核心是"准处理组"（QUG）识别策略：
1. 构造**处理组变化**（treatment change）变量
2. 用**未处理组**（或准未处理组）构造反事实
3. 使用局部多项式回归估计处理效应

### 伪处理效应（placebo）

```stata
* 估计2期事后效应 + 3期安慰剂
did_had y group time treatment, effects(2) placebo(3)
```

### 线性趋势调整

```stata
* 控制组内线性趋势
did_had y group time treatment, effects(2) trends_lin
```

### 累积处理效应（dynamic）

```stata
* 累积处理效应（处理强度的累积变化）
did_had y group time treatment, effects(3) dynamic
```

### 输出结果

输出包含以下信息：
- **Effect Estimates**：各期处理效应、SE、CI、QUG 检验的 T 统计量和 p 值
- **Placebo Estimates**：事前伪效应（应不显著）
- **Yatchew Test**（若指定）：异方差稳健性检验

---

## 6. ddtiming

**功能：** 实现了 Bacon 分解（Bacon decomposition），将 TWFE 估计量分解为所有 **2×2 DID** 比较的加权平均，揭示 TWFE 可能产生偏误的来源和大小。

**GitHub：** [tgoldring/ddtiming](https://github.com/tgoldring/ddtiming)

### 基本语法

```stata
ddtiming Y D [if]                              ///
    , i(panelvar) t(timevar)                   ///
    [ddline(string) noLine]                    ///
    [Msymbols(string)] [MColors(string)]       ///
    [MSIZes(string)]                           ///
    [SAVEGraph(string) SAVEData(string)]       ///
    [replace]                                  ///
    [*]
```

### 核心选项详解

| 选项 | 说明 | 备注 |
|------|------|------|
| `Y` | 结果变量 | **必选，第1个变量** |
| `D` | 处理指示变量（0/1 二值） | **必选，第2个变量** |
| `i(panelvar)` | 面板/个体 ID | **必选** |
| `t(timevar)` | 时间变量 | **必选** |
| `ddline(string)` | TWFE 估计量的垂直线位置 | 默认画在 TWFE 估计值处 |
| `noLine` | 不画 TWFE 垂直线 | |
| `Msymbols(string)` | 各类型散点的符号 | 4种类型，依次指定 |
| `MColors(string)` | 各类型散点的颜色 | 4种类型，依次指定 |
| `MSIZes(string)` | 各类型散点的大小 | 4种类型，依次指定 |
| `SAVEGraph(string)` | 保存图片（.gph 或 .png/.pdf） | |
| `SAVEData(string)` | 保存分解数据（.csv + .do） | 包含权重、2×2估计值 |
| `replace` | 覆盖已存在的保存文件 | |

### 2×2 比较的四种类型

`ddtiming` 将所有 2×2 比较分为四种类型：

| 类型 | 说明 | 理想权重占比 |
|------|------|-------------|
| **Type 1** | Earlier-treated group vs. Later-treated comparison | 处理组间比较（晚→早） |
| **Type 2** | Later-treated group vs. Earlier-treated comparison | 处理组间比较（早→晚） |
| **Type 3** | Treatment vs. **Never treated** | 与从未处理组比较 |
| **Type 4** | Treatment vs. **Already treated** | 与已处理组比较（可能偏误） |

### 输出解读

```
Diff-in-diff estimate: 0.123
(这是 TWFE 的总体加权估计)

DD Comparison              Weight      Avg DD Est
{hline 49}
Earlier T vs. Later C       0.234       0.089
Later T vs. Earlier C       0.456       0.198
T vs. Never treated         0.210       0.156
T vs. Already treated       0.100       0.301
{hline 49}
```

**警告信号：**
- Type 4（Already treated）权重过大 → 潜在 TWFE 偏误
- 不同类型的估计值差异很大 → 处理效应异质性严重

### 完整示例

```stata
* 基本用法
ddtiming y treat, i(id) t(year)

* 自定义图形
ddtiming y treat, i(id) t(year)       ///
    Msymbols(D T O S)                  ///
    MColors(gs8 black gs6 navy)        ///
    ddline(lcolor(red))

* 保存分解数据用于自定义绘图
ddtiming y treat, i(id) t(year) savedata(mydecomp)
```

---

## 命令对比速查表

| 场景 | 推荐命令 | 主要理由 |
|------|---------|---------|
| **诊断 TWFE 偏误** | `ddtiming` | 分解 TWFE，揭示权重结构 |
| **估计总体 ATT** | `csdid` (agg simple) 或 `did_imputation` | 允许异质性，稳健 |
| **事件研究图** | `csdid` (agg event) 或 `eventstudyinteract` | IW 估计量，稳健 |
| **从未处理组存在** | `csdid` / `did_imputation` 均支持 | never-treated 直观对照 |
| **无从未处理组** | `csdid` + `notyet` 或 `did_imputation` | not-yet-treated 对照 |
| **处理状态反复切换** | `did_multiplegt (dyn)` | 允许 on/off treatment |
| **处理强度连续变化** | `did_had` | 局部多项式，可处理强度 |
| **2025 新方法（QUG诊断）** | `did_had` | 支持伪处理检验、线性趋势 |
| **BJS 插补估计** | `did_imputation` | 插补反事实，效率高 |
| **需要协变量** | `csdid` / `did_imputation` | 支持协变量调整 |

---

## 安装方式汇总

```stata
* 主要命令（均通过 SSC 安装）
ssc install csdid, replace
ssc install did_imputation, replace
ssc install eventstudyinteract, replace
ssc install did_multiplegt, replace
ssc install did_had, replace
ssc install ddtiming, replace

* 依赖项（大部分自动安装）
ssc install reghdfe, replace    // csdid, did_multiplegt, eventstudyinteract
ssc install ftools, replace     // did_imputation
ssc install drdid, replace      // csdid（内部调用）
ssc install gtools, replace     // did_had
ssc install nprobust, replace   // did_had（局部多项式）
ssc install yatchew_test, replace // did_had（yatchew 选项）
```

> **提示：** 以上 GitHub 仓库已下载到本地当前文件夹，可直接参考源码了解更多实现细节。
