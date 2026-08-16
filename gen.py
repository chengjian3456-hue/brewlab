#!/usr/bin/env python3
"""BrewLab static site generator. Run: python gen.py  (outputs to ./dist)"""
import os, json, shutil
from urllib.parse import quote
from config import SITE, DISCLOSURE, NAV, INDEXNOW_KEY
from data.guides import GUIDES
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
STATIC = os.path.join(ROOT, "static")

DOMAIN = SITE["domain"]
TAG = SITE["amz_tag"]
AMZ = SITE["amz_search_base"]

SLUG_TITLE = {g["slug"]: g["title"] for g in GUIDES}

def amz(query):
    return f'{AMZ}{quote(query)}&tag={TAG}'

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# ---------------- builders ----------------
def nav_html(active):
    out = []
    for label, href in NAV:
        cls = ' class="active"' if active == href else ''
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    return "\n".join(out)

def footer_html():
    return f'''<footer>
  <p class="disclosure">{esc(DISCLOSURE)}</p>
  <nav class="foot-nav">{" · ".join(f'<a href="{h}">{l}</a>' for l,h in NAV)}</nav>
  <p class="copy">© {SITE["name"]} — brew better, spend less.</p>
</footer>'''

def page(title, meta, body, canonical="/", json_ld=None):
    ld = f'<script type="application/ld+json">{json_ld}</script>\n' if json_ld else ''
    return f'''<!DOCTYPE html>
<html lang="{SITE["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta)}">
<link rel="canonical" href="{DOMAIN}{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}{canonical}">
{ld}<link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
<header><div class="wrap"><a class="brand" href="/">{SITE["name"]}</a>
<nav class="top-nav">{nav_html(canonical)}</nav></div></header>
<main class="wrap">{body}</main>
{footer_html()}
<script src="/static/js/ads.js" defer></script>
</body>
</html>'''

def guide_jsonld(g, url):
    faq = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in g["faq"]]
    data = {
      "@context":"https://schema.org",
      "@type":"Article",
      "headline":g["title"],
      "description":g["meta"],
      "author":{"@type":"Organization","name":SITE["name"]},
      "publisher":{"@type":"Organization","name":SITE["name"]},
      "mainEntityOfPage":{"@type":"WebPage","@id":DOMAIN+url}
    }
    if faq:
        data["@type"] = ["Article","FAQPage"]
        data["mainEntity"] = faq
    return json.dumps(data, ensure_ascii=False)

def render_guide(g):
    url = f'/guides/{g["slug"]}.html'
    picks = []
    for p in g["picks"]:
        link = amz(p["query"])
        pros = "".join(f"<li>+ {esc(x)}</li>" for x in p["pros"])
        cons = "".join(f"<li>− {esc(x)}</li>" for x in p["cons"])
        picks.append(f'''<div class="pick">
  <h3><a href="{link}" rel="sponsored nofollow">{esc(p["name"])}</a></h3>
  <p>{esc(p["note"])}</p>
  <div class="pc"><ul class="pros">{pros}</ul><ul class="cons">{cons}</ul></div>
  <p class="buy"><a class="btn" href="{link}" rel="sponsored nofollow">Check price on Amazon →</a></p>
</div>''')
    picks_html = "\n".join(picks)
    faq_html = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in g["faq"])
    rel_html = ""
    if g.get("related"):
        items = "".join(f'<li><a href="/guides/{s}.html">{esc(SLUG_TITLE[s])}</a></li>' for s in g["related"] if s in SLUG_TITLE)
        rel_html = f'<section class="related"><h2>Related guides</h2><ul>{items}</ul></section>'
    body = f'''<article class="guide">
  <h1>{esc(g["h1"])}</h1>
  <p class="lead">{esc(g["intro"])}</p>
  <section class="picks">{picks_html}</section>
  <section class="advice"><h2>Buying advice</h2><p>{esc(g["advice"])}</p></section>
  <section class="faq"><h2>FAQ</h2>{faq_html}</section>
  {rel_html}
  <p class="cta">Want exact doses? Use our <a href="/tools.html">free brew calculators</a>.</p>
</article>'''
    return page(g["title"], g["meta"], body, canonical=url, json_ld=guide_jsonld(g, url))

