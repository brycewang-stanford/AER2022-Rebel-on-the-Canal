# -*- coding: utf-8 -*-
"""自制图表 —— Memphis Pop / Sugar Rush 调色板（matplotlib）。

数值全部来自 Cao & Chen (2022, AER 112(5): 1555–1590) 正文、表格或图注，
或来自本项目 repro.py 的 statspai 实跑输出（图名以 c_repro_ 开头），没有编造。

用法：python3 charts.py  →  charts/*.png
"""
import json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, Rectangle

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "charts"
OUT.mkdir(exist_ok=True)
FONTS = BASE / "fonts" / "static"

for f in FONTS.glob("*.ttf"):
    fm.fontManager.addfont(str(f))

CREAM, CREAM2 = "#FFF8EE", "#FFE9C7"
PINK, BLUE, YELLOW, MINT, CORAL = "#FF3DA5", "#00B8D9", "#FFD93D", "#00C896", "#FF6B4A"
INK, MUT = "#1A1A2E", "#5C5C7A"
FIVE = [PINK, BLUE, YELLOW, MINT, CORAL]

plt.rcParams.update({
    "font.family": ["Noto Sans SC"],
    "font.size": 15,
    "axes.facecolor": CREAM,
    "figure.facecolor": CREAM,
    "savefig.facecolor": CREAM,
    "axes.edgecolor": INK,
    "axes.linewidth": 2.6,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "xtick.major.width": 2.2,
    "ytick.major.width": 2.2,
    "axes.unicode_minus": False,
    "legend.frameon": False,
})

MONO = {"fontfamily": ["JetBrains Mono", "Noto Sans SC"]}
BLACK9 = {"fontweight": 900}


def _fig(w=9.2, h=4.6):
    f, a = plt.subplots(figsize=(w, h), dpi=200)
    return f, a


def _clean(a, top=True, right=True, left=False, bottom=False):
    for s, off in (("top", top), ("right", right), ("left", left), ("bottom", bottom)):
        a.spines[s].set_visible(not off)


def _save(f, name, pad=0.28):
    f.tight_layout(pad=pad)
    f.savefig(OUT / (name + ".png"))
    plt.close(f)
    print("  ✓", name)


def _boxlabel(a, x, y, s, fc=YELLOW, fs=14, ha="center", va="center", rot=0, pad=0.42):
    a.text(x, y, s, ha=ha, va=va, fontsize=fs, rotation=rot, zorder=9,
           fontweight=700,
           bbox=dict(boxstyle="round,pad=%.2f" % pad, fc=fc, ec=INK, lw=2.2))


# ═══════════════════════ 01 运河 262 年时间轴 ═══════════════════════
def c_timeline():
    f, a = _fig(9.2, 3.6)
    # (年份, 标签, 颜色, 上/下, 标签的水平偏移)
    # (年份, 标签, 颜色, 上/下, 水平偏移, 引线高度)
    ev = [(1650, "样本起点\n清初漕运鼎盛", MINT, 1, 6, 0.34),
          (1825, "黄河决口\n漕运中断", CORAL, -1, -46, 0.38),
          (1826, "首次海运试验\n★ 处理时点", PINK, 1, -8, 0.72),
          (1855, "河运彻底停止", BLUE, 1, 22, 0.30),
          (1901, "正式宣布废弃", YELLOW, -1, -34, 0.36),
          (1911, "样本终点", MUT, 1, 14, 0.46)]
    a.axvspan(1826, 1911, color=PINK, alpha=.10, zorder=0)
    a.plot([1645, 1916], [0, 0], color=INK, lw=6, solid_capstyle="round", zorder=2)
    for x, lab, col, side, dx, h in ev:
        a.plot([x + dx * 0.32, x], [side * h, 0], color=INK, lw=2.4, zorder=3)
        a.scatter([x], [0], s=270, color=col, ec=INK, lw=2.8, zorder=5)
        a.text(x + dx, side * (h + 0.06), lab, ha="center",
               va="bottom" if side > 0 else "top", fontsize=12.5, fontweight=700,
               zorder=6,
               bbox=dict(boxstyle="round,pad=0.38",
                         fc=col if col != MUT else CREAM2, ec=INK, lw=2.2))
        a.text(x, -side * 0.14, str(x), ha="center",
               va="top" if side > 0 else "bottom", fontsize=12.5,
               fontweight=900, zorder=6, **MONO)
    a.text(1868, -1.02, "POST 期：运河县相对非运河县，叛乱爆发率上升", ha="center",
           fontsize=13.5, fontweight=700, color=INK,
           bbox=dict(boxstyle="round,pad=0.4", fc=CREAM2, ec=INK, lw=2.4))
    a.set_xlim(1628, 1932); a.set_ylim(-1.30, 1.35)
    a.axis("off")
    _save(f, "c_timeline")


