# Grand Tour — top-down arcade racer

A relaxing, addictive top-down racer in a single self-contained HTML file. Cruise the
coast in a yellow sports car, or chase the perfect lap on faithfully recreated F1 circuits.

**Play:** [grand-tour-racer.vercel.app](https://grand-tour-racer.vercel.app) — or open `index.html` locally.

## Controls
- **Touch / mouse:** press and drag **left–right** to steer.
- **Keyboard:** `←` `→` to steer, `R` / `Enter` to retry.
- Keep your speed by driving a **clean line** (Trackmania-style momentum) — hard cornering
  and walls scrub speed. Beat your best lap; a translucent **ghost** replays your record.

## Tracks
- **Coastal Test** — relaxed cruise along the ocean (yellow sports car).
- **Monza**, **Silverstone**, **Red Bull Ring** — built from real circuit centerlines.

## Tech
- Plain HTML5 `<canvas>`, no framework, no build step. Cars are 3D-rendered top-down
  sprite sheets (36 angles) baked from the Kenney kits and inlined as data URIs.
- `render_sprites.py` — software renderer (numpy + trimesh) that bakes a `.glb` model
  into a top-down rotation sheet. `bake-sprites.html` does the same in the browser.

## Credits / licenses
- Car & track 3D models: **Kenney.nl** kits — CC0.
- F1 circuit geometry: **bacinger/f1-circuits** (real GPS centerlines).
- Game code: original.
