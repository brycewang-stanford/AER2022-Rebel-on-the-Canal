# statspai 对齐 Stata DID 命令的改进建议

> 本文档系统对比了 statspai Python 包与 6 个主流 Stata DID 命令的功能差距，从**估计方法选择**、**标准误设置**、**聚合方式**、**诊断工具**、**输出与后处理**五个维度逐项梳理，并提出具体改进建议。核心观察是：statspai 的架构覆盖了所有主流估计量，但在**选项灵活性**和**细粒度控制**上与 Stata 命令存在系统性差距。

---

## 一、对比总览

| 维度 | Stata | statspai | 差距等级 |
|------|-------|----------|---------|
| 估计方法选择 | 每命令 4–5 种 method 选项 | 仅 CS 支持 `estimator`（3 种）| ⭐⭐⭐ |
| 聚合方式 | 每命令各自独立实现，丰富多样 | 统一 `aggte()`，类型有限 | ⭐⭐⭐ |
| 标准误类型 | 聚类、HC、Bootstrap、Wild Bootstrap | 仅聚类 / robust | ⭐⭐⭐ |
| 置信区间 | 点wise + Uniform（统一） | 需手动开启 uniform | ⭐⭐ |
| 协变量处理 | 每命令单独规定与哪些 method 兼容 | 一揽子传入，无限制 | ⭐⭐ |
| 预趋势检验 | asinr、pretrends 联合检验 | `pretrends_test()` 独立函数 | ⭐ |
| 诊断工具 | Bacon 分解集成在 ddtiming 中 | `bacon_decomposition()` 独立函数 | ⭐ |
| 保存与复现 | `saverif()` / `savedata` | 无原生支持 | ⭐⭐⭐ |
| 事件研究图 | `agg(event)` 直接输出 | 需调用 `event_study_plot()` | ⭐ |
| RIF 自定义聚合 | `saverif()` 后可自由计算 | 无等效功能 | ⭐⭐⭐ |

---

## 二、逐命令对比与改进建议

### 2.1 csdid vs callaway_santanna()

#### Stata `csdid` 独有功能

| 功能 | Stata 选项 | statspai 现状 | 改进建议 |
|------|-----------|--------------|---------|
| Wild Bootstrap | `wboot` / `wboot1` | **缺失** | 实现 `wboot=True` 参数，支持 Mammen/Rademacher 类型，输出 uniform CI |
| Wild Bootstrap 重复次数 | `reps(999)` | **缺失** | 新增 `wboot_reps` 参数 |
| Bootstrap 类型 | `wbtype(mammen\|rademacher)` | **缺失** | 新增 `wboot_type` 参数 |
| 点wise CI vs Uniform CI | `pointwise` | **缺失** | 新增 `ci_type='pointwise'\|'uniform'` |
| 替代标准误估计器 | `stdipw`（稳定逆概率加权） | **缺失** | 在 `estimator` 选项中新增 `'stdipw'` |
| 长期/预趋势检验 | `asinr` | **缺失** | 实现 as-if 随机假设检验统计量 |
| RIF 保存与自定义聚合 | `saverif(filename)` | **缺失** | 实现类似 `saverif()` 的 RIF 导出，支持事后自定义加权聚合 |
| 不等长面板支持 | `long` / `long2` | **缺失** | 实现 `long=True` 处理非平行时间窗口 |
| 替代控制组（not-yet-treated）| `notyet` | `control_group='notyettreated'` | ✅ 已对齐 |
| 协变量 | `covariates(varlist)` | `covariates=[]` | ✅ 已对齐 |
| 聚类标准误 | `cluster(varname)` | `cluster=...` | ✅ 已对齐 |

#### 改进优先级：**P0（高）**