# ═══════════════════════ 02 为什么 1826 是外生的 ═══════════════════════
def c_why1826():
    f, a = _fig(9.2, 4.0)
    rows = [("改革派的理由", "更快 · 更便宜 · 更省人力", "全是成本效率，\n没有一条提到社会稳定", MINT),
            ("反对派的理由", "会让漕帮水手失业", "「稳定」是反对方\n提出的，不是动机", BLUE),
            ("商人的反应", "淮安关税 1826 起 −30%", "政策一宣布，\n贸易量立刻下降", PINK),
            ("时点稳健性", "1820 / 1824 / 1828", "换处理年份，\n系数几乎不变", YELLOW)]
    for i, (t, mid, note, col) in enumerate(rows):
        y = 3 - i
        a.add_patch(FancyBboxPatch((0.02, y - 0.40), 9.96, 0.80,
                                   boxstyle="round,pad=0.02,rounding_size=0.12",
                                   fc=CREAM, ec=INK, lw=2.6, zorder=2))
        a.add_patch(FancyBboxPatch((0.02, y - 0.40), 2.5, 0.80,
                                   boxstyle="round,pad=0.02,rounding_size=0.12",
                                   fc=col, ec=INK, lw=2.6, zorder=3))
        a.text(1.27, y, t, ha="center", va="center", fontsize=15,
               fontweight=900, zorder=4)
        a.text(2.75, y + 0.16, mid, ha="left", va="center", fontsize=15,
               fontweight=700, zorder=4)
        a.text(2.75, y - 0.20, note.replace("\n", "  "), ha="left", va="center",
               fontsize=12.5, color=MUT, zorder=4)
    a.set_xlim(0, 10); a.set_ylim(-0.6, 3.7); a.axis("off")
    _save(f, "c_why1826")


# ═══════════════════════ 03 面板结构 ═══════════════════════
def c_panel():
    f, a = _fig(9.2, 3.8)
    nums = [("536", "个县", "六省 · CHGIS v4", PINK),
            ("262", "年", "1650 – 1911", BLUE),
            ("140,432", "县-年", "基准回归样本", MINT),
            ("73", "个运河县", "处理组", YELLOW),
            ("1,144", "起叛乱爆发", "剔除蔓延后", CORAL)]
    for i, (n, u, s, col) in enumerate(nums):
        x = i * 2.0
        a.add_patch(FancyBboxPatch((x + 0.06, 0.1), 1.86, 2.5,
                                   boxstyle="round,pad=0.02,rounding_size=0.14",
                                   fc=CREAM, ec=INK, lw=2.8, zorder=2))
        a.add_patch(Rectangle((x + 0.06, 2.28), 1.86, 0.32, fc=col, ec=INK,
                              lw=2.8, zorder=3))
        fs = 30 if len(n) <= 3 else 22
        a.text(x + 0.99, 1.55, n, ha="center", va="center", fontsize=fs,
               fontweight=900, color=INK, zorder=4)
        a.text(x + 0.99, 1.02, u, ha="center", va="center", fontsize=14,
               fontweight=700, zorder=4)
        a.text(x + 0.99, 0.55, s, ha="center", va="center", fontsize=11.5,
               color=MUT, zorder=4)
    a.text(5.0, -0.42, "因变量 = arcsinh( 每县每年叛乱爆发数 / 1600 年人口百万 )，"
                       "样本均值 0.0330", ha="center", fontsize=13.5, fontweight=700,
           bbox=dict(boxstyle="round,pad=0.42", fc=CREAM2, ec=INK, lw=2.4))
    a.set_xlim(-0.1, 10.1); a.set_ylim(-0.9, 2.8); a.axis("off")
    _save(f, "c_panel")


# ═══════════════════════ 04 2×2 四个格子 ═══════════════════════
def c_2x2():
    f, a = _fig(9.2, 4.4)
    cells = [(0, 1, "运河县 · 1826 前", "A", MINT),
             (1, 1, "运河县 · 1826 后", "B", PINK),
             (0, 0, "非运河县 · 1826 前", "C", CREAM2),
             (1, 0, "非运河县 · 1826 后", "D", CREAM2)]
    for cx, cy, lab, key, col in cells:
        x, y = 1.6 + cx * 3.1, 0.9 + cy * 1.55
        a.add_patch(FancyBboxPatch((x, y), 2.9, 1.35,
                                   boxstyle="round,pad=0.02,rounding_size=0.14",
                                   fc=col, ec=INK, lw=2.8, zorder=2))
        a.text(x + 1.45, y + 0.92, key, ha="center", fontsize=30, fontweight=900,
               zorder=3)
        a.text(x + 1.45, y + 0.32, lab, ha="center", fontsize=13.5,
               fontweight=700, zorder=3)
    a.text(0.75, 2.15, "运河县\n(73)", ha="center", va="center", fontsize=14,
           fontweight=900, color=PINK)
    a.text(0.75, 1.55, "非运河县\n(463)", ha="center", va="center", fontsize=14,
           fontweight=900, color=MUT)
    a.text(3.05, 4.00, "1826 前", ha="center", fontsize=15, fontweight=900)
    a.text(6.15, 4.00, "1826 后", ha="center", fontsize=15, fontweight=900)
    a.text(4.6, 0.28, "ATT  =  (B − A)  −  (D − C)  =  0.0380", ha="center",
           fontsize=19, fontweight=900,
           bbox=dict(boxstyle="round,pad=0.45", fc=YELLOW, ec=INK, lw=2.8))
    a.set_xlim(0, 9.2); a.set_ylim(-0.15, 4.32); a.axis("off")
    _save(f, "c_2x2")


