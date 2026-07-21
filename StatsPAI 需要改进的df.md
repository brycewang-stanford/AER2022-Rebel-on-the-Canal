# StatsPAI 改进清单：基于《Rebel on the Canal》复现的发现

> **来源**：撰写《[论文解释.md](论文解释.md)》与《[论文模型解读与StatsPAI复现分析.md](论文模型解读与StatsPAI复现分析.md)》时反复触到的 StatsPAI v1.20.0 缺口。  
> **目标**：列出在"复现一篇标准 AER 应用计量论文 + 配套 agent-native 工作流"这个具体场景下，StatsPAI 接下来最值得改进的 5–7 件事。  
> **不重复**：本文不复述论文内容（见《论文解释.md》），也不复述 StatsPAI 能力全景（见旧版《论文模型解读与StatsPAI复现分析.md》删去的"StatsPAI 19 项能力对照表"）。

---

## 0. 优先级总览

| 级别 | 缺口 | 影响范围 | 工作量 | 价值 |
|---|---|---|---|---|
| **P0** | Conley 时空 HAC SE（带时间维度） | 历史/政治经济学整条文献带 GIS 面板 | 中 | 直接解锁"能复现 AER/QJE GIS 面板论文" |
| **P0** | formula 语法：交互 / varying slopes / FE 组合 | 所有"高维 FE + 大量交互"的论文 | 中 | 决定 fixest/reghdfe 用户能否迁过来 |
| **P1** | CIC 一键两步法 + 内置 bootstrap | CIC 在 DID/SCM 鲁棒性中已成标准 | 小 | 少 30 行样板代码 + 修复推断隐患 |
| **P1** | Event-study 自定义分箱 + 多期参照 | 历史事件研究的标配 | 小 | 少手工造列 |
| **P1** | Rambachan-Roth / honest DID / pretrends power 端到端 pipeline | 2022+ AER 几乎必问 | 小 | 直接对接 2024-2026 标准 |
| **P2** | reference-parity 基准测试（用本文） | 整体可信度 | 中 | 长期价值最高 |
| **P2** | GIS 前处理教程 + 薄封装 | 中文用户高频场景 | 小 | 解决"不属于包内但经常需要"的痛点 |

---

## 1. P0-1：Conley 时空标准误（Hsiang 2010 风格，论文第二套 SE 的基础）

### 1.1 问题（已在两篇 doc 中反复出现）

论文 Table 3-4 全部方括号 SE 用 **Conley (1999, 2008) + Hsiang (2010)** 风格：500 km 空间截断 + 262 年序列相关。论文附录 A2 还跑了 6 × 4 = 24 组带宽网格。

**StatsPAI 现状**：
- `sp.conley()`：cKDTree 稀疏，只做**空间**维，无时间维核
- `feols(vce="conley")`：与 HDFE 集成，但构造 n×n 稠密矩阵；n=14 万 → ~158 GB → **OOM**
- 两者都**不接受时间维参数**

### 1.2 修复方向

```
# 时间维 = 同行不同时期用时间核（如 Bartlett），同期不同单位用空间核
# 面板下坐标按 unit 去重（575 个县），不再按 14 万行两两算
# meat 矩阵按 (unit, time) 邻对分块累加，内存从 O(n²) 降到 O(邻对数)
```

### 1.3 价值

- 一旦补上，**AER/QJE 历史 + 经济学论文里"GIS 面板"这一大类**（Rebel on the Canal、Maurel-Serdan 2022、Hsiang 2016 等）都能直接复现
- 与 sp.conley 当前实现的差异主要是加上"按 unit 去重的面板优化"+"时间维核"两个特性

### 1.4 验收

- n=140,432 (575 县 × 262 年)，带宽 500 km × 262 年，**内存 < 4 GB**
- 系数对 14 万观测的 Stata `acreg` 输出一致（容差 1e-4）

---

## 2. P0-2：formula 语法扩展

### 2.1 问题

论文五列控制规格里，**三列**（列 2、列 3、列 4）都用 fixest 风格的交互语法。StatsPAI 当前 `feols` 的 formula：

- 只接受**裸列名**
- 不支持 `a:b`、`a*b`、FE 组合 `fe1^fe2`
- 不支持 varying slopes `i.factor#c.var`（即 `i.pref#c.year` 这类）
- HDFE 内核**没有斜率吸收**

→ 用户必须**手工造几十甚至几百列**，能算对但**离 fixest/reghdfe 一行公式的体验还差得远**。

### 2.2 修复方向

```
# 1. formula 解析器扩展：支持 a:b, a*b, i.factor#c.var, fe1^fe2
# 2. HDFE 内核：增加 varying-slope 投影（demeaning → 组内回归残差化）
# 3. 内置 fixest 语法兼容层：i(x) 虚函数化 / ^FE 组合
```

