"""Extract the right-hand Urchin half's outline, key positions, mounting holes and
nice!nano position from the Urchin KiCad PCB, for use in the viewer and CAD.

Usage: python3 extract_pcb.py path/to/urchin/main.kicad_pcb out.json

The KiCad file holds both halves joined by mouse bites at x ~ 128 mm. The part with
x < 128 is the right-hand half as seen from above (MCU and thumb keys on the inner,
low-x side; pinky column on the straight, high-x edge). The left half is its mirror.
Coordinates are KiCad's: millimetres, x to the right, y downwards.
"""
import json
import math
import re
import sys

SPLIT_X = 128.0          # halves are joined by mouse bites just above this x
PINKY_EDGE_X = 127.13    # straight pinky-side PCB edge of the right half
MCU_NOTCH_TOP_Y = 36.0   # the MCU mounting ears above this y are squared off


def arc_points(start, mid, end, step=1.0):
    (ax, ay), (bx, by), (cx, cy) = start, mid, end
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-12:
        raise ValueError(f"degenerate arc {start} {mid} {end}")
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    r = math.hypot(ax - ux, ay - uy)
    a0, am, a1 = (math.atan2(y - uy, x - ux) for x, y in (start, mid, end))
    norm = lambda a: a % (2 * math.pi)
    sweep = norm(a1 - a0) if norm(am - a0) < norm(a1 - a0) else -norm(a0 - a1)
    n = max(4, int(abs(sweep) * r / step))
    return [(ux + r * math.cos(a0 + sweep * i / n), uy + r * math.sin(a0 + sweep * i / n)) for i in range(n + 1)]


def edge_segments(src):
    segs = []
    pattern = (r'\(gr_(line|arc)\s*\(start ([-\d.]+) ([-\d.]+)\)\s*(?:\(mid ([-\d.]+) ([-\d.]+)\)\s*)?'
               r'\(end ([-\d.]+) ([-\d.]+)\)(.*?)\(layer "([^"]+)"\)')
    for m in re.finditer(pattern, src, re.S):
        kind, sx, sy, mx, my, ex, ey, _, layer = m.groups()
        if layer != "Edge.Cuts":
            continue
        s, e = (float(sx), float(sy)), (float(ex), float(ey))
        if kind == "line":
            segs.append((s, e))
        else:
            pts = arc_points(s, (float(mx), float(my)), e)
            segs.extend(zip(pts, pts[1:]))
    if not segs:
        raise ValueError("no Edge.Cuts geometry found")
    return segs


def chain(segs):
    key = lambda p: (round(p[0], 2), round(p[1], 2))
    rem, loops = list(segs), []
    while rem:
        loop = list(rem.pop(0))
        grown = True
        while grown:
            grown = False
            for i, (a, b) in enumerate(rem):
                if key(a) == key(loop[-1]):
                    loop.append(b); rem.pop(i); grown = True; break
                if key(b) == key(loop[-1]):
                    loop.append(a); rem.pop(i); grown = True; break
        loops.append(loop)
    return loops


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    length = math.hypot(bx - ax, by - ay) or 1e-9
    dist = lambda q: abs((bx - ax) * (ay - q[1]) - (ax - q[0]) * (by - ay)) / length
    i, dm = max(((i, dist(q)) for i, q in enumerate(pts[1:-1], 1)), key=lambda t: t[1])
    if dm > eps:
        return rdp(pts[: i + 1], eps)[:-1] + rdp(pts[i:], eps)
    return [pts[0], pts[-1]]


def right_half_outline(src):
    loop = max(chain(edge_segments(src)), key=len)
    pts = [p for p in loop if p[0] < SPLIT_X]
    n = len(pts)
    # start right after the jump across the mouse-bite gap so the sequence is contiguous
    j = max(range(n), key=lambda i: math.dist(pts[i], pts[(i + 1) % n]))
    pts = rdp(pts[j + 1:] + pts[: j + 1], 0.15)
    # flatten the mouse-bite tabs and square off the MCU mounting ears
    pts = [(min(x, PINKY_EDGE_X), y) for x, y in pts]
    ears = [i for i, (x, y) in enumerate(pts) if x < 36.0 and y < 39.9]
    if not ears or ears != list(range(ears[0], ears[-1] + 1)):
        raise ValueError("MCU notch not where expected; check the outline by hand")
    pts = pts[: ears[0]] + [(17.6, MCU_NOTCH_TOP_Y), (36.0, MCU_NOTCH_TOP_Y)] + pts[ears[-1] + 1:]
    out = []
    for p in pts:
        if not out or math.dist(p, out[-1]) > 0.3:
            out.append(p)
    return [[round(x, 2), round(y, 2)] for x, y in out]


def footprints(src):
    fps = []
    pattern = r'\(footprint "([^"]+)"\s*\(layer "([^"]+)"\)\s*\(uuid "[^"]+"\)\s*\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)'
    for m in re.finditer(pattern, src):
        name, layer, x, y, rot = m.groups()
        fps.append(dict(name=name.split(":")[-1], layer=layer, x=float(x), y=float(y), rot=float(rot or 0)))
    return [f for f in fps if f["x"] < SPLIT_X]


def main(pcb_path, out_path):
    src = open(pcb_path).read()
    fps = footprints(src)
    keys = [[round(f["x"], 2), round(f["y"], 2), f["rot"]] for f in fps if f["name"].startswith("SW_Hotswap")]
    if len(keys) != 17:
        raise ValueError(f"expected 17 keys on the right half, found {len(keys)}")
    holes = []
    for f in fps:
        if "M2_hole" in f["name"] and all(math.dist((f["x"], f["y"]), h) > 4 for h in holes):
            holes.append([round(f["x"], 2), round(f["y"], 2)])
    nanos = [f for f in fps if f["name"] == "nice_nano"]
    if len(nanos) != 1:
        raise ValueError(f"expected one nice_nano on the right half, found {len(nanos)}")
    others = [dict(name=f["name"], layer=f["layer"], x=round(f["x"], 2), y=round(f["y"], 2), rot=f["rot"])
              for f in fps if f["name"] in ("smt-slider-switch", "SW_RESET", "1pin_Battery", "nice_view", "Tenting_Puck2_no_pads")]
    data = dict(outline=right_half_outline(src), keys=keys, holes=holes,
                nano=[nanos[0]["x"], nanos[0]["y"]], other_parts=others)
    json.dump(data, open(out_path, "w"), indent=1)
    print(f"{len(data['outline'])} outline points, {len(keys)} keys, {len(holes)} holes -> {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
