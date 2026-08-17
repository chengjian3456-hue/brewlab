#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BrewLab Pinterest 成品 Pin 生成器
把标题文字烤进 seed 图 -> marketing/pins/finished/pinNN-*.png
同时输出 marketing/pinterest-batch1.md 发布清单（图片/标题/描述/链接/图板/类型）
"""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PINS_DIR = os.path.join(ROOT, "marketing", "pins")
OUT_DIR = os.path.join(PINS_DIR, "finished")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1000, 1500
FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"  # Arial Bold

# ---- 第一批 9 个 Pin：刻意覆盖 9 种内容类型，便于看点击信号 ----
BATCH = [
    dict(img="pin-espresso.png", type="product-rec", badge=None,
         title="Best Espresso Machine\nUnder $300",
         slug="best-espresso-machine-under-300-for-beginners",
         board="Espresso & Machines",
         desc="Save $200+ and still pull real shots. Our tested beginner espresso machines under $300 — no fluff, just what works. #espresso #espressomachine #homecafe"),
    dict(img="pin-espresso.png", type="troubleshooting", badge=None,
         title="Why Is My Espresso\nSour?",
         slug="why-is-my-espresso-sour",
         board="Espresso & Machines",
         desc="Sour = under-extracted. 3 quick fixes (grind, time, temp) that rescue your shot. #espresso #coffeetips #espressoproblems"),
    dict(img="pin-pourover.png", type="tutorial", badge=None,
         title="Pour-Over Coffee:\nStep by Step",
         slug="pour-over-guide",
         board="Pour-Over & Drip",
         desc="Bloom, pour, time — the full method on one page. Tutorial. #pourover #coffeetutorial #morningcoffee"),
    dict(img="pin-icedlatte.png", type="recipe", badge=None,
         title="Iced Latte at Home\n(3 Minutes)",
         slug="how-to-make-iced-latte",
         board="Cold Brew & Iced Coffee",
         desc="Cafe-quality iced latte in 3 minutes, for a fraction of the price. Recipe. #icedlatte #coffeerecipes #starbucksdupes"),
    dict(img="pin-coldbrew.png", type="comparison", badge=None,
         title="Cold Brew vs\nIced Coffee",
         slug="cold-brew-vs-iced-coffee",
         board="Cold Brew & Iced Coffee",
         desc="Same beans, totally different cup. The real difference on one card. #coldbrew #icedcoffee #coffee"),
    dict(img="pin-grinder.png", type="freebie", badge="FREE",
         title="Coffee Brewing\nCheat Sheet",
         slug="free/coffee-cheat-sheet",
         board="Grinders & Gear",
         desc="Ratios, grind sizes, temps & fixes for every method — print it and stick it on the fridge. Grab it free. #coffee #freebie #printable"),
    dict(img="pin-frenchpress.png", type="gift", badge=None,
         title="Best Coffee Gift\nfor Her",
         slug="best-coffee-gift-for-her",
         board="Coffee Gifts & Small Kitchen",
         desc="Thoughtful, actually-useful coffee gifts she'll love. #coffeegift #giftideas #coffeelover"),
    dict(img="pin-pourover.png", type="beginner-setup", badge=None,
         title="Best Pour-Over\nSetup for Beginners",
         slug="best-pour-over-coffee-setup-for-beginners",
         board="Pour-Over & Drip",
         desc="Everything you need for your first great V60 cup under one roof. Beginner setup guide. #pourover #v60 #specialtycoffee"),
    dict(img="pin-grinder.png", type="budget", badge=None,
         title="Best Grinder\nUnder $200",
         slug="best-coffee-grinder-under-200",
         board="Grinders & Gear",
         desc="Great bang-for-buck electric grinders that beat blade grinders instantly. #coffeegrinder #budgetfinds #coffee"),
]

DOMAIN = "https://brewlab-one.vercel.app"

def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def wrap_title(draw, title, font, max_w):
    """Wrap multi-line title (already has explicit \n)."""
    lines = []
    for para in title.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=font) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines

def make_pin(spec, idx):
    src = os.path.join(PINS_DIR, spec["img"])
    img = Image.open(src).convert("RGB")
    img = img.resize((W, H), Image.LANCZOS)
    draw = ImageDraw.Draw(img, "RGBA")

    # top scrim gradient for title readability
    scrim_h = 560
    for y in range(scrim_h):
        a = int(175 * (1 - y / scrim_h) ** 1.4)
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, a))

    # title
    font = load_font(78)
    pad = 60
    lines = wrap_title(draw, spec["title"], font, W - 2 * pad)
    line_h = font.size + 12
    y = 90
    for ln in lines:
        draw.text((pad, y), ln, font=font, fill=(255, 255, 255, 255))
        y += line_h

    # accent bar under title
    bar_y = y + 6
    draw.rectangle([pad, bar_y, pad + 130, bar_y + 10], fill=(214, 158, 92, 255))

    # FREE badge
    if spec["badge"]:
        bw, bh = 150, 56
        bx, by = W - bw - pad, 70
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(212, 92, 92, 255))
        bf = load_font(34)
        draw.text((bx + 26, by + 9), spec["badge"], font=bf, fill=(255, 255, 255, 255))

    # bottom brand bar: opaque to cover any platform watermark on seed images
    draw.rectangle([(0, H - 90), (W, H)], fill=(30, 24, 20, 255))
    brand = load_font(34)
    draw.text((pad, H - 66), "BrewLab", font=brand, fill=(255, 255, 255, 255))

    # type tag bottom-right
    tf = load_font(28)
    tag = "#" + spec["type"]
    tw = draw.textlength(tag, font=tf)
    draw.text((W - tw - pad, H - 64), tag, font=tf, fill=(214, 158, 92, 255))

    out = os.path.join(OUT_DIR, f"pin{idx:02d}-{spec['type']}.png")
    img.save(out, "PNG")
    return out

rows = []
for i, s in enumerate(BATCH, 1):
    out = make_pin(s, i)
    if s["slug"].startswith("free/"):
        link = f"{DOMAIN}/{s['slug']}.html"
    else:
        link = f"{DOMAIN}/guides/{s['slug']}.html"
    rows.append((i, os.path.basename(out), s["title"].replace("\n", " "), s["type"], s["board"], link, s["desc"]))
    print(f"pin{i:02d} -> {os.path.basename(out)} ({s['type']})")

# write batch1 md
md = ["# BrewLab · Pinterest 第一批发布清单（9 Pin）", "",
      "> 用法：打开 Pinterest → Create Pin → 上传对应图片 → 粘贴 Title/Description → 填 Link → 选 Board。",
      "> 这 9 个刻意覆盖 9 种内容类型，发完后看 Pinterest Analytics 哪类点击/收藏高，回来告诉我，我针对性加图加稿。", "",
      "| # | 图片 | 标题 | 类型 | 图板 | 链接 |", "|---|---|---|---|---|---|"]
for (i, fn, title, typ, board, link, desc) in rows:
    md.append(f"| {i} | {fn} | {title} | {typ} | {board} | {link} |")
md.append("")
md.append("## 逐条文案（复制粘贴）")
for (i, fn, title, typ, board, link, desc) in rows:
    md.append(f"**{i}. {title}**  · 类型 `{typ}` · Board: {board}")
    md.append(f"- 图片：`marketing/pins/finished/{fn}`")
    md.append(f"- Title: {title}")
    md.append(f"- Description: {desc}")
    md.append(f"- Link: {link}")
    md.append("")

with open(os.path.join(ROOT, "marketing", "pinterest-batch1.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))
print("\nWrote marketing/pinterest-batch1.md")
