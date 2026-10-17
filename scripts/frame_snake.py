"""Frame dist/snake-raw.svg as the contribution panel."""
import sys
import tomllib
from pathlib import Path

import cards
import theme


ROOT = Path(__file__).resolve().parent.parent
settings = tomllib.loads((ROOT / "config" / "profile.toml").read_text())
theme.configure(settings.get("theme", {}))
username = settings["profile"]["github"]
output = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
raw = output / "snake-raw.svg"
if raw.exists():
    (output / "snake.svg").write_text(cards.snake_panel(raw.read_text(), username))
    raw.unlink()
    print("wrote snake.svg")
else:
    print("no new snake render; keeping the previous snake.svg")
