"""Builds a minimal language chart from the owner's own public, non-fork repositories.

Run from the repository root:  python scripts/update_languages.py [username]
A GITHUB_TOKEN environment variable is used if present (it raises the API rate limit).
Real data only: it sums the byte counts GitHub reports for each repository.
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_profile_assets import SANS, THEMES, esc, write  # noqa: E402

USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REPOSITORY_OWNER", "isaad-ui")
LIMIT = 6


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-readme"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    totals = {}
    repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    for repo in repos:
        if repo.get("fork"):
            continue
        for lang, size in get(repo["languages_url"]).items():
            totals[lang] = totals.get(lang, 0) + size
    return totals


def chart(theme, c, rows):
    W = 700
    x = 2
    bar = []
    legend = []
    gap = 3
    usable = W - 4 - gap * (len(rows) - 1)
    for i, (name, pct) in enumerate(rows):
        op = round(max(0.28, 1 - i * 0.14), 2)
        w = max(4, usable * pct / 100)
        bar.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="8" rx="4" fill="{c["accent"]}" fill-opacity="{op}"/>')
        x += w + gap
        col, row = i % 3, i // 3
        lx, ly = 2 + col * 232, 40 + row * 30
        legend.append(f'<circle cx="{lx + 5}" cy="{ly - 5}" r="4.5" fill="{c["accent"]}" fill-opacity="{op}"/>'
                      f'<text x="{lx + 18}" y="{ly}" {SANS} font-size="16" fill="{c["text"]}">{esc(name)} <tspan fill="{c["muted"]}">{pct:.1f}%</tspan></text>')
    h = 40 + ((len(rows) - 1) // 3) * 30 + 12
    label = ", ".join(f"{n} {p:.1f}%" for n, p in rows)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" '
            f'aria-label="Languages across my public repositories: {esc(label)}">\n' + "\n".join(bar + legend) + "\n</svg>\n")


def main():
    totals = collect()
    total = sum(totals.values())
    if not total:
        print("no language data found; leaving the chart unchanged")
        return
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    top = ranked[:LIMIT]
    rows = [(n, s / total * 100) for n, s in top]
    for theme, c in THEMES.items():
        write("languages", theme, chart(theme, c, rows))
    print("languages:", ", ".join(f"{n} {p:.1f}%" for n, p in rows))


if __name__ == "__main__":
    main()
