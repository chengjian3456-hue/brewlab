# BrewLab site config — single place to edit before generating.
# Only thing the user MUST change later: AMZ_TAG (their Amazon Associates tracking id).

SITE = {
    "name": "BrewLab",
    "tagline": "Better coffee at home — beginner-friendly gear guides and free brew calculators.",
    # Updated to the real Vercel URL right after the first deploy, then regenerate + redeploy.
    "domain": "https://brewlab-one.vercel.app",
    # <-- Amazon Associates tracking id (approved 2026-08-17: brewlab-20). Then:
    #     run:  python gen.py   &&   vercel deploy --prod --yes --force
    "amz_tag": "brewlab-20",
    "amz_search_base": "https://www.amazon.com/s?k=",
    "author": "BrewLab Editorial",
    "lang": "en",
}

# IndexNow key for instant indexing on Bing/Yandex (no identity needed).
# The key file is served at /{INDEXNOW_KEY}.txt; we ping api.indexnow.org after each deploy.
INDEXNOW_KEY = "d4e5f60718293a4b5c6d7e8f90a1b2c3"

# Google Search Console verification (compresses Google indexing from weeks to days).
# Leave empty until the user claims the property once in GSC and pastes the code here.
# Safe, one-time action (verify own site) — not public posting, no ban risk.
GSC_CODE = ""

# Global footer affiliate disclosure (required by Amazon Associates + FTC).
DISCLOSURE = (
    "BrewLab is reader-supported. When you buy through links on our site, "
    "we may earn an affiliate commission (at no extra cost to you). "
    "As an Amazon Associate we earn from qualifying purchases. "
    "This never affects our editorial independence."
)

NAV = [
    ("Home", "/"),
    ("Calculators", "/tools.html"),
    ("Guides", "/guides/"),
    ("Disclosure", "/disclosure.html"),
    ("Privacy", "/privacy.html"),
    ("About", "/about.html"),
]
