
> **作者：** 林芷涵 (首都经济贸易大学)
> **邮箱：** [zhihan_lin0211@163.com](mailto:zhihan_lin0211@163.com)

&emsp; 

* **分类**：倍分法 DID
* **Title**: StatsPAI：交叠 DID 方法太多，实证时到底怎么选？
* **Keywords**: 双重差分法，交叠 DID，渐进 DID, Staggered DID, 交错 DID, 异质性处理效应，因果推断，Bacon 分解, Callaway-Sant'Anna 方法，Sun-Abraham 方法，Borusyak-Jaravel-Spiess 方法，平行趋势假设，稳健估计量，csdid, drdid, StatsPAI 包

---

<div style="background-color:#f6f9ff; border-left:6px solid #2f5f9f; padding:18px 20px; margin:24px 0; border-radius:8px;">

<p style="margin-top:0; font-size:17px;"><strong>导读</strong></p>

<p>交叠 DID 已经成为政策评估中的常见场景：不同地区、企业或个人并不是在同一年受到政策影响，而是分批进入处理状态。问题在于，传统双向固定效应模型在处理效应存在异质性时，可能把早处理组、晚处理组和已处理组放在一起做不合适的比较，进而产生难以解释的加权结果。</p>

<p style="margin-bottom:0;">本文不试图完整综述所有交叠 DID 文献，而是围绕一个更实际的问题展开：实证研究中到底应该如何选择估计方法？文章先说明 Bacon 分解、Callaway-Sant'Anna、Sun-Abraham、Borusyak-Jaravel-Spiess 和 de Chaisemartin-D'Haultfœuille 方法分别适合什么场景，再以 Python 工具包 <code>StatsPAI</code> 为例，展示一套从数据诊断、主估计、动态效应到结果报告的最小可复现流程。</p>

</div>

## 1. 交叠 DID 不能只报告 TWFE 的结果

DID 的基本想法并不复杂：如果某项政策只影响一部分样本，那么可以比较处理组和对照组在政策前后的变化差异。麻烦出现在更常见的多期场景中：政策不是一次性覆盖所有处理组，而是分批实施。

例如：

* 某项环保政策在 2013 年先覆盖第一批城市，2015 年覆盖第二批城市，2017 年覆盖第三批城市；
* 某项产业政策分年度扩围，不同企业进入政策名单的年份不同；
* 某项金融改革先在试点地区推行，随后逐步扩展到其他地区。

这类数据结构通常被称为 **交叠 DID** (staggered DID)，也常被称为交错 DID、渐进 DID 或多时点 DID。设 $E_{i}$ 表示个体 $i$ 首次接受处理的时间，处理变量可以写为：

$$
D_{it}=\mathbb{1}\{t\geq E_{i}\}
$$

其中，$D_{it}=1$ 表示个体 $i$ 在 $t$ 期已经处于处理状态。若不同个体的 $E_{i}$ 不同，就形成交叠处理时点。

传统 TWFE 模型通常写为：

$$
Y_{it}=\alpha_{i}+\lambda_{t}+\beta D_{it}+\varepsilon_{it}
$$

其中，$\alpha_{i}$ 是个体固定效应，$\lambda_{t}$ 是时间固定效应，$\beta$ 被解释为平均处理效应。这个模型的问题在于，它隐含了较强的处理效应同质性假设。如果不同批次处理组的政策效应不同，或者政策效应随处理后时间逐渐变化，那么一个单一的 $\beta$ 往往无法清楚回答研究问题。

