# -*- coding: utf-8 -*-
"""Memphis Pop · Sugar Rush —— 小红书竖版海报主题（1080×1440，@2x 输出 2160×2880）

视觉语言取自 many-ppt-skills 收录的 ppt-master 示例
`examples/ppt169_sugar_rush_memphis/design_spec.md`：
  奶油底 + 泡泡糖粉 / 电光蓝 / 鲜黄 / 薄荷绿 / 珊瑚红 五撞色；
  所有块必带 3px 墨黑粗描边 + 8px 硬投影；
  孟菲斯装饰碎片（圆点阵 / 波浪线 / Z 字闪电 / 45° 三角块 / 棋盘条纹）每页 1–3 个；
  标题走 Archivo Black（对应 spec 里的 Impact / Arial Black 角色），正文 Space Grotesk。

竖版适配（原 spec 是 1280×720 横版）：
  安全边距 52px；每页固定「顶部论文信息条 + 底部 StatsPAI 条」。
"""

import os as _os

W, H = 1080, 1440
_BASE = _os.path.dirname(_os.path.abspath(__file__))
FIG = "file://" + _BASE + "/figs/"
CH = "file://" + _BASE + "/charts/"
FONT = "file://" + _BASE + "/fonts/"
AV = "file://" + _BASE + "/avatars/"

# ---------------- 调色板（design_spec.md §III） ----------------
CREAM = "#FFF8EE"     # 页面奶油底
CREAM2 = "#FFE9C7"    # 浅奶油卡片底
PINK = "#FF3DA5"      # 泡泡糖粉 · primary
BLUE = "#00B8D9"      # 电光蓝 · accent
YELLOW = "#FFD93D"    # 鲜黄 · 高亮 / 数字
MINT = "#00C896"      # 薄荷绿 · 章节分色
CORAL = "#FF6B4A"     # 珊瑚红 · 装饰碎片
INK = "#1A1A2E"       # 墨黑 · 正文与描边
MUT = "#5C5C7A"       # 灰紫 · 注释
FIVE = [PINK, BLUE, YELLOW, MINT, CORAL]

# 论文信息（每页顶栏都要出现）
PAPER_CN = "运河上的叛乱"
PAPER_EN = "REBEL ON THE CANAL"
PAPER_META = "CAO &amp; CHEN · AER 2022 · 112(5): 1555–1590"
REPO = "github.com/brycewang-stanford/StatsPAI"

