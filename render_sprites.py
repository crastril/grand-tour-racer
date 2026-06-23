#!/usr/bin/env python
"""Software-render a GLB model into a top-down rotation sprite sheet (transparent PNG).
No GPU / Blender needed. Flat-shaded, which matches the Kenney low-poly look.

usage:
  python render_sprites.py <model.glb> <out.png> [--frames 36] [--cols 6] [--cell 160] [--tilt 28]
"""
import sys, argparse, numpy as np, trimesh
from PIL import Image

def load_geometry(path):
    scene = trimesh.load(path, process=False)
    verts, faces, fcol, fnrm = [], [], [], []
    items = []
    if isinstance(scene, trimesh.Trimesh):
        items = [(scene, np.eye(4))]
    else:
        for node in scene.graph.nodes_geometry:
            T, gname = scene.graph[node]
            items.append((scene.geometry[gname], np.asarray(T, float)))
    off = 0
    for geom, T in items:
        v = trimesh.transformations.transform_points(np.asarray(geom.vertices, float), T)
        f = np.asarray(geom.faces, int)
        # per-vertex colour (samples texture if present), then per-face mean
        try:
            vc = np.asarray(geom.visual.to_color().vertex_colors, float) / 255.0
            if vc.ndim == 1:                      # uniform flat colour for whole submesh
                fc = np.tile(vc[:3], (len(f), 1))
            else:                                 # per-vertex -> per-face mean
                fc = vc[:, :3][f].mean(axis=1)
        except Exception:
            base = (0.8, 0.8, 0.82)
            try:
                bcf = geom.visual.material.baseColorFactor
                if bcf is not None: base = np.asarray(bcf, float)[:3]
            except Exception: pass
            fc = np.tile(base, (len(f), 1))
        n = np.asarray(geom.face_normals, float) @ T[:3, :3].T
        n /= (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
        verts.append(v); faces.append(f + off); fcol.append(fc); fnrm.append(n)
        off += len(v)
    return (np.concatenate(verts), np.concatenate(faces),
            np.concatenate(fcol), np.concatenate(fnrm))

def roty(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def render_frame(V, F, FC, FN, cam, light, half, cell):
    right, camup, fwd = cam
    img = np.zeros((cell, cell, 4), np.float32)
    zbuf = np.full((cell, cell), 1e9, np.float32)
    # project all verts
    sx = V @ right; sy = V @ camup; dz = V @ fwd
    px = (sx / half * 0.5 + 0.5) * (cell - 1)
    py = (-sy / half * 0.5 + 0.5) * (cell - 1)   # flip y for image space
    # shading per face
    ndl = np.clip(FN @ light, 0, 1)
    shade = (0.35 + 0.75 * ndl)[:, None]
    col = np.clip(FC * shade, 0, 1)
    for i in range(len(F)):
        a, b, c = F[i]
        x = np.array([px[a], px[b], px[c]]); y = np.array([py[a], py[b], py[c]])
        z = np.array([dz[a], dz[b], dz[c]])
        minx, maxx = int(np.floor(x.min())), int(np.ceil(x.max()))
        miny, maxy = int(np.floor(y.min())), int(np.ceil(y.max()))
        minx = max(minx, 0); miny = max(miny, 0)
        maxx = min(maxx, cell - 1); maxy = min(maxy, cell - 1)
        if minx > maxx or miny > maxy: continue
        xs = np.arange(minx, maxx + 1); ys = np.arange(miny, maxy + 1)
        gx, gy = np.meshgrid(xs, ys)
        d = ((y[1]-y[2])*(x[0]-x[2]) + (x[2]-x[1])*(y[0]-y[2]))
        if abs(d) < 1e-9: continue
        w0 = ((y[1]-y[2])*(gx-x[2]) + (x[2]-x[1])*(gy-y[2])) / d
        w1 = ((y[2]-y[0])*(gx-x[2]) + (x[0]-x[2])*(gy-y[2])) / d
        w2 = 1 - w0 - w1
        inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not inside.any(): continue
        zz = w0*z[0] + w1*z[1] + w2*z[2]
        gxi = gx[inside]; gyi = gy[inside]; zzi = zz[inside]
        cur = zbuf[gyi, gxi]
        better = zzi < cur
        gxi, gyi, zzi = gxi[better], gyi[better], zzi[better]
        zbuf[gyi, gxi] = zzi
        img[gyi, gxi, 0:3] = col[i]
        img[gyi, gxi, 3] = 1.0
    return (img * 255).astype(np.uint8)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model"); ap.add_argument("out")
    ap.add_argument("--frames", type=int, default=36)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--cell", type=int, default=160)
    ap.add_argument("--tilt", type=float, default=28.0)
    ap.add_argument("--base", type=float, default=0.0, help="yaw of frame 0 (deg)")
    ap.add_argument("--tint", type=str, default="", help="recolor main body panel to this hex, e.g. f2c233")
    a = ap.parse_args()

    V0, F, FC, FN0 = load_geometry(a.model)
    V0 = V0 - V0.mean(axis=0)

    if a.tint:
        tint = np.array([int(a.tint[i:i+2], 16) for i in (0, 2, 4)], float) / 255.0
        tri = V0[F]
        area = 0.5 * np.linalg.norm(np.cross(tri[:, 1]-tri[:, 0], tri[:, 2]-tri[:, 0]), axis=1)
        mx = FC.max(1); mn = FC.min(1); sat = (mx - mn) / (mx + 1e-6)
        chroma = sat > 0.22                      # ignore black tyres / grey / glass
        if chroma.any():
            dom = np.average(FC[chroma], axis=0, weights=area[chroma])
            close = (np.linalg.norm(FC - dom, axis=1) < 0.33) & chroma
            FC[close] = tint                      # repaint the body, keep wheels/glass/lights

    th = np.radians(a.tilt)
    fwd = np.array([0, -np.cos(th), -np.sin(th)]); fwd /= np.linalg.norm(fwd)
    tmp = np.array([0, 0, -1.0])
    right = np.cross(tmp, fwd); right /= np.linalg.norm(right)
    camup = np.cross(fwd, right)
    cam = (right, camup, fwd)
    light = np.array([-0.5, 1.0, 0.45]); light /= np.linalg.norm(light)

    # fit: max projected extent over a few yaws so it never clips while spinning
    half = 0
    for ya in np.linspace(0, 2*np.pi, 12, endpoint=False):
        R = roty(ya); Vt = V0 @ R.T
        half = max(half, np.abs(Vt @ right).max(), np.abs(Vt @ camup).max())
    half *= 1.08

    cols = a.cols; rows = int(np.ceil(a.frames / cols)); cell = a.cell
    sheet = np.zeros((rows*cell, cols*cell, 4), np.uint8)
    base = np.radians(a.base)
    for i in range(a.frames):
        R = roty(base + i*2*np.pi/a.frames)
        V = V0 @ R.T; FN = FN0 @ R.T
        frame = render_frame(V, F, FC, FN, cam, light, half, cell)
        r, c = divmod(i, cols)
        sheet[r*cell:(r+1)*cell, c*cell:(c+1)*cell] = frame
        print(f"\rframe {i+1}/{a.frames}", end="", flush=True)
    print()
    Image.fromarray(sheet, "RGBA").save(a.out)
    # aspect hint (footprint width x vs length z)
    ext = V0.max(axis=0) - V0.min(axis=0)
    w, l = ext[0], ext[2]
    dh = 40.0; dw = round(dh * (w / l), 1) if l else dh
    print(f"saved {a.out}  ({cols}x{rows} cells, {cell}px)")
    print(f"suggest: frames:{a.frames}, cols:{cols}, rows:{rows}, dw:{dw}, dh:{dh}")

if __name__ == "__main__":
    main()
