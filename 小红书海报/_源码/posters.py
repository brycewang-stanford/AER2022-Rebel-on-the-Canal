# -*- coding: utf-8 -*-
"""Cao & Chen (2022, AER 112(5): 1555–1590)
《Rebel on the Canal: Disrupted Trade Access and Social Conflict in China, 1650–1911》
—— 50 张小红书竖版海报（Memphis Pop · Sugar Rush 主题）

每一页顶部固定「论文信息条」，底部固定「StatsPAI 仓库条」。
"""

from memphis import (W, H, FIG, CH, AV, CREAM, CREAM2, PINK, BLUE, YELLOW, MINT,
                     CORAL, INK, MUT, FIVE, card, fig, li, avatar, deco, dots,
                     wave, zig, tri, checker, ring, blob)

EXTRA_CSS = f"""
.qa {{ display:flex; gap:16px; align-items:flex-start; }}
.qa .q {{ font-family:'AB',sans-serif; font-size:46px; line-height:1; flex:none;
  width:56px; }}
.tw {{ display:grid; grid-template-columns:auto 1fr; gap:11px 16px;
  align-items:baseline; }}
.tw .k {{ font-family:'JB',monospace; font-size:19px; font-weight:700;
  white-space:nowrap; }}
.tw .v {{ font-size:22px; line-height:1.42; }}
.mini {{ font-size:20px; line-height:1.45; }}
.big-q {{ font-family:'AB','SC',sans-serif; font-size:46px; line-height:1.14; }}
.auth {{ display:flex; gap:22px; align-items:center; border:3px solid {INK};
  border-radius:14px; background:{CREAM}; padding:16px 20px;
  box-shadow:7px 7px 0 {INK}; }}
.auth .nm {{ font-family:'AB','SC',sans-serif; font-size:34px; line-height:1.06; }}
.auth .af {{ font-size:20px; line-height:1.38; margin-top:6px; }}
.auth .cb {{ font-family:'JB',monospace; font-size:16px; margin-top:7px; color:{MUT}; }}
.code {{ background:{INK}; border:3px solid {INK}; border-radius:12px;
  padding:16px 20px; font-family:'JB',monospace; font-size:19px; line-height:1.62;
  color:#E8E8F5; box-shadow:7px 7px 0 rgba(26,26,46,.3); overflow:hidden;
  white-space:pre; }}
.code .c {{ color:#7C7C9E; }}
.code .k {{ color:{PINK}; }}
.code .f {{ color:{YELLOW}; }}
.code .s {{ color:{MINT}; }}
.code .n {{ color:{BLUE}; }}
.out {{ background:{CREAM2}; border:3px solid {INK}; border-radius:12px;
  padding:14px 18px; font-family:'JB',monospace; font-size:18px; line-height:1.55;
  white-space:pre; }}
.out b {{ color:{PINK}; }}
.mapline {{ display:flex; align-items:center; gap:14px; }}
.mapline .no {{ width:52px; height:52px; border-radius:50%; border:3px solid {INK};
  display:flex; align-items:center; justify-content:center; flex:none;
  font-family:'AB',sans-serif; font-size:22px; color:{INK}; }}
.mapline .tt {{ font-family:'AB','SC',sans-serif; font-size:27px; line-height:1.1; }}
.mapline .dd {{ font-size:19px; color:{MUT}; margin-top:3px; }}
.mapline .rg {{ margin-left:auto; font-family:'JB',monospace; font-size:17px;
  color:{MUT}; flex:none; }}
"""

P = []
_N = [0]


def add(stem, inner):
    _N[0] += 1
    P.append(("%02d" % _N[0], stem, inner))


def total():
    return _N[0]


def meta(cn, en=""):
    e = f'<div class="micro mut">{en}</div>' if en else ""
    return f'<div class="micro">{cn}</div>{e}'


def PG(title, m, body, cls="", body_cls="", d=""):
    return (f'{d}<div class="page">__HDR__'
            f'<div class="top"><div class="ttl {cls}">{title}</div>'
            f'<div class="meta">{m}</div></div>'
            f'<div class="body {body_cls}">{body}</div></div>')


def CV(body, d=""):
    return f'{d}<div class="cover">__HDR__{body}</div>'


def station(no, cn, en, bullets, color, pages="", tail=""):
    """站扉页"""
    dd = deco(dots(772, 236, 5, 4, 18, 34, color, .9),
              zig(96, 1176, 78, 108, YELLOW, 1, -12),
              tri(902, 1150, 82, CORAL, 18),
              wave(64, 1082, 280, 48, BLUE, 8),
              ring(838, 418, 148, MINT, 10))
    items = "".join(
        f'<div class="li" style="font-size:25px"><div class="sq" '
        f'style="background:{FIVE[i % 5]}"></div><div>{b}</div></div>'
        for i, b in enumerate(bullets))
    return CV(f"""
  <div style="height:40px"></div>
  <div class="micro xl" style="color:{color}">STATION {no} · P {pages}</div>
  <div class="sec-no" style="color:{color};margin:2px 0 -10px">{no}</div>
  <div class="hero" style="font-size:82px">{cn}</div>
  <div class="micro lg mut" style="margin-top:14px">{en}</div>
  <div style="height:5px;background:{INK};margin:24px 0 26px"></div>
  <div style="display:flex;flex-direction:column;gap:17px">{items}</div>
  <div style="flex:1"></div>
  <div class="bar" style="padding:16px 22px;font-size:23px">{tail}</div>
""", dd)


# ═══════════════════════════════════════════ 01 封面
add("封面", CV(f"""
  <div style="height:52px"></div>
  <div class="hero" style="font-size:200px;letter-spacing:-.035em;line-height:1.0">
    <span style="color:{PINK}">AER</span> <span style="color:{BLUE}">DiD</span></div>
  <div class="hero" style="font-size:200px;letter-spacing:-.035em;line-height:1.06">
    论文解释</div>
  <div style="height:8px;background:{INK};margin:26px 0 24px"></div>
  <div class="hero" style="font-size:90px;letter-spacing:-.02em;line-height:1.1">
    京杭大运河<span style="color:{PINK}">上的叛乱</span></div>

  <div style="flex:1"></div>

  <div class="hero" style="font-size:30px;line-height:1.22;color:{BLUE}">
    REBEL ON THE CANAL: DISRUPTED TRADE<br>
    ACCESS AND SOCIAL CONFLICT IN CHINA</div>
  <div style="font-size:24px;line-height:1.5;margin-top:16px">
    Yiming Cao（曹一鸣） · Shuo Chen（陈硕）<br>
    <span style="color:{MUT}">American Economic Review, 2022, 112(5): 1555–1590</span></div>
  <div class="bar" style="margin-top:26px;margin-bottom:14px;padding:18px 24px;
       font-size:25px;text-align:center">
    50 张全解 · <b>原文 4 图 7 表全裁出</b> · <i>statspai 复现</i>
  </div>
""", deco(zig(880, 900, 92, 130, YELLOW, 1, 12),
          wave(64, 946, 300, 54, BLUE, 9),
          ring(430, 890, 116, CORAL, 10, .95),
          tri(676, 924, 84, MINT, 20))))

