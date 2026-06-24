#!/usr/bin/env python
"""Embed the car GLB models into index.html as base64 (placeholders __GLB_*__)."""
import base64
HTML = "index.html"
MODELS = {
    "__GLB_F1__":      "sprites/kenney_racing-kit/Models/GLTF format/raceCarRed.glb",
    "__GLB_MUSTANG__": "sprites/kenney_car-kit/Models/GLB format/sedan-sports.glb",
}
html = open(HTML, encoding="utf-8").read()
for ph, path in MODELS.items():
    b = base64.b64encode(open(path, "rb").read()).decode()
    n = html.count(ph)
    html = html.replace(ph, b)
    print(f"{ph}: {n} occurrence(s), {len(b)} b64 chars")
open(HTML, "w", encoding="utf-8").write(html)
print("index.html size:", len(html))