![](https://fig-lianxh.oss-cn-shenzhen.aliyuncs.com/%E6%9E%97%E8%8A%B7%E6%B6%B5_StatsPAI_Fig04.png)

> 图 1：交叠 DID 数据结构与 TWFE 比较逻辑

Goodman-Bacon (2021) 的分解结果说明，交叠处理时点下的 TWFE 估计量可以理解为许多 2×2 DID 比较的加权平均：

$$
\hat{\beta}_{\operatorname{TWFE}}=\sum_{k}w_{k}\hat{\beta}_{k}^{2\times 2}
$$

其中，$\hat{\beta}_{k}^{2\times 2}$ 表示某一个局部 2×2 DID 比较，$w_{k}$ 表示对应权重。问题不在于「分解」本身，而在于某些比较并不符合直觉。例如，较晚接受处理的组在早期可以作为对照组；但较早接受处理的组在后期已经受到政策影响，若再被用作较晚处理组的对照，就会形成所谓的 forbidden comparison。

因此，在交叠 DID 中，TWFE 可以作为一个参照结果，但不宜机械地作为唯一主估计。实证论文通常还需要说明：对照组来自哪里，估计对象是什么，处理效应是否允许随组别和时间变化。

## 2. 先看数据结构，再选估计方法

方法选择不应从「哪个估计量更流行」开始，而应从数据结构和研究目标开始。交叠 DID 至少要先回答五个问题：

* 处理是否为吸收状态，即一旦处理后是否持续处理？
* 样本中是否存在从未处理组 (never-treated group)？
* 是否可以使用尚未处理组 (not-yet-treated group) 作为对照？
* 研究重点是总体平均效应，还是动态事件研究效应？
* 是否需要控制协变量，且希望使用双重稳健估计？

![](https://fig-lianxh.oss-cn-shenzhen.aliyuncs.com/%E6%9E%97%E8%8A%B7%E6%B6%B5_StatsPAI_Fig05.png)

> 图 2：交叠 DID 方法选择决策树

更实用的选择逻辑可以概括为下表。

| 研究者面对的问题               | 更合适的起点                        | 解释                                                 |
| ------------------------------ | ----------------------------------- | ---------------------------------------------------- |
| 只是想知道 TWFE 是否可能有问题 | Bacon 分解                          | 诊断 TWFE 中不同 2×2 比较的来源和权重结构            |
| 希望估计总体平均处理效应       | CS 或 BJS                           | 二者都允许处理效应异质性，适合作为主估计或稳健性估计 |
| 希望画事件研究图               | SA、CS 动态聚合或 BJS 动态估计      | 不要直接使用传统 TWFE leads and lags                 |
| 样本中有从未处理组             | CS、SA、BJS 均可考虑                | never-treated 通常是更直观的多用的对照组                   |
| 样本中没有从未处理组           | CS 使用 not-yet-treated，或考虑 BJS | 需要检查后期是否仍有足够未处理观测                   |
| 处理状态可能反复切换           | dCDH / did_multiplegt               | 传统 CS、SA、BJS 通常默认处理状态吸收                |
| 担心平行趋势只是近似成立       | Rambachan-Roth / HonestDID          | 用敏感性分析替代「一检验通过就放心」的做法           |

这个表的含义不是让研究者每篇论文都跑所有方法，而是强调估计量要服务于研究设计。若政策确实是分批进入、处理后持续生效、且研究目标是平均处理效应，那么 CS 或 BJS 可以作为自然起点；若论文重点是政策效果的动态变化，则需要重点报告事件时间上的处理效应曲线；若政策有退出、撤销或反复进入，则应考虑允许处理状态切换的方法。

## 3. 几类方法分别解决什么问题？

### 3.1 Bacon 分解：先诊断 TWFE 比较结构

Bacon 分解不是一个新的主估计量，而是一个诊断工具。它告诉我们，TWFE 的结果由哪些局部 DID 比较构成，以及每类比较占多大权重。

在交叠 DID 中，比较大致包括三类：

* 早处理组 vs 从未处理组；
* 晚处理组 vs 从未处理组；
* 早处理组 vs 晚处理组，或晚处理组 vs 已处理组。

第三类比较最容易出问题。因为已经处理过的组不再是干净的反事实。如果政策效应具有动态变化，或者早晚处理组效应大小不同，这类比较会污染 TWFE 系数。

![](https://fig-lianxh.oss-cn-shenzhen.aliyuncs.com/%E6%9E%97%E8%8A%B7%E6%B6%B5_StatsPAI_Fig06.png)

> 图 3：Goodman-Bacon 分解逻辑与问题比较

### 3.2 Callaway-Sant'Anna 方法：先估计组别-时期 ATT

Callaway and Sant'Anna (2021) 的核心思想是：不要一开始就估计一个总的 $\beta$，而是先估计每个处理组在每个时期的处理效应。其基本估计对象为：

$$
\operatorname{ATT}(g,t)=E\left[Y_{it}(g)-Y_{it}(0)\mid G_{i}=g\right]
$$

其中，$G_{i}=g$ 表示个体 $i$ 属于第 $g$ 批处理组，$\operatorname{ATT}(g,t)$ 表示第 $g$ 批处理组在 $t$ 期的平均处理效应。

这个设定有两个好处。其一，它允许不同批次的处理效应不同；其二，它允许处理效应随政策实施后的时间变化。估计完 $\operatorname{ATT}(g,t)$ 之后，研究者可以根据研究目标进行聚合，例如总体平均效应、按日历时间聚合、按处理组聚合或按事件时间聚合。

CS 方法的另一个优势是可以纳入协变量，并支持回归调整、逆概率加权和双重稳健估计。实证写作中不必展开所有半参数公式，但要说明三个细节：使用 never-treated 还是 not-yet-treated 作为对照组，是否控制协变量，以及最终报告哪一种聚合效应。

### 3.3 Sun-Abraham 方法：为事件研究服务

传统事件研究通常在 TWFE 模型中加入政策前后的 leads and lags。然而 Sun and Abraham (2021) 指出，在交叠处理时点和异质性处理效应下，传统事件研究系数可能被其他时期的处理效应污染，甚至会出现表面上的 pretrend。

SA 方法的基本思路是构造 cohort-specific 的事件时间虚拟变量，再进行交互加权聚合。可写为：

$$
Y_{it}=\alpha_{i}+\lambda_{t}+\sum_{g}\sum_{e\neq -1}\beta_{g,e}\mathbb{1}\{G_{i}=g\}\mathbb{1}\{t-g=e\}+\varepsilon_{it}
$$

其中，$e=t-g$ 是事件时间，通常省略 $e=-1$ 作为基准期。SA 方法适合回答「政策实施后第 0 年、第 1 年、第 2 年的效应如何变化」这类问题。

需要说明的是，SA 不是唯一能做动态效应的方法。CS 的动态聚合和 BJS 的事件研究估计也可以服务于类似目标。实证中更稳妥的做法是：把 SA 作为动态效应的主要展示之一，同时用 CS 或 BJS 进行对照。

### 3.4 Borusyak-Jaravel-Spiess 方法：用未处理样本插补反事实

Borusyak, Jaravel and Spiess (2024) 提出的插补法思路很直观：先用未处理观测估计没有政策时的结果路径，再把这个模型外推到已处理观测，得到反事实结果。

基本逻辑可以写成：

$$
\hat{\tau}_{it}=Y_{it}-\hat{Y}_{it}^{0}
$$

其中，$Y_{it}$ 是实际观测结果，$\hat{Y}_{it}^{0}$ 是在未处理状态下的预测结果。BJS 方法尤其适合研究者希望构造清晰反事实路径的场景。它的解释也比较自然：政策效应就是实际结果与预测反事实之间的差额。

### 3.5 de Chaisemartin-D'Haultfœuille 方法：处理状态可以切换时使用

前面几类方法通常默认处理状态是吸收的，即一个个体一旦接受处理，之后一直处于处理状态。但一些政策或制度安排并不满足这个条件。例如：

* 企业进入补贴名单后又退出；
* 地区某年实施限购政策，之后政策取消或调整；
* 企业某些年份受到监管约束，某些年份又不再受到约束。

这时，处理变量不是单调上升的。de Chaisemartin and D'Haultfœuille (2020) 及后续 `did_multiplegt` 路线更适合这类「处理状态可切换」的场景。它的核心不是比较「已处理组」和「未处理组」，而是利用处理状态发生变化的样本进行识别。

### 3.6 平行趋势：不要只把事件研究图当作形式检验

所有 DID 方法都依赖某种平行趋势假设。一般可写为：

$$
E\left[Y_{it}(0)-Y_{is}(0)\mid G_{i}=g\right]=E\left[Y_{it}(0)-Y_{is}(0)\mid C_{i}=1\right]
$$

其中，$C_{i}=1$ 表示被用作对照的样本。这个公式的含义是：如果没有政策，处理组和对照组在结果变量上的变化趋势应当相同。

事件研究图可以帮助观察处理前趋势，但不能真正证明平行趋势成立。更稳妥的表述是：处理前系数没有明显系统性偏离，支持平行趋势假设；同时，研究者还应从政策背景、样本构造、协变量平衡和安慰剂检验等方面说明识别假设的合理性。

如果担心平行趋势只是近似成立，可以进一步考虑 Rambachan and Roth (2023) 的敏感性分析思路，即允许平行趋势存在一定偏离，并考察结论在多大偏离范围内仍然稳健。

## 4. 用 StatsPAI 跑通一套最小可复现流程

`StatsPAI` 是一个快速迭代中的 Python 因果推断与应用计量工具包，试图把 DID、RD、SCM、DML 等方法放在统一接口下。本文只使用其中的交叠 DID 相关函数，展示一套最小可复现流程。

为增强可读性，下面在关键代码后加入示例输出和结果图。图形和输出样式来自原稿 v1，但数据生成过程沿用本文修正后的设定：保留真正的 never-treated 组，避免把最后一批处理组误写为从未处理组。因此，读者本地运行时，具体数值可能随 `StatsPAI` 版本和随机数实现略有差异。

需要说明的是，`StatsPAI` 仍处于快速迭代阶段。读者复现本文示例时，建议固定版本，并在论文或附录中报告 Python 版本、`StatsPAI` 版本和主要函数名称。

### 4.1 安装与版本检查

本文示例基于 `StatsPAI==1.16.0` 编写。若后续版本更新导致函数参数变化，请以实际安装版本的帮助文件为准。

```bash
pip install "StatsPAI==1.16.0"
```

安装后，可以先检查版本和主要函数是否存在。

```python
# 导入 StatsPAI
import statspai as sp

# 查看当前安装版本
print(sp.__version__)

# 检查本文会用到的 DID 函数
for fname in [
    "bacon_decomposition",
    "callaway_santanna",
    "sun_abraham",
    "did_imputation",
    "did_multiplegt",
    "aggte",
    "cs_report"
]:
    print(fname, hasattr(sp, fname))
```

### 4.2 构造模拟数据

下面构造一个交叠 DID 数据。设定中有 800 个个体、10 个年份，处理组分别在 2013-2017 年进入处理状态，同时保留一部分真正的 never-treated 组。这样可以避免把最后一批处理组误当作从未处理组。

```python
import numpy as np
import pandas as pd
import statspai as sp

# 固定随机种子，保证结果可复现
np.random.seed(20260530)

# 基本参数
n_units = 800
years = np.arange(2010, 2020)

# 0 表示 never-treated，其余数值表示首次处理年份
cohorts = np.array([0, 2013, 2014, 2015, 2016, 2017])
probs = np.array([0.20, 0.16, 0.16, 0.16, 0.16, 0.16])

# 为每个个体分配首次处理年份
group_assignment = np.random.choice(cohorts, size=n_units, p=probs)

# 个体层面协变量
X1 = np.random.normal(0, 1, n_units)
X2 = np.random.normal(0, 1, n_units)

data_list = []

for i, g in enumerate(group_assignment):

    # 个体固定效应：允许与协变量相关
    alpha_i = np.random.normal(0, 0.7) + 0.2 * X1[i]

    for t in years:

        # treatment = 1 表示该期已经进入处理状态
        D = int(g != 0 and t >= g)

        # 事件时间：仅对处理组定义
        event_time = t - g if g != 0 else np.nan

        # 真实处理效应：早处理组效应略大，且处理后逐步上升
        tau = 0.0
        if D == 1:
            tau = 0.8 + 0.25 * event_time + 0.12 * (2017 - g)

        # 共同时间趋势和随机扰动项
        lambda_t = 0.15 * (t - 2010) + 0.02 * (t - 2010) ** 2 / 10
        eps = np.random.normal(0, 0.8)

        # 结果变量
        Y = 5 + alpha_i + lambda_t + 0.4 * X1[i] - 0.2 * X2[i] + tau + eps

        data_list.append({
            "unit_id": i,
            "year": t,
            "first_treat_year": g,
            "treatment": D,
            "event_time": event_time,
            "Y": Y,
            "X1": X1[i],
            "X2": X2[i]
        })

df = pd.DataFrame(data_list)

print("样本量：", len(df))
print("个体数：", df["unit_id"].nunique())
print("时期数：", df["year"].nunique())

print("\n按个体统计的首次处理年份分布：")
print(
    df.drop_duplicates("unit_id")["first_treat_year"]
      .value_counts()
      .sort_index()
)

print("\n各年份处理状态分布：")
print(
    df.groupby(["year", "treatment"])["unit_id"]
      .count()
      .unstack(fill_value=0)
)
```

**运行结果示例：**

```text
样本量： 8000
个体数： 800
时期数： 10

按个体统计的首次处理年份分布：
first_treat_year
0       156
2013    123
2014    118
2015    117
2016    136
2017    150
Name: count, dtype: int64

各年份处理状态分布：
treatment    0    1
year
2010       800    0
2011       800    0
2012       800    0
2013       677  123
2014       559  241
2015       442  358
2016       306  494
2017       156  644
2018       156  644
2019       156  644
```

从这个输出可以看到，样本中保留了 156 个 never-treated 个体；到 2017 年以后，仍有 156 个个体没有进入处理状态。这一点很关键，因为后续使用 never-treated 作为对照组时，对照组是真正没有接受处理的样本，而不是最后一批处理组。

这段代码有两个目的。其一，构造一个真正包含 never-treated 组的交叠 DID 数据；其二，让处理效应同时具有批次异质性和动态异质性。这样，传统 TWFE 就不再是一个干净的平均处理效应估计量。

### 4.3 Bacon 分解：查看 TWFE 的比较结构

先用 Bacon 分解诊断 TWFE 估计量的来源。这里的重点不是把 Bacon 分解作为主结果，而是观察 TWFE 是否混入了较多不合适的比较。

```python
# Bacon 分解：诊断 TWFE 中不同 2×2 DID 比较的来源
bacon = sp.bacon_decomposition(
    data=df,
    y="Y",
    treat="treatment",
    time="year",
    id="unit_id"
)

print("TWFE 估计量：", round(bacon["beta_twfe"], 4))
print("比较数量：", bacon["n_comparisons"])
print("问题比较占比：", round(bacon.get("negative_weight_share", np.nan), 4))

# 查看分解结果前几行
print(
    bacon["decomposition"]
      .head(10)
)
```

**运行结果示例：**

```text
Bacon 分解结果：
TWFE 估计量：1.2366
比较数量：25
问题比较占比：0.3908

分解详情：
                    type  treated control  estimate   weight
Earlier vs Later treated   2013.0  2014.0  0.429909 0.033513
Later vs Already-treated   2014.0  2013.0  0.012326 0.038301
Earlier vs Later treated   2013.0  2015.0  0.939714 0.033374
Later vs Already-treated   2015.0  2013.0 -0.165557 0.039731
...
```

这个结果的阅读重点不是某一个局部 DID 的数值，而是比较类型和权重结构。若 `Later vs Already-treated` 或类似问题比较占比较高，说明 TWFE 混入了已经处理组作为对照组的比较，主结果应转向更稳健的交叠 DID 估计量。

运行后，重点看 `decomposition` 表中的三列：

* `type`：局部 DID 比较类型；
* `estimate`：该局部比较对应的 DID 估计值；
* `weight`：该比较在 TWFE 中的权重。

如果 `Later vs Already-treated` 这类比较占比较高，说明 TWFE 明显使用了已经接受处理的组作为对照组。此时，TWFE 结果只能作为参照，不宜作为主结论。

### 4.4 Callaway-Sant'Anna：估计组别-时期 ATT

接下来使用 CS 方法。这里明确使用 never-treated 作为对照组，并控制两个协变量 `X1` 和 `X2`。估计器设定为双重稳健 (`estimator="dr"`)。

```python
# Callaway-Sant'Anna 估计
cs = sp.callaway_santanna(
    data=df,
    y="Y",
    g="first_treat_year",
    t="year",
    i="unit_id",
    x=["X1", "X2"],
    estimator="dr",
    control_group="nevertreated"
)

print(cs)

# 提取主要估计结果
print("Overall ATT：", round(cs.estimate, 4))
print("SE：", round(cs.se, 4))
print("95% CI：", tuple(round(v, 4) for v in cs.ci))

# 平行趋势检验
cs_pretrend = cs.pretrend_test()
print(
    f"平行趋势检验：chi2({cs_pretrend['df']}) = "
    f"{cs_pretrend['statistic']:.4f}, p-value = {cs_pretrend['pvalue']:.4f}"
)

# 生成动态效应图
cs.event_study_plot()
# 或
cs.plot()
```

**运行结果示例：**

```text
Callaway-Sant'Anna 估计

整体平均处理效应 (Overall ATT)：1.6338
标准误 (SE)：0.0505
95% 置信区间：[1.5348, 1.7327]
平行趋势检验：chi2(20) = 19.0886, p-value = 0.5161

事件研究系数范围：e = -7 到 e = 6，其中 e = -1 为基准期。
```

![](https://fig-lianxh.oss-cn-shenzhen.aliyuncs.com/%E6%9E%97%E8%8A%B7%E6%B6%B5_StatsPAIv4_Fig01.png)

> 图 4：Callaway-Sant'Anna 方法的动态效应展示

从展示效果看，CS 方法的优势在于可以把总体 ATT 和事件时间 ATT 放在同一套框架下理解。总体 ATT 给出平均效应，动态图则帮助读者判断政策效应是在处理当期一次性出现，还是在处理后逐步累积。

这部分结果可以分两层解读。总体平均处理效应用来回答「政策平均而言是否有效」；组别-时期 ATT 或事件时间 ATT 用来回答「哪一批处理组、政策实施后第几年，效应更强」。

```python
# 输出整洁格式结果
cs_tidy = cs.tidy()

# 查看事件研究结果
print(
    cs_tidy[cs_tidy["type"] == "event_study"]
      .head(15)
)

# 查看组别-时期 ATT 结果
print(
    cs_tidy[cs_tidy["type"] == "group_time"]
      .head(15)
)
```

论文中通常不需要展示完整的 $\operatorname{ATT}(g,t)$ 矩阵，但应在附录或复现代码中保留。正文更适合报告总体平均效应、动态效应图和主要稳健性检验。

### 4.5 Sun-Abraham：关注动态效应曲线

如果论文重点是政策效应的动态变化，可以使用 SA 方法估计事件时间系数。

```python
# Sun-Abraham 事件研究估计
sa = sp.sun_abraham(
    data=df,
    y="Y",
    g="first_treat_year",
    t="year",
    i="unit_id",
    control_group="nevertreated"
)

print(sa)

print("Overall ATT：", round(sa.estimate, 4))
print("SE：", round(sa.se, 4))
print("95% CI：", tuple(round(v, 4) for v in sa.ci))

# 生成事件研究图
sa.event_study_plot()
# 或
sa.plot()
```

**运行结果示例：**

```text
Sun-Abraham 估计

整体平均处理效应 (Overall ATT)：1.8650
标准误 (SE)：0.0589
95% 置信区间：[1.7496, 1.9805]

事件研究系数范围：e = -7 到 e = 6，其中 e = -1 为基准期。
```

![](https://fig-lianxh.oss-cn-shenzhen.aliyuncs.com/%E6%9E%97%E8%8A%B7%E6%B6%B5_StatsPAIv4_Fig02.png)

> 图 5：Sun-Abraham 方法的事件研究结果展示

SA 方法最适合用于展示动态效应图。结果解读时应重点看三点：处理前系数是否接近 0，处理当期是否出现跳变，处理后效应是否持续上升或逐渐衰减。

```python
# 生成事件研究图
# 不同版本的 StatsPAI 返回对象方法可能略有差异
sa.plot()
# 或
sa.event_study_plot()
```

需要说明的是，CS 和 SA 报告的总体 ATT 不一定完全相同。这不是错误，而是因为二者的估计对象、权重和聚合方式并不完全一致。实证写作时应解释差异来自哪里，而不是机械追求所有方法数值完全一致。

### 4.6 Borusyak-Jaravel-Spiess：用插补法构造反事实

BJS 方法适合把「反事实预测」讲清楚。它先用未处理观测拟合潜在结果模型，再将其外推到处理组，得到政策效应。

```python
# 根据数据推断完整事件时间范围，并剔除基准期 e = -1
rel_time = (
    df.loc[df["first_treat_year"] > 0, "year"]
    - df.loc[df["first_treat_year"] > 0, "first_treat_year"]
)
event_min = int(rel_time.min())
event_max = int(rel_time.max())
bjs_horizon = [e for e in range(event_min, event_max + 1) if e != -1]
print(f"事件研究系数范围：e = {event_min} 到 e = {event_max}，其中 e = -1 为基准期。")

# Borusyak-Jaravel-Spiess 插补估计
bjs = sp.did_imputation(
    data=df,
    y="Y",
    group="unit_id",
    time="year",
    first_treat="first_treat_year",
    controls=["X1", "X2"],
    horizon=bjs_horizon
)

print(bjs)

print("Overall ATT：", round(bjs.estimate, 4))
print("SE：", round(bjs.se, 4))
print("95% CI：", tuple(round(v, 4) for v in bjs.ci))
bjs_pretrend = bjs.pretrend_test()
print(
    f"平行趋势检验：chi2({bjs_pretrend['df']}) = "
    f"{bjs_pretrend['statistic']:.4f}, p-value = {bjs_pretrend['pvalue']:.4f}"
)

# 生成插补法事件研究图
bjs.event_study_plot()
# 或
bjs.plot()
```

**运行结果示例：**

```text
Borusyak-Jaravel-Spiess 估计

整体平均处理效应 (Overall ATT)：1.6666
标准误 (SE)：0.0314
95% 置信区间：[1.6050, 1.7282]
平行趋势检验：chi2(6) = 4.8618, p-value = 0.5617

事件研究系数范围：e = -7 到 e = 6，其中 e = -1 为基准期。
```
![](https://fig-lianxh.oss-cn-shenzhen.aliyuncs.com/%E6%9E%97%E8%8A%B7%E6%B6%B5_StatsPAIv4_Fig03.png)

> 图 6：Borusyak-Jaravel-Spiess 插补法估计结果展示

BJS 的解释方式比较直观：先预测没有政策时处理组本应如何变化，再把实际结果与预测反事实相减。若 BJS 和 CS 的估计方向一致，通常可以增强结果的说服力；若二者差异较大，则需要检查对照组选择、事件窗口、控制变量和样本支持区间。

### 4.7 dCDH / did_multiplegt：处理状态可切换时再使用

如果处理状态不是吸收的，例如企业进入补贴名单后又退出，就不能简单使用上面的吸收处理设定。此时可以考虑 `did_multiplegt` 路线。

下面仍在同一模拟数据上演示命令写法；实际应用中，dCDH 更适合处理状态可以切换的研究设计。

```python
# 根据样本年份范围设置 did_multiplegt 的动态期和安慰剂期数量
treated_cohorts = df.loc[df["first_treat_year"] > 0, "first_treat_year"]
dynamic_max = int(df["year"].max() - treated_cohorts.min())
placebo_max = int(treated_cohorts.max() - df["year"].min() - 1)

print("did_multiplegt dynamic：", dynamic_max)
print("did_multiplegt placebo：", placebo_max)

# de Chaisemartin-D'Haultfœuille / did_multiplegt 估计
# 适用于处理状态可能发生切换的场景
dcdh = sp.did_multiplegt(
    data=df,
    y="Y",
    group="unit_id",
    time="year",
    treatment="treatment",
    controls=["X1", "X2"],
    dynamic=dynamic_max,
    placebo=placebo_max,
    n_boot=100,
    seed=20260530
)

print(dcdh)
```

**运行结果示例：**

```text
de Chaisemartin-D'Haultfœuille 估计

did_multiplegt dynamic：6
did_multiplegt placebo：6
整体平均处理效应 (Overall ATT)：0.9567
标准误 (SE)：0.0567
95% 置信区间：[0.8455, 1.0678]
```

需要说明的是，如果研究对象本身是标准的吸收处理，即一旦进入政策状态后就持续处于政策状态，那么 dCDH 不一定是首选。它更适合处理状态可逆、政策强度变化或多次进入退出的设计。

## 5. 论文中应该如何报告？

交叠 DID 的实证报告不应只写「本文采用多期 DID」。更合适的写法是把研究设计、估计目标和稳健性检验说清楚。

### 5.1 研究设计部分

研究设计部分至少说明：

* 政策是否分批实施；
* 个体首次处理时间如何定义；
* 处理状态是否为吸收状态；
* 样本中是否存在 never-treated 组；
* 对照组使用 never-treated 还是 not-yet-treated；
* 是否允许处理效应随批次和事件时间变化。

可以写成：

> 本文研究对象属于交叠处理时点的 DID 设计。不同个体在不同年份首次受到政策影响，且处理状态在进入后持续保持。因此，传统 TWFE 模型可能在处理效应异质时混入不合适的组间比较。本文将 TWFE 结果作为基准参照，并使用允许处理效应异质的交叠 DID 估计量作为主结果。

### 5.2 主估计部分

如果使用 CS 方法，可以写：

> 本文采用 Callaway and Sant'Anna (2021) 的方法估计组别-时期平均处理效应 $\operatorname{ATT}(g,t)$，并将其聚合为总体平均处理效应和事件时间效应。该方法允许处理效应在不同处理批次和不同处理后时期之间存在异质性。基准设定中，本文使用从未处理组作为对照组，并控制基期协变量。

如果使用 BJS 方法，可以写：

> 作为稳健性检验，本文进一步使用 Borusyak, Jaravel and Spiess (2024) 的插补估计量。该方法先利用未处理观测估计反事实结果路径，再比较处理组实际结果与预测反事实结果之间的差异。

如果使用 SA 方法，可以写：

> 为展示动态处理效应，本文采用 Sun and Abraham (2021) 的交互加权事件研究方法。与传统 TWFE 事件研究不同，该方法允许处理效应在不同处理批次之间存在异质性，从而避免事件时间系数受到其他处理时期效应的污染。

### 5.3 结果展示部分

结果展示建议包括：

* 一张处理时点分布表；
* 一张 Bacon 分解或 TWFE 诊断表；
* 一张主估计结果表；
* 一张动态效应图；
* 一张多方法对比表；
* 一段平行趋势和识别假设讨论。

多方法结果不一定完全相同。只要估计对象不同，数值差异就是正常现象。关键是解释差异来自哪里：是控制组不同、聚合权重不同、事件窗口不同，还是处理状态设定不同。

### 5.4 软件和复现部分

使用 Python 工具包时，建议在文中或附录中报告软件环境。本文示例结果是在以下环境中得到的：

```text
Python version: 3.13.5
StatsPAI version: 1.16.0
NumPy version: 2.4.0
pandas version: 3.0.2
Main functions:
- bacon_decomposition()
- callaway_santanna()
- sun_abraham()
- did_imputation()
- did_multiplegt()
```

如果论文面向应用经济学期刊，最好同时提供完整代码和数据清洗流程。不要只报告估计命令，因为交叠 DID 的结果高度依赖样本窗口、处理时点定义和对照组选择。

## 6. 使用 StatsPAI 时还要注意什么？

`StatsPAI` 的优点是接口统一。研究者可以用类似的写法调用 Bacon 分解、CS、SA、BJS 和 dCDH 方法，减少在不同软件和不同包之间切换的成本。

但这也带来一个风险：接口越统一，越容易让人忽略估计量之间的差异。不同方法不是同一个模型的不同按钮，而是对应不同的识别对象、对照组构造和聚合权重。

实证使用中，建议遵守三个原则：

* 不要把所有方法都堆到正文里。主估计应由研究设计决定，其余方法作为稳健性或补充分析；
* 不要只报告总体 ATT。交叠 DID 的优势在于可以展示处理效应异质性，动态效应图通常比单一系数更有信息量；
* 不要把软件输出当作识别假设本身。平行趋势、样本可比性和政策时点外生性仍然需要通过制度背景和研究设计来支撑。

## 7. 小结

交叠 DID 方法很多，但选择逻辑并不复杂。研究者真正需要判断的是：政策是否分批实施，处理状态是否吸收，是否存在合适对照组，以及论文关注的是总体平均效应还是动态效应。

TWFE 可以作为基准结果，但在处理效应异质时不宜作为唯一结论。Bacon 分解适合诊断 TWFE；CS 适合估计组别-时期 ATT 并进行聚合；SA 适合展示动态事件研究；BJS 适合用插补法构造反事实；dCDH 更适合处理状态可切换的情形。

简言之，交叠 DID 的核心不是「多跑几个命令」，而是让估计方法、处理时点、对照组和研究问题保持一致。`StatsPAI` 的价值在于把这些方法放入统一的 Python 接口中，降低了实操门槛；但最终结论是否可信，仍取决于研究设计本身。

## 8. 相关资源

* **StatsPAI GitHub**：https://github.com/brycewang-stanford/StatsPAI
* **StatsPAI PyPI**：https://pypi.org/project/StatsPAI/
* **StatsPAI JOSS paper**：https://joss.theoj.org/papers/9f1c837b1b1df7adfcdd538c3698e332
* **StatsPAI 中文 README**：https://github.com/brycewang-stanford/statspai/blob/main/README_CN.md

## 9. 参考文献

* Baker, A. C., Callaway, B., Cunningham, S., Goodman-Bacon, A., & Sant'Anna, P. H. C. (2025). Difference-in-differences designs: A practitioner's guide. *arXiv*. [PDF](https://arxiv.org/abs/2503.13323), [Google](<https://scholar.google.com/scholar?q=Difference-in-Differences+Designs+A+Practitioner%27s+Guide>).

* Borusyak, K., Jaravel, X., & Spiess, J. (2024). Revisiting event-study designs: Robust and efficient estimation. *Review of Economic Studies*, 91(6), 3253-3285. [Link](https://doi.org/10.1093/restud/rdae007), [PDF](https://arxiv.org/abs/2108.12419), [Google](<https://scholar.google.com/scholar?q=Revisiting+Event-Study+Designs+Robust+and+Efficient+Estimation>).

* Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2), 200-230. [Link](https://doi.org/10.1016/j.jeconom.2020.12.001), [PDF](https://arxiv.org/abs/1803.09015), [Google](<https://scholar.google.com/scholar?q=Difference-in-Differences+with+Multiple+Time+Periods+Callaway+Sant%27Anna>).

* de Chaisemartin, C., & D'Haultfœuille, X. (2020). Two-way fixed effects estimators with heterogeneous treatment effects. *American Economic Review*, 110(9), 2964-2996. [Link](https://doi.org/10.1257/aer.20181169), [PDF](https://arxiv.org/abs/1803.08807), [Google](<https://scholar.google.com/scholar?q=Two-way+fixed+effects+estimators+with+heterogeneous+treatment+effects>).

* Goodman-Bacon, A. (2021). Difference-in-differences with variation in treatment timing. *Journal of Econometrics*, 225(2), 254-277. [Link](https://doi.org/10.1016/j.jeconom.2021.03.014), [PDF](https://www.nber.org/system/files/working_papers/w25018/w25018.pdf), [Google](<https://scholar.google.com/scholar?q=Difference-in-differences+with+variation+in+treatment+timing+Goodman-Bacon>).

* Rambachan, A., & Roth, J. (2023). A more credible approach to parallel trends. *Review of Economic Studies*, 90(5), 2555-2591. [Link](https://doi.org/10.1093/restud/rdad018), [PDF](https://www.jonathandroth.com/assets/files/HonestParallelTrends_Main.pdf), [Google](<https://scholar.google.com/scholar?q=A+More+Credible+Approach+to+Parallel+Trends>).

* Sun, L., & Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. *Journal of Econometrics*, 225(2), 175-199. [Link](https://doi.org/10.1016/j.jeconom.2020.09.006), [PDF](https://arxiv.org/abs/1804.05785), [Google](<https://scholar.google.com/scholar?q=Estimating+dynamic+treatment+effects+in+event+studies+with+heterogeneous+treatment+effects>).

* Wang, B., & Rozelle, S. (2026). *StatsPAI: The Agent-Native Causal Inference & Econometrics Toolkit for Python*. Zenodo. [Link](https://doi.org/10.5281/zenodo.19933900), [Google](<https://scholar.google.com/scholar?q=StatsPAI+The+Agent-Native+Causal+Inference+Econometrics+Toolkit+for+Python>).

## 10. 相关推文

> Note：产生如下推文列表的 Stata 命令为：
>   `lianxh 多期DID 交错DID 渐进 多时点 多期倍分法 csdid drdid goodman, md2 nocat`
> 安装最新版 `lianxh` 命令：
>   `ssc install lianxh, replace`

* 侯新烁, 2019, [多期DID：平行趋势检验图示](https://www.lianxh.cn/details/112.html).
* 周瑾, 2024, [sdid_event命令：合成DID事件研究法](https://www.lianxh.cn/details/1482.html).
* 宋燕欣, 2021, [DIDM：多期多个体倍分法-did_multiplegt](https://www.lianxh.cn/details/601.html).
* 张子楠, 2022, [DID偏误问题：两时期DID的双重稳健估计量(上)-drdid](https://www.lianxh.cn/details/1024.html).
* 张子楠, 2022, [DID偏误问题：多时期DID的双重稳健估计量(下)-csdid](https://www.lianxh.cn/details/1027.html).
* 张梓瑶, 2021, [如何在R语言中实现多期DID](https://www.lianxh.cn/details/829.html).
* 张远远, 2019, [Stata：多期倍分法 (DID) 详解及其图示](https://www.lianxh.cn/details/76.html).
* 彭晴, 2022, [DID新进展：异质性多期DID估计的新方法-csdid](https://www.lianxh.cn/details/1071.html).
* 朱学贵, 2020, [多期DID之安慰剂检验、平行趋势检验](https://www.lianxh.cn/details/259.html).
* 李闯, 2023, [多时点DID保姆级教程(上)-平行趋势检验](https://www.lianxh.cn/details/1201.html).
* 李闯, 2023, [多时点DID保姆级教程(下)-安慰剂检验](https://www.lianxh.cn/details/1163.html).
* 杨云帆, 2023, [论文复现：多期DID应用之地方选举的兴衰](https://www.lianxh.cn/details/1321.html).
* 王昆仑, 2019, [倍分法DID详解 (三)：多时点 DID (渐进DID) 的进一步分析](https://www.lianxh.cn/details/9.html).
* 王昆仑, 2019, [倍分法DID详解 (二)：多时点 DID (渐进DID)](https://www.lianxh.cn/details/72.html).
* 笑花心, 2020, [tfdiff：多期DID的估计及图示](https://www.lianxh.cn/details/464.html).
* 胡文涛, 2021, [倍分法：交错DID与Stata操作](https://www.lianxh.cn/details/638.html).
* 邹恬华, 2021, [多期DID文献解读：含铅汽油与死亡率和社会成本-L113](https://www.lianxh.cn/details/622.html).
* 高君, 2025, [Big-Bad-Bank并不稳健：DID元老级文献的脆弱](https://www.lianxh.cn/details/1548.html).
* 高瑜, 2024, [eventbaseline：事件研究的估算与可视化](https://www.lianxh.cn/details/1486.html).
* 高瑜, 2024, [事件研究和多期DID可视化新命令](https://www.lianxh.cn/details/1507.html).
