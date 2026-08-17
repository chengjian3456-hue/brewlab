#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BrewLab · Pinterest 批量导入生成器
1) 把 45 张成品 Pin 拷进 static/pins/ -> gen.py 会随部署上线 -> 得到可公网访问的图片 URL
2) 输出 marketing/pinterest-bulk.csv（Pinterest 原生批量上传格式）
   用法：Pinterest Business -> Ads -> Bulk -> 上传 CSV -> 45 张 Pin 一次性进草稿/排期，不再逐张手动发。
"""
import os, csv, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://brewlab-one.vercel.app"
SRC = os.path.join(ROOT, "marketing", "pins", "finished")
DST = os.path.join(ROOT, "static", "pins")
os.makedirs(DST, exist_ok=True)

BATCH1 = [
    ("pin-espresso.png","product-rec",None,"Best Espresso Machine Under $300","best-espresso-machine-under-300-for-beginners","Espresso & Machines","Save $200+ and still pull real shots. Our tested beginner espresso machines under $300. #espresso #espressomachine #homecafe"),
    ("pin-espresso.png","troubleshooting",None,"Why Is My Espresso Sour?","why-is-my-espresso-sour","Espresso & Machines","Sour = under-extracted. 3 quick fixes (grind, time, temp) that rescue your shot. #espresso #coffeetips #espressoproblems"),
    ("pin-pourover.png","tutorial",None,"Pour-Over Coffee: Step by Step","pour-over-guide","Pour-Over & Drip","Bloom, pour, time — the full method on one page. Tutorial. #pourover #coffeetutorial #morningcoffee"),
    ("pin-icedlatte.png","recipe",None,"Iced Latte at Home (3 Minutes)","how-to-make-iced-latte","Cold Brew & Iced Coffee","Cafe-quality iced latte in 3 minutes, for a fraction of the price. Recipe. #icedlatte #coffeerecipes #starbucksdupes"),
    ("pin-coldbrew.png","comparison",None,"Cold Brew vs Iced Coffee","cold-brew-vs-iced-coffee","Cold Brew & Iced Coffee","Same beans, totally different cup. The real difference on one card. #coldbrew #icedcoffee #coffee"),
    ("pin-grinder.png","freebie","FREE","Coffee Brewing Cheat Sheet","free/coffee-cheat-sheet","Grinders & Gear","Ratios, grind sizes, temps & fixes for every method — print it and stick it on the fridge. Grab it free. #coffee #freebie #printable"),
    ("pin-frenchpress.png","gift",None,"Best Coffee Gift for Her","best-coffee-gift-for-her","Coffee Gifts & Small Kitchen","Thoughtful, actually-useful coffee gifts she'll love. #coffeegift #giftideas #coffeelover"),
    ("pin-pourover.png","beginner-setup",None,"Best Pour-Over Setup for Beginners","best-pour-over-coffee-setup-for-beginners","Pour-Over & Drip","Everything you need for your first great V60 cup under one roof. Beginner setup guide. #pourover #v60 #specialtycoffee"),
    ("pin-grinder.png","budget",None,"Best Grinder Under $200","best-coffee-grinder-under-200","Grinders & Gear","Great bang-for-buck electric grinders that beat blade grinders instantly. #coffeegrinder #budgetfinds #coffee"),
]
BATCH2 = [
    ("pin-espresso.png","product-rec",None,"Best Espresso Machine Under $500","best-espresso-machine-under-500","Espresso & Machines","Stepping up from a $300 unit? Sub-$500 gets you dual boilers and real steam. #espresso #prosumer #homebarista"),
    ("pin-espresso.png","product-rec",None,"Best Espresso Machine Under $1000","best-espresso-machine-under-1000","Espresso & Machines","Serious home barista power without pro pricing. Our top $1k picks. #espresso #homecafe #coffeelover"),
    ("pin-espresso.png","product-rec",None,"Best Prosumer Espresso Machine","best-prosumer-espresso-machine","Espresso & Machines","Cafe-grade performance for the home counter. Compare the best prosumer units. #espresso #prosumer #homebarista"),
    ("pin-espresso.png","product-rec",None,"Best Dual-Boiler Espresso Machine","best-dual-boiler-espresso-machine","Espresso & Machines","Simultaneous brew + steam = better milk drinks. Our dual-boiler picks. #espresso #latte #homecafe"),
    ("pin-espresso.png","product-rec",None,"Best Espresso Machine for Small Kitchen","best-espresso-machine-for-small-apartment","Espresso & Machines","Big coffee, tiny counter. Space-saving machines that actually perform. #espresso #smallkitchen #apartmentliving"),
    ("pin-espresso.png","budget",None,"Best Espresso Machine Under $150","best-espresso-machine-under-150","Espresso & Machines","Real shots on a tight budget. Cheap machines that still pull a decent cup. #espresso #budgetfinds #coffee"),
    ("pin-espresso.png","troubleshooting",None,"Why Is My Espresso Bitter?","why-is-my-espresso-bitter","Espresso & Machines","Bitter = over-extracted. 3 fixes (grind, dose, temp) that sweeten your shot. #espresso #coffeetips #espressoproblems"),
    ("pin-grinder.png","product-rec",None,"Best Grinder for Espresso","best-grinder-for-espresso","Grinders & Gear","Espresso lives or dies on grind. The grinders we trust for espresso. #coffeegrinder #espresso #coffeegear"),
    ("pin-grinder.png","product-rec",None,"Best Coffee Grinder Under $300","best-coffee-grinder-under-300","Grinders & Gear","The sweet spot for electric grinders — real consistency, fair price. #coffeegrinder #coffeegear #homecafe"),
    ("pin-grinder.png","product-rec",None,"Best Coffee Grinder Under $500","best-coffee-grinder-under-500","Grinders & Gear","Enthusiast-grade grinders with near-commercial uniformity. #coffeegrinder #specialtycoffee #coffeegear"),
    ("pin-grinder.png","budget",None,"Best Coffee Grinder Under $100","best-coffee-grinder-under-100","Grinders & Gear","Huge upgrade from blade grinders for under $100. #coffeegrinder #budgetfinds #coffee"),
    ("pin-grinder.png","budget",None,"Best Coffee Grinder Under $50","best-coffee-grinder-under-50","Grinders & Gear","Entry-level grinders that beat pre-ground every time. #coffeegrinder #budgetfinds #coffee"),
    ("pin-grinder.png","gear",None,"Best Coffee Scale Under $50","best-coffee-scale-under-50","Grinders & Gear","A $20 scale is the cheapest accuracy upgrade in coffee. Our picks. #coffeescale #pourover #coffeegear"),
    ("pin-grinder.png","gear",None,"Best Milk Frother for Lattes","best-milk-frother-for-latte-at-home","Grinders & Gear","Cafe-style microfoam at home without a $1k machine. #milkfrother #latte #homecafe"),
    ("pin-grinder.png","gear",None,"How to Clean a Coffee Grinder","how-to-clean-coffee-grinder","Grinders & Gear","Oils go rancid and ruin flavor. A 5-minute cleaning routine. #coffeegrinder #coffeetips #cleaning"),
    ("pin-pourover.png","beginner-setup",None,"Best Pour-Over Starter Kit","best-pourover-starter-kit","Pour-Over & Drip","Everything you need for your first great V60 cup in one place. #pourover #v60 #specialtycoffee"),
    ("pin-pourover.png","comparison",None,"Drip vs Pour-Over Coffee","drip-vs-pour-over","Pour-Over & Drip","Two brewing worlds, totally different cups. The honest breakdown. #pourover #drip #coffee"),
    ("pin-pourover.png","product-rec",None,"Best Drip Maker (Thermal Carafe)","best-drip-coffee-maker-thermal-carafe","Pour-Over & Drip","Hot coffee that stays hot for hours. Our thermal-carafe picks. #dripcoffee #coffeemaker #morningcoffee"),
    ("pin-pourover.png","gear",None,"Best Coffee Scale With Timer","best-coffee-scales-with-timer","Pour-Over & Drip","Dial in pour-over with a scale that times your blooms. #coffeescale #pourover #coffeegear"),
    ("pin-coldbrew.png","product-rec",None,"Best Cold Brew Maker for Beginners","best-cold-brew-maker-for-beginners","Cold Brew & Iced Coffee","The easiest dedicated cold brew makers to start with. #coldbrew #icedcoffee #summerdrinks"),
    ("pin-coldbrew.png","recipe",None,"Cold Brew Concentrate at Home","best-cold-brew-concentrate-maker","Cold Brew & Iced Coffee","Make a week of smooth cold brew in one batch. #coldbrew #icedcoffee #coffeerecipes"),
    ("pin-coldbrew.png","beans",None,"Best Beans for Cold Brew","best-coffee-beans-for-cold-brew","Cold Brew & Iced Coffee","Low-acid, chocolatey beans that shine over ice. Our picks. #coldbrew #coffeebeans #coffeelover"),
    ("pin-icedlatte.png","recipe",None,"How to Make a Vanilla Latte","how-to-make-vanilla-latte","Cold Brew & Iced Coffee","Cafe vanilla latte at home for a fraction of the price. #vanillalatte #coffeerecipes #latte"),
    ("pin-icedlatte.png","recipe",None,"Pumpkin Spice Latte at Home","how-to-make-pumpkin-spice-latte","Cold Brew & Iced Coffee","Skip the line — make PSL in your own kitchen. #pumpkinspice #latte #fallvibes"),
    ("pin-icedlatte.png","comparison",None,"Latte vs Mocha","latte-vs-mocha","Cold Brew & Iced Coffee","Chocolate is the only difference — or is it? The real difference, explained. #latte #mocha #coffee"),
    ("pin-icedlatte.png","comparison",None,"Flat White vs Latte","flat-white-vs-latte","Cold Brew & Iced Coffee","Same ingredients, different ratios. finally explained. #flatwhite #latte #coffee"),
    ("pin-frenchpress.png","product-rec",None,"Best French Press (Glass vs Steel)","best-french-press","French Press","Our tested French presses by material and budget. #frenchpress #coffeegear #coffeelover"),
    ("pin-frenchpress.png","product-rec",None,"Best Stainless French Press","best-stainless-french-press","French Press","Unbreakable, keeps coffee hot longer. Top steel picks. #frenchpress #coffeegear #durable"),
    ("pin-frenchpress.png","product-rec",None,"Best French Press for One","best-french-press-for-one-person","French Press","Solo coffee drinker? Small French presses that don't waste. #frenchpress #singleserve #coffee"),
    ("pin-frenchpress.png","tutorial",None,"How to Use a Moka Pot","how-to-use-a-moka-pot","French Press","Stovetop espresso-style coffee, step by step. #mokapot #italiancoffee #coffee"),
    ("pin-frenchpress.png","comparison",None,"Moka Pot vs Espresso","moka-pot-vs-espresso-machine","French Press","Close enough to espresso? The real differences on one card. #mokapot #espresso #coffee"),
    ("pin-frenchpress.png","gift",None,"Best Travel Coffee Mug","best-coffee-travel-mug-thermos","Coffee Gifts & Small Kitchen","Keeps coffee hot for hours on the commute. Top travel mugs. #travelmug #coffeelover #giftideas"),
    ("pin-espresso.png","gift",None,"Best Coffee Gift for Him","best-coffee-gift-for-him","Coffee Gifts & Small Kitchen","Actually-useful coffee gifts for the guy who has everything. #coffeegift #giftideas #coffeelover"),
    ("pin-frenchpress.png","gift",None,"Best Coffee Gifts for Lovers","best-coffee-gifts-for-coffee-lovers","Coffee Gifts & Small Kitchen","Gift sets and gear any coffee lover will use daily. #coffeegift #giftideas #coffeelover"),
    ("pin-frenchpress.png","gift",None,"Best Coffee Gift Basket","best-coffee-gift-basket","Coffee Gifts & Small Kitchen","Build a coffee gift basket they'll actually thank you for. #coffeegift #giftbasket #giftideas"),
    ("pin-grinder.png","freebie","FREE","FREE Printable Coffee Cheat Sheet","free/coffee-cheat-sheet","Grinders & Gear","Ratios, grind sizes, temps & fixes for every method. Print it free. #coffee #freebie #printable"),
]
ROWS = BATCH1 + BATCH2

def link_of(slug):
    return f"{DOMAIN}/{slug}.html" if slug.startswith("free/") else f"{DOMAIN}/guides/{slug}.html"

# copy images to static/pins
copied = 0
for i, (img, typ, badge, title, slug, board, desc) in enumerate(ROWS, 1):
    fname = f"pin{i:02d}-{typ}.png"
    s = os.path.join(SRC, fname)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(DST, fname))
        copied += 1
    else:
        print("MISSING", s)

# write CSV (Pinterest bulk format)
out = os.path.join(ROOT, "marketing", "pinterest-bulk.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Pin Title", "Pin Description", "Board name", "", "Image", "Link", "Keyword 1", "Keyword 2", "Keyword 3", "Keyword 4", "Keyword 5"])
    for i, (img, typ, badge, title, slug, board, desc) in enumerate(ROWS, 1):
        fname = f"pin{i:02d}-{typ}.png"
        img_url = f"{DOMAIN}/static/pins/{fname}"
        title_full = (f"[{badge}] " if badge else "") + title
        kw = desc.split("#")[-1].strip().split() if "#" in desc else []
        kws = [k.lstrip("#") for k in desc.split("#")[1:6] if k.strip()]
        while len(kws) < 5:
            kws.append("")
        w.writerow([title_full, desc, board, "", img_url, link_of(slug)] + kws[:5])

print(f"copied {copied} pins to static/pins/")
print(f"wrote {out} with {len(ROWS)} rows")
