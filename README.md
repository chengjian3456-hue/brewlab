# BrewLab

Beginner-friendly coffee gear guides and free brew calculators.

BrewLab helps people make better coffee at home without overspending. It publishes
low-competition buyer's guides (espresso machines, grinders, french press, pour-over,
milk frothers, scales, camping gear) and free interactive tools that run 100% in the
browser.

👉 **Live site: https://brewlab-one.vercel.app**

## What's inside

- `gen.py` — static-site generator (no build step, no dependencies). Run `python gen.py`
  to rebuild the whole site into `./dist`.
- `config.py` — site config. **The only thing you must change is `amz_tag`** — your
  Amazon Associates tracking id. Everything else is pre-filled.
- `data/guides.py` — the 12 long-tail buyer's guides with real product picks.
- `static/js/brew.js` — the free brew-ratio and per-cup cost calculators.
- `static/js/ads.js` — AdSense slot loader (fill `PUB_ID` / `AD_SLOT` to enable).

## How it makes money

- **Amazon Associates** — every guide links to Amazon search results for the recommended
  product via the associate tag in `config.py`.
- **AdSense** — slot-ready; paste your publisher id to turn on display ads.

## Notes

- No servers, no databases, no tracking. Pure static HTML + vanilla JS.
- Affiliate disclosure is shown in the footer on every page (FTC compliant).

## License

MIT — see [LICENSE](LICENSE).