CSS = f"""
@font-face {{ font-family:'AB'; src:url('{FONT}ArchivoBlack.ttf'); font-weight:400 900; }}
@font-face {{ font-family:'SG'; src:url('{FONT}SpaceGrotesk.ttf'); font-weight:100 900; }}
@font-face {{ font-family:'JB'; src:url('{FONT}JetBrainsMono.ttf'); font-weight:100 800; }}
@font-face {{ font-family:'SC'; src:url('{FONT}NotoSansSC.ttf'); font-weight:100 900; }}

* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{W}px; height:{H}px; overflow:hidden; }}
body {{ background:{CREAM}; color:{INK}; position:relative;
  font-family:'SG','SC',sans-serif; -webkit-font-smoothing:antialiased; }}

/* 6px 网点纸纹 —— 每页必备的孟菲斯圆点阵底纹 */
.tex {{ position:absolute; inset:0; z-index:60; pointer-events:none;
  background-image:radial-gradient(circle at 1.4px 1.4px, rgba(26,26,46,.42) 1.3px, transparent 2px);
  background-size:7px 7px; opacity:.13; }}

.page {{ position:relative; z-index:10; width:{W}px; height:{H}px;
  padding:30px 52px 104px; display:flex; flex-direction:column; }}

/* ---------- 顶部论文信息条（每页固定） ---------- */
.hdr {{ display:flex; align-items:stretch; gap:0; flex:none; height:52px;
  border:3px solid {INK}; border-radius:26px; overflow:hidden;
  box-shadow:5px 5px 0 {INK}; background:{CREAM2}; }}
.hdr .tag {{ background:{INK}; color:{CREAM}; display:flex; align-items:center;
  padding:0 20px; font-family:'AB','SC',sans-serif; font-size:21px;
  letter-spacing:.02em; flex:none; }}
.hdr .mid {{ display:flex; align-items:center; padding:0 18px; flex:1;
  font-family:'JB',monospace; font-size:17px; letter-spacing:.02em; overflow:hidden;
  white-space:nowrap; }}
.hdr .pn {{ display:flex; align-items:center; padding:0 20px; flex:none;
  background:{PINK}; color:{CREAM}; font-family:'AB',sans-serif; font-size:22px; }}

/* ---------- 页面标题区 ---------- */
.top {{ display:flex; align-items:flex-end; gap:18px; flex:none;
  margin-top:24px; padding-bottom:14px;
  border-bottom:4px solid {INK}; }}
.top .ttl {{ font-family:'AB','SC',sans-serif; font-weight:900; letter-spacing:-.01em;
  line-height:1.0; font-size:62px; }}
.top .ttl em {{ font-style:normal; color:{PINK}; }}
.top .ttl.sm {{ font-size:52px; }}
.top .ttl.xs {{ font-size:44px; line-height:1.06; }}
.top .meta {{ margin-left:auto; text-align:right; flex:none; }}

.micro {{ font-family:'SG','SC',sans-serif; font-weight:700; font-size:18px;
  letter-spacing:.15em; text-transform:uppercase; line-height:1.3; }}
.micro.lg {{ letter-spacing:.22em; }}
.micro.xl {{ letter-spacing:.3em; }}
.micro.mut {{ color:{MUT}; }}

/* ---------- 正文容器 ---------- */
.body {{ flex:1; display:flex; flex-direction:column; gap:20px; padding-top:24px;
  min-height:0; justify-content:space-between; }}
.body.c {{ justify-content:center; }}
.row {{ display:flex; gap:18px; }}
.g2 {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
.g3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:15px; }}
.g4 {{ display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:13px; }}
.sp {{ flex:1; }}

/* ---------- 卡片（孟菲斯必带粗描边 + 硬投影） ---------- */
.card {{ border:3px solid {INK}; border-radius:12px; background:{CREAM};
  overflow:hidden; display:flex; flex-direction:column; box-shadow:7px 7px 0 {INK}; }}
.card.flat {{ box-shadow:none; }}
.card.dk {{ background:{CREAM2}; }}
.card .strip {{ height:24px; border-bottom:3px solid {INK}; }}
.card .in {{ padding:16px 20px 18px; display:flex; flex-direction:column; gap:8px; flex:1; }}
.card .nm {{ font-family:'AB','SC',sans-serif; font-size:34px; letter-spacing:-.01em;
  line-height:1.06; }}
.card .nm.sm {{ font-size:27px; }}
.card .nm.lg {{ font-size:42px; }}
.card p {{ font-size:22px; line-height:1.45; }}
.card p.big {{ font-size:25px; }}
.card .spec {{ font-family:'JB',monospace; font-size:17px; line-height:1.5;
  border-top:2.5px dashed rgba(26,26,46,.4); padding-top:8px; margin-top:auto; }}

/* ---------- 面板 ---------- */
.panel {{ border:3px solid {INK}; border-radius:12px; background:{CREAM};
  padding:20px 24px; }}
.panel.dk {{ background:{CREAM2}; }}
.panel.shadow {{ box-shadow:8px 8px 0 {INK}; }}
.panel h4 {{ font-family:'AB','SC',sans-serif; font-size:31px; line-height:1.1;
  margin-bottom:10px; }}
.panel p {{ font-size:23px; line-height:1.5; }}

/* 反白条 */
.bar {{ background:{INK}; color:{CREAM}; padding:16px 22px; font-size:24px;
  line-height:1.45; font-weight:600; border-radius:12px; }}
.bar b {{ color:{YELLOW}; font-weight:700; }}
.bar i {{ font-style:normal; color:{PINK}; font-weight:700; }}
.bar u {{ text-decoration:none; color:{BLUE}; font-weight:700; }}
.bar .h {{ font-family:'AB','SC',sans-serif; font-size:33px; line-height:1.12;
  display:block; margin-bottom:8px; }}

/* 印戳 / chip */
.stamp {{ display:inline-block; background:{PINK}; color:{CREAM}; padding:8px 18px;
  border:3px solid {INK}; border-radius:24px; font-family:'AB','SC',sans-serif;
  font-size:22px; letter-spacing:.01em; transform:rotate(-3deg);
  box-shadow:4px 4px 0 {INK}; }}
.stamp.flat {{ transform:none; }}
.stamp.ink {{ background:{INK}; color:{YELLOW}; }}
.stamp.blue {{ background:{BLUE}; }}
.stamp.mint {{ background:{MINT}; }}
.stamp.yl {{ background:{YELLOW}; color:{INK}; }}
.stamp.coral {{ background:{CORAL}; }}
.chip {{ display:inline-block; padding:5px 13px; border:2.5px solid {INK};
  border-radius:16px; font-family:'JB',monospace; font-size:16px; color:{INK};
  letter-spacing:.04em; background:{CREAM}; }}
.chip.f {{ color:{CREAM}; }}

/* 星章 */
.seal {{ width:120px; height:120px; background:{PINK}; color:{CREAM};
  border-radius:50%; border:4px solid {INK}; box-shadow:6px 6px 0 {INK};
  display:flex; align-items:center; justify-content:center; text-align:center;
  font-family:'AB','SC',sans-serif; font-size:30px; line-height:1.05; flex:none; }}
.seal.sm {{ width:92px; height:92px; font-size:23px; border-width:3px; }}
.seal.yl {{ background:{YELLOW}; color:{INK}; }}
.seal.blue {{ background:{BLUE}; }}
.seal.mint {{ background:{MINT}; }}
.seal.ink {{ background:{INK}; color:{YELLOW}; }}

/* 大数字 */
.num {{ font-family:'AB',sans-serif; letter-spacing:-.03em; line-height:.86;
  color:{PINK}; }}
.num.xl {{ font-size:190px; }}
.num.lg {{ font-size:132px; }}
.num.md {{ font-size:96px; }}
.num.sm {{ font-size:66px; }}
.num.blue {{ color:{BLUE}; }}
.num.mint {{ color:{MINT}; }}
.num.coral {{ color:{CORAL}; }}
.num.ink {{ color:{INK}; }}
.num.yl {{ color:{YELLOW}; -webkit-text-stroke:3px {INK}; }}

/* 列表 */
.li {{ display:flex; gap:12px; align-items:flex-start; font-size:23px; line-height:1.46; }}
.sq {{ width:18px; height:18px; flex:none; margin-top:7px; border:2.5px solid {INK}; }}
.sq.r {{ border-radius:50%; }}
.spec-list {{ display:flex; flex-direction:column; gap:9px; }}
.spec-row {{ display:flex; align-items:center; gap:12px; font-weight:700; font-size:23px; }}
.box {{ width:24px; height:24px; border:3px solid {INK}; flex:none; border-radius:5px;
  display:flex; align-items:center; justify-content:center;
  font-family:'AB',sans-serif; font-size:17px; color:{CREAM}; }}
.box.on {{ background:{MINT}; }}
.box.no {{ background:{CORAL}; }}

/* 图片盒 */
.figbox {{ border:3px solid {INK}; border-radius:12px; background:#fff; padding:12px;
  display:flex; align-items:center; justify-content:center; overflow:hidden;
  box-shadow:7px 7px 0 {INK}; }}
.figbox img {{ width:100%; height:100%; object-fit:contain; }}
.figbox.tight {{ padding:6px; }}
.figbox.cream {{ background:{CREAM}; padding:8px; }}
.figcap {{ font-family:'JB',monospace; font-size:16px; color:{MUT}; margin-top:8px; }}

/* 表格 */
.ledger {{ width:100%; border-collapse:collapse; font-size:21px; }}
.ledger th {{ font-family:'SG','SC',sans-serif; font-weight:700; font-size:17px;
  letter-spacing:.12em; text-transform:uppercase; text-align:left;
  border-bottom:3px solid {INK}; padding:8px 6px; }}
.ledger td {{ border-bottom:2px solid rgba(26,26,46,.2); padding:9px 6px;
  vertical-align:top; }}
.ledger td.m {{ font-family:'JB',monospace; font-size:18px; }}
.ledger td.n {{ font-family:'AB',sans-serif; font-size:26px; line-height:1; }}

/* 公式 */
.eq {{ font-family:'JB',monospace; font-size:24px; line-height:1.62; }}
.eq .k {{ color:{PINK}; font-weight:700; }}
.eq .b {{ color:{BLUE}; font-weight:700; }}
.eq .g {{ color:{MINT}; font-weight:700; }}
.eq .o {{ color:{CORAL}; font-weight:700; }}
.eq.sm {{ font-size:21px; }}

/* 高亮 */
.hl {{ background:linear-gradient(transparent 58%, {YELLOW} 58%); }}
.hl-p {{ background:linear-gradient(transparent 58%, #FFB8DE 58%); }}
.hl-b {{ background:linear-gradient(transparent 58%, #9BE9F5 58%); }}

/* ---------- 底部 StatsPAI 条（每页固定） ---------- */
.foot {{ position:absolute; left:52px; right:52px; bottom:22px; z-index:20;
  display:flex; align-items:center; gap:0; height:62px;
  border:3px solid {INK}; border-radius:31px; overflow:hidden; background:{INK};
  box-shadow:5px 5px 0 rgba(26,26,46,.28); }}
.foot .pip {{ background:{YELLOW}; color:{INK}; height:100%; display:flex;
  align-items:center; padding:0 20px; font-family:'AB',sans-serif; font-size:20px;
  flex:none; border-right:3px solid {INK}; }}
.foot .repo {{ color:{CREAM}; font-family:'JB',monospace; font-size:18px;
  padding:0 18px; letter-spacing:.01em; }}
.foot .repo b {{ color:{YELLOW}; font-weight:700; }}
.foot .rt {{ margin-left:auto; color:{CREAM}; font-family:'JB',monospace;
  font-size:16px; padding:0 22px; opacity:.75; }}

/* 装饰碎片层 */
.deco {{ position:absolute; inset:0; z-index:1; overflow:hidden; pointer-events:none; }}
.d {{ position:absolute; }}

/* 封面 */
.cover {{ position:relative; z-index:10; width:{W}px; height:{H}px;
  padding:30px 52px 104px; display:flex; flex-direction:column; }}
.hero {{ font-family:'AB','SC',sans-serif; letter-spacing:-.018em; line-height:.98; }}
.sec-no {{ font-family:'AB',sans-serif; font-size:250px; line-height:.8;
  letter-spacing:-.04em; -webkit-text-stroke:5px {INK}; }}
"""


