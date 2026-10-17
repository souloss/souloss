"""Render the locally generated profile cards into dist/."""
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import cards
import github_api
import theme


ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "profile.toml"


def main():
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    settings = tomllib.loads(CONFIG.read_text())
    profile = settings["profile"]
    recent = settings["cards"]["recent"]
    languages = settings["cards"]["languages"]
    theme.configure(settings.get("theme", {}))
    output.mkdir(parents=True, exist_ok=True)

    repos = github_api.repositories(profile["github"])
    excluded = {name.casefold() for name in recent.get("exclude_repositories", [])}
    repos = [repo for repo in repos
             if repo.get("pushed_at")
             and not repo.get("private", False)
             and repo.get("name", "").casefold() not in excluded
             and not (recent.get("exclude_forks", True) and repo.get("fork"))
             and not (recent.get("exclude_archived", True) and repo.get("archived"))]
    repos.sort(key=lambda repo: repo.get("pushed_at") or "", reverse=True)

    zone = ZoneInfo(profile.get("timezone", "UTC"))
    refreshed = datetime.now(timezone.utc).astimezone(zone).strftime("%d %b %H:%M %Z").upper()
    svg = cards.recent_repositories(repos, max(1, int(recent.get("limit", 5))), refreshed)
    (output / "recent.svg").write_text(svg)
    print(f"wrote recent.svg ({len(svg) // 1024} KB)")

    try:
        totals = github_api.language_totals(repos)
        svg = cards.language_distribution(totals, len(repos), max(1, int(languages.get("top", 6))), refreshed)
        (output / "languages.svg").write_text(svg)
        print(f"wrote languages.svg ({len(svg) // 1024} KB)")
    except Exception as error:
        print(f"language card unavailable; keeping previous render: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