```python
# 建议新增 API
cs = callaway_santanna(
    data=df, y='y', id='unit', time='year', cohort='first_treat',
    estimator='dr',              # 当前支持: 'dr', 'ipw', 'reg'
    # === 新增 ===
    alt_estimator='stdipw',      # 稳定逆概率加权估计量
    wboot=True,                  # Wild Bootstrap
    wboot_reps=999,              # Bootstrap 次数
    wboot_type='mammen',          # 'mammen' | 'rademacher'
    ci_type='uniform',           # 'pointwise' | 'uniform'
    long=True,                   # 允许非平行时间窗口
    save_rif='myrif.csv',        # 导出 RIF 用于自定义聚合
    pretest='asinr',             # as-if 随机假设检验
)
```

---

### 2.2 did_imputation vs bjs / did_imputation()

#### Stata `did_imputation` 独有功能

| 功能 | Stata 选项 | statspai 现状 | 改进建议 |
|------|-----------|--------------|---------|
| 前定趋势联合检验 | `pretrends(k)` 报告前 k 期系数并联合检验 | `pretrends_test()` 独立调用，需手动传入 | **整合**：新增 `pretrends=k` 参数，直接输出 Wald F 统计量和 p 值 |
| 平衡面板约束 | `hbalance` | **缺失** | 新增 `balanced=True`，仅保留所有 horizon 均有数据的单位 |
| 指定 horizon 范围 | `horizons(0 1 2 3 4)` | `min_e`/`max_e` 在 aggte 中 | 允许在估计阶段直接限定，而非聚合阶段 |
| 协变量分类 | `controls`（时不变）/ `unitcontrols`（个体时变）/ `timecontrols`（时间层面）| 统一 `covariates` | **拆分**：实现 `unit_covariates` 和 `time_covariates`，分别与个体 FE 和时间 FE 交互 |
| 最小样本阈值 | `minn(30)` | **缺失** | 新增 `min_n=30` 过滤太少的 cohort×horizon 组合 |
| 保存估计权重 | `saveweights(varlist)` | **缺失** | 新增 `save_weights=True`，导出各观测的估计权重用于诊断 |
| 投影变量 | `project(varlist)` | **缺失** | 实现投影变量支持，与 `hetby` 互斥 |
| 组间异质性分析 | `hetby(varname)` | **缺失** | 新增 `hetby='group_var'`，按分组输出异质性 ATT |
| 替代固定效应 | `fe(string)` 可改为 `i.t` 以外的形式 | 固定为 `i.t` | 新增 `fe='i.unit + i.time'` 语法，允许自定义 FE 结构 |
| 保存残差 | `saveresid(name)` | **缺失** | 新增 `save_residuals=True`，便于模型诊断 |

#### 改进优先级：**P1（中）**

```python
# 建议新增 API
bjs = did_imputation(
    data=df, y='y', id='unit', time='year', cohort='first_treat',
    # === 已有 ===
    cluster='unit',
    # === 新增 ===
    pretrends=2,                 # 联合检验前2期 pre-trend
    balanced=True,                # 平衡面板
    horizons=[0, 1, 2, 3, 4],    # 直接指定 horizon
    unit_covariates=['x1'],      # 与个体FE交互的时变协变量
    time_covariates=['x2'],      # 与时间FE交互的协变量
    min_n=30,                    # 最小样本阈值
    hetby='region',              # 组间异质性
    save_weights=True,           # 导出估计权重
    save_residuals=True,         # 导出残差
    fe='i.unit + i.time',       # 自定义固定效应结构
)
```

---

### 2.3 eventstudyinteract vs sun_abraham()

#### Stata `eventstudyinteract` 独有功能

| 功能 | Stata 选项 | statspai 现状 | 改进建议 |
|------|-----------|--------------|---------|
| 手动构建 leads & lags | 需手动 `gen rel_time_k = (rel_time == k)` | 内部自动构建 | ✅ 自动构建更友好，但**缺少自定义**选项 |
| 替代控制 cohort | `control_cohort(varname)` | **缺失** | 新增 `control_cohort` 参数，允许指定 never-treated cohort 值 |
| 异质性稳健 SE | `vce(robust\|cluster)` | `cluster` 支持 | ✅ 已对齐 |
| 协变量 | `covariates(varlist)` | `covariates` | ✅ 已对齐 |
| 允许 not-yet-treated | 隐含在 cohort 变量中 | `control_group='notyettreated'` | ✅ 已对齐 |