# ---------------- pages ----------------
def render_home():
    cards = "".join(f'''<a class="card" href="/guides/{g['slug']}.html">
      <h3>{esc(g['h1'])}</h3><p>{esc(g['meta'])}</p></a>''' for g in GUIDES[:6])
    body = f'''<section class="hero">
  <h1>{esc(SITE["name"])}</h1>
  <p class="tag">{esc(SITE["tagline"])}</p>
  <p class="hero-cta"><a class="btn big" href="/tools.html">Try the free brew calculators →</a></p>
</section>
<section class="tools-tease">
  <h2>Free tools</h2>
  <p>Lock a repeatable recipe with the <a href="/tools.html">Brew Ratio Calculator</a>, see what your habit costs with the <a href="/tools.html">Cost-per-Cup Calculator</a>, and estimate your intake with the <a href="/tools.html">Caffeine Calculator</a>.</p>
</section>
<section class="guides">
  <h2>Beginner gear guides</h2>
  <div class="grid">{cards}</div>
  <p class="more"><a href="/guides/">See all {len(GUIDES)} guides →</a></p>
</section>'''
    org = json.dumps({"@context":"https://schema.org","@type":"Organization",
                      "name":SITE["name"],"url":DOMAIN,"description":SITE["tagline"]}, ensure_ascii=False)
    return page(f'{SITE["name"]} — {SITE["tagline"]}', SITE["tagline"], body, canonical="/", json_ld=org)

def render_guides_index():
    items = "".join(f'<li><a href="/guides/{g["slug"]}.html">{esc(g["title"])}</a> — {esc(g["meta"])}</li>' for g in GUIDES)
    body = f'''<section class="guide-list"><h1>All BrewLab guides</h1>
    <ul class="index">{items}</ul></section>'''
    return page("BrewLab Guides — beginner coffee gear", "All BrewLab beginner coffee gear guides, from espresso machines to pour-over and camp coffee.", body, canonical="/guides/")

def render_tools():
    body = '''<section class="tools">
  <h1>Free brew calculators</h1>
  <p class="lead">No accounts, no uploads — everything runs in your browser. Use these to lock a repeatable recipe and see what your coffee habit really costs.</p>

  <div class="calc" id="ratio">
    <h2>Brew Ratio Calculator</h2>
    <p>Fill any two fields; we solve the third. 1:16 is a balanced filter start; 1:15 stronger, 1:18 lighter.</p>
    <label>Coffee dose (g) <input type="number" id="r-coffee" min="0" step="0.1" placeholder="18"></label>
    <label>Water (ml) <input type="number" id="r-water" min="0" step="1" placeholder="288"></label>
    <label>Ratio (1:N) <input type="number" id="r-ratio" min="1" step="0.5" placeholder="16"></label>
    <button class="btn" onclick="solveRatio()">Calculate recipe</button>
    <p class="result" id="r-out"></p>
  </div>

  <div class="calc" id="cost">
    <h2>Cost-per-Cup Calculator</h2>
    <p>See what each cup costs you versus a cafe.</p>
    <label>Bag price ($) <input type="number" id="c-price" min="0" step="0.01" placeholder="15"></label>
    <label>Bag weight (g) <input type="number" id="c-weight" min="0" step="1" placeholder="340"></label>
    <label>Dose per cup (g) <input type="number" id="c-dose" min="0" step="0.5" placeholder="18"></label>
    <label>Cups per day <input type="number" id="c-day" min="0" step="1" placeholder="1"></label>
    <button class="btn" onclick="solveCost()">Calculate</button>
    <p class="result" id="c-out"></p>
  </div>

  <div class="calc" id="cold">
    <h2>Cold Brew Calculator</h2>
    <p>Concentrate ratio is typically 1:8 (coffee:water). Fill any two fields; we solve the third and estimate servings after a 1:1 dilution.</p>
    <label>Coffee (g) <input type="number" id="cb-coffee" min="0" step="1" placeholder="100"></label>
    <label>Water (ml) <input type="number" id="cb-water" min="0" step="10" placeholder="800"></label>
    <label>Ratio (1:N) <input type="number" id="cb-ratio" min="1" step="0.5" placeholder="8"></label>
    <button class="btn" onclick="solveColdBrew()">Calculate</button>
    <p class="result" id="cb-out"></p>
  </div>

  <div class="calc" id="caf">
    <h2>Caffeine Calculator</h2>
    <p>Estimate the caffeine in your cup by brew method and size. Figures are typical averages per 8 oz (237 ml) serving.</p>
    <label>Brew method
      <select id="cf-method">
        <option>Drip / filter</option>
        <option>Pour-over</option>
        <option>French press</option>
        <option>AeroPress</option>
        <option>Cold brew</option>
        <option>Espresso (Americano, 8 oz)</option>
      </select>
    </label>
    <label>Serving size (oz) <input type="number" id="cf-oz" min="0" step="1" placeholder="8"></label>
    <button class="btn" onclick="solveCaffeine()">Estimate</button>
    <p class="result" id="cf-out"></p>
  </div>
</section>
<script src="/static/js/brew.js" defer></script>'''
    return page("Free Brew Calculators — ratio & cost per cup", "Free coffee calculators: brew ratio (coffee/water/ratio solver) and cost-per-cup. Runs in your browser, no sign-up.", body, canonical="/tools.html")

