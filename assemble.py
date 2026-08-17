#!/usr/bin/env python3
"""Assemble data/guides.py from the hand-written 47 + all batch chunks (_b_*.py).
Dedupes by slug (hand-written guides win) and writes a flat GUIDES list of dicts."""
import os, sys, glob, importlib

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import data.guides as old_mod
OLD = old_mod.GUIDES

chunk_files = sorted(glob.glob(os.path.join(ROOT, "data", "_b_*.py")))
chunks = []
for f in chunk_files:
    name = os.path.splitext(os.path.basename(f))[0]
    if name == "_b_common":
        continue
    chunks.append(name)

seen = set(g["slug"] for g in OLD)
merged = [dict(g) for g in OLD]
skipped = []
added = 0
for c in chunks:
    mod = importlib.import_module("data." + c)
    for item in mod.GUIDES:
        cat, d = item
        if d["slug"] in seen:
            skipped.append(d["slug"])
            continue
        seen.add(d["slug"])
        merged.append(dict(d))
        added += 1

# final safety dedup (keep first occurrence of each slug)
final = []
_seen = set()
for g in merged:
    if g["slug"] in _seen:
        continue
    _seen.add(g["slug"])
    final.append(g)
merged = final

# ---------- formatter ----------
def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def fmt(v, indent):
    pad = "    " * indent
    pad1 = "    " * (indent + 1)
    if isinstance(v, dict):
        if not v:
            return "{}"
        lines = [f'{pad1}{q(k)}: {fmt(val, indent + 1)}' for k, val in v.items()]
        return "{\n" + ",\n".join(lines) + "\n" + pad + "}"
    if isinstance(v, list):
        if not v:
            return "[]"
        lines = [f'{pad1}{fmt(x, indent + 1)}' for x in v]
        return "[\n" + ",\n".join(lines) + "\n" + pad + "]"
    if isinstance(v, tuple):
        if not v:
            return "()"
        inner = ", ".join(fmt(x, indent) for x in v)
        return "(" + inner + ",)" if len(v) == 1 else "(" + inner + ")"
    if isinstance(v, str):
        return q(v)
    if isinstance(v, bool):
        return "True" if v else "False"
    if v is None:
        return "None"
    return repr(v)

header = (
    "# BrewLab guide data. Each entry is one long-tail, low-competition buyer guide.\n"
    "# `query` is the Amazon search term used to build the affiliate link (no ASIN needed).\n"
    "# This file is assembled from data/guides.py (hand-written) + data/_b_*.py (batch chunks).\n"
    "# Regenerate with: python assemble.py\n\n"
)
lines = [header, "GUIDES = [\n"]
for g in merged:
    lines.append("    " + fmt(g, 1) + ",\n")
lines.append("]\n")

out = os.path.join(ROOT, "data", "guides.py")
with open(out, "w", encoding="utf-8") as f:
    f.write("".join(lines))

print(f"OLD hand-written guides : {len(OLD)}")
print(f"Batch chunks merged     : {added}")
print(f"Skipped duplicates      : {len(skipped)}")
if skipped:
    print("  dup slugs:", ", ".join(skipped))
print(f"TOTAL GUIDES            : {len(merged)}")
