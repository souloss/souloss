"""Reject malformed SVG documents before publishing."""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


output = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
required = ("recent.svg", "snake.svg")
missing = [name for name in required if not (output / name).exists()]
if missing:
    raise SystemExit("missing SVGs: " + ", ".join(missing))

for path in sorted(output.glob("*.svg")):
    try:
        ET.parse(path)
    except ET.ParseError as error:
        raise SystemExit(f"malformed SVG {path.name}: {error}") from error
print(f"{len(list(output.glob('*.svg')))} SVGs are well-formed")
