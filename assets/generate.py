#!/usr/bin/env python3
"""Generate the profile README graphics as static SVGs."""
import os, random, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    # accents are theme aware so text keeps its contrast on both backgrounds
    "dark": dict(bg="#0D1117", panel="#161B22", border="#30363D",
                 text="#E6EDF3", muted="#8B949E", grid="#1C2128",
                 v1="#6C63FF", v2="#8B84FF", g1="#E8B04B", g2="#D1952F"),
    "light": dict(bg="#FFFFFF", panel="#F6F8FA", border="#D0D7DE",
                  text="#1F2328", muted="#656D76", grid="#EBEDF0",
                  v1="#5A51E8", v2="#6F66F0", g1="#9A6A10", g2="#7E560B"),
}
# block fills in the banner grid stay bright on both themes
VIOLET, GOLD = "#6C63FF", "#E8B04B"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def banner(t):
    W, H = 1200, 260
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Uditha Landekumbura, Lecturer, Software Engineer, Builder">']
    p.append(f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>')

    # contribution-style grid, right hand side
    rng = random.Random(1994)
    sq, gap, rows, cols = 13, 5, 7, 14
    gw = cols * (sq + gap) - gap
    gx, gy = W - 64 - gw, (H - (rows * (sq + gap) - gap)) / 2
    for c in range(cols):
        for r in range(rows):
            x, y = gx + c * (sq + gap), gy + r * (sq + gap)
            roll = rng.random()
            if roll < 0.42:
                fill, op = t["grid"], 1
            elif roll < 0.62:
                fill, op = VIOLET, 0.22
            elif roll < 0.80:
                fill, op = VIOLET, 0.45
            elif roll < 0.92:
                fill, op = VIOLET, 0.78
            else:
                fill, op = GOLD, 0.85
            p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{sq}" height="{sq}" rx="3" '
                     f'fill="{fill}" opacity="{op}"/>')

    # left hand type block
    p.append(f'<rect x="56" y="58" width="52" height="4" rx="2" fill="{t["v1"]}"/>')
    p.append(f'<text x="56" y="116" font-family="{FONT}" font-size="44" font-weight="700" '
             f'fill="{t["text"]}">Uditha Landekumbura</text>')
    p.append(f'<text x="56" y="152" font-family="{FONT}" font-size="19" font-weight="600" '
             f'fill="{t["v1"]}">Lecturer · Software Engineer · Builder</text>')
    p.append(f'<text x="56" y="184" font-family="{MONO}" font-size="14" '
             f'fill="{t["muted"]}">Colombo, Sri Lanka</text>')
    p.append(f'<text x="56" y="212" font-family="{MONO}" font-size="13.5" '
             f'fill="{t["muted"]}" opacity="0.85">teaching by day · shipping by night</text>')
    p.append("</svg>")
    return "\n".join(p)


STEPS = [
    ("1", "Teach the module", ["what the syllabus needs", "MVC · REST · IoT"], "v1"),
    ("2", "Publish the build", ["students read the code", "sahana-health"], "v2"),
    ("3", "Ship it for real", ["it runs on campus", "msi-signage"], "g1"),
    ("4", "Back to the class", ["workshops and coaching", "ICPC · STACK"], "g2"),
]


def loop(t):
    W, H = 1200, 320
    bw, bh, gap = 250, 112, 38
    total = len(STEPS) * bw + (len(STEPS) - 1) * gap
    x0, by = (W - total) / 2, 52
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="How the work loops: teach a module, write the reference build, '
         f'ship the real thing, take it back to class">']
    p.append(f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>')
    p.append(f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
             f'markerHeight="6" orient="auto-start-reverse">'
             f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{t["muted"]}"/></marker></defs>')

    centers = []
    for i, (num, title, subs, akey) in enumerate(STEPS):
        accent = t[akey]
        bx = x0 + i * (bw + gap)
        centers.append(bx + bw / 2)
        p.append(f'<rect x="{bx:.0f}" y="{by}" width="{bw}" height="{bh}" rx="10" '
                 f'fill="{t["panel"]}" stroke="{t["border"]}"/>')
        p.append(f'<rect x="{bx:.0f}" y="{by}" width="4" height="{bh}" rx="2" fill="{accent}"/>')
        p.append(f'<circle cx="{bx + 30:.0f}" cy="{by + 28}" r="12" fill="{accent}" opacity="0.18"/>')
        p.append(f'<text x="{bx + 30:.0f}" y="{by + 33}" font-family="{MONO}" font-size="13" '
                 f'font-weight="700" fill="{accent}" text-anchor="middle">{num}</text>')
        p.append(f'<text x="{bx + 52:.0f}" y="{by + 33}" font-family="{FONT}" font-size="15.5" '
                 f'font-weight="700" fill="{t["text"]}">{esc(title)}</text>')
        ty = by + 62
        for j, s in enumerate(subs):
            fam = MONO if j == len(subs) - 1 and len(subs) > 1 else FONT
            col = accent if j == len(subs) - 1 and len(subs) > 1 else t["muted"]
            p.append(f'<text x="{bx + 20:.0f}" y="{ty}" font-family="{fam}" font-size="12.5" '
                     f'fill="{col}">{esc(s)}</text>')
            ty += 20
        if i < len(STEPS) - 1:
            sx, ex = bx + bw + 10, bx + bw + gap - 10
            p.append(f'<line x1="{sx:.0f}" y1="{by + bh/2:.0f}" x2="{ex:.0f}" y2="{by + bh/2:.0f}" '
                     f'stroke="{t["muted"]}" stroke-width="1.6" marker-end="url(#ah)"/>')

    # return arc
    ry = by + bh + 68
    p.append(f'<path d="M {centers[-1]:.0f} {by + bh + 8} V {ry} H {centers[0]:.0f} V {by + bh + 12}" '
             f'fill="none" stroke="{t["muted"]}" stroke-width="1.6" stroke-dasharray="5 5" '
             f'marker-end="url(#ah)" opacity="0.8"/>')
    p.append(f'<text x="{W/2:.0f}" y="{ry - 12}" font-family="{FONT}" font-size="13.5" '
             f'fill="{t["muted"]}" text-anchor="middle">every module turns into a real system, '
             f'and every system turns back into a lecture</text>')
    p.append("</svg>")
    return "\n".join(p)


for name, fn in (("banner", banner), ("loop", loop)):
    for theme, t in THEMES.items():
        path = os.path.join(OUT, f"{name}-{theme}.svg")
        with open(path, "w") as f:
            f.write(fn(t))
        print("wrote", path, os.path.getsize(path), "bytes")
