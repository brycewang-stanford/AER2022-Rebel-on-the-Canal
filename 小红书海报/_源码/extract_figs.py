# -*- coding: utf-8 -*-
"""从 Cao & Chen (2022, AER) 原文 PDF 中裁出全部 4 张图 + 7 张表（含分面子图）。

坐标单位为 PDF pt（页面 504×720），页码按 PDF 物理页（1 起）；
论文正文页码 = 物理页 + 1554。
"""
import pymupdf, pathlib

BASE = pathlib.Path(__file__).resolve().parent
SRC = (BASE.parent.parent /
       "AER2022-Rebel on the Canal- Disrupted Trade Access and Social Conflict in China.pdf")
OUT = BASE / "figs"
OUT.mkdir(parents=True, exist_ok=True)

# (名字, PDF 页码(1起), (x0,y0,x1,y1) 单位 pt, dpi)
T = [
    # ---------- 图 ----------
    ("fig1_canal_map",    6, (72, 50, 437, 303), 600),   # 运河位置图
    ("fig2_tribute",      8, (95, 52, 412, 242), 700),   # 漕运量趋势
    ("fig3_spatial",     13, (72, 55, 437, 352), 600),   # 叛乱空间分布 前/后
    ("fig3a_before",     13, (72, 55, 258, 352), 800),
    ("fig3b_after",      13, (266, 55, 437, 352), 800),
    ("fig4_eventstudy",  15, (95, 55, 408, 246), 750),   # 事件研究
    # ---------- 表 ----------
    ("tab1_summary",     12, (65, 60, 437, 355), 600),   # 数据来源与描述统计
    ("tab1_sources",     12, (65, 356, 437, 458), 600),  # 数据来源脚注
    ("tab2_pretrend",    16, (98, 60, 406, 254), 750),   # 前趋势
    ("tab3_baseline",    16, (65, 340, 437, 541), 700),  # 基准估计
    ("tab4_intensity",   19, (98, 60, 406, 312), 700),   # 处理强度
    ("tab5_northsouth",  25, (65, 60, 437, 312), 700),   # 南北对照
    ("tab6_placebo",     25, (65, 400, 437, 602), 700),  # 安慰剂
    ("tab7_distortions", 27, (98, 60, 406, 386), 700),   # 重大历史事件
]

if __name__ == "__main__":
    d = pymupdf.open(SRC)
    for name, pg, r, dpi in T:
        pm = d[pg - 1].get_pixmap(clip=pymupdf.Rect(*r), dpi=dpi)
        pm.save(OUT / (name + ".png"))
        print("%-18s p%-3d (AER p.%d) %4d x %4d" % (name, pg, pg + 1554,
                                                    pm.width, pm.height))
