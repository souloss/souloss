"""Shared SVG colors and safe document primitives."""
import html
import re


WIDTH = 880
COLORS = {
    "background": "#090b0e",
    "panel": "#0e1217",
    "line": "#1d232c",
    "text": "#ebe7df",
    "muted": "#7d8796",
    "accent": "#ffb224",
    "positive": "#35d07f",
    "negative": "#ff5d62",
    "cyan": "#62c7ff",
}
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def configure(overrides):
    for key, value in overrides.items():
        if key in COLORS and re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            COLORS[key] = value


def esc(value):
    return html.escape(str(value), quote=True)


def document(height, title, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-label="{esc(title)}">'
        f'<title>{esc(title)}</title><style>'
        f'.m{{font-family:{FONT};font-variant-numeric:tabular-nums}}'
        '@media (prefers-reduced-motion:reduce){.motion{display:none}}'
        f'</style><rect x=".5" y=".5" width="{WIDTH - 1}" height="{height - 1}" '
        f'rx="10" fill="{COLORS["background"]}" stroke="{COLORS["line"]}"/>'
        f'{body}</svg>\n'
    )


def label(x, y, value, *, size=10, color=None, anchor="start", weight=400, spacing=0):
    color = color or COLORS["muted"]
    return (
        f'<text x="{x}" y="{y}" class="m" font-size="{size}" font-weight="{weight}" '
        f'letter-spacing="{spacing}" fill="{color}" text-anchor="{anchor}">{esc(value)}</text>'
    )