#### 改进优先级：**P2（低）**

主要是新增 `control_cohort` 参数，用于当数据中存在多个 cohort 时显式指定对照组。

---

### 2.4 did_multiplegt vs did_multiplegt() / did_multiplegt_dyn()

#### Stata `did_multiplegt` 独有功能

| 功能 | Stata 选项 | statspai 现状 | 改进建议 |
|------|-----------|--------------|---------|
| 模式切换 | `(dyn)` / `(stat)` / `(old)` / `(had)` | `did_multiplegt()` 和 `did_multiplegt_dyn()` 分开 | ✅ 已通过两个函数覆盖 |
| 允许处理效应组内差异 | `diff` | **缺失** | 新增 `allow_heterogeneous_effects=True` |
| 静态 vs 动态切换 | 隐含在 mode 中 | 已有静态/动态两个函数 | ✅ |
| 汇总表格 | `table` | **缺失** | 新增 `summary_table=True` |
| 图片保存 | `saveplot(filename)` | `event_study_plot()` 可视化 | 建议新增 `save_plot='path.png'` |

#### 改进优先级：**P2（低）**

---

### 2.5 did_had vs did_had()

#### Stata `did_had` 独有功能

| 功能 | Stata 选项 | statspai 现状 | 改进建议 |
|------|-----------|--------------|---------|
| 带宽选择方法 | `bw_method(mse-dpi\|mse\|cc)` | **缺失** | 新增 `bandwidth_method='mse-dpi'` |
| 核函数选择 | `kernel(epa\|uniform\|triangular)` | **缺失** | 新增 `kernel='epa'` |
| 线性趋势调整 | `trends_lin` | **缺失** | 新增 `control_linear_trend=True` |
| QUG 诊断检验 | 内置于输出 | **缺失** | 实现 QUG（Quasi-Untreated Group）诊断，报告各期的 QUG t 统计量和 p 值 |
| 伪处理效应 | `placebo(k)` | **缺失** | 新增 `placebo_periods=k`，输出前 k 期伪处理效应（安慰剂检验）|
| 异方差稳健检验 | `yatchew` | **缺失** | 新增 `yatchew_test=True`（需安装 yatchew） |
| 累积处理效应 | `dynamic` | **缺失** | 新增 `cumulative=True`，输出累积处理效应（而非水平效应）|
| 不画图 | `graph_off` | `plot=False` | ✅ 部分对齐 |

#### 改进优先级：**P1（中）**

```python
# 建议新增 API
had = did_had(
    data=df, y='y', id='unit', time='year', treat='treatment',
    # === 新增 ===
    bandwidth_method='mse-dpi',   # 带宽选择
    kernel='epa',                 # 核函数
    control_linear_trend=True,    # 线性趋势调整
    placebo_periods=3,            # 3期安慰剂检验
    cumulative=True,               # 累积处理效应
    yatchew_test=True,            # 异方差稳健检验
    graph_off=True,               # 不画图
)
```

---

### 2.6 ddtiming vs twfe_decomposition() / bacon_decomposition()

#### Stata `ddtiming` 独有功能