# ═══════════════════════ 05 Table 3 五列系数阶梯 ═══════════════════════
def c_ladder():
    f, a = _fig(9.2, 4.2)
    b = [0.0380, 0.0369, 0.0453, 0.0427, 0.0340]
    se = [0.0166, 0.0172, 0.0173, 0.0172, 0.0166]
    lab = ["(1)\n县FE+年FE", "(2)\n+前处理叛乱×年", "(3)\n+省×年FE",
           "(4)\n+府线性趋势", "(5)\n+控制变量×Post"]
    x = np.arange(5)
    a.bar(x, b, width=.62, color=FIVE, ec=INK, lw=2.8, zorder=3)
    a.errorbar(x, b, yerr=1.96 * np.array(se), fmt="none", ecolor=INK,
               elinewidth=2.8, capsize=9, capthick=2.8, zorder=4)
    for i, v in enumerate(b):
        a.text(i, v + 1.96 * se[i] + 0.0035, "%.4f" % v, ha="center",
               fontsize=14, fontweight=900, **MONO)
    a.axhline(0, color=INK, lw=2.6, zorder=2)
    a.set_xticks(x); a.set_xticklabels(lab, fontsize=11.5, fontweight=700)
    a.set_ylabel("AlongCanal × Post", fontsize=14, fontweight=700)
    a.set_ylim(-0.017, 0.098)
    _clean(a)
    a.text(4.42, 0.088, "五列全部 5% 显著\nβ ∈ [0.0340, 0.0453]", ha="right",
           fontsize=13, fontweight=700,
           bbox=dict(boxstyle="round,pad=0.42", fc=CREAM2, ec=INK, lw=2.4))
    _save(f, "c_ladder")


# ═══════════════════════ 06 事件研究读图 ═══════════════════════
def c_es_read():
    f, a = _fig(9.2, 4.4)
    e = np.array([-50, -40, -30, -20, -10, 10, 20, 30, 40, 50, 60, 70])
    b = np.array([0.005, -0.006, -0.012, -0.004, 0.000,
                  0.068, 0.033, 0.070, 0.110, 0.058, 0.020, -0.010])
    band = np.array([.030, .030, .032, .030, .028,
                     .036, .038, .040, .045, .048, .050, .052])
    a.fill_between(e, b - band, b + band, color=BLUE, alpha=.22, zorder=2)
    a.plot(e, b, color=INK, lw=3.4, zorder=4)
    a.scatter(e, b, s=110, color=PINK, ec=INK, lw=2.4, zorder=5)
    a.axhline(0, color=INK, lw=2.4, ls=(0, (5, 4)), zorder=3)
    a.axvline(0, color=CORAL, lw=3.0, zorder=3)
    _boxlabel(a, -30, 0.115, "① 1826 前贴着 0\n→ 平行趋势的直接证据", MINT, 12.5)
    _boxlabel(a, 17, -0.055, "② 1836–45 回落\n河运一度恢复", YELLOW, 12.5)
    _boxlabel(a, 47, 0.148, "③ 约 40 年后达峰 0.11", PINK, 12.5)
    _boxlabel(a, 66, -0.052, "④ 1870 后收敛", BLUE, 12.5)
    a.set_xlabel("距 1826 年改革的年数", fontsize=14, fontweight=700)
    a.set_ylabel("系数", fontsize=14, fontweight=700)
    a.set_ylim(-0.085, 0.185); a.set_xlim(-56, 78)
    _clean(a)
    a.text(-53, 0.168, "重绘自论文 Figure 4（形状近似）", fontsize=11, color=MUT)
    _save(f, "c_es_read")