# ═══════════════════════ 组件助手 ═══════════════════════
def tex():
    return '<div class="tex"></div>'


def hdr(pn, total):
    """顶部论文信息条 —— 每一页都必须带。"""
    return (f'<div class="hdr"><div class="tag">AER 2022</div>'
            f'<div class="mid">{PAPER_EN} · {PAPER_META}</div>'
            f'<div class="pn">{pn}/{total}</div></div>')


def foot(right=""):
    """底部 StatsPAI 仓库条 —— 每一页都必须带。"""
    rt = f'<div class="rt">{right}</div>' if right else ""
    return (f'<div class="foot"><div class="pip">pip install statspai</div>'
            f'<div class="repo">{REPO}</div>{rt}</div>')


# ---------- 孟菲斯装饰碎片 ----------
def dots(x, y, cols=4, rows=3, d=16, gap=28, color=None, op=1.0):
    """圆点阵"""
    color = color or PINK
    s = "".join(
        f'<div class="d" style="left:{x + c * gap}px;top:{y + r * gap}px;width:{d}px;'
        f'height:{d}px;border-radius:50%;background:{color};opacity:{op}"></div>'
        for r in range(rows) for c in range(cols))
    return s


def wave(x, y, w=220, h=42, color=None, sw=7, op=1.0, rot=0):
    """波浪线"""
    color = color or BLUE
    seg = w / 4.0
    p = f"M0,{h/2}"
    for i in range(4):
        up = -1 if i % 2 == 0 else 1
        p += f" q{seg/2},{up * h/2} {seg},0"
    return (f'<div class="d" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);'
            f'opacity:{op}"><svg width="{w}" height="{h}">'
            f'<path d="{p}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round"/></svg></div>')


