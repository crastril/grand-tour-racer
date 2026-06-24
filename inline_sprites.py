#!/usr/bin/env python
"""Embed sprites/<key>.png into index.html as base64 data URIs (works in any context).
Re-run after every re-bake. Matches both a path and an existing data URI.
"""
import base64, re
HTML = "index.html"
KEYS = ["mustang", "f1"]

html = open(HTML, encoding="utf-8").read()
for key in KEYS:
    b = base64.b64encode(open(f"sprites/{key}.png", "rb").read()).decode()
    uri = "data:image/png;base64," + b
    html, n = re.subn(rf'({key}:\s*\{{ src:")[^"]*(")', lambda m: m.group(1)+uri+m.group(2), html)
    print(f"{key}: replaced {n}")
open(HTML, "w", encoding="utf-8").write(html)
print("index.html size:", len(html))
