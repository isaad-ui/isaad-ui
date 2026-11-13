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
def whorl(cx, cy, rx, ry, rot, ink):
    """A thumbprint: a few broken concentric ridges pressed into the clay."""
    rings = []
    for k, scale in enumerate((1.0, 0.76, 0.54, 0.34)):
        dash = ("15 4 9 4", "11 3 7 3", "8 3 5 3", "5 3")[k]
        rings.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * scale:.1f}" ry="{ry * scale:.1f}" fill="none" '
                     f'stroke="{ink}" stroke-width="1.3" stroke-dasharray="{dash}" transform="rotate({rot} {cx} {cy})"/>')
    return "".join(rings)


CLAY_FONT = "font-family=\"'Arial Rounded MT Bold','Nunito','Trebuchet MS','Segoe UI Black',Arial,sans-serif\" font-weight=\"900\""


def header(theme, c):
    """Claymation-style header: plasticine lettering that boils frame to frame, thumbprints, a small clay character."""
    dark = theme == "dark"
    name_clay = "#DCE5DF" if dark else "#2B3733"
    body = "#75B9A8" if dark else "#3F7F6E"
    deep = "#4E8C7C" if dark else "#2C5C4E"
    ink = "rgba(0,0,0,0.16)"
    l1, l2 = "Issaka Sa-ad", "Timbilla"
    t1 = f'x="6" y="84" {CLAY_FONT} font-size="58" textLength="404" lengthAdjust="spacingAndGlyphs"'
    t2 = f'x="6" y="150" {CLAY_FONT} font-size="58" textLength="262" lengthAdjust="spacingAndGlyphs"'
    prints_text = (whorl(60, 62, 17, 12, -20, ink) + whorl(228, 56, 15, 11, 25, ink) + whorl(352, 64, 16, 12, 10, ink)
                   + whorl(70, 128, 15, 11, 15, ink) + whorl(176, 134, 15, 11, -25, ink) + whorl(250, 126, 13, 10, 20, ink))
    body_path = "M65 10C100 10 118 40 118 80C118 125 95 150 65 150C35 150 12 125 12 80C12 40 30 10 65 10Z"
    prints_body = whorl(30, 112, 12, 9, 30, ink) + whorl(98, 124, 12, 9, -30, ink) + whorl(66, 24, 11, 8, 0, ink)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 214" width="700" height="214" role="img" aria-label="Issaka Sa-ad Timbilla. Computer Science student building practical software. Claymation-style lettering with a small clay character.">
<defs>
<filter id="clay" x="-4%" y="-6%" width="108%" height="112%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="1" result="warp"><animate attributeName="seed" values="1;2;3;4;5;6;7;8" dur="1.1s" calcMode="discrete" repeatCount="indefinite"/></feTurbulence>
<feDisplacementMap in="SourceGraphic" in2="warp" scale="4" xChannelSelector="R" yChannelSelector="G" result="shape"/>
<feGaussianBlur in="shape" stdDeviation="1.5" result="soft"/>
<feSpecularLighting in="soft" surfaceScale="3" specularConstant=".55" specularExponent="18" lighting-color="#ffffff" result="spec"><feDistantLight azimuth="225" elevation="55"/></feSpecularLighting>
<feComposite in="spec" in2="shape" operator="in" result="specIn"/>
<feComposite in="shape" in2="specIn" operator="arithmetic" k1="0" k2="1" k3=".45" k4="0"/>
</filter>
<clipPath id="lettersA"><text {t1}>{l1}</text></clipPath>
<clipPath id="lettersB"><text {t2}>{l2}</text></clipPath>
<clipPath id="bodyClip"><path d="{body_path}"/></clipPath>
</defs>
<style>
.step{{animation:step 1.6s steps(1,end) infinite}}
@keyframes step{{0%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
.blink{{transform-box:fill-box;transform-origin:center;animation:blink 4.6s steps(1,end) infinite}}
@keyframes blink{{0%,93%{{transform:scaleY(1)}}94%,97%{{transform:scaleY(.12)}}98%,100%{{transform:scaleY(1)}}}}
</style>
<g filter="url(#clay)">
<text {t1} fill="{name_clay}">{l1}</text>
<text {t2} fill="{name_clay}">{l2}</text>
<g clip-path="url(#lettersA)">{prints_text}</g>
<g clip-path="url(#lettersB)">{prints_text}</g>
</g>
<g transform="translate(548,34)" filter="url(#clay)"><g class="step">
<ellipse cx="14" cy="104" rx="9" ry="16" fill="{body}" transform="rotate(14 14 104)"/>
<ellipse cx="116" cy="104" rx="9" ry="16" fill="{body}" transform="rotate(-14 116 104)"/>
<ellipse cx="42" cy="152" rx="17" ry="8" fill="{deep}"/><ellipse cx="88" cy="152" rx="17" ry="8" fill="{deep}"/>
<path d="{body_path}" fill="{body}"/>
<g clip-path="url(#bodyClip)">{prints_body}</g>
<path d="M33 41Q47 32 59 38M71 38Q83 32 97 41" fill="none" stroke="{deep}" stroke-width="5" stroke-linecap="round"/>
<circle cx="47" cy="62" r="14" fill="#F2F2EA"/><circle cx="83" cy="62" r="14" fill="#F2F2EA"/>
<g class="blink"><circle cx="49" cy="64" r="5.5" fill="#1B1F1D"/></g><g class="blink"><circle cx="81" cy="64" r="5.5" fill="#1B1F1D"/></g>
<path d="M38 98Q65 126 92 98Q65 109 38 98Z" fill="#2A1F1C"/>
<path d="M45 99Q65 108 85 99L83 105Q65 113 47 105Z" fill="#F2F2EA"/>
</g></g>
<text x="6" y="198" {SANS} font-size="19" fill="{c['muted']}">Computer Science student building practical software.</text>
</svg>
'''


def header_minimal(theme, c):
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
