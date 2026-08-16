# BrewLab site config — single place to edit before generating.
# Only thing the user MUST change later: AMZ_TAG (their Amazon Associates tracking id).

SITE = {
    "name": "BrewLab",
    "tagline": "Better coffee at home — beginner-friendly gear guides and free brew calculators.",
    # Updated to the real Vercel URL right after the first deploy, then regenerate + redeploy.
    "domain": "https://brewlab-one.vercel.app",
    # <-- USER ACTION (free, ~15 min): paste your Amazon Associates tracking id here, then
    #     run:  python gen.py   &&   vercel deploy --prod --yes --force
    "amz_tag": "brewlab0a-20",
    "amz_search_base": "https://www.amazon.com/s?k=",
    "author": "BrewLab Editorial",
    "lang": "en",
}

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