| 功能 | Stata 选项 | statspai 现状 | 改进建议 |
|------|-----------|--------------|---------|
| 四种 2×2 比较的分类可视化 | 四种符号/颜色/大小 | `bacon_plot()` 统一散点图 | **增强**：实现按 Type 1/2/3/4 分类的散点图，分别控制 `Msymbols`、`MColors`、`MSIZes` |
| TWFE 垂直线 | `ddline()` 默认画在 TWFE 估计值处 | **缺失** | 新增 `dd_line=True` 在图中标注 TWFE 估计位置 |
| 保存分解数据 | `savedata(filename)` 保存 .csv + .do | **缺失** | 新增 `save_decomposition='file.csv'`，导出每种 2×2 比较的权重和估计值 |
| 四种类型权重汇总表 | 内置于输出 | `bacon_decomposition()` 返回 DataFrame | ✅ 已返回数据，但**缺少负权重占比诊断**（这是 TWFE 偏误的核心信号）|
| 偏误来源解读 | 自动报告 | **缺失** | 在返回结果中增加 `negative_weight_share`（Type 4 中为负的权重占比），这是判断 TWFE 偏误严重程度的关键指标 |

#### 改进优先级：**P1（中）**

```python
# 建议新增 API
decomp = twfe_decomposition(
    data=df, y='y', treat='treatment', id='unit', time='year',
    # === 新增 ===
    plot_type='by_category',     # 'all' | 'by_category'
    show_dd_line=True,            # 显示 TWFE 垂直线
    symbols=['D', 'T', 'O', 'S'], # 4种散点符号
    colors=['gray', 'black', 'navy', 'red'],
    sizes=[0.5, 1.0, 0.7, 1.2],
    save_decomposition='bacon_decomp.csv',  # 导出详细数据
    # === 已有但缺诊断 ===
    return_negative_weights=True, # 返回负权重占比
)
```

---

## 三、跨命令的系统性改进建议

### 3.1 标准误体系增强（⭐⭐⭐ 优先级最高）

Stata 所有 DID 命令都支持多种 SE 估计方式，而 statspai 在这一块明显薄弱：

| Stata 支持 | statspai 现状 | 建议实现 |
|-----------|--------------|---------|
| 聚类稳健 SE | ✅ `cluster=...` | 保留 |
| HC0/HC1 稳健 SE | ✅ `robust=True`（仅 2×2/DDD）| 向所有方法推广 |
| Wild Bootstrap | ❌ | 对 CS 和 BJS 实现 `wboot=True` |
| 乘数 Bootstrap（uniform CI）| 仅 aggte 的 `bstrap` | 统一到各估计函数 |
| 自动选择最优 SE | ❌ | 新增 `se_method='auto'` |

```python
# 建议统一 SE API
result = callaway_santanna(
    data=df, y='y', id='unit', time='year', cohort='first_treat',
    se_method='cluster',         # 'cluster' | 'robust' | 'bootstrap' | 'wild-bootstrap' | 'auto'
    cluster='unit',              # 聚类变量
    bootstrap_reps=999,          # Bootstrap 次数
    ci_type='uniform',           # 'pointwise' | 'uniform'
    wboot=True,                  # Wild Bootstrap（推荐小样本）
)
```

### 3.2 RIF（Recentred Influence Function）导出与自定义聚合（⭐⭐⭐）

这是 Stata `csdid` 最强大的特性之一，statspai 完全缺失：

**Stata 实现：**
```stata
csdid y, ivar(id) time(year) gvar(cohort) saverif(myrif) replace
* 之后可以任意加权聚合
```

**建议 statspai 实现：**
```python
# 阶段1：保存 RIF
cs = callaway_santanna(data=df, y='y', id='unit', time='year', cohort='first_treat',
                       save_influence_functions='cs_rif.csv')

# 阶段2：加载 RIF，自定义聚合
from statspai.did import aggte_from_rif

agg = aggte_from_rif(
    rif_file='cs_rif.csv',
    type='event',           # 事件研究聚合
    min_e=-4, max_e=8,      # 限制窗口
    min_n=30,               # 最小样本过滤
    bstrap=True,
    cband=True,
)
```

### 3.3 协变量分类与交互（⭐⭐）

Stata `did_imputation` 区分了三类协变量，statspai 统一处理：

