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
- Real-time **3D** with [Three.js](https://threejs.org) (loaded via CDN). The road is
  extruded from the track centerline; cars are the actual Kenney `.glb` models, inlined
  as base64 so the single `index.html` stays self-contained. A chase camera follows the car.
- `inline_assets.py` re-embeds the car models after you swap them.
- Earlier 2D sprite tooling (`render_sprites.py`, `bake-sprites.html`) is kept for reference.

## Credits / licenses
- Car & track 3D models: **Kenney.nl** kits — CC0.
- F1 circuit geometry: **bacinger/f1-circuits** (real GPS centerlines).
- Game code: original.