### 2.3 价值

- 这是 fixest/reghdfe 用户迁移到 StatsPAI 的**第一痛点**——写完《论文解释.md》后我深有体会
- 论文式 1（列 2-4）共需手工造 262 + 6 + 90 = 约 360 列；接受 `pre_reb#c.year + province^year + i.pref#c.year` 后**只剩 3 行**

### 2.4 验收

```python
m = sp.feols("y ~ canal_post + pre_reb#c.year | county + province^year + i.pref#c.year",
             data=df, cluster="county")
# 系数与论文 Table 3 列 4 一致
```

---

## 3. P1-1：CIC 一键两步法 + 内置 bootstrap

### 3.1 问题

论文 Appendix A5 用 **Melly-Santangelo (2015) 两步法**：
- 第一步：OLS 把协变量 / 固定效应 partial out（残差化）
- 第二步：对残差做无条件 CIC
- bootstrap SE

StatsPAI `sp.cic()` 当前只做**无条件 CIC**，不支持协变量。论文场景可以手工组合（feols 取残差 → cic），但**有两个隐患**：
1. 残差化后 `keep_mask`（HDFE singleton 剔除后）需要手动对齐原 df
2. 手工组合时 bootstrap 只重抽**第二步**，应重抽**两步一起**

### 3.2 修复方向

```python
sp.cic(
    data=df, y="y", group="along_canal", time="post",
    covariates=["pre_reb#year", "province^year", "i.pref#c.year"],
    first_stage="feols",  # 内部 feols 残差化
    n_boot=500,
)
# 输出与 Melly-Santangelo 2015 的 cic 命令对齐
```

### 3.3 价值

- 少 30 行样板代码
- 自动处理 `keep_mask` 对齐、协变量列表展开、bootstrap 重抽
- 解决推断隐患（只重抽第二步会低估 SE）

---

## 4. P1-2：Event-study 自定义分箱 + 多期参照

### 4.1 问题

论文事件研究用**按十年分箱**、**参照组为"前 50 年以上"那段整段**。StatsPAI `sp.event_study()` 当前：

- 固定为**逐期 dummy**（每年一个）
- 只接受**单期参照**
- 没有自定义分箱宽度

→ 论文这种"按 decade 分箱 + 区段参照"是 2018 以来 AER 事件研究的**事实标配**，需要手写 + 减速度。

### 4.2 修复方向

```python
sp.event_study(
    data=df, y="y", unit="county", time="year",
    treat_time=1826,
    bin_width=10,                    # 每 10 年一 bin
    ref_period=("<=", -50),         # 参照组：τ ≤ -50
    covariates=["county", "province^year"],
)
# 直接输出 Figure 4 风格的 coefficients + confidence band
```

### 4.3 价值

- 少手工造列 + 手工选参照
- 与 Rambachan-Roth (2023) 的 breakdown 分析**接口对齐**——事件研究 β + 协方差矩阵是 Rambachan-Roth 的唯一输入

---

## 5. P1-3：Rambachan-Roth / pretrends power 端到端 pipeline

### 5.1 问题

2022 之后 AER 应用计量论文**几乎必做**两件事：
- Roth (2022) pre-trend test power
- Rambachan-Roth (2023) honest DID

《论文解释.md》§5.3 已用论文数字（baseline 0.0380、SE 0.0166、pre-trend max ≈ 0.02）跑出**breakdown $\bar M^* \approx 1.9$**——这是论文应补但**未补**的关键增项。

StatsPAI 工具已经齐了（`sp.pretrends_power`、`sp.sensitivity_rr`、`sp.honest_did_from_result`），但**没有现成 pipeline**，需要用户知道：
1. fit event study 拿到 result_id
2. 调三个工具
3. 自己解释 breakdown $\bar M^*$

### 5.2 修复方向

```python
# 一个端到端 pipeline
sp.parallel_trends_robustness(
    result_id="es_handle",
    m_grid=2 ** np.arange(-3, 4) * 0.01,  # log-grid of M
    families=["SD", "RM"],
)
# 输出：
#   - pre-trend power 表（Roth 2022）
#   - breakdown $\bar M^*$ 表格（RM/SD 各一个）
#   - robust CI 网格
#   - 一句话结论："在 M < 1.9 时结论稳健"
```

### 5.3 价值

- 论文这类 AER 论文评审时**直接拿这张表贴到附录**就能满足"稳健性"要求
- 与 2024-2026 应用计量标准对齐

---

## 6. P2-1：Reference-parity 基准测试

### 6.1 问题

StatsPAI 已有 `validation_status` / `sp.cross_validate` 机制，但**没有标准基准**。撰写《论文模型解读与StatsPAI复现分析.md》时通篇只能写"理论应一致"，无法贴一个具体论文的 parity 测试结果。

