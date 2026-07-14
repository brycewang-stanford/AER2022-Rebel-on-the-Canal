# 《Rebel on the Canal》论文模型解读 与 StatsPAI 复现可行性分析

> **论文**：Cao, Yiming and Shuo Chen (2022). "Rebel on the Canal: Disrupted Trade Access and Social Conflict in China, 1650–1911." *American Economic Review*, 112(5): 1555–1590. DOI: [10.1257/aer.20201283](https://doi.org/10.1257/aer.20201283)
>
> **复现包**：openICPSR 项目 157781，DOI: [10.3886/E157781V1](https://doi.org/10.3886/E157781V1)（原始代码为 Stata）
>
> **分析对象**：[StatsPAI](https://github.com/brycewang-stanford/StatsPAI) v1.20.0（基于仓库源码逐模块核查，非仅凭 README）

---

## 目录

1. [论文概览](#一论文概览)
2. [计量模型逐一拆解](#二计量模型逐一拆解)
3. [原论文的 Stata 工具链](#三原论文的-stata-工具链)
4. [StatsPAI 能力对照表](#四statspai-能力对照表)
5. [用 StatsPAI 复现的示例路线](#五用-statspai-复现的示例路线)
6. [差距清单与改进建议（按优先级）](#六差距清单与改进建议按优先级)
7. [总体结论](#七总体结论)

---

## 一、论文概览

### 1.1 研究问题

贸易通道的**丧失**（extensive margin 的负向贸易冲击）是否会引发社会动乱？现有文献几乎全部关注贸易**波动**（intensive margin，如价格、天气冲击），且多为农村场景；本文首次利用一个"永久性、城市部门、国内贸易"的自然实验来回答这一问题。

### 1.2 自然实验与识别来源

- **处理事件**：1826 年清政府因 1825 年黄河决口而试行漕粮海运。这次试验虽然次年即恢复河运，但标志着大运河命运的转折点——海运从此成为可行替代，运河使用量自 1826 年起趋势性下降，1855 年漕运停止，1901 年正式宣布废弃。
- **外生性论证**：1826 年海运试验的动因是成本效率（更快、更省、更省人力），而非既有或预期的叛乱——朝议记录显示恰恰是**反对派**以社会稳定为由反对海运。
- **处理组/控制组**：运河沿线县（575 县中的 73 个"运河县"） vs 远离运河的县。

### 1.3 数据

| 维度 | 内容 |
|---|---|
| 面板结构 | 575 个县 × 262 年（1650–1911），基准回归样本 536 县、140,432 个县-年观测 |
| 因变量 | 每县每年叛乱爆发数 / 1600 年百万人口，再做反双曲正弦（arcsinh/IHS）变换 |
| 叛乱来源 | 《清实录》，共 1,144 起叛乱爆发（只计爆发 onset，剔除既有叛军的蔓延） |
| 处理强度 | ① 沿运河二值指标；② 县内运河长度/100km²；③ 1820 年距运河 10km 内市镇占比；④ 县治到运河的距离 |
| 控制变量 | 土地面积、地形崎岖度、1600 年人口密度、温度异常、旱涝、玉米/番薯引种、稻麦适宜度 |
| GIS 来源 | CHGIS v4 历史 shapefile（哈佛燕京学社 & 复旦史地中心），需空间叠加（spatial join）与邻近分析 |

### 1.4 核心结论

运河废弃后，运河县相对非运河县的叛乱增加约 **117%**（基准系数 0.0380，对应样本均值 0.0330 的 117%），5% 水平显著。效应集中在运河以北（完全断航段）、地理上和经济上更依赖运河的县，并向外扩散至 150km。机制证据指向**贸易通道丧失→城市失业（水手、码头工人）→叛乱与帮会（青帮）形成**，而非国家镇压能力下降。

---

## 二、计量模型逐一拆解

### 2.1 基准 DID（式 1，Table 3）

$$Y_{ct} = \beta \, \text{AlongCanal}_c \times \text{Post}_t + \delta_c + \sigma_t + \chi_{ct} + \varepsilon_{ct}$$

- $Y_{ct}$：IHS 变换后的人均叛乱数；$\text{Post}_t = \mathbf{1}[t \ge 1826]$。
- **固定效应结构（逐列加码，这是复现的难点所在）**：
  - 列 1：县 FE + 年 FE（二维高维 FE，536 × 262）
  - 列 2：+ **前处理期叛乱水平 × 年虚拟变量**（连续变量与 262 个年份虚拟变量的交互）
  - 列 3：+ **省 × 年 FE**（6 省 × 262 年）
  - 列 4：+ **府级线性时间趋势**（prefecture-specific linear trends，即 `i.prefecture#c.year` 型 varying slopes）
  - 列 5：+ **10 个控制变量 × Post** 交互
- **两套标准误**：
  - 圆括号：县级聚类（cluster at county）
  - 方括号：**Conley 空间 HAC 标准误**，空间截断 500km + **时间序列相关 262 年**（即时空两维核函数，Hsiang 2010 实现）
- 稳健性：不同时间窗口（20/100/200/262 年）、不同样本半径（100/150/200km）、府级加总、多种因变量构造（1820 年人口标准化、逐年插值人口、土地面积标准化、不变换原始计数、去掉 IHS）、Conley 带宽网格（距离 50–2000km × 时间 20–262 年）。

### 2.2 事件研究（式 2，Figure 4）

$$Y_{ct} = \sum_{\tau=-50}^{70} \beta_\tau \, \text{AlongCanal}_c \times \text{Decade}_t^\tau + \delta_c + \sigma_t + \chi_{ct} + \varepsilon_{ct}$$

- 相对 1826 年**按十年分组**（decade bins），参照组为 1826 年之前 50 年以上的所有年份（自定义、非单期参照组）。
- 发现"倒 V + 再上升 + 1870 年代后收敛"的动态形态，与运河使用量的 V 形波动互为镜像。

### 2.3 前趋势检验（式 3，Table 2）

限制在 1776–1825 年（改革前 50 年），估计 $\text{AlongCanal}_c \times \text{Year}_t$（处理组 × 连续年份趋势项），系数应为零。四列固定效应结构与基准表平行。

### 2.4 处理强度与空间梯度（式 4–7，Table 4）

- 线性强度：$\text{CanalLength}_c \times \text{Post}_t$（运河长度/100km²）、$\text{CanalTownShare}_c \times \text{Post}_t$（10km 内市镇占比）、$\text{Distance}_c \times \text{Post}_t$（距离梯度，预期为负）。
- 分组强度（式 5、7）：按强度分箱 / 按 25km 距离区间分别估计 $\beta_k$，参照组为 400km 以外的县；发现效应衰减至 **150km**。

### 2.5 Changes-in-Changes（Athey & Imbens 2006，附录图 A5）

- 采用 **Melly & Santangelo (2015) 两步法**：第一步 OLS 把协变量/固定效应的影响 partial out；第二步对**残差**做无条件 CIC，估计整个分布上的**分位数处理效应（QTE）**，bootstrap 标准误。
- 发现效应在左尾（原本平静的县）更大——排除"叛乱多发县对全国性动荡更敏感"的替代解释。

### 2.6 合成控制法（SCM，附录图 A6）

- 遵循 **Cavallo et al. (2013)** 的多处理单元扩展：为**每个运河县**分别构造合成控制，再把个体估计**加总平均**；
- **Donor pool 限制**：只用距运河 150km 以外的非运河县（避免溢出污染，Abadie 2021）；
- 推断：**随机化推断（randomization inference）**——将主效应与 placebo 效应分布比较得 p 值（Galiani & Quistorff 2017 的 `synth_runner` 流程）。

### 2.7 安慰剂与三重交互（Table 5–7）

- **南北分段**（Table 5）：$\text{AlongCanal} \times \text{Post} \times \text{North}$ 三重交互——效应全部来自断航的北段，南段近零。
- **替代交通线安慰剂**（Table 6）：长江、黄河、海岸线、驿道，均无效应。
- **重大历史事件**（Table 7）：剔除鸦片战争/太平天国战区子样本重估；与战区指标的三重交互。

### 2.8 机制检验（附录 Table A4–A7）

- 镇压能力：驻军规模（Soldiers）、府治（PrefectureCapital）三重交互；被攻击/被撤入次数作为 placebo 结果。
- 贸易通道：1820→1911 市镇数量增长对运河强度的回归；驿道可达性三重交互（缓解效应）；运河 × 温度异常 × Post（风险平滑功能消失）。
- 收入冲击类型：粮价回归；稻麦适宜度三重交互（排除农业渠道）;距长江距离子样本（锁定城市失业渠道）；青帮高层成员分布的横截面相关。

---

## 三、原论文的 Stata 工具链

论文脚注 8、11 及参考文献明确了原始实现依赖：

| 功能 | Stata 工具 | 出处 |
|---|---|---|
| 高维固定效应 OLS | `reghdfe` | Correia (2017) |
| Conley 时空标准误 | Hsiang (2010) 提供的 ado（`ols_spatial_HAC` 系） | Conley (1999, 2008); Hsiang (2010) |
| Changes-in-Changes | Melly & Santangelo (2015) 的 `cic` 命令 | Athey & Imbens (2006) |
| 多单元合成控制 + RI | `synth` + `synth_runner` | Abadie et al. (2010); Cavallo et al. (2013); Galiani & Quistorff (2017) |
| GIS 变量构造 | ArcGIS/QGIS 空间叠加 + CHGIS v4 shapefile | Berman (2017) |

openICPSR 复现包目录含 `Program/Adofile` 文件夹（打包了上述 ado 依赖），数据为 `.dta` 格式。**复现包中处理强度等变量应已预构造好**，因此 GIS 步骤对"复现表格"而言是可选项，对"从原始 shapefile 重建变量"才是必需项。

---

## 四、StatsPAI 能力对照表

以下结论基于对 StatsPAI v1.20.0 源码（`src/statspai/`，1,139 个注册函数、87 个子模块）的逐项核查：

| # | 论文需求 | StatsPAI 对应 | 现状 | 结论 |
|---|---|---|---|---|
| 1 | reghdfe 式高维 FE OLS（县 FE + 年 FE，14 万观测） | `sp.feols("y ~ x \| county + year")`（`panel/feols.py`，Rust HDFE 内核） | 支持多维 FE 吸收、singleton 剔除、within R² | ✅ **可复现** |
| 2 | 县级聚类标准误 | `feols(..., cluster="county")`（CR1），另有 CR2/CR3/jackknife/wild bootstrap | 完整 | ✅ **可复现** |
| 3 | 省×年 FE | 手工生成组合列后作为 FE 吸收（`df["prov_year"] = prov + "_" + year`） | 无 `fe1^fe2` 语法糖，但可绕行 | 🟡 **可绕行** |
| 4 | 前处理叛乱 × 年虚拟变量（连续×262 个 dummy） | formula **不支持交互语法**（文档明确"bare column names, no Patsy"），需手工生成 262 列 | 可行但极不 ergonomic；无 fixest `i()` / `var#c.var` | 🟡 **可绕行** |
| 5 | 府级线性时间趋势（varying slopes，`i.pref#c.year`） | `panel/hdfe.py` **不支持斜率吸收**（grep 无 slope/trend 处理）；需手工加约 90 列 `pref_j × year` 连续回归元 | 可行但降速、易错 | 🟡 **可绕行** |
| 6 | 控制变量 × Post（10 列交互） | 手工生成列即可 | 简单 | ✅ 可复现 |
| 7 | IHS（arcsinh）变换 | `np.arcsinh` 一行 | — | ✅ 可复现 |
| 8 | **Conley 时空标准误（500km + 262 年序列相关）** | ① 顶层 `sp.conley()`：cKDTree 稀疏实现但**只有空间维度、且只接 `sp.regress` 结果**；② `feols(vce="conley")`：与 HDFE 集成、匹配 Stata `acreg`，但 `conley_vcov_matrix` 构造**稠密 n×n 距离矩阵**——n=140,432 时约需 **158 GB 内存，不可行**；③ 两者均**无时间滞后/序列相关截断参数** | **论文每张表的第二套标准误都无法计算** | ❌ **不可复现（最大缺口）** |
| 9 | 事件研究（十年分箱 + "前 50 年以上"自定义参照组） | `sp.event_study()`（`did/event_study.py`）：逐期相对时间 dummy、端点归并、单期参照、内置前趋势检验 | 无自定义分箱宽度（decade bins）与多期参照组；可退回 feols + 手工 dummy | 🟡 **可绕行** |
| 10 | 前趋势线性检验（式 3） | feols + 手工 `treat × year` 列 | 简单 | ✅ 可复现 |
| 11 | CIC + QTE + bootstrap | `sp.cic()`（`did/cic.py`）：标准 Athey-Imbens 连续型，QTE 网格、bootstrap SE | **不支持协变量**；但论文用的正是"OLS 残差化→无条件 CIC"两步法，可用 `feols` 残差 + `sp.cic` **精确组合复现** | 🟡 **可组合复现** |
| 12 | 多处理单元 SCM（Cavallo 2013）+ 随机化推断 | `sp.synth()` 统一调度 20 种变体；`staggered_synth(method="separate")` 为每个处理单元分别拟合 + placebo 推断；另有 `synth_loo`、`synth_donor_sensitivity` 等诊断套件 | 无 `synth_runner` 式 RMSPE 过滤/加权聚合的原样流程；donor pool 限制可通过预筛数据实现 | 🟡 **近似可复现**（功能等价，非逐行对齐） |
| 13 | 三重交互 / 安慰剂回归（Table 5–7、A4–A6） | 全部是带交互列的 feols 回归 | 手工造列即可 | ✅ 可复现 |
| 14 | 泊松/负二项稳健性（若附录涉及计数模型） | `fast/fepois.py`（FE Poisson） | 存在 | ✅ 可复现 |
| 15 | GIS 变量构造（spatial join、县内运河长度、10km 缓冲区市镇占比、距离计算） | `spatial/` 模块是**空间计量**（GWR、ESDA、空间权重、Delgado-Florax 空间 DID），**不是地理处理**；仅 2 个文件可选依赖 geopandas | 需要 geopandas/shapely 外部完成；复现包若含预构造变量则不受影响 | ❌ **包外解决** |
| 16 | 出版级表格（对应 outreg2/esttab） | `sp.outreg2()`、`sp.modelsummary()`、`.to_latex()`、`.to_docx()` | 完整 | ✅ 可复现 |
| 17 | 读取 Stata `.dta` | `pandas.read_stata`（生态标准能力） | — | ✅ 可复现 |
| 18 | Stata 代码理解/翻译 | 配套 [`stata-code`](https://github.com/brycewang-stanford/stata-code) 仓库 + agent 工作流 | 对翻译复现包 do 文件有直接价值 | ✅ 辅助 |
| 19 | 与 Stata 结果交叉验证 | `sp.cross_validate` + `validation_status` 元数据 + reference-parity 测试 | 已有机制，但本文场景未被覆盖为基准 | 🟡 建议新增 |

---

## 五、用 StatsPAI 复现的示例路线

假设复现包数据已整理为 `df`（县-年长面板），以下代码勾勒可行部分的复现路径：

```python
import numpy as np
import pandas as pd
import statspai as sp

df = pd.read_stata("data/rebellion_panel.dta")

# ── 因变量与交互项（式 1）──────────────────────────────
df["y"] = np.arcsinh(df["rebellions_pm"])          # IHS 变换
df["post"] = (df["year"] >= 1826).astype(int)
df["canal_post"] = df["along_canal"] * df["post"]

# 省×年 FE：组合成单列即可被吸收
df["prov_year"] = df["province"].astype(str) + "_" + df["year"].astype(str)

# 前处理叛乱 × 年 dummy（262 列，绕行方案）
pre_reb = df.groupby("county")["y"].transform(
    lambda s: s[df.loc[s.index, "year"] < 1826].mean())
year_dummies = pd.get_dummies(df["year"], prefix="yr").iloc[:, 1:]
inter = year_dummies.mul(pre_reb, axis=0)
inter.columns = [c + "_x_prereb" for c in inter.columns]
df = pd.concat([df, inter], axis=1)

# 府级线性趋势（绕行方案：~90 列 pref×year 连续项）
pref_trend = pd.get_dummies(df["prefecture"], prefix="pt").mul(df["year"], axis=0)
df = pd.concat([df, pref_trend], axis=1)

rhs = " + ".join(["canal_post", *inter.columns, *pref_trend.columns])

# ── Table 3 列 4：县 FE + 年 FE + 省×年 FE + 府趋势，县级聚类 SE ──
m4 = sp.feols(f"y ~ {rhs} | county + prov_year", data=df, cluster="county")
print(m4.summary())

# ⚠️ Conley 时空 SE（500km + 262 年）目前无法计算 —— 见第六节 P0 缺口
# m4c = sp.feols(..., vce="conley", conley_lat="lat", conley_lon="lon",
#                conley_cutoff=500)   # ← 稠密 n×n 矩阵，14 万观测会 OOM，
#                                     #    且缺少时间序列相关维度

# ── 事件研究（式 2）：十年分箱需手工 dummy，然后 feols ──
df["decade_rel"] = ((df["year"] - 1826) // 10).clip(-5, 7)
dec = pd.get_dummies(df["decade_rel"], prefix="dec")
dec = dec.drop(columns=["dec_-5"])                 # 参照组：50 年以上之前
dec = dec.mul(df["along_canal"], axis=0)
df = pd.concat([df, dec], axis=1)
es = sp.feols(f"y ~ {' + '.join(dec.columns)} | county + prov_year",
              data=df, cluster="county")

# ── CIC（两步法，精确对应论文附录图 A5）─────────────────
step1 = sp.feols(f"y ~ {' + '.join(inter.columns)} | county + prov_year",
                 data=df, cluster="county")
df_cic = df.loc[step1.absorber.keep_mask].copy()
df_cic["resid"] = step1.residuals
cic_res = sp.cic(df_cic, y="resid", group="along_canal", time="post",
                 quantiles=[0.1, 0.25, 0.5, 0.75, 0.9], n_boot=500)
cic_res.plot()

# ── SCM（Cavallo 式多处理单元 + placebo 推断）────────────
donor_ok = (df["along_canal"] == 0) & (df["dist_canal"] > 150)
scm_df = df[donor_ok | (df["along_canal"] == 1)]
scm = sp.staggered_synth(scm_df, outcome="y", unit="county", time="year",
                         treatment="canal_post", method="separate",
                         placebo=True)

# ── 表格导出 ──────────────────────────────────────────
sp.outreg2([m1, m2, m3, m4, m5], file="table3.tex")
```

**能跑通的**：基准 DID 五列的点估计与县级聚类 SE、前趋势检验、处理强度/距离梯度、南北与安慰剂三重交互、CIC 两步组合、SCM 变体、事件研究（手工分箱）、全部表格导出。
**跑不通的**：所有表格里方括号中的 Conley 时空标准误（论文的第二套推断）；从 CHGIS shapefile 重建处理强度变量。

---

## 六、差距清单与改进建议（按优先级）

### P0 —— 决定"能否宣称完整复现"的硬缺口

**1. Conley 时空 HAC 标准误（spatio-temporal，Hsiang 2010 风格）**

- **现状**：
  - `inference/conley.py` 的 `sp.conley()`：cKDTree 稀疏、可扩展，但只做**纯空间**核，且只接受 `sp.regress` 的结果对象；
  - `feols(vce="conley")` → `inference/jackknife.py::conley_vcov_matrix`：与 HDFE 集成、对齐 Stata `acreg`，但构造 **n×n 稠密距离矩阵**（`lat_v[:, None] - lat_v[None, :]`），n=140,432 时内存约 158 GB，直接 OOM；
  - 两条路径都**没有时间维度参数**——论文要求"500km 空间截断 + 262 年序列相关"，还要做 6×4=24 组带宽网格的稳健性图（附录图 A2）。
- **建议**：
  1. 给 `feols(vce="conley")` 增加 `conley_lag_cutoff=`（时间滞后截断）与 `kernel=("uniform"|"bartlett")`，按 Hsiang (2010) 的做法：同期跨单位用空间核，同单位跨期用时间核（面板去重后每个单位坐标只算一次）；
  2. 把稠密实现替换为 cKDTree 邻对枚举（顶层 `sp.conley` 已有现成代码可复用），按 (unit, time) 分块累加 meat 矩阵，内存降到 O(邻对数)；
  3. 面板场景下坐标应按 **unit 去重**（575 个县）建树，而不是对 14 万行两两算距离——这是数量级差异的关键。
- **价值**：Conley SE 是历史/政治经济学论文（用 CHGIS、GIS 面板的整个文献族）的标配，修复后 StatsPAI 可以覆盖这一大类 AER/QJE 复现场景。

**2. formula 语法：交互项与 varying slopes**

- **现状**：`feols` 的 formula 只接受裸列名（无 `x1:x2`、无 `i.factor#c.var`、无 `fe1^fe2`、无 fixest 的 `i()`）；HDFE 内核不支持斜率吸收（prefecture-specific trends）。本文列 2/列 4 各需手工造 262 列和约 90 列。
- **建议**：
  1. formula 解析器支持 `a:b` 与 `a*b`（自动展开）、FE 侧支持 `province^year`（组合 FE）与 `prefecture[year]`（varying slopes，fixest 语法）；
  2. HDFE 吸收器（`panel/hdfe.py` / Rust 内核）增加连续斜率投影（demeaning 推广为组内回归残差化），使 `i.pref#c.year` 被吸收而非进入显式回归元。
- **价值**：这是 `reghdfe`/`fixest` 用户迁移的第一痛点；本文五列规格里有三列离不开它。

### P1 —— 影响"复现的忠实度与便利性"

**3. CIC 支持协变量（内置 Melly-Santangelo 两步法）**

- **现状**：`sp.cic()` 仅无条件版本。论文用的两步法目前可以手工组合（feols 残差 → cic），结果等价，但样板代码多、容易在样本对齐（singleton 剔除后的 `keep_mask`）上出错。
- **建议**：增加 `sp.cic(..., covariates=[...], first_stage="ols")` 一步式接口，内部完成残差化、样本对齐与 bootstrap（bootstrap 应重抽原始数据、两步一起重估，而不是只对第二步 bootstrap——这是当前手工组合方案在推断上的隐患）。

**4. `synth_runner` 式多处理单元 SCM 流程**

- **现状**：`staggered_synth(method="separate")` + placebo 推断在功能上接近 Cavallo et al. (2013)，但缺少：donor pool 显式排除参数（目前靠预筛数据）、RMSPE 比率过滤与加权聚合、逐期随机化推断 p 值序列（论文附录图 A6b 逐年 p 值）。
- **建议**：提供 `sp.synth_runner(...)` 兼容层：`exclude_donors=`、`agg="mean"|"rmspe_weighted"`、输出逐期 placebo p 值 DataFrame，便于直接画出论文式的 gap + p 值双图。

**5. 事件研究的自定义分箱与多期参照组**

- **现状**：`event_study()` 固定为逐期 dummy + 单期参照 + 端点归并。本文需要十年分箱、参照组为"处理前 50 年以上"的整段。
- **建议**：增加 `bin_width=10`（或 `bins=[...]` 自定义切点）与 `ref_period=("<=", -50)` 区间式参照组；顺带把 `pretrends`（Roth 检验，包内已有 `did/pretrends.py`）接进结果对象。

### P2 —— 生态与工作流层面

**6. GIS 前处理不在包内，建议文档化标准配方**

- 县内运河长度、10km 缓冲区市镇占比、县治到运河距离都是 geopandas 十几行的操作（`gpd.overlay`、`buffer`、`distance`）。不建议 StatsPAI 自己造 GIS 轮子，但建议：
  1. 在文档/examples 里加一篇"CHGIS + geopandas → StatsPAI"的教程（历史中国经济史是中文用户高频场景）；
  2. 提供 `sp.spatial.utils.line_length_in_polygon()`、`share_within_buffer()` 这类薄封装（内部 import geopandas，作为可选依赖）。

**7. 把本文纳入 reference-parity 基准**

- StatsPAI 已有 `validation_status`/`sp.cross_validate` 机制。建议在拿到 openICPSR 复现包后，把 Table 3 列 1–5 的系数与县级聚类 SE 做成 parity 测试用例（Stata `reghdfe` vs `sp.feols`，容差 1e-6），并把（修复后的）Conley SE 与 Hsiang ado 的输出对齐——这会成为 StatsPAI"能复现 AER 论文"的直接证据。

**8. `.dta`/do 文件工作流**

- 复现包是 Stata 代码 + ado 依赖。配套的 `stata-code` 仓库 + agent 翻译流程适合把 `Program/` 下的 do 文件半自动翻译为 StatsPAI 脚本；建议在 `StatsPAI_full_data_analysis_skill` 中加入"AEA openICPSR 复现包"的标准操作剧本（下载→读 README→翻译→parity 检查）。

---

## 七、总体结论

**StatsPAI 目前能复现这篇论文的大部分点估计，但不能复现它的全部推断（inference）**：

- ✅ **可直接或组合复现（约占论文结果的 70–80%）**：基准 DID 全部五列的系数与县级聚类标准误、前趋势检验、处理强度与空间梯度、南北/替代路线/战争安慰剂的全部三重交互回归、CIC 分位数处理效应（两步组合）、多处理单元合成控制（功能等价变体）、FE Poisson 稳健性、出版级表格导出。
- ❌ **当前不可复现的两个缺口**：
  1. **Conley 时空标准误**（每张表的方括号 SE + 附录 A2 的 24 组带宽稳健性）——现有实现既缺时间维度，又在 14 万观测下内存不可行。这是唯一真正"硬"的计量缺口，也是修复价值最大的一项（P0-1）；
  2. **GIS 变量构造**——不属于计量包的职责，用 geopandas 补齐即可，若复现包提供预构造变量则完全不影响复现表格。
- 🟡 **体验层面的主要摩擦**：formula 不支持交互与 varying slopes 吸收（P0-2），导致本文这类"高维 FE + 大量交互"的规格需要几百列手工构造——能算对，但离 `reghdfe` 一行公式的体验还有距离。

一句话总结：**补上"时空 Conley + formula 交互/斜率吸收"这两块拼图，StatsPAI 就能端到端复现这篇 AER；在那之前，它可以复现论文的全部因果结论，但复现不了论文的第二套标准误。**

---

*本文档由 Claude Code 基于仓库内论文 PDF 全文与 StatsPAI v1.20.0 源码逐模块核查后撰写（2026-07）。openICPSR 复现包（157781-V1）因需登录下载，尚未纳入仓库；拿到后可按第六节第 7 条建立 parity 测试。*
