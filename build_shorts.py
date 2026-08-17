#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BrewLab · 无真人出镜 YouTube Shorts / TikTok 样片渲染器
PIL 把标题/贴士/CTA 文字烤进 1080x1920 图(同 Pin 风格) -> ffmpeg 转 mp4。
agent 全包渲染，用户只把 mp4 传到 YouTube Shorts / TikTok（发一次，算法长期推荐）。
运行：用带 Pillow 的 venv python 执行本脚本。
"""
import os, subprocess, shutil, tempfile
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.abspath(__file__))
PINS = os.path.join(ROOT, "marketing", "pins")
OUT = os.path.join(ROOT, "marketing", "shorts")
os.makedirs(OUT, exist_ok=True)
FF = shutil.which("ffmpeg") or "ffmpeg"
FONT_B = "C:/Windows/Fonts/arialbd.ttf"
FONT_R = "C:/Windows/Fonts/arial.ttf"
W, H = 1080, 1920

SHORTS = [
    ("pin-espresso.png", "Best Espresso Machine\nUnder $300", "Real shots at home -\nno cafe line", "BrewLab . full guide in bio"),
    ("pin-pourover.png", "Pour-Over in\n3 Steps", "Bloom, pour slow,\nwait 3 minutes", "BrewLab . free cheat sheet"),
    ("pin-coldbrew.png", "Cold Brew vs\nIced Coffee", "One is steeped 12h,\none is chilled", "BrewLab . brew guide in bio"),
]

def font(sz):
    try:
        return ImageFont.truetype(FONT_B, sz)
    except Exception:
        return ImageFont.load_default()

def fontr(sz):
    try:
        return ImageFont.truetype(FONT_R, sz)
    except Exception:
        return ImageFont.load_default()

def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=fnt) <= max_w:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines

def make_frame(img, title, tip, cta):
    src = os.path.join(PINS, img)
    base = Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(base, "RGBA")
    # top scrim
    for y in range(520):
        a = int(150 * (1 - y / 520) ** 1.3)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    # title
    fb = font(86)
    y = 150
    for ln in wrap(d, title, fb, W - 120):
        d.text((60, y), ln, font=fb, fill=(255, 255, 255, 255))
        y += fb.size + 14
    # tip (middle)
    fr = fontr(52)
    y2 = 760
    for ln in wrap(d, tip, fr, W - 120):
        d.text((60, y2), ln, font=fr, fill=(214, 158, 92, 255))
        y2 += fr.size + 12
    # bottom bar + cta
    d.rectangle([(0, H - 110), (W, H)], fill=(30, 24, 20, 255))
    d.text((60, H - 82), cta, font=font(48), fill=(255, 255, 255, 255))
    return base

def render(spec, idx):
    img, title, tip, cta = spec
    frame = make_frame(img, title, tip, cta)
    tmp = os.path.join(tempfile.gettempdir(), f"bl_short{idx}.png")
    frame.save(tmp, "PNG")
    out = os.path.join(OUT, f"short{idx:02d}.mp4")
    cmd = [FF, "-y", "-loop", "1", "-i", tmp, "-t", "18", "-r", "30",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    ok = os.path.exists(out) and os.path.getsize(out) > 5000
    msg = f"short{idx:02d}: {'OK' if ok else 'FAIL'} ({os.path.getsize(out) if os.path.exists(out) else 0} bytes)"
    if not ok:
        msg += "\n" + (r.stderr or "")[-400:]
    return msg

res = [render(s, i) for i, s in enumerate(SHORTS, 1)]
open("probe_shorts_summary.txt", "w", encoding="utf-8").write("\n".join(res))
print("\n".join(res))
