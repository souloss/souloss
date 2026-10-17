"""SVG renderers for profile panel cards."""
from datetime import datetime, timezone

from theme import COLORS, WIDTH, document, label


def recent_repositories(repositories, limit, refreshed):
    rows = repositories[:limit]
    row_height = 58
    height = 96 + max(len(rows), 1) * row_height + 28
    body = [
        f'<rect x="18" y="17" width="5" height="12" rx="1" fill="{COLORS["accent"]}"/>',
        label(34, 27, "RECENT PUSHES", size=11, color=COLORS["accent"], weight=600, spacing=.7),
        label(WIDTH - 20, 27, "PUBLIC REPOSITORIES", size=10, anchor="end"),
        f'<line x1="18" y1="42.5" x2="{WIDTH - 18}" y2="42.5" stroke="{COLORS["line"]}"/>',
    ]

    if not rows:
        body.append(label(WIDTH / 2, 105, "NO PUBLIC REPOSITORIES TO DISPLAY", anchor="middle"))
    for index, repo in enumerate(rows):
        y = 76 + index * row_height
        name = _truncate(repo.get("name") or "untitled", 48)
        description = _truncate((repo.get("description") or "No description").strip(), 88)
        language = (repo.get("language") or "Other").upper()
        pushed = _age(repo.get("pushed_at"))
        body.extend([
            f'<rect x="18" y="{y - 18}" width="3" height="31" rx="1.5" fill="{COLORS["accent"]}" fill-opacity=".72"/>',
            label(32, y, name, size=14, color=COLORS["text"], weight=600),
            label(32, y + 19, description, size=10.5, color=COLORS["muted"]),
            label(WIDTH - 20, y, f"{language}  ·  {pushed}", size=10, color=COLORS["cyan"], anchor="end"),
        ])
        if index < len(rows) - 1:
            body.append(f'<line x1="32" y1="{y + 31}.5" x2="{WIDTH - 20}" y2="{y + 31}.5" stroke="{COLORS["line"]}"/>')

    body.append(label(20, height - 15, f"SOULOSS  /  UPDATED {refreshed}", size=9, spacing=.4))
    return document(height, "Recently pushed public repositories", "".join(body))


def snake_panel(raw_svg, username):
    """Place the generated contribution snake inside the shared panel frame."""
    start = raw_svg.find(">", raw_svg.find("<svg"))
    end = raw_svg.rfind("</svg>")
    if start < 0 or end < 0:
        raise ValueError("snk output is not an SVG document")
    header = raw_svg[raw_svg.find("<svg"):start + 1]
    x0, y0, view_width, view_height = _viewbox(header)
    inner = raw_svg[start + 1:end]
    crop_y = y0 + 12
    crop_height = min(view_height - 12, 156)
    rendered_height = (WIDTH - 40) * crop_height / view_width
    height = round(74 + rendered_height + 24)
    body = (
        f'<rect x="18" y="17" width="5" height="12" rx="1" fill="{COLORS["accent"]}"/>'
        + label(34, 27, "CONTRIBUTION GRID", size=11, color=COLORS["accent"], weight=600, spacing=.7)
        + label(WIDTH - 20, 27, f"LAST 12 MONTHS  ·  {username.upper()}", size=10, anchor="end")
        + f'<line x1="18" y1="42.5" x2="{WIDTH - 18}" y2="42.5" stroke="{COLORS["line"]}"/>'
        + f'<svg x="20" y="54" width="{WIDTH - 40}" height="{rendered_height:.1f}" '
        f'viewBox="{x0:g} {crop_y:g} {view_width:g} {crop_height:g}">{inner}</svg>'
    )
    return document(height, f"{username} GitHub contribution grid", body)


def _viewbox(svg_header):
    import re

    match = re.search(r'viewBox="([^"]+)"', svg_header)
    if not match:
        raise ValueError("snk SVG is missing a viewBox")
    values = [float(part) for part in match.group(1).replace(",", " ").split()]
    if len(values) != 4 or values[2] <= 0 or values[3] <= 12:
        raise ValueError("snk SVG has an invalid viewBox")
    return values


def _truncate(value, limit):
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[:limit - 1].rstrip() + "…"


def _age(timestamp):
    if not timestamp:
        return "DATE UNKNOWN"
    pushed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    days = max((datetime.now(timezone.utc) - pushed.astimezone(timezone.utc)).days, 0)
    if days == 0:
        return "TODAY"
    if days < 30:
        return f"{days}D AGO"
    if days < 365:
        return f"{days // 30}MO AGO"
    return f"{days // 365}Y AGO"
