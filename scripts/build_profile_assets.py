"""Builds the small SVG assets used by README.md.

Run from the repository root:  python scripts/build_profile_assets.py

Everything is transparent so it sits directly on GitHub's own background.
Each asset is written twice: <name>-dark.svg and <name>-light.svg, and the
README picks the right one with <picture>.
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "profile")
ICONS = os.path.join(ROOT, "assets", "icons")

# Palette. Dark follows the brief; light is the same hues, darkened for contrast.
THEMES = {
    "dark": dict(text="#DCE5DF", accent="#75B9A8", muted="#A9B5B0", surface="#20282B"),
    "light": dict(text="#1F2A27", accent="#3F7F6E", muted="#5F6B66", surface="#E3E9E6"),
}
SERIF = "font-family=\"Georgia,'Iowan Old Style','Times New Roman',serif\""
SANS = "font-family=\"'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif\""
MONO = "font-family=\"Consolas,'SFMono-Regular','Courier New',monospace\""


def esc(t):
    return html.escape(t, quote=False)


def write(name, theme, text):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f:
        f.write(text)


# ---------------------------------------------------------------- header
def header(theme, c):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 130" width="700" height="130" role="img" aria-label="Issaka Sa-ad Timbilla. Computer Science student building practical software.">
<style>
.fade{{opacity:0;animation:fade .9s ease-out forwards}}
.line{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:line .9s ease-out .5s forwards}}
@keyframes fade{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes line{{to{{transform:scaleX(1)}}}}
</style>
<text class="fade" x="2" y="58" {SERIF} font-size="46" fill="{c['text']}">Issaka Sa-ad Timbilla</text>
<rect class="line" x="2" y="76" width="64" height="2" fill="{c['accent']}"/>
<text class="fade" style="animation-delay:.7s" x="2" y="110" {SANS} font-size="19" fill="{c['muted']}">Computer Science student building practical software.</text>
</svg>
'''


# ---------------------------------------------------------------- typing
PHRASES = [
    "Python development",
    "Practical software projects",
    "Backend engineering",
    "Growing towards AI engineering",
]
ADV = 0.6          # monospace advance, in em
FS = 20
X0 = 30            # where typed text starts


def fmt(v):
    return f"{v:.4f}".rstrip("0").rstrip(".")


def typing(theme, c):
    t_char, t_del, hold, gap = 0.085, 0.04, 1.7, 0.35
    spans = []
    t = 0.0
    for p in PHRASES:
        n = len(p)
        start = t
        typed = start + n * t_char
        held = typed + hold
        deleted = held + n * t_del
        spans.append((start, typed, held, deleted, n))
        t = deleted + gap
    total = t
    parts = []
    for i, (p, (start, typed, held, deleted, n)) in enumerate(zip(PHRASES, spans)):
        L = round(n * FS * ADV, 1)
        step = L / n
        events = [(0.0, 0.0)]
        for k in range(1, n + 1):
            events.append((start + k * t_char, k * step))
        for k in range(1, n + 1):
            events.append((held + k * t_del, (n - k) * step))
        events = [(max(0.0, a), b) for a, b in events]
        events.sort(key=lambda e: e[0])
        # keep keyTimes strictly increasing
        cleaned = []
        for a, b in events:
            if cleaned and a <= cleaned[-1][0]:
                a = cleaned[-1][0] + 0.001
            cleaned.append((a, b))
        kt = ";".join(fmt(a / total) for a, _ in cleaned)
        wv = ";".join(fmt(b) for _, b in cleaned)
        cx = ";".join(fmt(X0 + b) for _, b in cleaned)
        vis_kt = f"0;{fmt(start / total)};{fmt((deleted + 0.05) / total)}"
        first = "1" if i == 0 else "0"
        init_w = L if i == 0 else 0
        parts.append(f'''<g opacity="{first}">
<animate attributeName="opacity" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" keyTimes="{vis_kt}" values="0;1;0"/>
<clipPath id="c{i}"><rect x="{X0}" y="0" width="{init_w}" height="44"><animate attributeName="width" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" keyTimes="{kt}" values="{wv}"/></rect></clipPath>
<text x="{X0}" y="29" {MONO} font-size="{FS}" fill="{c['text']}" textLength="{L}" lengthAdjust="spacingAndGlyphs" clip-path="url(#c{i})" xml:space="preserve">{esc(p)}</text>
<rect x="{X0 + init_w}" y="9" width="2" height="24" fill="{c['accent']}"><animate attributeName="x" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" keyTimes="{kt}" values="{cx}"/><animate attributeName="opacity" calcMode="discrete" dur="1s" repeatCount="indefinite" values="1;0" keyTimes="0;.5"/></rect>
</g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 44" width="700" height="44" role="img" aria-label="{esc('. '.join(PHRASES))}.">
<text x="2" y="29" {MONO} font-size="{FS}" fill="{c['accent']}">&gt;</text>
{chr(10).join(parts)}
</svg>
'''


# ---------------------------------------------------------------- stack
STACK = [
    [("python", "Python"), ("openjdk", "Java"), ("javascript", "JavaScript"), ("html5", "HTML"), ("css3", "CSS")],
    [("react", "React"), ("mysql", "MySQL"), ("git", "Git"), ("github", "GitHub")],
]


def icon_path(name):
    with open(os.path.join(ICONS, f"{name}.svg"), encoding="utf-8") as f:
        svg = f.read()
    return "".join(re.findall(r'<path[^>]*\sd="([^"]+)"', svg))


def stack(theme, c):
    cell, size = 112, 34
    out = []
    labels = []
    for r, row in enumerate(STACK):
        y = r * 86
        for i, (key, label) in enumerate(row):
            x = i * cell + 2
            out.append(f'<g transform="translate({x},{y}) scale({size / 24})" fill="{c["accent"]}"><path d="{icon_path(key)}"/></g>')
            out.append(f'<text x="{x}" y="{y + size + 24}" {SANS} font-size="15" fill="{c["muted"]}">{label}</text>')
            labels.append(label)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 570 166" width="570" height="166" role="img" aria-label="{esc(', '.join(labels))}">
{chr(10).join(out)}
</svg>
'''


# ---------------------------------------------------------------- connect icons
def connect_icon(key, theme, c):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="{c['accent']}"><path d="{icon_path(key)}"/></svg>
'''


def main():
    for theme, c in THEMES.items():
        write("header", theme, header(theme, c))
        write("typing", theme, typing(theme, c))
        write("stack", theme, stack(theme, c))
        write("icon-linkedin", theme, connect_icon("linkedin", theme, c))
        write("icon-github", theme, connect_icon("github", theme, c))
    print("assets written to", OUT)


if __name__ == "__main__":
    main()