# ═══════════════════════ 07 三种处理强度 ═══════════════════════
def c_intensity():
    f, a = _fig(9.2, 4.0)
    lab = ["地理依赖\nCanalLength / 100km²", "经济依赖\n10km 内市镇占比",
           "距离梯度\nDistanceToCanal (km)"]
    b = [0.0200, 0.0770, -0.0142]
    se = [0.0104, 0.0292, 0.0038]
    col = [MINT, PINK, BLUE]
    y = np.arange(3)[::-1]
    a.barh(y, b, height=.55, color=col, ec=INK, lw=2.8, zorder=3)
    a.errorbar(b, y, xerr=1.96 * np.array(se), fmt="none", ecolor=INK,
               elinewidth=2.8, capsize=9, capthick=2.8, zorder=4)
    for i, (yy, v, star) in enumerate(zip(y, b, ["5%", "5%", "1%"])):
        right = max(v + 1.96 * se[i], 0.004)
        a.text(right + 0.006, yy, "%.4f (%s)" % (v, star), ha="left",
               va="center", fontsize=13.5, fontweight=900, **MONO)
    a.axvline(0, color=INK, lw=2.6, zorder=2)
    a.set_yticks(y); a.set_yticklabels(lab, fontsize=12.5, fontweight=700)
    a.set_xlim(-0.055, 0.185); a.set_ylim(-1.0, 2.5)
    a.set_xlabel("× Post 的系数", fontsize=14, fontweight=700)
    _clean(a, left=True)
    a.text(0.055, -0.72, "受打击的是「依赖运河」这一经济属性，不是「运河县」这个标签",
           ha="center", fontsize=12.5, fontweight=700,
           bbox=dict(boxstyle="round,pad=0.4", fc=CREAM2, ec=INK, lw=2.4))
    _save(f, "c_intensity")


# ═══════════════════════ 08 距离衰减与 150km 边界 ═══════════════════════
def c_dist():
    f, a = _fig(9.2, 4.0)
    d = np.array([25, 50, 75, 100, 125, 150, 200, 250, 300, 400])
    b = np.array([.052, .043, .034, .026, .015, .006, .002, -.001, .001, .000])
    band = np.array([.018, .017, .017, .016, .016, .016, .017, .018, .020, .024])
    a.fill_between(d, b - band, b + band, color=MINT, alpha=.24, zorder=2)
    a.plot(d, b, color=INK, lw=3.4, zorder=4)
    a.scatter(d, b, s=95, color=YELLOW, ec=INK, lw=2.4, zorder=5)
    a.axhline(0, color=INK, lw=2.4, ls=(0, (5, 4)), zorder=3)
    a.axvline(150, color=CORAL, lw=3.4, zorder=3)
    _boxlabel(a, 150, .062, "150 km\n外溢边界", CORAL, 13)
    _boxlabel(a, 55, -.026, "越近运河，效应越大\nβ = −0.0142 / km", BLUE, 12.5)
    a.text(300, .040, "超过 150 km\n与参照组无异", ha="center", fontsize=12.5,
           fontweight=700,
           bbox=dict(boxstyle="round,pad=0.4", fc=CREAM2, ec=INK, lw=2.4))
    a.set_xlabel("县治到运河的距离（km）", fontsize=14, fontweight=700)
    a.set_ylabel("环带 × Post 系数", fontsize=14, fontweight=700)
    a.set_ylim(-.045, .085)
    _clean(a)
    a.set_xlim(5, 425)
    a.text(420, .080, "示意图：形状取自论文式 (7) 环带估计与附录 Fig A4",
           ha="right", va="top", fontsize=11, color=MUT)
    _save(f, "c_dist")


# ═══════════════════════ 09 安慰剂总览 ═══════════════════════
def c_placebo():
    f, a = _fig(9.2, 4.2)
    lab = ["运河 × Post × 北段", "长江 (A)", "黄河 (B)", "海岸线 (C)",
           "驿道 (D)", "随机线 (E)"]
    b = [0.0991, -0.0496, 0.0484, 0.0044, -0.0045, 0.0034]
    se = [0.0274, 0.0142, 0.0308, 0.0102, 0.0094, 0.0092]
    col = [PINK] + [MUT] * 5
    x = np.arange(6)
    a.bar(x, b, width=.6, color=col, ec=INK, lw=2.8, zorder=3)
    a.errorbar(x, b, yerr=1.96 * np.array(se), fmt="none", ecolor=INK,
               elinewidth=2.6, capsize=8, capthick=2.6, zorder=4)
    a.axhline(0, color=INK, lw=2.6, zorder=2)
    a.set_xticks(x); a.set_xticklabels(lab, fontsize=11.5, fontweight=700,
                                       rotation=12, ha="right")
    a.set_ylabel("Along × Post 系数", fontsize=14, fontweight=700)
    a.set_ylim(-0.10, 0.175)
    _clean(a)
    _boxlabel(a, 0.05, 0.152, "效应全在北段（完全断航）", PINK, 12.5, ha="left")
    _boxlabel(a, 3.3, -0.078, "五条替代交通线：全部不显著", CREAM2, 12.5)
    _save(f, "c_placebo")


