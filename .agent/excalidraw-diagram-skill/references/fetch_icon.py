"""Resolve a tool/provider name to a cached SVG icon, fetching it into the repo cache on a miss.

This is NOT a diagram generator — it only handles icon sourcing. The diagram JSON itself
is still hand-crafted per SKILL.md. Use this script to get the base64 dataURL + a ready-to-paste
"image" element + "files" entry for a named tool/provider, then splice them into the .excalidraw
JSON you're authoring by hand.

Usage:
    uv run python fetch_icon.py <name> [--x X] [--y Y] [--size SIZE]

Always checks references/icons/ (committed to the repo) before fetching anything from the network.
Prints nothing and exits 1 if the name isn't in icon_map.json (no icon exists for that term yet —
add it to icon_map.json first if Lobe Icons has it; see SKILL.md).
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.request
from pathlib import Path

REF_DIR = Path(__file__).resolve().parent
ICON_MAP_PATH = REF_DIR / "icon_map.json"
ICON_CACHE_DIR = REF_DIR / "icons"
RAW_BASE = "https://raw.githubusercontent.com/lobehub/lobe-icons/master/packages/static-svg/icons"


def resolve_slug(name: str) -> str | None:
    icon_map = json.loads(ICON_MAP_PATH.read_text())
    return icon_map.get(name.strip().lower())


def cached_or_fetch(slug: str) -> Path:
    """Repo cache first; only hits the network on a genuine miss."""
    dest = ICON_CACHE_DIR / f"{slug}.svg"
    if dest.exists():
        return dest
    ICON_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    url = f"{RAW_BASE}/{slug}.svg"
    with urllib.request.urlopen(url, timeout=10) as resp:
        dest.write_bytes(resp.read())
    return dest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--x", type=float, default=0)
    parser.add_argument("--y", type=float, default=0)
    parser.add_argument("--size", type=float, default=48)
    parser.add_argument("--id", default=None, help="element id to use (default: '<name>_icon')")
    args = parser.parse_args()

    slug = resolve_slug(args.name)
    if not slug:
        print(
            f"No icon mapped for {args.name!r}. Check icon_map.json, or see if Lobe Icons "
            "has it (SKILL.md has the lookup command) before giving up.",
            file=sys.stderr,
        )
        return 1

    svg_path = cached_or_fetch(slug)
    data = svg_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    file_id = f"{slug}_file"
    element_id = args.id or f"{args.name.strip().lower().replace(' ', '_')}_icon"

    files_entry = {
        file_id: {
            "mimeType": "image/svg+xml",
            "id": file_id,
            "dataURL": f"data:image/svg+xml;base64,{b64}",
            "created": 1700000000000,
            "lastRetrieved": 1700000000000,
        }
    }
    image_element = {
        "type": "image",
        "id": element_id,
        "x": args.x,
        "y": args.y,
        "width": args.size,
        "height": args.size,
        "angle": 0,
        "strokeColor": "transparent",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "seed": 90001,
        "version": 1,
        "versionNonce": 90002,
        "isDeleted": False,
        "groupIds": [],
        "boundElements": None,
        "link": None,
        "locked": False,
        "fileId": file_id,
        "status": "saved",
        "scale": [1, 1],
    }

    print(f"# icon cached at: {svg_path.relative_to(REF_DIR.parent.parent.parent)}")
    print("# Add this entry to the top-level \"files\" object:")
    print(json.dumps(files_entry, indent=2))
    print("\n# Add this element to \"elements\":")
    print(json.dumps(image_element, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