| Stata 协变量类型 | statspai 现状 | 建议 |
|----------------|--------------|------|
| `controls(varlist)` — 时不变或时变 | `covariates` | 保留 |
| `unitcontrols(varlist)` — 与个体 FE 交互 | 隐含在模型中 | 新增 `unit_covariates` |
| `timecontrols(varlist)` — 与时间 FE 交互 | 隐含在模型中 | 新增 `time_covariates` |

### 3.4 灵活的固定效应规范（⭐⭐）

Stata 允许用 `fe(string)` 自定义 FE 结构，statspai 固定为 `i.unit + i.time`：

```python
# 建议新增
result = did_imputation(
    data=df, y='y', id='unit', time='year', cohort='first_treat',
    fixed_effects='i.unit + i.time + i.unit#i.year',  # 允许双向 FD + 交错交互
)
```

### 3.5 统一的预趋势检验接口（⭐⭐）

Stata 各命令各自内置预趋势检验，statspai 是独立函数：

```python
# 建议：各估计函数新增 pretest 参数
cs = callaway_santanna(
    data=df, y='y', id='unit', time='year', cohort='first_treat',
    pretest='joint',          # 'joint' | 'individual' | 'none'
    pretest_periods=3,        # 检验前3期
    pretest_alpha=0.05,
)
# 直接在回归输出中包含 pre-trend F 统计量和 p 值
```

### 3.6 输出格式与保存（⭐⭐⭐）

Stata 可保存 RIF、分解数据、估计权重，statspai 缺少这些：

| 功能 | Stata | statspai 建议 |
|------|-------|-------------|
| 保存估计结果 | `estimates save` | `result.save('file.pkl')` |
| 保存 RIF | `saverif()` | `save_influence_functions()` |
| 保存分解数据 | `savedata()` | `save_decomposition()` |
| 保存权重 | `saveweights()` | `save_weights()` |
| 保存残差 | `saveresid()` | `save_residuals()` |
| 导出 LaTeX | `esttab` | `to_latex()` ✅ 已有 |
| 导出 Excel | - | `to_excel()` ✅ 已有 |

---

## 四、改进路线图建议

### Phase 1：缩小核心差距（P0）
1. **Wild Bootstrap** for `callaway_santanna()` — 这是 Stata 最常用的小样本推断方法
2. **RIF 导出 + 自定义聚合** — 实现 Stata `saverif()` 的等效功能
3. **统一的 SE 方法参数** — 整合聚类/robust/bootstrap/wild-bootstrap

### Phase 2：完善预趋势与诊断（P1）
4. **pretrends 整合进估计函数** — 从独立函数改为 `pretest=k` 参数
5. **Bacon 分解增强** — 负权重占比、4种类别可视化
6. **did_had 完整实现** — 带宽/核函数/QUG检验/placebo/trends_lin
7. **did_imputation 增强** — `hetby`、`balanced`、`min_n`、三类协变量

### Phase 3：高级功能（P2）
8. **`control_cohort` for `sun_abraham()`**
9. **`long` / `long2` for `callaway_santanna()`**
10. **`save_weights` / `save_residuals` / `save_decomposition`**
11. **自定义固定效应语法**
12. **Yatchew 异方差检验**

---

## 五、总结

statspai 的**覆盖广度**已经相当完善（支持 20+ 估计量），但在**选项深度**上与 Stata 存在系统性差距，尤其体现在：

1. **推断方法单一** — 缺少 Wild Bootstrap 和 uniform CI
2. **RIF 功能缺失** — 无法做事后自定义聚合
3. **协变量处理粗糙** — 缺少时变协变量与不同 FE 的交互选项
4. **输出保存薄弱** — 无法导出 RIF、权重、残差供进一步诊断
5. **预趋势检验碎片化** — 应整合进各估计函数而非独立调用

这些问题使得 statspai 在**实证研究的精细化使用**场景下不如 Stata 灵活。改进建议的核心思路是：**在保持 statspai 统一 API 优势的同时，向下渗透 Stata 命令的细粒度控制能力。**