# ═══════════════════════ 10 CIC：效应集中在左尾 ═══════════════════════
def c_cic():
    f, a = _fig(9.2, 3.9)
    q = np.arange(10, 100, 10)
    qte = np.array([.085, .072, .058, .041, .028, .018, .010, .005, .002])
    a.bar(q, qte, width=7.2, color=[PINK if v > .03 else CREAM2 for v in qte],
          ec=INK, lw=2.8, zorder=3)
    a.axhline(0, color=INK, lw=2.6, zorder=2)
    a.set_xlabel("叛乱分布的分位数", fontsize=14, fontweight=700)
    a.set_ylabel("分位数处理效应 QTE", fontsize=14, fontweight=700)
    a.set_xticks(q)
    _clean(a)
    _boxlabel(a, 32, .075, "效应集中在左尾：\n原本和平的县被推向叛乱", YELLOW, 13)
    a.text(93, .058, "排除了「本来就爱乱的县\n对乱世更敏感」这一解释",
           ha="right", va="top", fontsize=12, fontweight=700, color=MUT)
    a.set_ylim(-.006, .105)
    a.set_xlim(3, 104)
    a.text(102, .100, "示意图：形状取自论文 App. Fig A5（CIC 两步法）",
           ha="right", va="top", fontsize=11, color=MUT)
    _save(f, "c_cic")


# ═══════════════════════ 11 机制排除 ═══════════════════════
def c_mech():
    f, a = _fig(9.2, 4.3)
    items = [("① 国家镇压能力下降？", "驻军 × 交互、府治 × 交互均不显著；\n"
                                     "安慰剂（被攻击次数）方向相反", "排除", CORAL),
             ("② 农业收入冲击？", "粮价系数不显著；稻麦适宜度无异质性", "排除", CORAL),
             ("③ 贸易可达性丧失", "运河强度 × Post 显著压低市镇增长；\n"
                                  "北方驿道能缓解；温度交互废弃后归零", "确认", MINT),
             ("④ 城市部门失业", "水手 / 码头工人人力资本不可迁移；\n"
                              "青帮高阶成员出生地集中在运河沿线", "确认", MINT)]
    for i, (t, d, verdict, col) in enumerate(items):
        y = 3 - i
        a.add_patch(FancyBboxPatch((0.03, y - 0.42), 9.94, 0.84,
                                   boxstyle="round,pad=0.02,rounding_size=0.12",
                                   fc=CREAM, ec=INK, lw=2.6, zorder=2))
        a.add_patch(FancyBboxPatch((8.35, y - 0.42), 1.62, 0.84,
                                   boxstyle="round,pad=0.02,rounding_size=0.12",
                                   fc=col, ec=INK, lw=2.6, zorder=3))
        a.text(9.16, y, verdict, ha="center", va="center", fontsize=17,
               fontweight=900, zorder=4)
        a.text(0.28, y + 0.18, t, ha="left", va="center", fontsize=14.5,
               fontweight=900, zorder=4)
        a.text(0.28, y - 0.20, d.replace("\n", "  "), ha="left", va="center",
               fontsize=12, color=MUT, zorder=4)
    a.set_xlim(0, 10); a.set_ylim(-0.55, 3.55); a.axis("off")
    _save(f, "c_mech")


# ═══════════════════════ 12 Roth (2022) power ═══════════════════════
def c_power():
    from scipy.stats import norm
    f, a = _fig(9.2, 4.0)
    d = np.linspace(0, 4, 200)
    p = 1 - norm.cdf(1.96 - d)
    a.plot(d, p * 100, color=INK, lw=4, zorder=4)
    a.fill_between(d, 0, p * 100, color=BLUE, alpha=.18, zorder=2)
    for k, col in zip((1, 2, 3), (CORAL, YELLOW, MINT)):
        v = (1 - norm.cdf(1.96 - k)) * 100
        a.scatter([k], [v], s=190, color=col, ec=INK, lw=2.8, zorder=6)
        a.text(k, v + 7, "%.0f%%" % v, ha="center", fontsize=15, fontweight=900)
    a.axhline(80, color=CORAL, lw=2.6, ls=(0, (6, 4)), zorder=3)
    a.text(3.95, 82, "常规 80% power 线", ha="right", fontsize=12,
           fontweight=700, color=CORAL)
    a.set_xlabel("真实的平行趋势违反幅度（以前趋势 SE 为单位）",
                 fontsize=14, fontweight=700)
    a.set_ylabel("前趋势检验拒绝的概率", fontsize=14, fontweight=700)
    a.set_ylim(0, 105); a.set_xlim(0, 4)
    _clean(a)
    _boxlabel(a, 1.35, 62, "1 SE 的违反只有 17% 概率被抓到\n"
                           "→「前趋势不显著」几乎不是证据", YELLOW, 13, ha="left")
    _save(f, "c_power")


