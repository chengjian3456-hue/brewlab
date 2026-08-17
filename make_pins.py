#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BrewLab Pinterest 成品 Pin 生成器（两批合一）
读取 6 张种子图 -> 叠加标题/BrewLab 品牌/FREE 徽章/类型标签 -> marketing/pins/finished/pinNN-*.png
同时输出 marketing/pinterest-batch1.md(前9) + pinterest-batch2.md(其余) 发布清单。
零新增 ImageGen 成本：只用已有 6 张种子图做文字合成。
"""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PINS_DIR = os.path.join(ROOT, "marketing", "pins")
OUT_DIR = os.path.join(PINS_DIR, "finished")
os.makedirs(OUT_DIR, exist_ok=True)
W, H = 1000, 1500
FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
DOMAIN = "https://brewlab-one.vercel.app"

# ---------- 第一批（已发，9 张，9 种内容类型做点击信号） ----------
BATCH1 = [
    dict(img="pin-espresso.png", type="product-rec", badge=None, title="Best Espresso Machine\nUnder $300", slug="best-espresso-machine-under-300-for-beginners", board="Espresso & Machines", desc="Save $200+ and still pull real shots. Our tested beginner espresso machines under $300. #espresso #espressomachine #homecafe"),
    dict(img="pin-espresso.png", type="troubleshooting", badge=None, title="Why Is My Espresso\nSour?", slug="why-is-my-espresso-sour", board="Espresso & Machines", desc="Sour = under-extracted. 3 quick fixes (grind, time, temp) that rescue your shot. #espresso #coffeetips #espressoproblems"),
    dict(img="pin-pourover.png", type="tutorial", badge=None, title="Pour-Over Coffee:\nStep by Step", slug="pour-over-guide", board="Pour-Over & Drip", desc="Bloom, pour, time — the full method on one page. Tutorial. #pourover #coffeetutorial #morningcoffee"),
    dict(img="pin-icedlatte.png", type="recipe", badge=None, title="Iced Latte at Home\n(3 Minutes)", slug="how-to-make-iced-latte", board="Cold Brew & Iced Coffee", desc="Cafe-quality iced latte in 3 minutes, for a fraction of the price. Recipe. #icedlatte #coffeerecipes #starbucksdupes"),
    dict(img="pin-coldbrew.png", type="comparison", badge=None, title="Cold Brew vs\nIced Coffee", slug="cold-brew-vs-iced-coffee", board="Cold Brew & Iced Coffee", desc="Same beans, totally different cup. The real difference on one card. #coldbrew #icedcoffee #coffee"),
    dict(img="pin-grinder.png", type="freebie", badge="FREE", title="Coffee Brewing\nCheat Sheet", slug="free/coffee-cheat-sheet", board="Grinders & Gear", desc="Ratios, grind sizes, temps & fixes for every method — print it and stick it on the fridge. Grab it free. #coffee #freebie #printable"),
    dict(img="pin-frenchpress.png", type="gift", badge=None, title="Best Coffee Gift\nfor Her", slug="best-coffee-gift-for-her", board="Coffee Gifts & Small Kitchen", desc="Thoughtful, actually-useful coffee gifts she'll love. #coffeegift #giftideas #coffeelover"),
    dict(img="pin-pourover.png", type="beginner-setup", badge=None, title="Best Pour-Over\nSetup for Beginners", slug="best-pour-over-coffee-setup-for-beginners", board="Pour-Over & Drip", desc="Everything you need for your first great V60 cup under one roof. Beginner setup guide. #pourover #v60 #specialtycoffee"),
    dict(img="pin-grinder.png", type="budget", badge=None, title="Best Grinder\nUnder $200", slug="best-coffee-grinder-under-200", board="Grinders & Gear", desc="Great bang-for-buck electric grinders that beat blade grinders instantly. #coffeegrinder #budgetfinds #coffee"),
]

# ---------- 第二批（36 张，向高客单价/高意图倾斜，AOV 杠杆最高） ----------
BATCH2 = [
    dict(img="pin-espresso.png", type="product-rec", badge=None, title="Best Espresso Machine\nUnder $500", slug="best-espresso-machine-under-500", board="Espresso & Machines", desc="Stepping up from a $300 unit? Sub-$500 gets you dual boilers and real steam. #espresso #prosumer #homebarista"),
    dict(img="pin-espresso.png", type="product-rec", badge=None, title="Best Espresso Machine\nUnder $1000", slug="best-espresso-machine-under-1000", board="Espresso & Machines", desc="Serious home barista power without pro pricing. Our top $1k picks. #espresso #homecafe #coffeelover"),
    dict(img="pin-espresso.png", type="product-rec", badge=None, title="Best Prosumer\nEspresso Machine", slug="best-prosumer-espresso-machine", board="Espresso & Machines", desc="Cafe-grade performance for the home counter. Compare the best prosumer units. #espresso #prosumer #homebarista"),
    dict(img="pin-espresso.png", type="product-rec", badge=None, title="Best Dual-Boiler\nEspresso Machine", slug="best-dual-boiler-espresso-machine", board="Espresso & Machines", desc="Simultaneous brew + steam = better milk drinks. Our dual-boiler picks. #espresso #latte #homecafe"),
    dict(img="pin-espresso.png", type="product-rec", badge=None, title="Best Espresso Machine\nfor Small Kitchen", slug="best-espresso-machine-for-small-apartment", board="Espresso & Machines", desc="Big coffee, tiny counter. Space-saving machines that actually perform. #espresso #smallkitchen #apartmentliving"),
    dict(img="pin-espresso.png", type="budget", badge=None, title="Best Espresso Machine\nUnder $150", slug="best-espresso-machine-under-150", board="Espresso & Machines", desc="Real shots on a tight budget. Cheap machines that still pull a decent cup. #espresso #budgetfinds #coffee"),
    dict(img="pin-espresso.png", type="troubleshooting", badge=None, title="Why Is My Espresso\nBitter?", slug="why-is-my-espresso-bitter", board="Espresso & Machines", desc="Bitter = over-extracted. 3 fixes (grind, dose, temp) that sweeten your shot. #espresso #coffeetips #espressoproblems"),
    dict(img="pin-grinder.png", type="product-rec", badge=None, title="Best Grinder\nfor Espresso", slug="best-grinder-for-espresso", board="Grinders & Gear", desc="Espresso lives or dies on grind. The grinders we trust for espresso. #coffeegrinder #espresso #coffeegear"),
    dict(img="pin-grinder.png", type="product-rec", badge=None, title="Best Coffee Grinder\nUnder $300", slug="best-coffee-grinder-under-300", board="Grinders & Gear", desc="The sweet spot for electric grinders — real consistency, fair price. #coffeegrinder #coffeegear #homecafe"),
    dict(img="pin-grinder.png", type="product-rec", badge=None, title="Best Coffee Grinder\nUnder $500", slug="best-coffee-grinder-under-500", board="Grinders & Gear", desc="Enthusiast-grade grinders with near-commercial uniformity. #coffeegrinder #specialtycoffee #coffeegear"),
    dict(img="pin-grinder.png", type="budget", badge=None, title="Best Coffee Grinder\nUnder $100", slug="best-coffee-grinder-under-100", board="Grinders & Gear", desc="Huge upgrade from blade grinders for under $100. #coffeegrinder #budgetfinds #coffee"),
    dict(img="pin-grinder.png", type="budget", badge=None, title="Best Coffee Grinder\nUnder $50", slug="best-coffee-grinder-under-50", board="Grinders & Gear", desc="Entry-level grinders that beat pre-ground every time. #coffeegrinder #budgetfinds #coffee"),
    dict(img="pin-grinder.png", type="gear", badge=None, title="Best Coffee Scale\nUnder $50", slug="best-coffee-scale-under-50", board="Grinders & Gear", desc="A $20 scale is the cheapest accuracy upgrade in coffee. Our picks. #coffeescale #pourover #coffeegear"),
    dict(img="pin-grinder.png", type="gear", badge=None, title="Best Milk Frother\nfor Lattes", slug="best-milk-frother-for-latte-at-home", board="Grinders & Gear", desc="Cafe-style microfoam at home without a $1k machine. #milkfrother #latte #homecafe"),
    dict(img="pin-grinder.png", type="gear", badge=None, title="How to Clean a\nCoffee Grinder", slug="how-to-clean-coffee-grinder", board="Grinders & Gear", desc="Oils go rancid and ruin flavor. A 5-minute cleaning routine. #coffeegrinder #coffeetips #cleaning"),
    dict(img="pin-pourover.png", type="beginner-setup", badge=None, title="Best Pour-Over\nStarter Kit", slug="best-pourover-starter-kit", board="Pour-Over & Drip", desc="Everything you need for your first great V60 cup in one place. #pourover #v60 #specialtycoffee"),
    dict(img="pin-pourover.png", type="comparison", badge=None, title="Drip vs\nPour-Over Coffee", slug="drip-vs-pour-over", board="Pour-Over & Drip", desc="Two brewing worlds, totally different cups. The honest breakdown. #pourover #drip #coffee"),
    dict(img="pin-pourover.png", type="product-rec", badge=None, title="Best Drip Maker\n(Thermal Carafe)", slug="best-drip-coffee-maker-thermal-carafe", board="Pour-Over & Drip", desc="Hot coffee that stays hot for hours. Our thermal-carafe picks. #dripcoffee #coffeemaker #morningcoffee"),
    dict(img="pin-pourover.png", type="gear", badge=None, title="Best Coffee Scale\nWith Timer", slug="best-coffee-scales-with-timer", board="Pour-Over & Drip", desc="Dial in pour-over with a scale that times your blooms. #coffeescale #pourover #coffeegear"),
    dict(img="pin-coldbrew.png", type="product-rec", badge=None, title="Best Cold Brew Maker\nfor Beginners", slug="best-cold-brew-maker-for-beginners", board="Cold Brew & Iced Coffee", desc="The easiest dedicated cold brew makers to start with. #coldbrew #icedcoffee #summerdrinks"),
    dict(img="pin-coldbrew.png", type="recipe", badge=None, title="Cold Brew Concentrate\nat Home", slug="best-cold-brew-concentrate-maker", board="Cold Brew & Iced Coffee", desc="Make a week of smooth cold brew in one batch. #coldbrew #icedcoffee #coffeerecipes"),
    dict(img="pin-coldbrew.png", type="beans", badge=None, title="Best Beans\nfor Cold Brew", slug="best-coffee-beans-for-cold-brew", board="Cold Brew & Iced Coffee", desc="Low-acid, chocolatey beans that shine over ice. Our picks. #coldbrew #coffeebeans #coffeelover"),
    dict(img="pin-icedlatte.png", type="recipe", badge=None, title="How to Make a\nVanilla Latte", slug="how-to-make-vanilla-latte", board="Cold Brew & Iced Coffee", desc="Cafe vanilla latte at home for a fraction of the price. #vanillalatte #coffeerecipes #latte"),
    dict(img="pin-icedlatte.png", type="recipe", badge=None, title="Pumpkin Spice Latte\nat Home", slug="how-to-make-pumpkin-spice-latte", board="Cold Brew & Iced Coffee", desc="Skip the line — make PSL in your own kitchen. #pumpkinspice #latte #fallvibes"),
    dict(img="pin-icedlatte.png", type="comparison", badge=None, title="Latte vs Mocha", slug="latte-vs-mocha", board="Cold Brew & Iced Coffee", desc="Chocolate is the only difference — or is it? The real difference, explained. #latte #mocha #coffee"),
    dict(img="pin-icedlatte.png", type="comparison", badge=None, title="Flat White\nvs Latte", slug="flat-white-vs-latte", board="Cold Brew & Iced Coffee", desc="Same ingredients, different ratios. finally explained. #flatwhite #latte #coffee"),
    dict(img="pin-frenchpress.png", type="product-rec", badge=None, title="Best French Press\n(Glass vs Steel)", slug="best-french-press", board="French Press", desc="Our tested French presses by material and budget. #frenchpress #coffeegear #coffeelover"),
    dict(img="pin-frenchpress.png", type="product-rec", badge=None, title="Best Stainless\nFrench Press", slug="best-stainless-french-press", board="French Press", desc="Unbreakable, keeps coffee hot longer. Top steel picks. #frenchpress #coffeegear #durable"),
    dict(img="pin-frenchpress.png", type="product-rec", badge=None, title="Best French Press\nfor One", slug="best-french-press-for-one-person", board="French Press", desc="Solo coffee drinker? Small French presses that don't waste. #frenchpress #singleserve #coffee"),
    dict(img="pin-frenchpress.png", type="tutorial", badge=None, title="How to Use\na Moka Pot", slug="how-to-use-a-moka-pot", board="French Press", desc="Stovetop espresso-style coffee, step by step. #mokapot #italiancoffee #coffee"),
    dict(img="pin-frenchpress.png", type="comparison", badge=None, title="Moka Pot vs\nEspresso", slug="moka-pot-vs-espresso-machine", board="French Press", desc="Close enough to espresso? The real differences on one card. #mokapot #espresso #coffee"),
    dict(img="pin-frenchpress.png", type="gift", badge=None, title="Best Travel\nCoffee Mug", slug="best-coffee-travel-mug-thermos", board="Coffee Gifts & Small Kitchen", desc="Keeps coffee hot for hours on the commute. Top travel mugs. #travelmug #coffeelover #giftideas"),
    dict(img="pin-espresso.png", type="gift", badge=None, title="Best Coffee Gift\nfor Him", slug="best-coffee-gift-for-him", board="Coffee Gifts & Small Kitchen", desc="Actually-useful coffee gifts for the guy who has everything. #coffeegift #giftideas #coffeelover"),
    dict(img="pin-frenchpress.png", type="gift", badge=None, title="Best Coffee Gifts\nfor Lovers", slug="best-coffee-gifts-for-coffee-lovers", board="Coffee Gifts & Small Kitchen", desc="Gift sets and gear any coffee lover will use daily. #coffeegift #giftideas #coffeelover"),
    dict(img="pin-frenchpress.png", type="gift", badge=None, title="Best Coffee\nGift Basket", slug="best-coffee-gift-basket", board="Coffee Gifts & Small Kitchen", desc="Build a coffee gift basket they'll actually thank you for. #coffeegift #giftbasket #giftideas"),
    dict(img="pin-grinder.png", type="freebie", badge="FREE", title="FREE Printable\nCoffee Cheat Sheet", slug="free/coffee-cheat-sheet", board="Grinders & Gear", desc="Ratios, grind sizes, temps & fixes for every method. Print it free. #coffee #freebie #printable"),
]

def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def wrap_title(draw, title, font, max_w):
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
    img = Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)
    draw = ImageDraw.Draw(img, "RGBA")
    scrim_h = 560
    for y in range(scrim_h):
        a = int(175 * (1 - y / scrim_h) ** 1.4)
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    font = load_font(78)
    pad = 60
    lines = wrap_title(draw, spec["title"], font, W - 2 * pad)
    line_h = font.size + 12
    y = 90
    for ln in lines:
        draw.text((pad, y), ln, font=font, fill=(255, 255, 255, 255))
        y += line_h
    bar_y = y + 6
    draw.rectangle([pad, bar_y, pad + 130, bar_y + 10], fill=(214, 158, 92, 255))
    if spec["badge"]:
        bw, bh = 150, 56
        bx, by = W - bw - pad, 70
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(212, 92, 92, 255))
        bf = load_font(34)
        draw.text((bx + 26, by + 9), spec["badge"], font=bf, fill=(255, 255, 255, 255))
    draw.rectangle([(0, H - 90), (W, H)], fill=(30, 24, 20, 255))
    brand = load_font(34)
    draw.text((pad, H - 66), "BrewLab", font=brand, fill=(255, 255, 255, 255))
    tf = load_font(28)
    tag = "#" + spec["type"]
    tw = draw.textlength(tag, font=tf)
    draw.text((W - tw - pad, H - 64), tag, font=tf, fill=(214, 158, 92, 255))
    out = os.path.join(OUT_DIR, f"pin{idx:02d}-{spec['type']}.png")
    img.save(out, "PNG")
    return out

def link_of(slug):
    if slug.startswith("free/"):
        return f"{DOMAIN}/{slug}.html"
    return f"{DOMAIN}/guides/{slug}.html"

def write_md(path, items, start):
    md = [f"# BrewLab · Pinterest 发布清单（第 {start}-{start+len(items)-1} 批，共 {len(items)} Pin）", "",
          "> 用法：Pinterest → Create Pin → 上传图片 → 粘贴 Title/Description → 填 Link → 选 Board。",
          "> 第二批向高客单价(意式机/磨豆机)与高意图(礼物/入门套装)倾斜，同样的点击单笔佣金差数十倍。", "",
          "| # | 图片 | 标题 | 类型 | 图板 | 链接 |", "|---|---|---|---|---|---|"]
    for i, s in enumerate(items, start):
        md.append(f"| {i} | pin{i:02d}-{s['type']}.png | {s['title'].replace(chr(10),' ')} | {s['type']} | {s['board']} | {link_of(s['slug'])} |")
    md.append("")
    md.append("## 逐条文案")
    for i, s in enumerate(items, start):
        md.append(f"**{i}. {s['title'].replace(chr(10),' ')}** · 类型 `{s['type']}` · Board: {s['board']}")
        md.append(f"- 图片：`marketing/pins/finished/pin{i:02d}-{s['type']}.png`")
        md.append(f"- Title: {s['title'].replace(chr(10),' ')}")
        md.append(f"- Description: {s['desc']}")
        md.append(f"- Link: {link_of(s['slug'])}")
        md.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

all_pins = BATCH1 + BATCH2
for i, s in enumerate(all_pins, 1):
    out = make_pin(s, i)
    link = link_of(s["slug"])
    print(f"pin{i:02d} -> {os.path.basename(out)} ({s['type']}) {link}")

write_md(os.path.join(ROOT, "marketing", "pinterest-batch1.md"), BATCH1, 1)
write_md(os.path.join(ROOT, "marketing", "pinterest-batch2.md"), BATCH2, 10)
print(f"\nTotal {len(all_pins)} pins. Batch1={len(BATCH1)} Batch2={len(BATCH2)}")
