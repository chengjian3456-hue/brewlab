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
- `data/guides.py` — 300+ long-tail buyer's guides with real product picks (espresso,
  grinders, french press, pour-over, gift guides, seasonal Black Friday / Cyber Monday).
- `static/js/brew.js` — the free brew-ratio and per-cup cost calculators.
- `static/js/ads.js` — AdSense slot loader (fill `PUB_ID` / `AD_SLOT` to enable).

## Free embeddable tool

Grab the **Brew Ratio & Timer Calculator** — free, no sign-up, runs entirely in the
browser, no ads. Embed it on your coffee blog or café site in one line:

```html
<iframe src="https://brewlab-one.vercel.app/brew-calculator.html"
        width="420" height="820" style="border:0;border-radius:14px"
        title="Brew Ratio & Timer Calculator"></iframe>
```

Pick a brew method, enter your dose, get exact water weight — plus a built-in brew
timer and cost-per-cup estimate. Single static HTML, zero dependencies.

## How it makes money

- **Amazon Associates** — every guide links to Amazon search results for the recommended
  product via the associate tag in `config.py`.
- **AdSense** — slot-ready; paste your publisher id to turn on display ads.

## Notes

- No servers, no databases, no tracking. Pure static HTML + vanilla JS.
- Affiliate disclosure is shown in the footer on every page (FTC compliant).

## License

MIT — see [LICENSE](LICENSE).