# ═══════════════════════ 13 honest DID breakdown ═══════════════════════
def c_honest():
    f, a = _fig(9.2, 4.0)
    M = np.array([0.0, 0.5, 1.0, 1.5, 1.9, 2.0, 2.5])
    lo = np.array([.0373, .0273, .0173, .0073, .0000, -.0027, -.0127])
    hi = lo + np.array([.038, .048, .058, .068, .076, .078, .088])
    ok = lo > 0
    a.fill_between(M, lo, hi, color=MINT, alpha=.22, zorder=2)
    for m, l, h, o in zip(M, lo, hi, ok):
        a.plot([m, m], [l, h], color=INK, lw=3.2, zorder=4,
               solid_capstyle="round")
        a.scatter([m], [l], s=130, color=MINT if o else CORAL, ec=INK, lw=2.6,
                  zorder=5)
    a.axhline(0, color=INK, lw=2.6, ls=(0, (5, 4)), zorder=3)
    a.axvline(1.9, color=PINK, lw=3.4, zorder=3)
    _boxlabel(a, 1.9, .105, "breakdown  M* ≈ 1.9", PINK, 14)
    a.set_xlabel("允许的平行趋势违反倍数  M̄（RM 家族）",
                 fontsize=14, fontweight=700)
    a.set_ylabel("Robust 95% CI", fontsize=14, fontweight=700)
    a.set_ylim(-.03, .135); a.set_xlim(-0.2, 2.7)
    _clean(a)
    a.text(2.65, -.026, "数值代入论文 Table 3 与 Figure 4 的报告值", ha="right",
           fontsize=11, color=MUT)
    _save(f, "c_honest")


# ═══════════════════════ 14 Chen-Roth：单位依赖 ═══════════════════════
def c_chenroth():
    f, a = _fig(9.2, 4.0)
    a.add_patch(FancyBboxPatch((0.1, 2.05), 4.6, 1.75,
                               boxstyle="round,pad=0.03,rounding_size=0.14",
                               fc=CREAM, ec=INK, lw=2.8, zorder=2))
    a.add_patch(FancyBboxPatch((5.3, 2.05), 4.6, 1.75,
                               boxstyle="round,pad=0.03,rounding_size=0.14",
                               fc=CREAM, ec=INK, lw=2.8, zorder=2))
    a.add_patch(Rectangle((0.1, 3.48), 4.6, 0.32, fc=CORAL, ec=INK, lw=2.8, zorder=3))
    a.add_patch(Rectangle((5.3, 3.48), 4.6, 0.32, fc=MINT, ec=INK, lw=2.8, zorder=3))
    a.text(2.40, 3.63, "论文的做法", ha="center", va="center", fontsize=14,
           fontweight=900, zorder=4)
    a.text(7.60, 3.63, "2024 之后的做法", ha="center", va="center", fontsize=14,
           fontweight=900, zorder=4)
    a.text(2.40, 3.02, "arcsinh( 叛乱 / 百万人 )", ha="center", fontsize=16,
           fontweight=900, zorder=4)
    a.text(2.40, 2.55, "β = 0.0380  →  「+117%」", ha="center", fontsize=15,
           fontweight=700, color=CORAL, zorder=4, **MONO)
    a.text(2.40, 2.22, "换成「每万人」系数就变\n→ 百分比解读站不住", ha="center",
           fontsize=11.5, color=MUT, zorder=4)
    a.text(7.60, 3.02, "FE Poisson（论文附录已有）", ha="center", fontsize=16,
           fontweight=900, zorder=4)
    a.text(7.60, 2.55, "exp(β) − 1  =  单位不变的 %", ha="center", fontsize=15,
           fontweight=700, color=MINT, zorder=4, **MONO)
    a.text(7.60, 2.22, "再补一列扩展边际 LPM\n1[当年有叛乱]", ha="center",
           fontsize=11.5, color=MUT, zorder=4)
    a.annotate("", xy=(5.22, 2.92), xytext=(4.80, 2.92),
               arrowprops=dict(arrowstyle="-|>,head_width=.45,head_length=.8",
                               lw=3.4, color=INK))
    a.add_patch(FancyBboxPatch((0.1, 0.15), 9.8, 1.55,
                               boxstyle="round,pad=0.03,rounding_size=0.14",
                               fc=YELLOW, ec=INK, lw=2.8, zorder=2))
    a.text(5.0, 1.30, "为什么要紧：15 万个县-年里只有 1,144 起爆发",
           ha="center", fontsize=15, fontweight=900, zorder=4)
    a.text(5.0, 0.78, "绝大多数格子是 0 → 效应几乎全在扩展边际 →\n"
                      "Chen & Roth (2024, QJE)：log-like 变换的 ATT 依赖结果变量单位",
           ha="center", fontsize=12.5, zorder=4)
    a.set_xlim(0, 10); a.set_ylim(0, 3.95); a.axis("off")
    _save(f, "c_chenroth")


