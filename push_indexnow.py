#!/usr/bin/env python3
"""Push all BrewLab URLs to IndexNow for instant Bing/Yandex indexing."""
import json, urllib.request, os
os.environ["HTTPS_PROXY"] = ""
os.environ["HTTP_PROXY"] = ""
import re

DOMAIN = "https://brewlab-one.vercel.app"
KEY = "d4e5f60718293a4b5c6d7e8f90a1b2c3"

txt = open("data/guides.py", encoding="utf-8").read()
slugs = re.findall(r'"slug":\s*"([^"]+)"', txt)
urls = [DOMAIN + "/", DOMAIN + "/tools.html", DOMAIN + "/guides/",
        DOMAIN + "/about.html", DOMAIN + "/disclosure.html", DOMAIN + "/privacy.html"]
urls += [f"{DOMAIN}/guides/{s}.html" for s in slugs]

def chunk(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]

body = {"host": "brewlab-one.vercel.app", "key": KEY, "urlList": urls}
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json"},
    method="POST")
try:
    r = urllib.request.urlopen(req, timeout=30)
    print(f"IndexNow full batch: HTTP {r.status} for {len(urls)} URLs")
except urllib.error.HTTPError as e:
    print(f"IndexNow HTTPError {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    print(f"IndexNow error: {e}")