# ═══════════════════════════════════════════ 02 第一作者
add("第一作者", PG("第一作者", meta("WHO WROTE IT", "YIMING CAO"), f"""
<div style="display:flex;gap:24px;align-items:flex-start">
  {avatar("cao.png", 250, PINK, 20)}
  <div style="flex:1;display:flex;flex-direction:column;gap:10px">
    <div class="hero" style="font-size:52px">Yiming Cao</div>
    <div class="hero" style="font-size:34px;color:{PINK}">曹一鸣</div>
    <div style="font-size:22px;line-height:1.45">
      香港大学经济与工商管理学院 助理教授<br>
      <span style="color:{MUT}">Boston University 经济学博士（2022）</span></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:2px">
      <span class="chip" style="background:{PINK};color:{CREAM}">发展经济学</span>
      <span class="chip" style="background:{BLUE};color:{CREAM}">政治经济学</span>
      <span class="chip" style="background:{MINT};color:{CREAM}">经济史</span>
    </div>
  </div>
</div>
<div class="panel dk shadow">
  <h4>他关心什么</h4>
  <p>制度与文化如何造成发展障碍 —— 腐败、冲突、国家能力。
     本文是他的 job market paper：用清代 262 年的县级面板，
     把「贸易通道被切断」这件事做成一个干净的准自然实验。</p>
</div>
<div class="g2">
  <div class="card"><div class="strip" style="background:{PINK}"></div>
    <div class="in"><div class="nm sm">AER 2022</div>
      <p>Rebel on the Canal（本文，与陈硕合作）</p></div></div>
  <div class="card"><div class="strip" style="background:{BLUE}"></div>
    <div class="in"><div class="nm sm">AEJ: Policy 2023</div>
      <p>SOEs and Soft Incentive Constraints in State Bank Lending
         （与 Fisman、Lin、Wang 合作）</p></div></div>
</div>
<div class="auth">
  <div class="seal sm mint">陈硕</div>
  <div>
    <div class="nm">Shuo Chen · 通讯作者</div>
    <div class="af">复旦大学经济学院 教授 · 香港科技大学社会科学博士</div>
    <div class="cb">发展经济学 / 政治经济学 / 中国经济史 / 应用微观计量</div>
  </div>
</div>
""", cls="", d=deco(dots(806, 250, 4, 3, 15, 30, YELLOW, .9),
                    tri(940, 1090, 74, CORAL, 20))))

# ═══════════════════════════════════════════ 03 核心模型
add("核心模型", PG("五个核心模型", meta("THE MODELS", "ONE PAGE"), f"""
<div class="panel" style="padding:16px 20px;background:{CREAM2}">
  <div class="eq" style="font-size:22px">
    <span class="k">Y</span><sub>ct</sub> = <span class="k">β</span>·AlongCanal<sub>c</sub>
    × Post<sub>t</sub> + δ<sub>c</sub> + σ<sub>t</sub> + χ<sub>ct</sub> + ε<sub>ct</sub>
  </div>
  <div style="font-size:19px;color:{MUT};margin-top:6px">
    式 (1)：所有其它模型都是这一行的变体。Post = 1[年份 ≥ 1826]</div>
</div>
<div style="display:flex;flex-direction:column;gap:12px">
  {card(PINK, "① 基准 2×2 DID", "式 (1)，≡ Table 3。二值处理 × 单一时点，"
        "五列固定效应逐步加码。", "β = 0.0380 (0.0166) · 5% 显著", "sm")}
  {card(BLUE, "② 事件研究", "式 (2)，≡ Figure 4。把 β 拆成十年一箱的 β<sub>τ</sub>，"
        "参照组是 1826 年前 50 年以上那整段。", "τ ∈ [−50, +70]", "sm")}
  {card(MINT, "③ 前趋势检验", "式 (3)，≡ Table 2。只用 1776–1825 的样本，"
        "估 AlongCanal × 连续年份。", "β ∈ [−0.0003, 0.0003] · 全不显著", "sm")}
  {card(YELLOW, "④ 处理强度", "式 (4)(5)，≡ Table 4。把二值处理换成三种连续剂量："
        "运河长度 / 市镇占比 / 距离。", "0.0200 · 0.0770 · −0.0142", "sm")}
  {card(CORAL, "⑤ 距离衰减与外溢", "式 (6)(7)。按到运河的距离切环带，"
        "找出效应消失的边界。", "溢出边界 ≈ 150 km", "sm")}
</div>
""", cls="sm", d=deco(zig(950, 1150, 74, 104, YELLOW, 1, 16))))