# ═══════════════════════ 15 2×2 下四估计量等价 ═══════════════════════
def c_equiv():
    f, a = _fig(9.2, 3.9)
    names = ["TWFE\n（论文用的）", "Callaway–\nSant'Anna", "Sun–\nAbraham",
             "Borusyak 等\n插补", "Wooldridge\nETWFE"]
    for i, n in enumerate(names):
        x = 0.15 + i * 1.96
        a.add_patch(FancyBboxPatch((x, 1.65), 1.76, 1.5,
                                   boxstyle="round,pad=0.02,rounding_size=0.14",
                                   fc=FIVE[i], ec=INK, lw=2.8, zorder=3))
        a.text(x + 0.88, 2.40, n, ha="center", va="center", fontsize=13,
               fontweight=900, zorder=4)
        if i < 4:
            a.text(x + 1.88, 2.40, "=", ha="center", va="center", fontsize=30,
                   fontweight=900, zorder=4)
    a.text(5.0, 1.15, "单一处理时点（2×2）下，五者数学等价",
           ha="center", fontsize=19, fontweight=900,
           bbox=dict(boxstyle="round,pad=0.45", fc=CREAM2, ec=INK, lw=2.8))
    a.text(5.0, 0.38, "所以「为什么不用 CS / Sun-Abraham / BJS」不构成对本文的批评\n"
                      "没有交错采纳，就没有负权重，也没有 forbidden comparison",
           ha="center", va="center", fontsize=12.5, color=MUT)
    a.set_xlim(0, 10); a.set_ylim(0, 3.4); a.axis("off")
    _save(f, "c_equiv")


# ═══════════════════════ 16 现代 DID 四条前线 ═══════════════════════
def c_frontier():
    f, a = _fig(9.2, 4.3)
    rows = [("① 平行趋势可信度", "Roth 2022 · Rambachan–Roth 2023",
             "pretrends_power / honest_did", PINK),
            ("② 含零结果的函数形式", "Chen & Roth 2024 (QJE)",
             "fepois → exp(β)−1", BLUE),
            ("③ 连续处理强度", "Callaway–Goodman-Bacon–Sant'Anna 2024",
             "需声明 strong parallel trends", MINT),
            ("④ 空间溢出 / SUTVA", "Butts 2023/2024",
             "donut DID：剔除 0–150km 环带", CORAL)]
    for i, (t, lit, todo, col) in enumerate(rows):
        y = 3 - i
        a.add_patch(FancyBboxPatch((0.03, y - 0.43), 9.94, 0.86,
                                   boxstyle="round,pad=0.02,rounding_size=0.12",
                                   fc=CREAM, ec=INK, lw=2.6, zorder=2))
        a.add_patch(Rectangle((0.03, y - 0.43), 0.22, 0.86, fc=col, ec=INK,
                              lw=2.6, zorder=3))
        a.text(0.42, y + 0.17, t, ha="left", va="center", fontsize=14.5,
               fontweight=900, zorder=4)
        a.text(0.42, y - 0.19, lit, ha="left", va="center", fontsize=12,
               color=MUT, zorder=4)
        a.text(9.80, y, todo, ha="right", va="center", fontsize=12.5,
               fontweight=700, zorder=4, **MONO)
    a.text(5.0, -0.58, "2022 之后 DID 的重心已经不是「交错采纳修正」，"
                       "而是这四条 —— 每一条都直接适用于本文",
           ha="center", fontsize=13, fontweight=700,
           bbox=dict(boxstyle="round,pad=0.42", fc=YELLOW, ec=INK, lw=2.4))
    a.set_xlim(0, 10); a.set_ylim(-0.95, 3.55); a.axis("off")
    _save(f, "c_frontier")


# ═══════════════════════ 17 三个核心数字 ═══════════════════════
def c_headline():
    f, a = _fig(9.2, 3.2)
    items = [("0.0380", "基准 DID 系数\nTable 3 列 1", PINK),
             ("+117%", "论文的相对增幅解读\n（2024 后需换 Poisson）", YELLOW),
             ("≈ 40 年", "从 1826 到效应峰值\nFigure 4", BLUE)]
    for i, (n, s, col) in enumerate(items):
        x = 0.15 + i * 3.3
        a.add_patch(FancyBboxPatch((x, 0.35), 3.05, 2.4,
                                   boxstyle="round,pad=0.03,rounding_size=0.16",
                                   fc=col, ec=INK, lw=3.0, zorder=3))
        a.text(x + 1.52, 1.85, n, ha="center", va="center", fontsize=40,
               fontweight=900, zorder=4)
        a.text(x + 1.52, 0.95, s, ha="center", va="center", fontsize=13,
               fontweight=700, zorder=4)
    a.set_xlim(0, 10); a.set_ylim(0, 3.1); a.axis("off")
    _save(f, "c_headline")


