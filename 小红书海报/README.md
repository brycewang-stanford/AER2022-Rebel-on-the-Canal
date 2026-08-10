# 运河上的叛乱 · 50 张小红书竖版海报

对 **Cao, Yiming and Shuo Chen (2022)**
《*Rebel on the Canal: Disrupted Trade Access and Social Conflict in China, 1650–1911*》
（*American Economic Review*, 112(5): 1555–1590，doi `10.1257/aer.20201283`）的逐节拆解。

- 尺寸：**2160 × 2880 px**（1080×1440 @2x），小红书竖版 3:4
- 风格：**Memphis Pop · Sugar Rush** —— 奶油底 + 泡泡糖粉 / 电光蓝 / 鲜黄 / 薄荷绿 / 珊瑚红
  五撞色；所有块必带 3px 墨黑粗描边 + 硬投影；孟菲斯装饰碎片（圆点阵 / 波浪线 /
  Z 字闪电 / 45° 三角块 / 棋盘条纹）。主题取自
  [many-ppt-skills](https://github.com/brycewang-stanford/many-ppt-skills) 收录的
  `ppt-master` 示例 `examples/ppt169_sugar_rush_memphis`（`design_spec.md` §III–V），
  由 1280×720 横版适配到 1080×1440 竖版
- **每一页顶部**是同一条论文信息条（`AER 2022 · REBEL ON THE CANAL · 112(5): 1555–1590` + 页码），
  **每一页底部**是同一条仓库条（`pip install statspai` ·
  [github.com/brycewang-stanford/StatsPAI](https://github.com/brycewang-stanford/StatsPAI)）
- 快速浏览：本地跑一次 `python3 _源码/render.py`，会额外生成
  `00-联系表-contact-sheet.png`（50 宫格）与 `00-全部预览.pdf`。
  这两个合成文件体积大，不入库；50 张 PNG 才是源。

---

## 一、50 张目录

### 开场（01–06）

| # | 文件 | 讲什么 | 主图 |
|---|---|---|---|
| 01 | 封面 | 论文完整标题、作者、期刊、一句话结论 | — |
| 02 | 第一作者 | Yiming Cao 头像 + 任职 + 研究方向 + 陈硕 | 官方头像 |
| 03 | 核心模型 | 五个核心 DID 模型压成一页 | — |
| 04 | 核心亮点 | 为什么这篇能上 AER：五条 | — |
| 05 | 一句话结论 | 0.0380 / +117% / 40 年 | 自制 `c_headline` |
| 06 | 全册地图 | 六站路线 | — |

### 站 1 · 运河怎么废的（07–13）

| # | 文件 | 讲什么 | 主图 |
|---|---|---|---|
| 07 | 站 1 扉页 | — | — |
| 08 | 运河 262 年 | 1,776 km / 350 万石 / 陆运成本 10× | 自制 `c_timeline` |
| 09 | 1826 发生了什么 | 事件链 + 为什么不选 1825 / 1855 | — |
| 10 | 外生性四条 | 廷议论据方向 · 淮安关税 −30% · 替代时点 | 自制 `c_why1826` |
| 11 | ★ 原文 Fig 2 | 漕运量趋势与 1826 转折 | **原文 Figure 2** |
| 12 | ★ 原文 Fig 1 | 运河位置与六省 | **原文 Figure 1** |
| 13 | 断航的后果 | 漕帮解散 · 临清塌方 · 北段 vs 南段 | — |

### 站 2 · 数据怎么造（14–18）

| # | 文件 | 讲什么 | 主图 |
|---|---|---|---|
| 14 | 站 2 扉页 | — | — |
| 15 | 面板结构 | 536 × 262 = 140,432；1,144 起爆发 | 自制 `c_panel` |
| 16 | ★ 原文 Tab 1 | 数据来源与描述统计 | **原文 Table 1** |
| 17 | 变量定义 | 因变量 + 四种处理度量 | — |
| 18 | ★ 原文 Fig 3 | 叛乱空间分布 前 / 后 | **原文 Figure 3** |

### 站 3 · 五个模型（19–31）

| # | 文件 | 讲什么 | 主图 |
|---|---|---|---|
| 19 | 站 3 扉页 | — | — |
| 20 | 2×2 四个格子 | ATT = (B−A) − (D−C) | 自制 `c_2x2` |
| 21 | 模型 ① 式 (1) | 逐项拆解基准 DID | — |
| 22 | 五列控制在防什么 | 每一列各防一件事 | — |
| 23 | ★ 原文 Tab 3 | 基准估计（两套 SE） | **原文 Table 3** |
| 24 | 系数阶梯 | 五列画成带 CI 的柱状图 | 自制 `c_ladder` |
| 25 | 系数怎么读 | 0.0380 → 117% → 每年多 130 起 | — |
| 26 | 两套标准误 | 县级聚类 vs Conley 时空 HAC | — |
| 27 | 模型 ② 式 (2) | 事件研究的三个设计选择 | — |
| 28 | ★ 原文 Fig 4 | 事件研究图 | **原文 Figure 4** |
| 29 | 事件研究怎么读 | 四个读点：平行 / 倒 V / 峰 / 收敛 | 自制 `c_es_read` |
| 30 | 模型 ③ 式 (3) | 前趋势检验 | **原文 Table 2** |
| 31 | 模型 ④⑤ 剂量 | 三种连续强度 + 距离 | **原文 Table 4** |

### 站 4 · 稳不稳（32–39）

| # | 文件 | 讲什么 | 主图 |
|---|---|---|---|
| 32 | 站 4 扉页 | — | — |
| 33 | 强度三条 | 0.0200 / 0.0770 / −0.0142 | 自制 `c_intensity` |
| 34 | 距离衰减 150km | 溢出边界与 donut 的伏笔 | 自制 `c_dist` |
| 35 | ★ 原文 Tab 5 | 南北三重差分 | **原文 Table 5** |
| 36 | ★ 原文 Tab 6 | 五条替代交通线安慰剂 | **原文 Table 6** + 自制 `c_placebo` |
| 37 | ★ 原文 Tab 7 | 鸦片战争 / 太平天国 | **原文 Table 7** |
| 38 | 换估计量 | CIC 与合成控制 | 自制 `c_cic` |
| 39 | 机制排除 | 四条竞争解释怎么被排掉 | 自制 `c_mech` |

### 站 5 · 2026 年怎么看（40–45）

| # | 文件 | 讲什么 | 主图 |
|---|---|---|---|
| 40 | 站 5 扉页 | — | — |
| 41 | 五者等价 | 2×2 下 TWFE = CS = SA = BJS = ETWFE | 自制 `c_equiv` |
| 42 | 四条前线 | 2022–2026 DID 的新重心 | 自制 `c_frontier` |
| 43 | 前趋势 power | Roth (2022)：1 SE 违反只有 17% 检出率 | 自制 `c_power` |
| 44 | honest DID | Rambachan-Roth (2023)：breakdown M* ≈ 1.9 | 自制 `c_honest` |
| 45 | Chen-Roth 零值 | 「117%」为什么要改口 | 自制 `c_chenroth` |

### 站 6 · statspai 复现（46–50）

| # | 文件 | 讲什么 | 主图 |
|---|---|---|---|
| 46 | 八步流程 | 照这八步，你也能写一篇 2×2 DID | 自制 `c_steps` |
| 47 | 五行代码 | 五个模型 → 五行 statspai | — |
| 48 | 实跑系数 | 论文报告值 vs statspai 实跑 | 自制 `c_repro_bar` |
| 49 | 实跑事件研究 | `event_study` + `honest_did` 的真实输出 | 自制 `c_repro_es` |
| 50 | 封底 | 方法 ↔ 函数对照表 + 带走三句话 | — |

---

## 二、从原文截出来的图与表

`_源码/figs/` 里共 14 张，由 [`_源码/extract_figs.py`](_源码/extract_figs.py) 按页码 +
点坐标从 PDF 直接裁出（600–800 dpi）。**论文正文的 4 张图 + 7 张表一张不落**：

- **图**：`fig1_canal_map`（运河位置，AER p.1560）· `fig2_tribute`（漕运量，p.1562）·
  `fig3_spatial` / `fig3a_before` / `fig3b_after`（空间分布，p.1567）·
  `fig4_eventstudy`（事件研究，p.1569）
- **表**：`tab1_summary` + `tab1_sources`（p.1566）· `tab2_pretrend`（p.1570）·
  `tab3_baseline`（p.1570）· `tab4_intensity`（p.1573）· `tab5_northsouth`（p.1579）·
  `tab6_placebo`（p.1579）· `tab7_distortions`（p.1581）

## 三、自制图表

`_源码/charts/` 里共 20 张，由 [`_源码/charts.py`](_源码/charts.py) 用 matplotlib +
Memphis 五色调色板绘制。数值全部来自原文正文、表格或图注，或来自 `repro.py` 的
statspai 实跑输出，没有编造；形状取自原文附录图的会在图内注明「示意图」。

`c_timeline` · `c_why1826` · `c_panel` · `c_2x2` · `c_ladder` · `c_es_read` ·
`c_intensity` · `c_dist` · `c_placebo` · `c_cic` · `c_mech` · `c_power` ·
`c_honest` · `c_chenroth` · `c_equiv` · `c_frontier` · `c_headline` · `c_steps` ·
`c_repro_es` · `c_repro_bar`

## 四、作者头像

`_源码/avatars/cao.png` 取自
[香港大学经管学院教师主页](https://www.hkubs.hku.hk/people/yiming-cao/)。

## 五、statspai 复现（v1.22.0）

[`_源码/repro.py`](_源码/repro.py) 用 **StatsPAI v1.22.0** 跑通了论文的五个核心模型
+ 两项现代补充。

> ⚠️ **这不是论文数字的复现。** 论文的分析面板（openICPSR 157781-V1）不随本仓库分发，
> `repro.py` 用的是一份**按论文报告值标定的模拟面板**：
> 536 县 × 262 年 = 140,432 个县-年，73 个运河县，处理时点 1826，
> 真实 ATT 设为 0.0380，动态形状按 Figure 4 的倒 V + 40 年峰值标定。
> 目的是演示 statspai 的调用路径与输出形态。
> 拿到真实 `rebellion.dta` 之后，把 `simulate()` 换成 `pd.read_stata()` 即可，
> 其余代码一行不用改。

本次实跑结果（seed 固定，见 `_源码/repro/results.json`）：

| 模型 | statspai 调用 | 结果 |
|---|---|---|
| ① 基准 2×2 DID | `sp.feols("y ~ canal_post \| county + year", vcov={"CRV1":"county"})` | β = 0.0417 (0.0065) |
| ①b + 省×年 FE | `sp.feols("y ~ canal_post \| county + prov_year", ...)` | β = 0.0416 (0.0066) |
| ② 事件研究 | `sp.event_study(..., window=(-50,70), bin_width=10)` | 13 个分箱，峰值在 e = 30 |
| ③ 前趋势 | `sp.feols("y ~ canal_year \| county + year", data=pre)` | β = 0.00003, p = 0.92 |
| ④ 处理强度 | `sp.feols("y ~ len_post \| county + year", ...)` | β = 0.00082 (0.00020) |
| ⑤A power | Roth (2022) 公式 | 1 SE → 17% · 2 SE → 52% · 3 SE → 85% |
| ⑤B honest DID | `sp.honest_did(es, e=30, method="relative_magnitude")` | M̄ = 2.0 时 CI 下界仍为 0.0242 |

> `honest_did` 的 `relative_magnitude` 家族在 native 后端返回的是
> worst-case-bias 区间，不是 Rambachan-Roth 的 ARP 条件置信集；
> 要精确结果需 `backend="r"`（依赖 R 的 HonestDiD 包）。
> `smoothness` 家族在十年分箱下会因为二阶差分的尺度而爆掉，因此本册只报 RM 家族。

方法 ↔ 函数完整对照见第 50 张。

## 六、怎么重新生成

```bash
cd _源码
python3 fonts/build_fonts.py   # 下载并子集化字体（只需跑一次）
python3 extract_figs.py        # 从 PDF 裁图裁表 → figs/
python3 repro.py               # statspai 实跑 → repro/results.json（约 3 分钟）
python3 charts.py              # 画自制图表 → charts/
python3 render.py              # 渲染 50 张 PNG + 联系表 + 预览 PDF
```

依赖：`pymupdf` `pillow` `matplotlib` `fonttools` `pandas` `scipy` `statspai>=1.22`
`playwright`（含 chromium）。
`render.py` 会逐页检查内容是否溢出，溢出会在终端打印页名与像素数。

字体（均为 SIL Open Font License）：Archivo Black · Space Grotesk ·
JetBrains Mono · Noto Sans SC。仓库里的 Noto Sans SC 按本项目用到的字符子集化，
改文案后需要重跑 `build_fonts.py`。

---

## 七、引用

```bibtex
@article{cao2022rebel,
  author  = {Cao, Yiming and Chen, Shuo},
  title   = {Rebel on the Canal: Disrupted Trade Access and Social Conflict
             in China, 1650--1911},
  journal = {American Economic Review},
  year    = {2022},
  volume  = {112},
  number  = {5},
  pages   = {1555--1590},
  doi     = {10.1257/aer.20201283}
}
```

论文 PDF 版权属于 American Economic Association；本册裁出的图表仅用于学习与评论。
