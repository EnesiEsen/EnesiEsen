"""Hand-drawn style scenes for the project cards, one per add-on, as SVG text (1200 x 420).

Style: black ink outlines that wobble a little (SVG displacement filter), flat muted fills, hatching and paper grain, in
the palette of the "Walter" drawing: dark maroon-brown room, olive and tan, a green cross, red and yellow accents.
Everything is generated from code with seeded randomness, so the cards are reproducible.
"""
import math
import random

W, H = 1200, 420
INK = "#0d0908"


def defs(seed):
    return f"""<defs>
<filter id="rough" x="-3%" y="-3%" width="106%" height="106%"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="{seed}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>
<filter id="rough2" x="-3%" y="-3%" width="106%" height="106%"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="{seed + 7}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3"/></filter>
<filter id="soft" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(40)"><line x1="0" y1="0" x2="0" y2="9" stroke="#000" stroke-opacity=".34" stroke-width="2"/></pattern>
<pattern id="hatch2" width="13" height="13" patternUnits="userSpaceOnUse" patternTransform="rotate(-32)"><line x1="0" y1="0" x2="0" y2="13" stroke="#000" stroke-opacity=".28" stroke-width="2"/></pattern>
</defs>"""


def fmt(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def poly(points):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points) + " Z"


def smooth(points, closed=False):
    """Catmull-Rom spline through the points as an SVG path (open unless closed)."""
    pts = list(points)
    n = len(pts)
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n if closed else n - 1):
        p0, p1 = pts[(i - 1) % n] if (closed or i > 0) else pts[0], pts[i]
        p2, p3 = pts[(i + 1) % n], pts[(i + 2) % n] if (closed or i + 2 < n) else pts[(i + 1) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + (" Z" if closed else "")


def shape(d, fill, width=4, hatch="hatch", shade=0.5, flt="rough"):
    """A filled shape with an ink outline and a hatching overlay."""
    out = f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{width}" stroke-linejoin="round" filter="url(#{flt})"/>'
    if hatch:
        out += f'<path d="{d}" fill="url(#{hatch})" opacity="{shade}" filter="url(#{flt})"/>'
    return out


def line(x1, y1, x2, y2, color=INK, width=3, extra=""):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" {extra}/>')


def grain():
    return ("<filter id='gr'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2' seed='3'/>"
            "<feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .5 0'/></filter>"
            f'<rect width="{W}" height="{H}" filter="url(#gr)" opacity=".16" style="mix-blend-mode:overlay"/>')


def wrap(seed, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f"{defs(seed)}{body}{grain()}</svg>")


# --------------------------------------------------------------------------------------------- Terrain Blend
def scene_terrain():
    rnd = random.Random(11)
    b = ['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1213"/>'
         '<stop offset=".45" stop-color="#4a3330"/><stop offset=".66" stop-color="#a98562"/></linearGradient>'
         '<radialGradient id="halo"><stop offset="0" stop-color="#e6dcc4" stop-opacity=".35"/>'
         '<stop offset="1" stop-color="#e6dcc4" stop-opacity="0"/></radialGradient></defs>']
    b.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    b.append('<circle cx="930" cy="108" r="90" fill="url(#halo)"/>')
    b.append(f'<circle cx="930" cy="108" r="34" fill="#e6dcc4" stroke="{INK}" stroke-width="4" filter="url(#rough)"/>')
    far = [(0, 262), (90, 215), (170, 245), (280, 190), (380, 238), (470, 170), (560, 232), (660, 150), (760, 228),
           (850, 182), (950, 240), (1040, 196), (1120, 230), (1200, 205), (1200, 310), (0, 310)]
    b.append(shape(poly(far), "#4b3a39", 4, "hatch2", 0.7))
    mid = [(0, 288), (140, 246), (260, 270), (400, 232), (540, 274), (700, 240), (860, 278), (1000, 248), (1200, 282),
           (1200, 340), (0, 340)]
    b.append(shape(poly(mid), "#5f4a40", 4, "hatch", 0.55))
    for tx in (610, 655, 700, 742, 790, 1040, 1085):  # small pines on the middle ridge
        ty = 262 + rnd.randint(-6, 8)
        for k, (w, h) in enumerate(((22, 26), (17, 22), (12, 18))):
            y0 = ty - k * 14
            b.append(shape(poly([(tx - w, y0), (tx, y0 - h), (tx + w, y0)]), "#2c3a28", 3, None))
    ridge = [(0, 340), (250, 304), (520, 296), (800, 308), (1050, 292), (1200, 304)]
    hill = smooth(ridge) + " L1200 420 L0 420 Z"
    b.append(f'<clipPath id="hill"><path d="{hill}"/></clipPath>')
    b.append(shape(hill, "#56733a", 4, "hatch", 0.35))
    b.append('<g clip-path="url(#hill)">')
    # zones: blurred edges show the blend between texture sets
    path_l = [(700, 424), (790, 372), (850, 336), (935, 313), (1020, 300)]
    path_r = [(1062, 300), (992, 324), (950, 348), (936, 384), (958, 424)]
    b.append(f'<path d="{smooth(path_l)} L{path_r[0][0]} {path_r[0][1]} {smooth(path_r)[smooth(path_r).index("C"):]} Z" fill="#c4a56f" filter="url(#soft)"/>')
    b.append('<ellipse cx="1010" cy="352" rx="190" ry="58" fill="#7d776f" filter="url(#soft)"/>')
    b.append('<ellipse cx="560" cy="392" rx="150" ry="30" fill="#3a2a22" filter="url(#soft)"/>')
    b.append('<ellipse cx="560" cy="388" rx="70" ry="9" fill="#7a6a62" opacity=".7" filter="url(#rough2)"/>')
    # wireframe of the terrain mesh in perspective
    for i in range(-14, 15):
        b.append(line(600 + i * 40, 296, 600 + i * 150, 424, "#e2d9c6", 1.4, 'opacity=".16"'))
    for k in range(1, 9):
        y = 296 + (k ** 1.55) * 3.6
        b.append(line(0, y, W, y, "#e2d9c6", 1.4, 'opacity=".16"'))
    b.append("</g>")
    # rocks
    for cx, cy, s in ((1090, 330, 0.95), (1150, 350, 1.2), (780, 372, 0.8)):
        pts = [(cx - 30 * s, cy + 18 * s), (cx - 22 * s, cy - 10 * s), (cx - 2 * s, cy - 24 * s), (cx + 24 * s, cy - 12 * s),
               (cx + 32 * s, cy + 18 * s)]
        b.append(shape(poly(pts), "#8a847b", 4, "hatch", 0.6))
        b.append(line(cx - 2 * s, cy - 24 * s, cx + 2 * s, cy + 6 * s, INK, 2.5, 'filter="url(#rough2)"'))
    b.append(shape(smooth(ridge), "none", 4.5, None))
    for _ in range(70):  # grass tufts
        x, y = rnd.uniform(0, W), rnd.uniform(352, 414)
        for dx, dy in ((-7, -16), (0, -22), (7, -15)):
            b.append(f'<path d="M{x:.1f} {y:.1f} q{dx / 2:.1f} {dy / 2:.1f} {dx:.1f} {dy:.1f}" stroke="{INK}" stroke-width="3" '
                     f'fill="none" stroke-linecap="round"/>')
            b.append(f'<path d="M{x:.1f} {y:.1f} q{dx / 2:.1f} {dy / 2:.1f} {dx:.1f} {dy:.1f}" stroke="#86a45a" stroke-width="1.4" '
                     f'fill="none" stroke-linecap="round"/>')
    return wrap(11, "".join(b))


# ------------------------------------------------------------------------------------------------ Retopo Kit
def scene_retopo():
    rnd = random.Random(5)
    top = [(553, 282), (572, 258), (618, 246), (676, 218), (742, 194), (830, 186), (900, 196), (948, 230), (1000, 246),
           (1050, 258), (1068, 284)]
    xs, ys = [p[0] for p in top], [p[1] for p in top]

    def top_y(x):
        x = min(max(x, xs[0]), xs[-1])
        for i in range(len(xs) - 1):
            if xs[i] <= x <= xs[i + 1]:
                t = (x - xs[i]) / (xs[i + 1] - xs[i])
                return ys[i] * (1 - t) + ys[i + 1] * t
        return ys[-1]

    body_d = smooth(top) + " L1064 318 L560 318 Z"
    b = [f'<rect width="{W}" height="{H}" fill="#1c1413"/>']
    for x in range(0, W, 40):  # blueprint grid
        b.append(line(x, 0, x, H, "#e2d9c6", 1, 'opacity=".07"'))
    for y in range(0, H, 40):
        b.append(line(0, y, W, y, "#e2d9c6", 1, 'opacity=".07"'))
    b.append('<ellipse cx="812" cy="348" rx="300" ry="14" fill="#000" opacity=".55"/>')
    b.append(f'<clipPath id="car"><path d="{body_d}"/></clipPath>')
    b.append(shape(body_d, "#6a5240", 5, "hatch", 0.4))
    # messy triangle mesh (before) on the left half
    b.append('<g clip-path="url(#car)">')
    pts = {}
    for i in range(0, 14):
        for j in range(0, 8):
            pts[i, j] = (548 + i * 21 + rnd.uniform(-8, 8), 180 + j * 20 + rnd.uniform(-8, 8))
    for i in range(0, 13):
        for j in range(0, 7):
            a, bb, c, d = pts[i, j], pts[i + 1, j], pts[i, j + 1], pts[i + 1, j + 1]
            segs = [(a, bb), (a, c)] + ([(a, d)] if rnd.random() < .5 else [(bb, c)])
            for p, q in segs:
                if p[0] < 806 and q[0] < 806:
                    b.append(line(p[0], p[1], q[0], q[1], "#b3a58c", 1.5, 'opacity=".75"'))
    # clean quad flow (after) on the right half
    for k in range(1, 6):
        t = k / 6
        pl = " ".join(f"{x},{top_y(x) * (1 - t) + 318 * t:.1f}" for x in range(806, 1072, 10))
        b.append(f'<polyline points="{pl}" fill="none" stroke="#e0cf45" stroke-width="2.6"/>')
    for x in range(806, 1072, 27):
        b.append(line(x, top_y(x), x, 318, "#e0cf45", 2.6))
        for k in range(0, 7):
            t = k / 6
            b.append(f'<rect x="{x - 3:.1f}" y="{top_y(x) * (1 - t) + 318 * t - 3:.1f}" width="6" height="6" fill="#e0cf45"/>')
    b.append("</g>")
    b.append(shape(smooth(top) + " L1064 318 L560 318 Z", "none", 5, None))
    win = [(700, 226), (748, 202), (826, 194), (892, 204), (928, 232)]
    b.append(shape(smooth(win) + " L928 232 Z", "#2f3b40", 4, "hatch2", 0.5))
    b.append(line(806, 190, 806, 232, INK, 3, 'stroke-dasharray="2 8"'))
    for cx, clean in ((650, False), (985, True)):  # wheels
        b.append(f'<circle cx="{cx}" cy="322" r="54" fill="#140e0d" filter="url(#rough2)"/>')
        b.append(shape(f"M{cx - 46} 322 a46 46 0 1 0 92 0 a46 46 0 1 0 -92 0 Z", "#2b2220", 5, None))
        b.append(f'<circle cx="{cx}" cy="322" r="24" fill="#6a5f55" stroke="{INK}" stroke-width="4" filter="url(#rough2)"/>')
        if clean:
            for r in (31, 39):
                b.append(f'<circle cx="{cx}" cy="322" r="{r}" fill="none" stroke="#e0cf45" stroke-width="2.4"/>')
            for a in range(0, 360, 30):
                b.append(line(cx + 24 * math.cos(math.radians(a)), 322 + 24 * math.sin(math.radians(a)),
                              cx + 40 * math.cos(math.radians(a)), 322 + 40 * math.sin(math.radians(a)), "#e0cf45", 2))
        else:
            for _ in range(18):
                a1, a2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
                b.append(line(cx + 38 * math.cos(a1), 322 + 38 * math.sin(a1), cx + 30 * math.cos(a2), 322 + 30 * math.sin(a2),
                              "#b3a58c", 1.5, 'opacity=".8"'))
    # guide curve with handles
    b.append('<path d="M596 268 C700 236 900 236 1048 270" fill="none" stroke="#c0392f" stroke-width="5" stroke-linecap="round" filter="url(#rough2)"/>')
    for hx, hy, px, py in ((700, 236, 596, 268), (900, 236, 1048, 270)):
        b.append(line(px, py, hx, hy, "#c0392f", 2, 'stroke-dasharray="6 6"'))
        b.append(f'<circle cx="{hx}" cy="{hy}" r="7" fill="#17100f" stroke="#c0392f" stroke-width="3.5"/>')
        b.append(f'<rect x="{px - 8}" y="{py - 8}" width="16" height="16" fill="#c0392f" stroke="{INK}" stroke-width="3"/>')
    return wrap(5, "".join(b))


# ----------------------------------------------------------------------------------------------- FiveM Toolkit
def cube(cx, cy, s, detail):
    """An isometric crate; `detail` 2 = planks and nails, 1 = one plank line, 0 = bare wireframe (LOD steps)."""
    dx, dy = s * 0.87, s * 0.5
    top = [(cx, cy - 2 * dy - s * 0.1), (cx + dx, cy - dy - s * 0.1), (cx, cy - s * 0.1), (cx - dx, cy - dy - s * 0.1)]
    left = [(cx - dx, cy - dy - s * 0.1), (cx, cy - s * 0.1), (cx, cy + s * 0.9), (cx - dx, cy + s * 0.9 - dy)]
    right = [(cx, cy - s * 0.1), (cx + dx, cy - dy - s * 0.1), (cx + dx, cy + s * 0.9 - dy), (cx, cy + s * 0.9)]
    out = []
    fill = ("#b08a63", "#7a5a3f", "#5f4430")
    if detail == 0:
        for face, col in zip((left, right, top), fill[1:] + fill[:1]):
            out.append(f'<path d="{poly(face)}" fill="{col}" fill-opacity=".35" stroke="#e2d9c6" stroke-width="3" stroke-dasharray="7 6"/>')
        return "".join(out)
    for face, col in ((left, fill[1]), (right, fill[2]), (top, fill[0])):
        out.append(shape(poly(face), col, 4, "hatch", 0.4, "rough2"))
    lines = 3 if detail == 2 else 1
    for k in range(1, lines + 1):
        t = k / (lines + 1)
        for face in (left, right):
            a = (face[0][0] * (1 - t) + face[3][0] * t, face[0][1] * (1 - t) + face[3][1] * t)
            c = (face[1][0] * (1 - t) + face[2][0] * t, face[1][1] * (1 - t) + face[2][1] * t)
            out.append(line(a[0], a[1], c[0], c[1], INK, 2.6))
    if detail == 2:
        for face in (left, right):
            for p in face:
                q = (p[0] * 0.86 + (face[0][0] + face[2][0]) / 2 * 0.14, p[1] * 0.86 + (face[0][1] + face[2][1]) / 2 * 0.14)
                out.append(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="2.6" fill="#d8cfbd" stroke="{INK}" stroke-width="1.4"/>')
    return "".join(out)


def scene_fivem():
    rnd = random.Random(23)
    b = ['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#150e11"/>'
         '<stop offset=".5" stop-color="#3a1c20"/><stop offset=".8" stop-color="#a8452f"/></linearGradient>'
         '<radialGradient id="lamp"><stop offset="0" stop-color="#e0cf45" stop-opacity=".7"/>'
         '<stop offset="1" stop-color="#e0cf45" stop-opacity="0"/></radialGradient></defs>']
    b.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    b.append(f'<circle cx="900" cy="262" r="92" fill="#d05a3a" opacity=".9" stroke="{INK}" stroke-width="4" filter="url(#rough)"/>')
    x = 330
    while x < 1230:  # skyline, far row then near row
        w, h = rnd.randint(46, 92), rnd.randint(90, 215)
        d = poly([(x, 330), (x, 330 - h), (x + w, 330 - h), (x + w, 330)])
        b.append(shape(d, "#241719", 4, "hatch", 0.35))
        if rnd.random() < .3:
            b.append(line(x + w / 2, 330 - h, x + w / 2, 330 - h - 26, INK, 3))
        for wy in range(int(330 - h + 14), 318, 22):
            for wx in range(int(x + 9), int(x + w - 10), 17):
                if rnd.random() < .55:
                    b.append(f'<rect x="{wx}" y="{wy}" width="9" height="12" fill="#e0cf45" opacity="{rnd.uniform(.5, .95):.2f}"/>')
        x += w + rnd.randint(-4, 10)
    for px, lean in ((505, -1), (1090, 1)):  # palm trees
        trunk = [(px, 345), (px + lean * 14, 280), (px + lean * 8, 215), (px - lean * 6, 160)]
        b.append(f'<path d="{smooth(trunk)}" fill="none" stroke="{INK}" stroke-width="17" stroke-linecap="round" filter="url(#rough2)"/>')
        b.append(f'<path d="{smooth(trunk)}" fill="none" stroke="#5a4333" stroke-width="10" stroke-linecap="round" filter="url(#rough2)"/>')
        tx, ty = trunk[-1]
        for a in range(-80, 260, 48):
            ex, ey = tx + 86 * math.cos(math.radians(a)), ty + 62 * math.sin(math.radians(a)) + 30
            cx_, cy_ = tx + 48 * math.cos(math.radians(a)), ty + 42 * math.sin(math.radians(a)) - 24
            fr = f"M{tx:.1f} {ty:.1f} Q{cx_:.1f} {cy_:.1f} {ex:.1f} {ey:.1f}"
            b.append(f'<path d="{fr}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" filter="url(#rough2)"/>')
            b.append(f'<path d="{fr}" fill="none" stroke="#4d6b3a" stroke-width="5" stroke-linecap="round" filter="url(#rough2)"/>')
    b.append(shape(poly([(0, 330), (W, 330), (W, H), (0, H)]), "#1b1315", 4, "hatch2", 0.4))
    for dx in range(0, W, 90):
        b.append(line(dx, 388, dx + 46, 388, "#e2d9c6", 4, 'opacity=".55" filter="url(#rough2)"'))
    # street lamp
    b.append('<circle cx="760" cy="196" r="80" fill="url(#lamp)"/>')
    b.append(f'<path d="M766 332 L766 214 Q766 192 744 192" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round" filter="url(#rough2)"/>')
    b.append('<path d="M766 332 L766 214 Q766 192 744 192" fill="none" stroke="#6a5f55" stroke-width="6" stroke-linecap="round" filter="url(#rough2)"/>')
    b.append(shape(poly([(728, 192), (762, 192), (756, 202), (734, 202)]), "#e0cf45", 3, None))
    # crates with falling detail (LOD steps)
    for cx, detail, label in ((630, 2, "LOD0"), (810, 1, "LOD1"), (990, 0, "LOD2")):
        b.append(cube(cx, 332, 60, detail))
        b.append(f'<text x="{cx}" y="402" text-anchor="middle" font-family="Courier Prime, monospace" font-weight="700" font-size="26" '
                 f'fill="#d8cfbd" stroke="{INK}" stroke-width="5" paint-order="stroke">{label}</text>')
    return wrap(23, "".join(b))


# -------------------------------------------------------------------------------------------------- UE5 Bridge
def bone(a, b_, w=9, fill="#cfc5ac", alpha=1.0):
    ax, ay = a
    bx, by = b_
    dx, dy = bx - ax, by - ay
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln * w, dx / ln * w
    mx, my = ax + dx * 0.2, ay + dy * 0.2
    pts = [(ax, ay), (mx + nx, my + ny), (bx, by), (mx - nx, my - ny)]
    return (f'<g opacity="{alpha}">' + shape(poly(pts), fill, 3, "hatch", 0.35, "rough2")
            + f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="5" fill="#efe8d6" stroke="{INK}" stroke-width="2.4"/></g>')


def figure(x, hip_y, pose, alpha):
    """A walking skeleton as bones; angles in degrees from straight down, positive = forward."""
    lt, ls, rt, rs, la, ra, lift = pose
    hips = (x, hip_y - lift)

    def limb(origin, thigh, shin, l1=64, l2=62):
        k = (origin[0] + l1 * math.sin(math.radians(thigh)), origin[1] + l1 * math.cos(math.radians(thigh)))
        f = (k[0] + l2 * math.sin(math.radians(shin)), k[1] + l2 * math.cos(math.radians(shin)))
        return k, f

    out = []
    spine = [hips, (x + 4, hips[1] - 36), (x + 8, hips[1] - 74), (x + 10, hips[1] - 104)]
    for i in range(3):
        out.append(bone(spine[i], spine[i + 1], 8, alpha=alpha))
    out.append(bone(spine[3], (x + 14, hips[1] - 138), 11, "#d9d0b8", alpha))
    for thigh, shin in ((lt, ls), (rt, rs)):
        k, f = limb(hips, thigh, shin)
        out.append(bone(hips, k, 9, alpha=alpha))
        out.append(bone(k, f, 8, alpha=alpha))
        out.append(bone(f, (f[0] + 26, f[1] + 4), 6, "#bfb59c", alpha))
    shoulder = (x + 8, hips[1] - 92)
    for ang in (la, ra):
        e = (shoulder[0] + 46 * math.sin(math.radians(ang)), shoulder[1] + 46 * math.cos(math.radians(ang)))
        hand = (e[0] + 40 * math.sin(math.radians(ang + 14)), e[1] + 40 * math.cos(math.radians(ang + 14)))
        out.append(bone(shoulder, e, 7, alpha=alpha))
        out.append(bone(e, hand, 6, "#bfb59c", alpha))
    return "".join(out), hips


def scene_ue5():
    b = [f'<rect width="{W}" height="{H}" fill="#161012"/>', f'<rect y="238" width="{W}" height="{H - 238}" fill="#201718"/>']
    for i in range(-16, 17):  # viewport floor grid
        b.append(line(800 + i * 36, 238, 800 + i * 150, H, "#e2d9c6", 1.5, 'opacity=".12"'))
    for k in range(1, 9):
        y = 238 + (k ** 1.6) * 3.4
        b.append(line(0, y, W, y, "#e2d9c6", 1.5, 'opacity=".12"'))
    ground = 352
    poses = [  # thigh L, shin L, thigh R, shin R, arm L, arm R, hips lift
        (30, 28, -22, -38, -26, 26, 0), (12, 6, -10, -42, -12, 12, -9),
        (0, 0, 28, -4, 6, -6, 2), (-18, -32, 30, 26, 24, -24, 8)]
    alphas = (0.34, 0.5, 0.7, 1.0)
    hips_pts = []
    xs = (660, 810, 960, 1110)
    figs = []
    for x, pose, al in zip(xs, poses, alphas):
        svg, hips = figure(x, 224, pose, al)
        figs.append(svg)
        hips_pts.append(hips)
    b.append(f'<path d="{smooth(hips_pts)}" fill="none" stroke="#e0cf45" stroke-width="3.5" stroke-dasharray="3 9" stroke-linecap="round"/>')
    b.append(line(xs[0], ground + 6, xs[-1], ground + 6, "#c0392f", 4, 'stroke-dasharray="12 8"'))
    b.append(f'<path d="M{xs[-1] + 4} {ground + 6} l-16 -9 l0 18 z" fill="#c0392f"/>')
    b.extend(figs)
    rx = xs[-1]  # root marker under the last pose
    b.append(f'<rect x="{rx - 15}" y="{ground - 9}" width="30" height="30" fill="none" stroke="#c0392f" stroke-width="4" filter="url(#rough2)"/>')
    b.append(line(rx, ground + 6, rx + 42, ground + 6, "#c0392f", 4))
    b.append(line(rx, ground + 6, rx, ground - 40, "#7fa65a", 4))
    # timeline
    b.append(f'<rect x="440" y="382" width="680" height="30" fill="#120c0d" stroke="{INK}" stroke-width="4" filter="url(#rough2)"/>')
    for tx in range(452, 1110, 22):
        b.append(line(tx, 382, tx, 392 if (tx - 452) % 110 else 398, "#8c8374", 2))
    for tx in (474, 584, 760, 1002):
        b.append(f'<path d="M{tx} 389 l8 8 l-8 8 l-8 -8 z" fill="#e0cf45" stroke="{INK}" stroke-width="2.4"/>')
    b.append(line(1002, 378, 1002, 414, "#c0392f", 4))
    return wrap(31, "".join(b))


# ----------------------------------------------------------------------------------------------- Scatter Brush
def tuft(x, y, h, rnd):
    out = []
    for dx, dy in ((-0.45, -0.72), (0.0, -1.0), (0.45, -0.7)):
        end = (dx * h * 0.55 + rnd.uniform(-1.5, 1.5), dy * h)
        for color, width in ((INK, 3), ("#8fb55a", 1.4)):
            out.append(f'<path d="M{x:.1f} {y:.1f} q{end[0] / 2:.1f} {end[1] / 2:.1f} {end[0]:.1f} {end[1]:.1f}" stroke="{color}" '
                       f'stroke-width="{width}" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def pine(x, y, s):
    out = [f'<path d="M{x - 4 * s:.1f} {y:.1f} L{x - 4 * s:.1f} {y - 16 * s:.1f} L{x + 4 * s:.1f} {y - 16 * s:.1f} L{x + 4 * s:.1f} {y:.1f} Z" '
           f'fill="#5a4333" stroke="{INK}" stroke-width="3"/>']
    for k, (w, h) in enumerate(((30, 36), (24, 32), (17, 28))):
        y0 = y - 12 * s - k * 22 * s
        out.append(shape(poly([(x - w * s, y0), (x, y0 - h * s), (x + w * s, y0)]), "#2f4a2e", 3.2, "hatch", 0.5, "rough2"))
    return "".join(out)


def rock(cx, cy, s):
    pts = [(cx - 30 * s, cy + 18 * s), (cx - 22 * s, cy - 10 * s), (cx - 2 * s, cy - 24 * s), (cx + 24 * s, cy - 12 * s),
           (cx + 32 * s, cy + 18 * s)]
    return shape(poly(pts), "#8a847b", 4, "hatch", 0.6) + line(cx - 2 * s, cy - 24 * s, cx + 2 * s, cy + 6 * s, INK, 2.5)


def scene_scatter():
    rnd = random.Random(41)
    b = ['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#171011"/>'
         '<stop offset=".5" stop-color="#3b2c2a"/><stop offset=".72" stop-color="#8f7a52"/></linearGradient></defs>']
    b.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    far = [(0, 232), (120, 196), (240, 220), (380, 172), (520, 212), (660, 160), (800, 206), (940, 178), (1080, 212),
           (1200, 188), (1200, 300), (0, 300)]
    b.append('<circle cx="870" cy="150" r="96" fill="#e8c27a" opacity=".22" filter="url(#glow)"/>')
    b.append(f'<circle cx="870" cy="150" r="38" fill="#ecd29a" stroke="{INK}" stroke-width="4" filter="url(#rough)"/>')
    b.append(shape(poly(far), "#4b3a39", 4, "hatch2", 0.7))
    ridge = [(0, 284), (250, 258), (540, 252), (820, 262), (1060, 250), (1200, 258)]
    hill = smooth(ridge) + " L1200 420 L0 420 Z"
    b.append(f'<clipPath id="hill"><path d="{hill}"/></clipPath>')
    b.append(shape(hill, "#5d4a35", 4, "hatch", 0.35))
    b.append('<g clip-path="url(#hill)">')
    # weight paint: the same blue-green-yellow-red heat map Blender shows
    for rx, ry, color in ((340, 66, "#2a3fb8"), (262, 52, "#2a9fc0"), (190, 40, "#4cbf5a"), (118, 25, "#d8d040"), (54, 11, "#d96a2a")):
        b.append(f'<ellipse cx="905" cy="316" rx="{rx}" ry="{ry}" fill="{color}" opacity=".82" filter="url(#soft)"/>')
    for i in range(-14, 15):
        b.append(line(600 + i * 40, 256, 600 + i * 150, 424, "#e2d9c6", 1.4, 'opacity=".14"'))
    for k in range(1, 9):
        y = 256 + (k ** 1.55) * 4.4
        b.append(line(0, y, W, y, "#e2d9c6", 1.4, 'opacity=".14"'))
    b.append("</g>")
    b.append(shape(smooth(ridge), "none", 4.5, None))
    for x, y, s in ((655, 288, 1.0), (708, 302, 0.82), (1160, 282, 0.9)):
        b.append(pine(x, y, s))
    for cx, cy, s in ((1112, 322, 0.9), (1160, 350, 1.15), (735, 344, 0.75)):
        b.append(rock(cx, cy, s))
    tufts = []
    while len(tufts) < 300:  # denser where the weight is high
        x, y = rnd.gauss(905, 150), 318 + rnd.gauss(0, 26)
        if 266 < y < 414 and 560 < x < 1190:
            tufts.append((x, y))
    for x, y in sorted(tufts, key=lambda p: p[1]):
        closeness = max(0.0, 1 - ((x - 905) / 330) ** 2 - ((y - 316) / 66) ** 2)
        b.append(tuft(x, y, 11 + 14 * closeness, rnd))
    # the brush: a ring on the ground, a cursor, and a few fresh stamps inside it
    b.append(f'<ellipse cx="1015" cy="306" rx="100" ry="27" fill="none" stroke="{INK}" stroke-width="9" filter="url(#rough2)"/>')
    b.append('<ellipse cx="1015" cy="306" rx="100" ry="27" fill="none" stroke="#8be05a" stroke-width="4.5" filter="url(#rough2)"/>')
    for dx, dy, s in ((-44, 6, 0.42), (6, 12, 0.5), (46, -2, 0.38)):
        b.append(rock(1015 + dx, 304 + dy, s))
    b.append(shape(poly([(1040, 268), (1040, 302), (1049, 294), (1056, 308), (1063, 305), (1056, 292), (1068, 292)]), "#efe8d6", 3,
                   None, 0, "rough2"))
    return wrap(41, "".join(b))


SCENES = {"terrain-blend": scene_terrain, "retopo-kit": scene_retopo, "fivem-toolkit": scene_fivem, "ue5-bridge": scene_ue5,
          "scatter-brush": scene_scatter}