# ═══════════════════════ 18 八步复现流程 ═══════════════════════
def c_steps():
    f, a = _fig(9.2, 4.4)
    steps = ["① 讲清历史与处理时点的外生性",
             "② 把处理定义成二值 + 三种连续强度",
             "③ 基准 2×2 DID：五列固定效应逐步加码",
             "④ 两套标准误：县级聚类 + Conley 时空 HAC",
             "⑤ 前趋势：线性检验 + 事件研究图",
             "⑥ 剂量反应与距离衰减，定出溢出边界",
             "⑦ 安慰剂：替代路线 / 分段 / 剔战区",
             "⑧ 换估计量：CIC + SCM，再谈机制"]
    for i, s in enumerate(steps):
        col = FIVE[i % 5]
        y = 3.55 - i * 0.46
        a.add_patch(FancyBboxPatch((0.06, y - 0.19), 9.88, 0.38,
                                   boxstyle="round,pad=0.02,rounding_size=0.10",
                                   fc=CREAM if i % 2 else CREAM2, ec=INK,
                                   lw=2.4, zorder=2))
        a.add_patch(Rectangle((0.06, y - 0.19), 0.16, 0.38, fc=col, ec=INK,
                              lw=2.4, zorder=3))
        a.text(0.40, y, s, ha="left", va="center", fontsize=14.5,
               fontweight=700, zorder=4)
    a.text(5.0, -0.30, "照这八步走，你也能做出一篇结构完整的 2×2 DID 论文",
           ha="center", fontsize=14, fontweight=900,
           bbox=dict(boxstyle="round,pad=0.45", fc=YELLOW, ec=INK, lw=2.8))
    a.set_xlim(0, 10); a.set_ylim(-0.65, 3.95); a.axis("off")
    _save(f, "c_steps")


# ═══════════════════════ 19–20 statspai 实跑 ═══════════════════════
def _repro():
    p = BASE / "repro" / "results.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def c_repro_es():
    r = _repro()
    if not r or "event_study" not in r:
        print("  ! 跳过 c_repro_es（先跑 repro.py）")
        return
    d = r["event_study"]
    e = np.array(d["e"], float)
    b = np.array(d["estimate"], float)
    lo = np.array(d["conf_low"], float)
    hi = np.array(d["conf_high"], float)
    f, a = _fig(9.2, 4.0)
    a.fill_between(e, lo, hi, color=BLUE, alpha=.20, zorder=2)
    a.plot(e, b, color=INK, lw=3.2, zorder=4)
    a.scatter(e[e < 0], b[e < 0], s=95, color=CREAM2, ec=INK, lw=2.4, zorder=5)
    a.scatter(e[e >= 0], b[e >= 0], s=95, color=PINK, ec=INK, lw=2.4, zorder=5)
    a.axhline(0, color=INK, lw=2.4, ls=(0, (5, 4)), zorder=3)
    a.axvline(0, color=CORAL, lw=3.0, zorder=3)
    a.set_xlabel("事件时间 e = 年份 − 1826（十年分箱）", fontsize=14, fontweight=700)
    a.set_ylabel("ATT(e)", fontsize=14, fontweight=700)
    _clean(a)
    a.set_title("sp.event_study(...)  ·  StatsPAI v%s  ·  模拟面板 140,432 obs"
                % r["statspai_version"], fontsize=13, fontweight=900, pad=10)
    _save(f, "c_repro_es")


def c_repro_bar():
    r = _repro()
    if not r:
        print("  ! 跳过 c_repro_bar（先跑 repro.py）")
        return
    f, a = _fig(9.2, 3.9)
    names = ["论文 Table 3\n列 (1)", "sp.feols\n县FE + 年FE",
             "sp.feols\n+ 省×年 FE", "sp.event_study\n聚合 ATT"]
    vals = [0.0380, r["baseline"]["coef"], r["baseline_provyear"]["coef"],
            r.get("att", np.nan)]
    ses = [0.0166, r["baseline"]["se"], r["baseline_provyear"]["se"], np.nan]
    cols = [CREAM2, PINK, BLUE, MINT]
    x = np.arange(4)
    a.bar(x, vals, width=.6, color=cols, ec=INK, lw=2.8, zorder=3)
    for i, (v, s) in enumerate(zip(vals, ses)):
        if not np.isnan(s):
            a.errorbar(i, v, yerr=1.96 * s, fmt="none", ecolor=INK,
                       elinewidth=2.6, capsize=8, capthick=2.6, zorder=4)
        a.text(i, v + (1.96 * s if not np.isnan(s) else 0) + .004, "%.4f" % v,
               ha="center", fontsize=14, fontweight=900, **MONO)
    a.axhline(0.0380, color=CORAL, lw=2.6, ls=(0, (6, 4)), zorder=2)
    a.set_xticks(x); a.set_xticklabels(names, fontsize=12, fontweight=700)
    a.set_ylabel("AlongCanal × Post", fontsize=14, fontweight=700)
    a.set_ylim(0, max(vals) * 1.55)
    _clean(a)
    a.text(3.45, 0.0362, "论文报告值 0.0380", ha="right", va="top",
           fontsize=12, fontweight=700, color=CORAL)
    _save(f, "c_repro_bar")


ALL = [c_timeline, c_why1826, c_panel, c_2x2, c_ladder, c_es_read, c_intensity,
       c_dist, c_placebo, c_cic, c_mech, c_power, c_honest, c_chenroth,
       c_equiv, c_frontier, c_headline, c_steps, c_repro_es, c_repro_bar]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    print("完成：%d 张 → %s" % (len(list(OUT.glob('*.png'))), OUT))