### 6.2 修复方向

把本文（《Rebel on the Canal》）作为首个 reference-parity 基准：
- 拿到 openICPSR 复现包
- 跑论文 Table 3 列 1-5，对比 Stata `reghdfe` vs `sp.feols` 输出（容差 1e-6）
- 跑论文 Appendix A5 CIC，对比 Stata `cic` vs `sp.cic`
- 跑论文 Appendix A6 SCM，对比 `synth_runner` vs `sp.staggered_synth`
- 跑 Rambachan-Roth breakdown（论文目前没有这一项），把本文的 ~1.9 作为 StatsPAI 复现验证的"真实目标"

### 6.3 价值

- 长期价值最高：**一个"我们复现过 AER 论文并验证过系数"的声明** 比任何 README 都更有说服力
- 一旦建立，**后续每篇 AER/QJE 复现都可以复用同一个 parity 框架**

---

## 7. P2-2：GIS 前处理（不属于包内，但要教程化）

### 7.1 问题

论文处理强度（运河长度/100 km²、10 km 缓冲区市镇占比、距离）的构造属 geopandas 范畴，**StatsPAI 不应自己造 GIS 轮子**，但**完全缺少教程**——用户每次都得从 0 写 spatial join。

### 7.2 修复方向

1. `docs/examples/CHGIS+geopandas+StatsPAI.md`：从原始 shapefile 到最终 df 的**完整教程**
2. `sp.spatial.utils` 提供薄封装（内部 lazy import geopandas，作为可选依赖）：
   - `line_length_in_polygon(canal_gdf, county_gdf)` → 县内运河长度
   - `share_within_buffer(towns_gdf, canal_gdf, buffer_km=10)` → 10 km 缓冲区市镇占比
   - `distance_to_feature(county_centroids, canal_gdf)` → 县治到运河距离

### 7.3 价值

- 中文用户做"中国历史 GIS 面板"是高频场景（CHGIS + 复旦史地中心 shapefile 几乎是标配）
- 薄封装（不到 200 行）即可让 80% 用户不用关心 geopandas 细节

---

## 8. agent-native 通用缺口（不仅限本文）

撰写两份 doc 时还发现一些**与本文无关但影响 agent 体验**的问题：

### 8.1 工具描述应明确"什么时候用 / 什么时候不用"

现状：很多 `mcp__statspai__*` 工具的 description 写得很长但**没说什么时候不要用**。agent 容易：
- 在 2×2 DID 设定下调用 `sp.callaway_santanna`（无意义但耗时）
- 在 575 县 × 262 年 = 14 万观测下调用 `sp.feols(vce="conley")`（直接 OOM）

→ **建议**：每个工具的 description 模板加上"⚠️ Don't use when ..." 和"memory cost"。

### 8.2 错误消息应可被 agent 恢复

实际遇到：调用 `sp.honest_did` 传 `betas` 直接报错，但错误消息没说明正确的参数名（我得自己试 `result` 才猜到）。

→ **建议**：错误消息模板为"expected argument X, got Y; try {correction_suggestion}"。

### 8.3 工具应可链式组合

现状：调用 `sp.feols` 后用 `result.absorber.keep_mask` 取保留样本，再喂给 `sp.cic`——可行但**要求 agent 记得这个 hack**。

→ **建议**：高阶 pipeline 工具（如 `sp.did_pipeline`、`sp.parallel_trends_robustness`）自动处理 keep_mask 对齐、bootstrap 重抽、单位配对。

### 8.4 应有"replication skill"作为 agent 入口

现状：每篇 AER 论文的复现都需要 agent 自己摸索 5-8 步（下载 → 读 README → 翻译 → parity 检查）。

→ **建议**：建立 `replication-skill.md`，模板化"openICPSR 复现包 → StatsPAI 复现"的标准操作剧本；每篇新论文复用此 skill。

---

## 9. 总结：当前复现 AER 论文的最大瓶颈不是工具不全，而是工具链缝合度

如果按 P0-1 + P0-2 补完，StatsPAI 可以端到端复现本文**所有**的系数、SE 和稳健性检验（含 Rambachan-Roth）。

如果再补 P1-1/2/3，用户**不需要自己写 30-50 行样板代码**即可跑出 2024-2026 AER 标准的全套稳健性。

P2 的两项是**长期价值**：reference-parity 是"我们真的复现过 AER 论文"的硬证据；GIS 教程是中文用户高频场景的入门。

> **不要做的事**：不要为了"完整性"自己造一个 DML/RL/RDD 估计器——现有 `sp.dml`、`sp.rdrobust` 等已经够用。改进应该集中在**接口体验**和**论文级工作流**，不是**估计方法库**。
