# -*- coding: utf-8 -*-
"""渲染 1080×1440 @2x → 2160×2880 PNG，输出联系表与预览 PDF，并检测溢出。"""
import os, pathlib
from memphis import CSS, W, H, hdr, foot, tex
import posters

BASE = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
OUT = BASE.parent
TMP = BASE / "html"
TMP.mkdir(exist_ok=True)

css = CSS + posters.EXTRA_CSS
N = posters.total()

pages = []
for label, stem, inner in posters.P:
    body = inner.replace("__HDR__", hdr(label, N))
    name = "%s-%s" % (label, stem)
    html = ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            f"<style>{css}</style></head><body>{tex()}{body}{foot()}</body></html>")
    f = TMP / (name + ".html")
    f.write_text(html, encoding="utf-8")
    pages.append((name, f))

from playwright.sync_api import sync_playwright

paths, over = [], []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
    for name, f in pages:
        pg.goto("file://" + str(f))
        pg.wait_for_timeout(160)
        sh = pg.evaluate("""(H) => {
            let s = 0;
            const bd = document.querySelector('.body');
            if (bd) s = Math.max(s, bd.scrollHeight - bd.clientHeight);
            const pgel = document.querySelector('.page') || document.querySelector('.cover');
            if (pgel) s = Math.max(s, pgel.scrollHeight - pgel.clientHeight);
            document.querySelectorAll('.body > *, .cover > *, .figbox, .bar, .panel, .card, .code, .out')
              .forEach(el => {
                if (el.closest('.deco')) return;
                const r = el.getBoundingClientRect();
                if (r.height > 0) s = Math.max(s, Math.round(r.bottom - (H - 96)));
              });
            return s; }""", H)
        if sh > 2:
            over.append((name, sh))
        p = OUT / (name + ".png")
        pg.screenshot(path=str(p))
        paths.append(p)
        print("  %s %-30s %s" % ("!" if sh > 2 else "OK", name,
                                 "溢出 %dpx" % sh if sh > 2 else ""))
    b.close()

if over:
    print("\n! 溢出页面：")
    for n, s in over:
        print("   ", n, s, "px")
else:
    print("\n全部 %d 页无溢出" % len(paths))

from PIL import Image
cols, tw = 7, 300
ims = [Image.open(p).convert("RGB") for p in paths]
th = int(tw * H / W)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * th), "#FFF8EE")
for i, im in enumerate(ims):
    sheet.paste(im.resize((tw, th), Image.LANCZOS), ((i % cols) * tw, (i // cols) * th))
sheet.save(OUT / "00-联系表-contact-sheet.png")

import pymupdf
doc = pymupdf.open()
for p in paths:
    pix = pymupdf.Pixmap(str(p))
    pg2 = doc.new_page(width=W / 2, height=H / 2)
    pg2.insert_image(pg2.rect, pixmap=pix)
doc.save(str(OUT / "00-全部预览.pdf"), deflate=True)
doc.close()
print("共 %d 张 · 已写入 %s" % (len(paths), OUT))