# ═══════════════════════════════════════════ 04 核心亮点
add("核心亮点", PG("为什么是<em>AER</em>", meta("THE HIGHLIGHTS", "5 REASONS"), f"""
<div style="display:flex;flex-direction:column;gap:13px">
  <div class="panel shadow" style="padding:16px 20px">
    <div class="qa"><div class="q" style="color:{PINK}">01</div><div>
      <div class="nm" style="font-family:'AB','SC',sans-serif;font-size:29px">
        问题选得准：扩展边际上的首个因果证据</div>
      <p style="font-size:21px;line-height:1.44;margin-top:5px;color:{MUT}">
        已有文献几乎都在研究贸易量的<b>涨跌</b>（集约边际）且结论互相打架。
        本文研究的是整条通道的<b>永久丧失</b>。</p></div></div>
  </div>
  <div class="panel shadow" style="padding:16px 20px">
    <div class="qa"><div class="q" style="color:{BLUE}">02</div><div>
      <div class="nm" style="font-family:'AB','SC',sans-serif;font-size:29px">
        识别讲得透：1826 为什么外生，用史料说清楚</div>
      <p style="font-size:21px;line-height:1.44;margin-top:5px;color:{MUT}">
        改革派的理由全是成本效率；「社会稳定」是反对派提的。
        再加淮安关税 −30% 与三个替代时点的稳健性。</p></div></div>
  </div>
  <div class="panel shadow" style="padding:16px 20px">
    <div class="qa"><div class="q" style="color:{MINT}">03</div><div>
      <div class="nm" style="font-family:'AB','SC',sans-serif;font-size:29px">
        数据造得狠：536 县 × 262 年 = 14 万个县-年</div>
      <p style="font-size:21px;line-height:1.44;margin-top:5px;color:{MUT}">
        叛乱逐条编码并剔除「蔓延」，GIS 从 CHGIS v4 历史地图算出
        运河长度、市镇缓冲区、距离。</p></div></div>
  </div>
  <div class="panel shadow" style="padding:16px 20px">
    <div class="qa"><div class="q" style="color:{YELLOW}">04</div><div>
      <div class="nm" style="font-family:'AB','SC',sans-serif;font-size:29px">
        处理量得细：从 0/1 到剂量到距离梯度</div>
      <p style="font-size:21px;line-height:1.44;margin-top:5px;color:{MUT}">
        四种处理度量互相印证，还顺手把空间溢出边界定在 150 km。</p></div></div>
  </div>
  <div class="panel shadow" style="padding:16px 20px">
    <div class="qa"><div class="q" style="color:{CORAL}">05</div><div>
      <div class="nm" style="font-family:'AB','SC',sans-serif;font-size:29px">
        稳健性堆得满：换估计量 + 三类安慰剂 + 排机制</div>
      <p style="font-size:21px;line-height:1.44;margin-top:5px;color:{MUT}">
        CIC 与合成控制各跑一遍，替代交通线全部落空，
        Conley 时空 HAC 在 50–2000 km × 20–262 年网格上都显著。</p></div></div>
  </div>
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 05 三个数字
add("一句话结论", PG("一句话结论", meta("THE PUNCHLINE", "3 NUMBERS"), f"""
<div class="bar">
  <span class="h">1826 年，海运替代河运的口子一开</span>
  运河沿线县份就此失去贸易生命线。与远离运河的县相比，
  运河县的叛乱爆发率相对上升 <b>约 117%</b>；效应<u>约 40 年后达峰</u>，
  1870 年代起收敛。<i>受伤最深的是水手、码头工人这些城市流通部门。</i>
</div>
{fig(CH + "c_headline.png")}
<div class="g2">
  <div class="panel dk"><h4>它回答了什么争论</h4>
    <p><b>稳定论</b>：贸易带来收入，抬高造反的机会成本。<br>
       <b>动乱论</b>：贸易繁荣意味着可掠夺的奖品更大。<br>
       <span style="color:{MUT}">本文站稳定论，且是「通道整体丧失」这一侧的首个因果证据。</span></p>
  </div>
  <div class="panel dk"><h4>为什么今天还重要</h4>
    <p>在逆全球化与贸易保护主义抬头的年代，本文提醒：
       切断既有贸易通道的代价不止于经济账，还包括社会与政治稳定，
       而<b>城市流通部门的工人</b>是最先被冲垮的那群人。</p>
  </div>
</div>
""", cls="", d=deco(dots(60, 250, 3, 2, 14, 28, MINT, .8))))

# ═══════════════════════════════════════════ 06 全册地图
_MAP = [("1", "历史与识别", "运河怎么废的，1826 为什么外生", "07–13", PINK),
        ("2", "数据", "536 县 × 262 年的面板怎么造出来", "14–18", BLUE),
        ("3", "五个核心模型", "式 (1)–(7) 与它们对应的表和图", "19–31", MINT),
        ("4", "稳健性与机制", "安慰剂、换估计量、排除竞争解释", "32–39", YELLOW),
        ("5", "现代 DID 视角", "2022 之后该怎么看这篇论文", "40–45", CORAL),
        ("6", "statspai 复现", "五个模型 → 五行 Python", "46–50", PINK)]
add("全册地图", PG("这 50 张<em>怎么走</em>", meta("THE MAP", "6 STATIONS"), f"""
<div style="display:flex;flex-direction:column;gap:15px">
  {"".join(f'''<div class="mapline">
    <div class="no" style="background:{c}">{n}</div>
    <div><div class="tt">{t}</div><div class="dd">{d}</div></div>
    <div class="rg">P {r}</div></div>''' for n, t, d, r, c in _MAP)}
</div>
<div class="panel shadow" style="background:{CREAM2}">
  <h4>怎么用这一册</h4>
  <p>想快速抓住结论 → 看 <b>03 / 04 / 05</b>；<br>
     想学怎么写一篇 2×2 DID → 看 <b>站 3</b> 的十三张；<br>
     想知道 2026 年的审稿人会问什么 → 看 <b>站 5</b>；<br>
     想自己跑一遍 → 看 <b>站 6</b>，代码可以直接抄。</p>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  带 <b>★</b> 的页面是<u>直接从原文 PDF 裁下来的图与表</u> ——
  共 4 张图 + 7 张表，一张不落。
</div>
""", cls="", d=deco(wave(700, 1180, 300, 50, BLUE, 8), tri(64, 1160, 70, MINT, 12))))

# ═══════════════════════════════════════════ 07 站 1
add("站1扉页", station("1", "运河怎么废的", "HISTORY & IDENTIFICATION",
                       ["1,776 公里的人工水道，一年运 350 万石漕粮",
                        "1825 黄河决口 → 1826 首次海运试验 → 此后二十年逐步弃修",
                        "关键问题：为什么处理时点选 1826，而不是 1825 或 1855",
                        "答案藏在廷议记录、关税账本和三个替代时点的稳健性里"], PINK,
                       "07–13",
                       "本站七张：运河的一生 · 1826 的事件链 · 外生性四条 · <b>原文 Figure 1 与 Figure 2</b> · 断航之后"))

# ═══════════════════════════════════════════ 08 运河 262 年
add("运河262年", PG("大运河的<em>一生</em>", meta("THE GRAND CANAL", "1650–1911"), f"""
{fig(CH + "c_timeline.png")}
<div class="g3">
  {card(PINK, "1,776 km", "世界上最古老的人工水道，贯通北京与杭州。", "", "sm")}
  {card(BLUE, "350 万石", "鼎盛期每年北运的漕粮，约 5.6 亿磅。", "", "sm")}
  {card(MINT, "10 ×", "陆运成本约为水运的十倍 —— 断航等于断经济。", "", "sm")}
</div>
<div class="bar">
  <span class="h">「木龙断，天下乱」</span>
  山东民谣。木龙指的就是运河上首尾相接的漕船 ——
  这句话是当地人对断航后果的历史记忆。
</div>
""", cls="", d=deco(dots(60, 250, 3, 2, 14, 28, YELLOW, .85))))

# ═══════════════════════════════════════════ 09 1826 发生了什么
add("1826发生了什么", PG("1826 年<br>到底发生了什么", meta("THE SHOCK", "1826"), f"""
<div class="panel shadow">
  <h4>事件链</h4>
  <p><b>1825</b>　黄河决口，运河淤塞，漕运中断。<br>
     <b>1826</b>　朝廷首次试行<b>海运</b>：从上海走海路运漕粮到天津，一次成功。<br>
     <b>1826 之后</b>　政府一度反悔恢复河运，但此后约二十年<b>逐步放弃维护</b>。<br>
     <b>1855</b>　黄河改道，漕粮河运彻底停止。<br>
     <b>1901</b>　正式宣布废弃大运河。</p>
</div>
<div class="g2">
  <div class="panel dk"><h4>为什么不选 1855？</h4>
    <p>1855 年的彻底停运<b>内生于</b> 1826 年的试验 ——
       正因为海运被证明可行，朝廷才敢在黄河改道后不再修复运河。
       用 1855 会把「反应」当成「冲击」。</p></div>
  <div class="panel dk"><h4>为什么不选 1825？</h4>
    <p>1825 只是一次自然灾害，改革尚未发生，运河仍在修复轨道上。
       真正改变<b>预期</b>的是 1826 —— 海运从此成为随时可启用的替代方案。</p></div>
</div>
<div class="bar">
  <span class="h">处理不是「断航」，是「预期改变」</span>
  1826 之后，商人和水手都知道：这条河，朝廷不会再拼命保了。
</div>
""", cls="xs", d=deco(zig(940, 1140, 76, 108, CORAL, 1, 14))))

# ═══════════════════════════════════════════ 10 外生性
add("外生性四条", PG("凭什么说<em>外生</em>", meta("EXOGENEITY", "4 ARGUMENTS"), f"""
{fig(CH + "c_why1826.png")}
<div class="bar">
  <span class="h">识别的根基就在这四行</span>
  如果 1826 的改革是<i>对已有或预期叛乱的反应</i>，整个 DID 就垮了。
  论文用<u>廷议记录里双方的论据方向</u>做了最关键的一击：
  谈稳定的是反对派，不是改革派。
</div>
<div class="panel dk"><h4>一个容易被忽略的细节</h4>
  <p>1818–1831 年淮安关的税收报告显示，贸易量<b>自 1826 年起下降约 30%</b>。
     这说明商人在政策宣布后<b>立刻</b>改变了行为 ——
     处理效应不需要等到 1855 年河道真正断掉才开始。</p></div>
""", cls="", d=deco(dots(62, 250, 3, 2, 14, 28, BLUE, .85))))

# ═══════════════════════════════════════════ 11 ★ Figure 2
add("★原文Fig2漕运量", PG("★ 原文 Figure 2", meta("CANAL USAGE", "TRIBUTE RICE"), f"""
{fig(FIG + "fig2_tribute.png", "Figure 2. Canal Usage Measured by Tribute Rice "
                               "Transportation（AER p.1562）")}
<div class="g2">
  <div class="panel dk"><h4>怎么读这张图</h4>
    <p>纵轴是漕粮运输量（对数百万石），红色竖线是 <b>1826</b>。
       左边的虚线拟合几乎水平，右边的虚线明显下坠 ——
       这是「1826 是转折点」最直白的一张图。</p></div>
  <div class="panel dk"><h4>它在论文里干什么</h4>
    <p>它不是识别的一部分，而是<b>第一阶段的说服力</b>：
       先让读者相信运河真的从 1826 起被废弃了，
       后面的 reduced-form 才有意义。</p></div>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  自己写论文时的对应动作：<b>先画一张「处理真的发生了」的图</b>，再谈结果变量。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 12 ★ Figure 1
add("★原文Fig1运河位置", PG("★ 原文 Figure 1", meta("WHERE", "THE GRAND CANAL"), f"""
{fig(FIG + "fig1_canal_map.png", "Figure 1. Location of the Grand Canal（AER p.1560）")}
<div class="g3">
  {card(PINK, "6 省", "运河流经或毗邻的六个省份构成研究样本。", "", "sm")}
  {card(BLUE, "北京→杭州", "北段依赖持续维护，废弃后完全断航；南段仍可通航。", "", "sm")}
  {card(MINT, "73 县", "包含或毗邻运河的县 = 处理组。", "", "sm")}
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  南北差异后面会变成一个关键的<u>三重差分安慰剂</u>（见第 35 张）。
</div>
""", cls="sm", d=deco(tri(950, 1120, 72, YELLOW, 16))))

# ═══════════════════════════════════════════ 13 断航的后果
add("断航的后果", PG("断航之后", meta("THE AFTERMATH", "WHAT BROKE"), f"""
<div class="g2">
  {card(PINK, "漕帮解散", "官方雇佣的漕运水手及其行会失去生计。"
        "这些人的人力资本<b>不可迁移</b> —— 会撑船不等于会种地。",
        "运河沿线主要城市的就业群体")}
  {card(BLUE, "免税商品消失", "漕船顺带运载的大量私人商品一并消失，"
        "沿线市镇的商业基础被抽掉。", "陆运成本 ≈ 水运的 10 倍")}
</div>
<div class="g2">
  <div class="panel shadow" style="background:{CREAM2}">
    <h4>临清：一座城的塌方</h4>
    <p>运河重镇临清的人口从<b>二十多万</b>跌到<b>不足五万</b>。
       这不是慢慢衰退，是一代人之内的崩塌。</p>
  </div>
  <div class="panel shadow" style="background:{CREAM2}">
    <h4>北段断得比南段惨</h4>
    <p>北段依赖持续疏浚，弃修后<b>完全断航</b>；
       南段仍能承担江浙到上海的转运 —— 这个差异后面变成一张关键的表。</p>
  </div>
</div>
<div class="bar">
  <span class="h">于是有了论文的因果链</span>
  贸易通道丧失 → <b>城市流通部门失业</b> → 造反的机会成本骤降 →
  <i>叛乱爆发</i>。第 39 张会看到论文怎么把其它解释一条条排掉。
</div>
""", cls="", d=deco(dots(64, 250, 3, 3, 15, 30, CORAL, .85),
                    wave(680, 1190, 300, 50, MINT, 8))))

# ═══════════════════════════════════════════ 14 站 2
add("站2扉页", station("2", "数据怎么造", "THE PANEL",
                       ["575 个县里，536 个进入基准回归",
                        "1650–1911，262 年，一年一格",
                        "1,144 起叛乱「爆发」—— 蔓延不算，只算新起点",
                        "四种处理度量：二值 / 长度 / 市镇占比 / 距离"], BLUE,
                       "14–18",
                       "本站五张：面板结构 · <b>原文 Table 1</b> · 变量定义 · <b>原文 Figure 3</b>"))

# ═══════════════════════════════════════════ 15 面板结构
add("面板结构", PG("面板长什么样", meta("THE DATA", "536 × 262"), f"""
{fig(CH + "c_panel.png")}
<div class="g2">
  <div class="panel dk"><h4>为什么除以 1600 年人口</h4>
    <p>用<b>处理前很久</b>的人口做分母，避免分母本身被处理影响 ——
       这是历史面板里的常规做法，也是一个值得学的小技巧。</p></div>
  <div class="panel dk"><h4>为什么做 arcsinh</h4>
    <p>叛乱数极度右偏且大量为零，log 不能取。arcsinh 能处理零值 ——
       但这个选择在 2024 年后有了新的争议（见第 45 张）。</p></div>
</div>
<div class="panel shadow" style="background:{CREAM2}">
  <h4>「爆发」为什么要单独定义</h4>
  <p>如果把已有叛军的<b>蔓延</b>也算进来，一场太平天国能把整个华南的格子都点亮，
     结果变量就变成了「战争地理」而不是「新冲突的发生」。
     论文只计入<b>新起事件</b> —— 262 年里一共 1,144 起。</p>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  GIS 底图来自 <b>CHGIS v4</b>（哈佛燕京学社 &amp; 复旦史地中心 2007）。
</div>
""", cls=""))

# ═══════════════════════════════════════════ 16 ★ Table 1
add("★原文Tab1描述统计", PG("★ 原文 Table 1", meta("SUMMARY STATS", "SOURCES"), f"""
{fig(FIG + "tab1_summary.png", "Table 1—Data Sources and Summary Statistics（AER p.1566）")}
<div class="panel dk" style="padding:14px 18px">
  <p style="font-size:21px">九类史料拼出这张表：<b>清实录</b>（叛乱）· CHGIS 历史地图（地理）·
     Mann 等 2009（气候）· 陈硕与孔鹏 2016 · Nunn &amp; Qian 2012（新作物）·
     梁方仲 1980（人口）· 罗 1984 · IIASA &amp; FAO 2012（土地适宜度）·
     《青帮通草会海》（青帮成员）。</p>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  学它的地方：把每个变量的<u>来源编号</u>写进表里 —— 审稿人不用翻正文就知道数据从哪来。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 17 变量定义
add("变量定义", PG("因变量与<em>四种处理</em>", meta("VARIABLES", "Y AND D"), f"""
<div class="panel shadow" style="background:{CREAM2}">
  <h4>因变量 Y<sub>ct</sub></h4>
  <div class="eq" style="font-size:22px;margin-top:4px">
    Y<sub>ct</sub> = arcsinh( <span class="k">叛乱爆发数</span><sub>ct</sub> /
    <span class="b">1600 年人口（百万）</span><sub>c</sub> )</div>
  <p style="font-size:20px;margin-top:8px;color:{MUT}">
    「爆发」= 新起事件，已有叛军的蔓延不重复计入。样本均值 0.0330。</p>
</div>
<div style="display:flex;flex-direction:column;gap:12px">
  {card(PINK, "① 二值：AlongCanal", "县是否包含或毗邻运河。73 个县 = 1。",
        "Table 3 的主力", "sm")}
  {card(BLUE, "② 地理依赖：CanalLength", "县内运河长度 / 100 km²，均值 32.45 km。",
        "Table 4 列 (1)", "sm")}
  {card(MINT, "③ 经济依赖：CanalTownShare", "运河 10 km 内的市镇占全县市镇的比例，均值 50%。",
        "Table 4 列 (2)", "sm")}
  {card(YELLOW, "④ 距离：DistanceToCanal", "县治到运河的直线距离，均值 118 km，最远 499 km。",
        "Table 4 列 (3)", "sm")}
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  控制变量：地形崎岖度 · 1600 年人口密度 · 温度异常 · 旱涝 · 稻麦适宜度 · 新作物引种时间。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 18 ★ Figure 3
add("★原文Fig3空间分布", PG("★ 原文 Figure 3", meta("BEFORE / AFTER", "SPATIAL"), f"""
{fig(FIG + "fig3_spatial.png",
     "Figure 3. The Spatial Distribution of Rebellions before and after the "
     "Abandonment（AER p.1567）")}
<div class="g2">
  <div class="panel dk"><h4>左图：1826 之前</h4>
    <p>叛乱零星分布，与运河线没有明显关系。</p></div>
  <div class="panel dk"><h4>右图：1826 之后</h4>
    <p>深色格子明显沿着<b>运河北段</b>聚集 —— 从北京、天津、临清一路到济宁。</p></div>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  这张图不构成识别，但它<u>先把结论摆在读者眼前</u>，后面的回归只是把它量化。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 19 站 3
add("站3扉页", station("3", "五个模型", "THE CORE MODELS",
                       ["式 (1)：基准 2×2 DID —— 一个处理时点，最干净的形式",
                        "式 (2)：事件研究 —— 把一个 β 拆成十三个",
                        "式 (3)：前趋势 —— 只用改革前 50 年",
                        "式 (4)–(7)：剂量反应与距离衰减"], MINT,
                       "19–31",
                       "本站十三张：把式 (1)–(7) 逐个拆开，配上 <b>原文 Table 2 / 3 / 4 与 Figure 4</b>"))

# ═══════════════════════════════════════════ 20 2×2 四格
add("2x2四个格子", PG("2×2 的<em>四个格子</em>", meta("THE ENGINE", "2 × 2 DID"), f"""
{fig(CH + "c_2x2.png")}
<div class="panel shadow" style="background:{CREAM2}">
  <h4>为什么这篇论文的设定特别干净</h4>
  <p>所有处理单位在<b>同一年（1826）</b>同时被处理 —— 没有交错采纳（staggered adoption），
     就没有 2018 年之后 DID 文献反复讨论的负权重与 forbidden comparison。
     这一点会在第 41 张详细展开。</p>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  固定效应做的事：<b>δ<sub>c</sub></b> 吸收 A/C 的水平差异，<b>σ<sub>t</sub></b> 吸收全国共同冲击。
</div>
""", cls=""))

# ═══════════════════════════════════════════ 21 模型①
add("模型①基准式1", PG("模型 ①：<em>式 (1)</em>", meta("EQ (1)", "BASELINE DID"), f"""
<div class="panel shadow" style="background:{CREAM2}">
  <div class="eq">
    <span class="k">Y</span><sub>ct</sub> = <span class="k">β</span> ·
    AlongCanal<sub>c</sub> × Post<sub>t</sub>
    + <span class="b">δ<sub>c</sub></span> + <span class="g">σ<sub>t</sub></span>
    + <span class="o">χ<sub>ct</sub></span> + ε<sub>ct</sub></div>
</div>
<div class="tw">
  <div class="k">Y<sub>ct</sub></div>
  <div class="v">arcsinh( 县 c 在年 t 的叛乱爆发数 / 1600 年人口百万 )</div>
  <div class="k">AlongCanal<sub>c</sub></div>
  <div class="v">县 c 是否包含或毗邻运河（0/1），<b>不随时间变</b> → 被 δ<sub>c</sub> 吸收</div>
  <div class="k">Post<sub>t</sub></div>
  <div class="v">1[ t ≥ 1826 ]，<b>不随县变</b> → 被 σ<sub>t</sub> 吸收</div>
  <div class="k">β</div>
  <div class="v">交互项系数 = <b>ATT</b>，唯一能被识别出来的那个数</div>
  <div class="k">δ<sub>c</sub></div>
  <div class="v">县固定效应：吸收所有不随时间变化的县层面因素</div>
  <div class="k">σ<sub>t</sub></div>
  <div class="v">年固定效应：吸收所有全国同步的时间冲击</div>
  <div class="k">χ<sub>ct</sub></div>
  <div class="v">五种逐步加码的控制结构（下一张详解）</div>
</div>
<div class="bar">
  <span class="h">识别假定只有一条</span>
  如果 1826 没有发生，运河县与非运河县的叛乱率会<b>沿着平行的路径</b>走下去。
  这条假定不可检验 —— 论文用式 (3) 与式 (2) 从两个角度间接支持它。
</div>
""", cls="sm", d=deco(dots(60, 250, 3, 2, 14, 28, MINT, .8))))

# ═══════════════════════════════════════════ 22 五列控制
add("五列控制在防什么", PG("五列控制<br><em>各防一件事</em>", meta("EQ (1)", "χct"), f"""
<div style="display:flex;flex-direction:column;gap:12px">
  {card(PINK, "(1) 县 FE + 年 FE", "最朴素的双向固定效应。"
        "<b>防不了</b>：某些县本来就对 19 世纪的动荡更敏感。", "β = 0.0380", "sm")}
  {card(BLUE, "(2) + 前处理叛乱 × 年 FE", "让「本来就爱乱」的县对每一年的共同冲击"
        "有<b>自己的反应系数</b>。这一列专治「处理组本来就不一样」。", "β = 0.0369", "sm")}
  {card(MINT, "(3) + 省 × 年 FE", "吸收省级共同冲击 —— 比较只发生在<b>同省内部</b>。",
        "β = 0.0453", "sm")}
  {card(YELLOW, "(4) + 府级线性时间趋势", "允许每个府沿着自己的斜率走。"
        "这是对「趋势不平行」最直接的让步。", "β = 0.0427", "sm")}
  {card(CORAL, "(5) + 控制变量 × Post", "让地形、人口密度、气候等在废弃前后"
        "有<b>不同的效应</b>。", "β = 0.0340", "sm")}
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  五列的意义不在于哪一列「最对」，而在于<b>系数在五种设定下都不动</b>。
</div>
""", cls="xs"))

# ═══════════════════════════════════════════ 23 ★ Table 3
add("★原文Tab3基准", PG("★ 原文 Table 3", meta("BASELINE", "TABLE 3"), f"""
{fig(FIG + "tab3_baseline.png",
     "Table 3—Canal Closure and Rebellions: Baseline Estimates（AER p.1570）")}
<div class="g2">
  <div class="panel dk"><h4>圆括号 vs 方括号</h4>
    <p><b>( )</b> = 县级聚类标准误（536 个 cluster）<br>
       <b>[ ]</b> = <b>Conley 时空 HAC</b>：500 km 空间截断 + 262 年序列相关</p></div>
  <div class="panel dk"><h4>怎么快速扫这张表</h4>
    <p>先看第一行五个系数是否同号同量级，再看下方 FE 勾选行 ——
       这两块决定了这张表的说服力。</p></div>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  β ∈ [0.0340, 0.0453]，<b>五列全部 5% 显著</b>。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 24 系数阶梯
add("系数阶梯", PG("五列画成一张图", meta("TABLE 3", "AS A CHART"), f"""
{fig(CH + "c_ladder.png")}
<div class="panel shadow" style="background:{CREAM2}">
  <h4>为什么要自己再画一遍</h4>
  <p>表格看的是<b>数字</b>，图看的是<b>稳定性</b>。
     把五列画成带置信区间的柱子，读者一眼就能判断
     「这个结果是不是靠某一种设定撑起来的」。
     写论文时这张图放附录，做汇报时这张图放正片。</p>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  注意列 (3) 反而最大（0.0453）—— 省内比较把噪音去掉后，效应更清楚。
</div>
""", cls=""))

# ═══════════════════════════════════════════ 25 系数翻译
add("系数怎么读", PG("0.0380 <em>是多少</em>", meta("INTERPRETATION", "0.0380"), f"""
<div class="panel shadow">
  <h4>论文自己的换算</h4>
  <p>arcsinh 变换下，exp(0.0380) − 1 ≈ <b>0.0387</b>；
     样本均值是 0.0330 → 相对增幅 ≈ <b>117%</b>。</p>
</div>
<div class="panel dk"><h4>翻译成一个故事</h4>
  <p>运河县 1650–1825 年平均每百万人每年约 <b>1.6</b> 起叛乱；
     1826 后相对增幅 117% → 约 <b>3.5</b> 起；增量约 1.9 起 / 百万人·年。<br>
     运河沿线约 7,000 万人 → <b>每年多出约 130 起叛乱</b>（粗估），
     1870 年代后逐渐回落。</p></div>
<div class="bar">
  <span class="h">⚠ 但这个「117%」在 2024 年之后要打折</span>
  Chen &amp; Roth (2024, <i>QJE</i>) 证明：含零结果的 arcsinh / log(1+y) 变换，
  其 ATT <b>依赖结果变量的计量单位</b> —— 把「每百万人」换成「每万人」，
  系数会不成比例地变化。<u>正确做法见第 45 张。</u>
</div>
""", cls="", d=deco(zig(950, 1120, 74, 104, CORAL, 1, 14))))

# ═══════════════════════════════════════════ 26 两套标准误
add("两套标准误", PG("两套<em>标准误</em>", meta("INFERENCE", "SE"), f"""
<div class="g2">
  {card(PINK, "县级聚类 SE", "允许同一个县在 262 年里的误差任意相关。"
        "536 个 cluster —— 数量充足，不需要 wild bootstrap 救场。",
        "Table 3 的圆括号")}
  {card(BLUE, "Conley 时空 HAC", "同时允许<b>空间</b>相关（500 km 内的县互相相关）"
        "与<b>时间</b>相关（最长 262 年）。实现来自 Hsiang (2010) 的 spatial_HAC。",
        "Table 3 的方括号")}
</div>
<div class="panel shadow" style="background:{CREAM2}">
  <h4>为什么这篇论文非做 Conley 不可</h4>
  <p>叛乱天然会<b>空间外溢</b> —— 隔壁县起事，这个县也容易被波及。
     只做县级聚类会低估标准误。论文还在
     <b>距离 50–2000 km × 时间 20–262 年</b> 的带宽网格上逐一检查，
     t 值全程显著。</p>
</div>
<div class="bar">
  <span class="h">这一项论文做得比 2026 年的平均水平还好</span>
  Conley 时空 HAC 在今天仍是空间面板的标配 —— <i>这里没有可批评的地方。</i>
</div>
""", cls="", d=deco(dots(62, 250, 3, 2, 14, 28, BLUE, .8))))

# ═══════════════════════════════════════════ 27 模型②
add("模型②事件研究式2", PG("模型 ②：<em>式 (2)</em>", meta("EQ (2)", "EVENT STUDY"), f"""
<div class="panel shadow" style="background:{CREAM2}">
  <div class="eq sm">
    <span class="k">Y</span><sub>ct</sub> = Σ<sub>τ=−50</sub><sup>70</sup>
    <span class="k">β<sub>τ</sub></span> · AlongCanal<sub>c</sub> ×
    Decade<sup>τ</sup><sub>t</sub>
    + δ<sub>c</sub> + σ<sub>t</sub> + χ<sub>ct</sub> + ε<sub>ct</sub></div>
</div>
<div style="display:flex;flex-direction:column;gap:12px">
  {card(PINK, "把一个 β 拆成十三个", "τ 按<b>十年一箱</b>，从 −50 一直到 +70。"
        "每个 β<sub>τ</sub> 是那个十年里运河县相对非运河县的差异。", "", "sm")}
  {card(BLUE, "参照组是「1826 前 50 年以上」那<b>整段</b>",
        "不是某一个单期。这样做能降低参照期本身的抽样噪音 ——"
        "长面板里很实用的一个选择。", "", "sm")}
  {card(MINT, "十年分箱是为了看清波动",
        "262 年逐年估会太噪；十年分箱刚好能显示出「倒 V」这个关键形状。",
        "", "sm")}
</div>
<div class="bar">
  <span class="h">事件研究图有两个用途，别混了</span>
  <b>τ &lt; 0 的部分</b>用来支持平行趋势；
  <i>τ ≥ 0 的部分</i>用来看动态效应。前者是识别，后者是结果。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 28 ★ Figure 4
add("★原文Fig4事件研究", PG("★ 原文 Figure 4", meta("EVENT STUDY", "FIGURE 4"), f"""
{fig(FIG + "fig4_eventstudy.png",
     "Figure 4. Canal Closure and Rebellions: Event Study（AER p.1569）")}
<div class="g2">
  <div class="panel dk"><h4>横轴</h4>
    <p>距 1826 年改革的年数，−50 到 +70，十年一箱。</p></div>
  <div class="panel dk"><h4>灰带</h4>
    <p>95% 置信区间。1826 之前几乎全部覆盖 0 线。</p></div>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  下一张把这张图的四个关键读点标出来。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 29 事件研究怎么读
add("事件研究怎么读", PG("这张图<em>怎么读</em>", meta("HOW TO READ", "4 POINTS"), f"""
{fig(CH + "c_es_read.png")}
<div class="g2">
  <div class="panel dk"><h4>倒 V 不是噪音</h4>
    <p>1836–45 的回落对应<b>河运一度恢复</b>那段历史 ——
       形状和史实对上了，这比系数显著更有说服力。</p></div>
  <div class="panel dk"><h4>40 年才达峰</h4>
    <p>永久性冲击打击城市部门的典型动态：先急升，几十年后达峰，
       等到人们调整预期、另谋出路，才慢慢收敛。</p></div>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  写作提示：<b>把事件研究图的形状和历史叙事对上</b> —— 这是审稿人最买账的一种论证。
</div>
""", cls=""))

# ═══════════════════════════════════════════ 30 模型③ + Table 2
add("模型③前趋势", PG("模型 ③：<em>式 (3)</em>", meta("EQ (3)", "PRE-TRENDS"), f"""
<div class="panel" style="background:{CREAM2};padding:14px 18px">
  <div class="eq sm">
    <span class="k">Y</span><sub>ct</sub> = <span class="k">β</span> ·
    AlongCanal<sub>c</sub> × <span class="b">Year<sub>t</sub></span>
    + δ<sub>c</sub> + σ<sub>t</sub> + χ<sub>ct</sub> + ε<sub>ct</sub>,
    &nbsp; t ∈ [1776, 1825]</div>
</div>
{fig(FIG + "tab2_pretrend.png",
     "Table 2—Canal Closure and Rebellions: Pretreatment Trends（AER p.1570）")}
<div class="bar">
  <span class="h">只用改革前 50 年，估一条「趋势差」</span>
  四列结构下 β ∈ [−0.0003, 0.0003]，<b>全部接近零且不显著</b>。
  <i>但请记住第 43 张：不显著 ≠ 平行趋势成立。</i>
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 31 模型④⑤ + Table 4
add("模型④⑤强度", PG("模型 ④⑤：<em>剂量</em>", meta("EQ (4)–(7)", "INTENSITY"), f"""
<div class="panel" style="background:{CREAM2};padding:14px 18px">
  <div class="eq sm">
    <span class="k">Y</span><sub>ct</sub> = <span class="k">β</span> ·
    <span class="b">CanalIntensity<sub>c</sub></span> × Post<sub>t</sub>
    + δ<sub>c</sub> + σ<sub>t</sub> + χ<sub>ct</sub> + ε<sub>ct</sub></div>
</div>
{fig(FIG + "tab4_intensity.png",
     "Table 4—Canal Closure and Rebellions: Treatment Intensities（AER p.1573）")}
<div class="bar" style="padding:14px 20px;font-size:22px">
  三列换三种剂量：<b>运河长度</b> · <b>市镇占比</b> · <b>距离</b>。
  非参数版本（式 5、7）显示运河长度 &lt; 2 km/100km² 的县与参照组无异。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 32 站 4
add("站4扉页", station("4", "稳不稳", "ROBUSTNESS & MECHANISMS",
                       ["剂量反应：越依赖运河，受创越重",
                        "空间外溢：效应到 150 km 就消失",
                        "三类安慰剂：南北分段 / 替代交通线 / 剔除战区",
                        "换估计量：CIC 与合成控制各跑一遍",
                        "机制：排除镇压能力，确认城市失业"], YELLOW,
                       "32–39",
                       "本站八张：剂量反应 · 150 km 边界 · <b>原文 Table 5 / 6 / 7</b> · CIC 与 SCM · 机制"))

# ═══════════════════════════════════════════ 33 强度三条
add("强度三条", PG("越依赖，<em>越惨</em>", meta("DOSE RESPONSE", "TABLE 4"), f"""
{fig(CH + "c_intensity.png")}
<div class="g2">
  <div class="panel dk"><h4>地理依赖</h4>
    <p>县内运河越长，叛乱增加越多。0.0200（5% 显著）。</p></div>
  <div class="panel dk"><h4>经济依赖</h4>
    <p>10 km 内市镇占比越高，受创越重。0.0770 —— 三者里最大。</p></div>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  这组结果把「运河县」这个标签替换成了<b>可度量的经济依赖程度</b> —— 因果故事更硬。
</div>
""", cls=""))

# ═══════════════════════════════════════════ 34 距离衰减
add("距离衰减150km", PG("效应走多远", meta("SPILLOVER", "150 KM"), f"""
{fig(CH + "c_dist.png")}
<div class="panel shadow" style="background:{CREAM2}">
  <h4>为什么这件事很重要</h4>
  <p>如果溢出到 150 km，那基准回归里 0–150 km 的「非运河县」<b>其实也被部分处理了</b>。
     控制组被同向污染 → 基准 β 是<b>保守的低估</b>。
     论文的合成控制已经把 donor pool 限制在 ≥ 150 km，
     只差把同样的逻辑搬回基准 TWFE（见第 42 张的 donut DID）。</p>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  自己写论文时：<b>先估出溢出边界，再决定控制组怎么切</b>。
</div>
""", cls=""))

# ═══════════════════════════════════════════ 35 ★ Table 5
add("★原文Tab5南北", PG("★ 原文 Table 5", meta("NORTH VS SOUTH", "TABLE 5"), f"""
{fig(FIG + "tab5_northsouth.png",
     "Table 5—Canal Closure and Rebellions: North versus South（AER p.1579）")}
<div class="panel shadow">
  <h4>一个设计得很漂亮的三重差分</h4>
  <p>运河<b>北段</b>依赖持续维护，废弃后完全断航；
     <b>南段</b>仍可承担江浙到上海的转运。
     如果效应真的来自「贸易通道丧失」，那它应该<b>只出现在北段</b>。</p>
</div>
<div class="bar">
  <span class="h">结果正如预期</span>
  三重交互项 β<sub>2</sub> ∈ <b>[0.0687, 0.0998]</b>（1% 显著），
  而南段的 AlongCanal × Post 接近零。
  <i>这是全文最有说服力的一张表。</i>
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 36 ★ Table 6 安慰剂
add("★原文Tab6安慰剂", PG("★ 原文 Table 6", meta("PLACEBO", "TABLE 6"), f"""
{fig(FIG + "tab6_placebo.png",
     "Table 6—Canal Closure and Rebellions: Placebo Treatments（AER p.1579）")}
{fig(CH + "c_placebo.png")}
<div class="bar" style="padding:14px 20px;font-size:22px">
  换成长江 / 黄河 / 海岸线 / 驿道去做「假处理」，
  <b>× Post 全部不显著</b> —— 说明结果不是「沿着任意一条交通线都会出现」的伪相关。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 37 ★ Table 7
add("★原文Tab7重大事件", PG("★ 原文 Table 7", meta("MAJOR DISTORTIONS", "TABLE 7"), f"""
{fig(FIG + "tab7_distortions.png",
     "Table 7—Canal Closure and Rebellions: Major Distortions（AER p.1581）")}
<div class="g2">
  <div class="panel dk"><h4>Panel A</h4>
    <p>剔除鸦片战争战区的县 —— 系数<b>不降反增</b>（0.0438 → 0.1032）。</p></div>
  <div class="panel dk"><h4>Panel B</h4>
    <p>显式控制太平天国交互项 —— 主系数依然稳（0.0437 / 0.1034）。</p></div>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  19 世纪中国最大的两场动荡都不是本文效应的来源。<b>这一关必须过。</b>
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 38 CIC + SCM
add("换估计量CIC与SCM", PG("换两个<em>估计量</em>", meta("CIC & SCM", "ALTERNATIVES"), f"""
{fig(CH + "c_cic.png")}
<div class="g2">
  {card(PINK, "CIC（Athey–Imbens 2006）",
        "两步法（Melly–Santangelo 2015）：先 OLS 残差化，再对残差做无条件 CIC，"
        "恢复<b>整个反事实分布</b>上的分位数处理效应。", "放松「分布同形」假设", "sm")}
  {card(BLUE, "SCM（Cavallo 等 2013）",
        "为每个运河县单独构造合成控制，donor pool 限制在<b>距运河 ≥ 150 km</b>，"
        "加总得 ATT，用随机化推断做检验。", "放松平行趋势", "sm")}
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  SCM 的一个副产品：合成出来的「非运河县」30 年后也出现叛乱高峰 ——
  <b>全国性动荡是真的，但运河县更惨。</b>
</div>
""", cls=""))

# ═══════════════════════════════════════════ 39 机制
add("机制排除", PG("到底是<em>为什么</em>", meta("MECHANISMS", "4 CHECKS"), f"""
{fig(CH + "c_mech.png")}
<div class="bar">
  <span class="h">留下来的解释只有一个</span>
  贸易可达性丧失 → <b>城市流通部门失业</b> → 造反的机会成本骤降。
  <i>水手会撑船，不会种地 —— 人力资本不可迁移，这才是关键。</i>
</div>
<div class="panel dk" style="padding:14px 18px">
  <p style="font-size:21px">一个耐人寻味的长期回响：<b>青帮</b>高阶成员的出生地
     高度集中在运河沿线 —— 论文明确说明这是横截面相关，不是因果。</p>
</div>
""", cls=""))

# ═══════════════════════════════════════════ 40 站 5
add("站5扉页", station("5", "2026 年怎么看", "THE MODERN LENS",
                       ["好消息：2×2 设定下，TWFE 与 CS / SA / BJS 数学等价",
                        "所以「为什么不用交错采纳估计量」不构成批评",
                        "坏消息：2022 之后 DID 的重心换到了另外四条线",
                        "这四条 —— 平行趋势、函数形式、连续剂量、空间溢出 —— 都适用于本文"], CORAL,
                       "40–45",
                       "本站六张：五者等价 · 四条前线 · Roth power · honest DID · Chen-Roth"))

# ═══════════════════════════════════════════ 41 等价
add("五者等价", PG("不该被批评的地方", meta("EQUIVALENCE", "2 × 2"), f"""
{fig(CH + "c_equiv.png")}
<div class="panel shadow" style="background:{CREAM2}">
  <h4>为什么等价</h4>
  <p>Callaway–Sant'Anna、Sun–Abraham、Borusyak 等人的插补估计量、Wooldridge ETWFE，
     解决的是<b>交错采纳</b>带来的两个病：已处理组被当成对照（forbidden comparison），
     以及权重可能为负。<br>
     本文所有处理单位在 1826 年<b>同时</b>被处理 —— 这两个病根本不会发生。</p>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  在 2×2 设定里强行套 CS，不会改变系数，只会多花五倍算力。
</div>
""", cls=""))

# ═══════════════════════════════════════════ 42 四条前线
add("现代DID四条前线", PG("2022 之后的<em>四条线</em>", meta("FRONTIERS", "2022–2026"), f"""
{fig(CH + "c_frontier.png")}
<div class="g2">
  <div class="panel dk"><h4>论文缺的（必补）</h4>
    <p><b>①</b> 前趋势 power 评估<br><b>②</b> honest DID 敏感性分析</p></div>
  <div class="panel dk"><h4>论文该改口径的（易补）</h4>
    <p><b>③</b> 把 FE Poisson 升级为 headline<br>
       <b>④</b> 声明 Table 4 依赖 strong parallel trends</p></div>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  加分项：基准表补一列 <b>donut DID</b>（剔除 0–150 km 环带），
  再跑一遍 <b>SDID</b> 或 <b>LP-DiD</b>。
</div>
""", cls="sm"))

# ═══════════════════════════════════════════ 43 power
add("前趋势power", PG("「不显著」<br><em>不是证据</em>", meta("ROTH 2022", "POWER"), f"""
{fig(CH + "c_power.png")}
<div class="panel shadow">
  <h4>Roth (2022, <i>AER: Insights</i>) 的警告</h4>
  <p>前趋势检验常常<b>严重 underpowered</b>：即使平行趋势已被大幅违反，
     检验仍可能给出「不显著」。论文式 (3) 只报告了「β 接近 0 且不显著」，
     没有报告<b>这个检验有多大能力发现问题</b>。</p>
</div>
<div class="bar">
  <span class="h">该补什么</span>
  在 1826 前每 10 年的子样本上重复前趋势检验，
  并报告「若真实存在 1 SE 的趋势违反，检验有多大概率拒绝」。
  <i>如果 power 偏低 —— 就必须做下一张的敏感性分析。</i>
</div>
""", cls="xs"))

# ═══════════════════════════════════════════ 44 honest DID
add("honestDID", PG("结论能扛<em>多大偏差</em>", meta("RAMBACHAN-ROTH 2023", "HONEST DID"), f"""
{fig(CH + "c_honest.png")}
<div class="panel shadow" style="background:{CREAM2}">
  <h4>怎么读 breakdown M*</h4>
  <p>M̄ 是允许的「post 期平行趋势偏离」相对于「pre 期最大偏离」的倍数。
     代入论文报告值后 <b>M* ≈ 1.9</b> —— 意思是：<br>
     只要 post 期的趋势破坏不超过 pre 期最大偏离的 <b>1.9 倍</b>，
     0.0380 这个结论仍然成立。</p>
</div>
<div class="bar">
  <span class="h">这才是一句可信的话</span>
  比「前趋势不显著所以平行趋势成立」强得多 ——
  它把<i>可信度量化</i>成一个数字，让读者自己判断 1.9 倍够不够。
</div>
""", cls="xs"))

# ═══════════════════════════════════════════ 45 Chen-Roth
add("ChenRoth零值", PG("「117%」<em>要改口</em>", meta("CHEN & ROTH 2024", "LOGS WITH ZEROS"), f"""
{fig(CH + "c_chenroth.png")}
<div class="panel shadow">
  <h4>修复成本最低的一件事</h4>
  <p>论文附录<b>已经跑过 FE Poisson</b>。要做的只是把它从附录搬到正文，
     用 exp(β̂) − 1 作为 headline 百分比效应，
     再补一列扩展边际 LPM（因变量 = 1[当年有叛乱]）。
     结论方向不会变，只是数字要换个说法。</p>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  在 statspai 里就是一行：<b>sp.fepois("rebellions ~ canal_post | county + year", ...)</b>
</div>
""", cls="xs"))

# ═══════════════════════════════════════════ 46 八步流程
add("八步流程", PG("照这八步<br><em>你也能写</em>", meta("THE RECIPE", "8 STEPS"), f"""
{fig(CH + "c_steps.png")}
<div class="bar">
  <span class="h">这篇论文真正值得抄的不是结论，是结构</span>
  一个干净的 2×2 DID 故事，靠的是<b>把每一个「你怎么知道」都提前answered</b>：
  时点为什么外生、控制组会不会被污染、换个估计量还成不成立、
  <i>有没有别的机制能解释</i>。
</div>
<div class="g2">
  <div class="panel dk"><h4>最省力的抄法</h4>
    <p>找一个<b>单一时点、二值处理</b>的政策冲击，
       按 ①–⑧ 逐条落地 —— 这是一篇结构完整论文的最短路径。</p></div>
  <div class="panel dk"><h4>2026 年记得加的两步</h4>
    <p>在 ⑤ 之后插入 <b>Roth power</b> 与 <b>honest DID</b>；
       结果变量含大量零值时，headline 用 <b>FE Poisson</b>。</p></div>
</div>
""", cls="xs"))

# ═══════════════════════════════════════════ 47 statspai 五行代码
add("statspai五行代码", PG("五个模型<br><em>五行代码</em>", meta("STATSPAI", "v1.22.0"), f"""
<div class="code">
<span class="c"># pip install statspai</span>
<span class="k">import</span> statspai <span class="k">as</span> sp

<span class="c">① 基准 2×2 DID —— 式 (1) ≡ Table 3</span>
m1 = sp.<span class="f">feols</span>(<span class="s">"y ~ canal_post | county + year"</span>,
              data=df, vcov={{<span class="s">"CRV1"</span>: <span class="s">"county"</span>}})

<span class="c">② 事件研究 —— 式 (2) ≡ Figure 4，十年分箱</span>
es = sp.<span class="f">event_study</span>(df, y=<span class="s">"y"</span>, treat_time=<span class="s">"first_treat"</span>,
                    time=<span class="s">"year"</span>, unit=<span class="s">"county"</span>,
                    window=(<span class="n">-50</span>, <span class="n">70</span>), bin_width=<span class="n">10</span>)

<span class="c">③ 前趋势 —— 式 (3) ≡ Table 2（只用 1776–1825）</span>
m3 = sp.<span class="f">feols</span>(<span class="s">"y ~ canal_year | county + year"</span>, data=pre)

<span class="c">④ 现代补充：前趋势检验的 power（Roth 2022）</span>
sp.<span class="f">pretrends_power</span>(es)

<span class="c">⑤ 现代补充：honest DID（Rambachan-Roth 2023）</span>
sp.<span class="f">honest_did</span>(es, e=<span class="n">30</span>, method=<span class="s">"relative_magnitude"</span>)
</div>
<div class="g2">
  {card(PINK, "为什么值得试", "论文里 Stata 要装 reghdfe + spatial_HAC + 一堆 ado；"
        "statspai 把 DID 全家桶做进一个 Python 包。", "", "sm")}
  {card(MINT, "AI 原生", "每个结果都能 <b>as_handle</b> 拿到 result_id，"
        "直接喂给下游的稳健性检查工具链。", "", "sm")}
</div>
""", cls="xs", d=deco(dots(60, 250, 3, 2, 14, 28, YELLOW, .8))))

# ═══════════════════════════════════════════ 48 实跑结果
add("statspai实跑系数", PG("真的跑了一遍", meta("REPRODUCTION", "RUN"), f"""
{fig(CH + "c_repro_bar.png")}
<div class="panel shadow" style="background:{CREAM2}">
  <h4>⚠ 请注意这是什么数据</h4>
  <p>论文的分析面板（openICPSR 157781-V1）不随本仓库分发，
     这里用的是一份<b>按论文报告值标定的模拟面板</b>：
     536 县 × 262 年 = 140,432 个县-年，73 个运河县，处理时点 1826，
     真实 ATT 设为 0.0380，动态形状按 Figure 4 标定。<br>
     <b>目的是演示调用路径，不是复现论文数字。</b>
     换成真实 .dta 之后，代码一行都不用改。</p>
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  三种设定都把标定的真值 0.0380 稳稳圈在 95% CI 里。
</div>
""", cls=""))

# ═══════════════════════════════════════════ 49 实跑事件研究
add("statspai实跑事件研究", PG("事件研究<br>与<em>敏感性</em>", meta("REPRODUCTION", "ES + HONEST"), f"""
{fig(CH + "c_repro_es.png")}
<div class="out">
&gt;&gt;&gt; sp.honest_did(es, e=30, method="relative_magnitude")
  M̄     ci_lower   ci_upper   rejects_zero
 0.0     <b>0.0592</b>     0.1160        True
 0.5     <b>0.0504</b>     0.1247        True
 1.0     <b>0.0417</b>     0.1334        True
 1.5     <b>0.0329</b>     0.1422        True
 2.0     <b>0.0242</b>     0.1509        True
</div>
<div class="bar" style="padding:14px 20px;font-size:22px">
  即使允许 post 期的偏离达到 pre 期最大偏离的 <b>2 倍</b>，
  峰值处的效应仍然显著为正。
</div>
""", cls="xs"))

# ═══════════════════════════════════════════ 50 封底
add("封底", CV(f"""
  <div style="height:22px"></div>
  <div class="micro xl" style="color:{PINK}">METHOD → FUNCTION</div>
  <div style="height:4px;background:{INK};margin:12px 0 16px"></div>
  <table class="ledger" style="font-size:20px">
    <tr><th>论文里的做法</th><th>statspai 函数</th></tr>
    <tr><td>基准 2×2 DID（式 1）</td><td class="m">feols · did_2x2 · did</td></tr>
    <tr><td>事件研究（式 2）</td><td class="m">event_study · did_plot · aggte</td></tr>
    <tr><td>前趋势与敏感性（式 3）</td>
        <td class="m">pretrends_test · pretrends_power · honest_did</td></tr>
    <tr><td>Conley 时空 HAC</td><td class="m">conley · feols(vce="conley")</td></tr>
    <tr><td>CIC / 合成控制</td><td class="m">cic · synth · staggered_synth · sdid</td></tr>
    <tr><td>FE Poisson（Chen-Roth）</td><td class="m">fepois · ppmlhdfe</td></tr>
    <tr><td>双稳健 / 交错采纳</td>
        <td class="m">drdid · callaway_santanna · sun_abraham</td></tr>
    <tr><td>表格导出</td><td class="m">etable · to_latex · to_markdown</td></tr>
  </table>

  <div style="height:26px"></div>
  <div class="panel shadow" style="padding:22px 26px;background:{CREAM2}">
    <div class="micro lg" style="color:{PINK};margin-bottom:14px">TAKE THREE THINGS HOME</div>
    <div style="display:flex;flex-direction:column;gap:14px">
      <div class="qa"><div class="q" style="color:{PINK}">01</div>
        <div class="big-q" style="font-size:30px">
          <span class="hl">切断贸易通道</span>的代价，不止于经济账。</div></div>
      <div class="qa"><div class="q" style="color:{BLUE}">02</div>
        <div class="big-q" style="font-size:30px">
          2×2 设定下 TWFE <span class="hl-b">没问题</span>；<br>真正要补的是平行趋势的敏感性分析。</div></div>
      <div class="qa"><div class="q" style="color:{MINT}">03</div>
        <div class="big-q" style="font-size:30px">
          含零结果别急着说百分比 ——<br><span class="hl-p">先跑一遍 Poisson</span>。</div></div>
    </div>
  </div>
  <div style="flex:1"></div>
  <div class="bar" style="padding:15px 22px;font-size:22px;margin-bottom:22px">
    想自己跑一遍：<b>pip install statspai</b> ·
    真实数据从 <u>openICPSR 157781-V1</u> 取，把 repro.py 里的 simulate() 换成
    read_stata() 就行。
  </div>
  <div style="height:4px;background:{INK};margin:0 0 16px"></div>
  <div style="display:flex;align-items:center;gap:18px">
    <div style="flex:1">
      <div class="micro">CAO &amp; CHEN (2022)</div>
      <div class="micro mut" style="margin-top:6px">
        AER 112(5): 1555–1590 · doi 10.1257/aer.20201283</div>
      <div class="micro mut">复现包 openICPSR 157781-V1</div>
    </div>
    <div class="seal sm">全 50 张</div>
  </div>
""", deco(dots(690, 168, 5, 2, 15, 30, PINK, .9),
          wave(64, 1024, 240, 44, BLUE, 8, .85),
          tri(940, 1016, 64, MINT, 20, .9),
          zig(360, 1010, 60, 88, YELLOW, .9, -10),
          ring(620, 1006, 92, CORAL, 8, .85))))
