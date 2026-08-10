# -*- coding: utf-8 -*-
"""重建字体：从 Google Fonts 拉字体 → 生成 matplotlib 用的静态实例 →
按本项目实际用到的字符做子集化（把 Noto Sans SC 从 10MB 压到 ~300KB）。

用法：python3 build_fonts.py
需要联网（只在首次或字体缺失时）。

字体全部为 SIL Open Font License：
  Archivo Black（标题 · Memphis 粗黑海报字）
  Space Grotesk（正文 · 几何怪味无衬线）
  JetBrains Mono（代码 / 规格行）
  Noto Sans SC（中文）
"""
import pathlib, subprocess, sys, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent            # _源码/
STATIC = HERE / "static"
STATIC.mkdir(exist_ok=True)
PY = sys.executable

GF = "https://github.com/google/fonts/raw/main/ofl/{d}/{f}"
DOWNLOAD = {
    "ArchivoBlack.ttf": ("archivoblack", "ArchivoBlack-Regular.ttf"),
    "SpaceGrotesk.ttf": ("spacegrotesk", "SpaceGrotesk%5Bwght%5D.ttf"),
    "JetBrainsMono.ttf": ("jetbrainsmono", "JetBrainsMono%5Bwght%5D.ttf"),
    "NotoSansSC.ttf": ("notosanssc", "NotoSansSC%5Bwght%5D.ttf"),
}
# matplotlib 需要的静态实例：(输出名, 源可变字体, 权重, 家族名, 样式名)
INSTANCES = [
    ("NotoSansSC-Regular.ttf", "NotoSansSC.ttf", 400, "Noto Sans SC", "Regular"),
    ("NotoSansSC-Bold.ttf", "NotoSansSC.ttf", 700, "Noto Sans SC", "Bold"),
    ("NotoSansSC-Black.ttf", "NotoSansSC.ttf", 900, "Noto Sans SC", "Black"),
    ("JetBrainsMono-Regular.ttf", "JetBrainsMono.ttf", 400, "JetBrains Mono", "Regular"),
    ("SpaceGrotesk-Bold.ttf", "SpaceGrotesk.ttf", 700, "Space Grotesk", "Bold"),
]
SUBSET = {"NotoSansSC.ttf", "NotoSansSC-Regular.ttf", "NotoSansSC-Bold.ttf",
          "NotoSansSC-Black.ttf"}


def charset():
    """本项目源码里出现过的所有非 ASCII 字符 + 完整 ASCII + 常用数学符号。"""
    txt = ""
    for f in SRC.glob("*.py"):
        txt += f.read_text(encoding="utf-8")
    chars = {c for c in txt if ord(c) >= 0xA0}
    chars |= {chr(i) for i in range(0x20, 0x7F)}
    chars |= set("←→↑↓≈≤≥±×÷∞∈∑√′″‰°ΔΣβθηελμπτεϵωγ𝔼·—–…“”‘’①②③④⑤⑥⑦⑧⑨⑩")
    return "".join(sorted(chars))


def main():
    for out, (d, f) in DOWNLOAD.items():
        p = HERE / out
        if not p.exists():
            print("download", out)
            urllib.request.urlretrieve(GF.format(d=d, f=f), p)

    for out, src, w, fam, sub in INSTANCES:
        subprocess.run([PY, "-m", "fontTools.varLib.instancer", str(HERE / src),
                        f"wght={w}", "-o", str(STATIC / out)],
                       check=True, capture_output=True)
        print("instance", out)
    # Archivo Black 本身就是静态字体，直接复制
    (STATIC / "ArchivoBlack.ttf").write_bytes((HERE / "ArchivoBlack.ttf").read_bytes())

    cs = HERE / "_charset.txt"
    text = charset()
    cs.write_text(text, encoding="utf-8")
    print("charset: %d chars" % len(text))

    for name in SUBSET:
        for d in (HERE, STATIC):
            p = d / name
            if not p.exists():
                continue
            subprocess.run(
                [PY, "-m", "fontTools.subset", str(p),
                 "--text-file=" + str(cs), "--output-file=" + str(p),
                 "--layout-features=*", "--no-hinting", "--desubroutinize"],
                check=True, capture_output=True)
            print("subset  %-28s %6.1f KB" % (str(p.relative_to(HERE)),
                                              p.stat().st_size / 1024))


if __name__ == "__main__":
    main()
