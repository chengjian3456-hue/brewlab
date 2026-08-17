"""Shared helpers for BrewLab batch guide chunks."""
def P(name, query, note, pros, cons):
    return {"name": name, "query": query, "note": note, "pros": pros, "cons": cons}

def G(cat, slug, title, meta, h1, intro, picks, advice, faq):
    return (cat, {"slug": slug, "title": title, "meta": meta, "h1": h1,
                  "intro": intro, "picks": picks, "advice": advice,
                  "faq": [(q, a) for q, a in faq]})