def zig(x, y, w=80, h=110, color=None, op=1.0, rot=0):
    """Z 字闪电"""
    color = color or YELLOW
    pts = (f"{w*.55},0 {w*.05},{h*.55} {w*.42},{h*.55} {w*.2},{h} "
           f"{w},{h*.4} {w*.6},{h*.4} {w},0")
    return (f'<div class="d" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);'
            f'opacity:{op}"><svg width="{w+8}" height="{h+8}">'
            f'<polygon points="{pts}" fill="{color}" stroke="{INK}" stroke-width="3" '
            f'stroke-linejoin="round"/></svg></div>')


def tri(x, y, s=70, color=None, rot=0, op=1.0):
    """45° 三角块"""
    color = color or CORAL
    return (f'<div class="d" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);'
            f'opacity:{op}"><svg width="{s+6}" height="{s+6}">'
            f'<polygon points="{s/2},2 {s-1},{s} 2,{s}" fill="{color}" '
            f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/></svg></div>')


def checker(x, y, cols=8, rows=2, c=18, color=None, rot=0):
    """棋盘条纹"""
    color = color or INK
    cells = "".join(
        f'<rect x="{i*c}" y="{j*c}" width="{c}" height="{c}" fill="{color}"/>'
        for j in range(rows) for i in range(cols) if (i + j) % 2 == 0)
    return (f'<div class="d" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)">'
            f'<svg width="{cols*c}" height="{rows*c}">{cells}</svg></div>')


def ring(x, y, d=110, color=None, sw=9, op=1.0):
    """空心圆环"""
    color = color or MINT
    return (f'<div class="d" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;'
            f'border-radius:50%;border:{sw}px solid {color};opacity:{op}"></div>')


def blob(x, y, w=160, h=160, color=None, op=1.0, rot=0):
    """圆角色块"""
    color = color or YELLOW
    return (f'<div class="d" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background:{color};border:3px solid {INK};border-radius:{min(w,h)//3}px;'
            f'opacity:{op};transform:rotate({rot}deg)"></div>')


def deco(*parts):
    return '<div class="deco">' + "".join(parts) + "</div>"


# ---------- 内容块助手 ----------
def card(color, name, desc, spec="", nm_cls="", extra="", cls=""):
    sp = f'<div class="spec">{spec}</div>' if spec else ""
    return (f'<div class="card {cls}"><div class="strip" style="background:{color}"></div>'
            f'<div class="in"><div class="nm {nm_cls}">{name}</div>'
            f'<p>{desc}</p>{extra}{sp}</div></div>')


def li(color, text, round_=False):
    return (f'<div class="li"><div class="sq{" r" if round_ else ""}" '
            f'style="background:{color}"></div><div>{text}</div></div>')


def avatar(name, size=120, ring_color=None, radius=None):
    ring_color = ring_color or INK
    radius = size // 2 if radius is None else radius
    return (f'<div style="width:{size}px;height:{size}px;border-radius:{radius}px;'
            f'flex:none;overflow:hidden;border:4px solid {ring_color};'
            f'box-shadow:6px 6px 0 {INK};background:{CREAM2}">'
            f'<img src="{AV}{name}" style="width:100%;height:100%;object-fit:cover">'
            f'</div>')


def fig(src, cap="", h=None, tight=False, flex=None, w=976):
    """图片盒。按图片真实宽高比算出「刚好装下」的高度设为 max-height，
    避免宽图在高盒子里留出大片空白。w = 该图可用的内容宽度。"""
    cream = "/charts/" in src
    pad = 8 if cream else (6 if tight else 12)
    st = []
    try:
        from PIL import Image as _I
        with _I.open(src.replace("file://", "")) as _im:
            ar = _im.width / _im.height
        st.append("max-height:%dpx" % (round((w - 2 * pad - 6) / ar) + 2 * pad + 6))
    except Exception:
        pass
    if h:
        st.append(f"height:{h}px")
    style = f' style="{";".join(st)}"' if st else ""
    c = f'<div class="figcap">{cap}</div>' if cap else ""
    return (f'<div style="display:flex;flex-direction:column;min-height:0'
            + (f';flex:{flex}' if flex else '') + '">'
            f'<div class="figbox{" tight" if tight else ""}'
            f'{" cream" if cream else ""}"{style}><img src="{src}"></div>{c}</div>')