def render_simple(title, meta, body, canonical):
    return page(title, meta, body, canonical=canonical)

# ---------------- write ----------------
def write(path, content):
    full = os.path.join(DIST, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def copy_static():
    # Mirror STATIC -> DIST/static without ever calling rmtree (sandbox blocks it).
    for root, _, files in os.walk(STATIC):
        for fn in files:
            src = os.path.join(root, fn)
            rel = os.path.relpath(src, STATIC)
            dst = os.path.join(DIST, "static", rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

def main():
    os.makedirs(DIST, exist_ok=True)
    # copy static
    if os.path.exists(STATIC):
        copy_static()
    # pages
    write("/index.html", render_home())
    write("/tools.html", render_tools())
    write("/guides/index.html", render_guides_index())
    write("/about.html", render_simple(
        "About BrewLab", "Why we built BrewLab: beginner-friendly, calculator-first coffee gear advice with no jargon and no fluff.",
        '''<section class="simple"><h1>About BrewLab</h1>
        <p>BrewLab helps beginners make better coffee at home without overspending or drowning in jargon. We test and recommend gear by one rule: does it help a real person pull a better cup?</p>
        <p>Every guide is written to be useful on its own. Our free calculators turn the vague "a bit more coffee" into exact, repeatable recipes.</p>
        <p>We may earn a commission if you buy through our links — it never changes what we recommend. See the <a href="/disclosure.html">full disclosure</a>.</p></section>''',
        "/about.html"))
    write("/disclosure.html", render_simple(
        "Affiliate Disclosure", "BrewLab affiliate disclosure: how we make money and how it affects our recommendations.",
        f'''<section class="simple"><h1>Affiliate Disclosure</h1>
        <p>{esc(DISCLOSURE)}</p>
        <p>Some links are "sponsored" (affiliate) links to Amazon or other retailers. If you click and buy, we may receive a commission at no extra cost to you. This does not influence our editorial choices — we recommend what we believe is best for beginners regardless of commission.</p>
        <p>Amazon and the Amazon logo are trademarks of Amazon.com, Inc.</p></section>''',
        "/disclosure.html"))
    write("/privacy.html", render_simple(
        "Privacy Policy", "BrewLab privacy policy: what we collect, what we don't, cookies, and third-party links.",
        '''<section class="simple"><h1>Privacy Policy</h1>
        <p>Effective date: 2026-08-17. This policy explains what BrewLab collects and what it does not.</p>
        <h2>What we collect</h2>
        <p>BrewLab is a static website. We do not operate accounts, and we do not ask you to submit personal information through forms. Our free calculators run entirely in your browser; the numbers you type never leave your device.</p>
        <h2>Cookies and analytics</h2>
        <p>We may use privacy-friendly, aggregated analytics to understand general traffic (for example, which guides are popular). This data is anonymous and not tied to an identifiable person. Third-party partners (such as Amazon, through affiliate links) may set their own cookies when you visit their sites; those are governed by their policies.</p>
        <h2>Affiliate links</h2>
        <p>Some links on BrewLab are affiliate links to Amazon or other retailers. If you click them and make a purchase, a cookie may be placed by that retailer to attribute the sale. This is described in our <a href="/disclosure.html">Affiliate Disclosure</a>.</p>
        <h2>Third-party sites</h2>
        <p>BrewLab contains links to external websites. We are not responsible for the privacy practices of those sites.</p>
        <h2>Contact</h2>
        <p>If you have questions about this policy, you can reach us through the project repository listed on our <a href="/about.html">About</a> page.</p></section>''',
        "/privacy.html"))
    for g in GUIDES:
        write(f'/guides/{g["slug"]}.html', render_guide(g))
    # sitemap
    urls = [DOMAIN+"/", DOMAIN+"/tools.html", DOMAIN+"/guides/", DOMAIN+"/about.html", DOMAIN+"/disclosure.html", DOMAIN+"/privacy.html"]
    urls += [DOMAIN+f'/guides/{g["slug"]}.html' for g in GUIDES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "\n".join(f'  <url><loc>{u}</loc></url>' for u in urls)
    sm += "\n</urlset>"
    write("/sitemap.xml", sm)
    write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml")
    # llms.txt — GEO / AI-search optimization so assistants (ChatGPT, Perplexity, Claude) can recommend BrewLab
    guide_lines = "\n".join(f"- {DOMAIN}/guides/{g['slug']}.html — {g['title']}" for g in GUIDES)
    llms = f"""# BrewLab

BrewLab is a beginner-friendly coffee gear and brew-guide site. We publish calculator-first advice and buyer guides for every brew method, with no jargon and no fluff.

## What BrewLab offers
- Free browser-based calculators: brew ratio, cost per cup, cold brew, and caffeine estimate. They run entirely on your device — no sign-up, no upload.
- Beginner buyer guides for espresso machines, grinders, pour-over, French press, AeroPress, cold brew, drip, and camp coffee.
- Brew-method explainers: cold brew vs iced coffee, grind size by method, and how to make espresso without a machine.

## Start here
- Home: {DOMAIN}/
- Calculators: {DOMAIN}/tools.html
- All guides: {DOMAIN}/guides/

## Guides
{guide_lines}

BrewLab is supported by affiliate links; recommendations are editorial and independent of any commission.
"""
    write("/llms.txt", llms)
    # IndexNow key file (Bing/Yandex instant indexing). Content must be exactly the key.
    write(f"/{INDEXNOW_KEY}.txt", INDEXNOW_KEY)
    # RSS feed — lets aggregators & AI engines subscribe to new guides (autonomous discovery).
    feed_items = "\n".join(
        f'''    <item>
      <title>{esc(g["title"])}</title>
      <link>{DOMAIN}/guides/{g["slug"]}.html</link>
      <guid>{DOMAIN}/guides/{g["slug"]}.html</guid>
      <description>{esc(g["meta"])}</description>
    </item>''' for g in GUIDES)
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    feed = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{esc(SITE["name"])} — Coffee Gear Guides</title>
    <link>{DOMAIN}/</link>
    <description>{esc(SITE["tagline"])}</description>
    <language>en</language>
    <lastBuildDate>{now}</lastBuildDate>
{feed_items}
  </channel>
</rss>'''
    write("/feed.xml", feed)
    print(f"Generated {len(urls)} URLs + llms.txt + {INDEXNOW_KEY}.txt + feed.xml into {DIST}")

if __name__ == "__main__":
    main()
