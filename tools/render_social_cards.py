#!/usr/bin/env python3
"""Render every social graphic in branding/social/ at every placement size.

    python3 tools/render_social_cards.py                  # all cards
    python3 tools/render_social_cards.py forums-card      # just one

One HTML master per card renders at four aspect ratios, each LAID OUT for
its own shape rather than scaled and cropped. Output goes to
assets/social/<card>-<format>.png.

Formats and why each exists:
  square   1080x1080  square feed posts, profile grid
  portrait 1080x1350  Facebook + Instagram feed — the default placement
  story    1080x1920  Stories / Reels; inset for the platform's UI chrome
  wide     1200x630   link previews, shared-link cards

Headless Chrome, because the masters use the campaign's real webfonts
(Lora + Source Sans Pro) and any other rasterizer substitutes faces.
"""

import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "branding" / "social"
OUT = ROOT / "assets" / "social"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

FORMATS = {
    "square": (1080, 1080),
    "portrait": (1080, 1350),
    "story": (1080, 1920),
    "wide": (1200, 630),
}


def render(master, fmt, size, out_path):
    w, h = size
    before = out_path.stat().st_mtime if out_path.exists() else 0
    with tempfile.TemporaryDirectory() as profile:
        proc = subprocess.Popen(
            [
                CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                f"--user-data-dir={profile}",
                f"--window-size={w},{h}",
                "--force-device-scale-factor=1",
                # Webfonts must finish loading before the shot; the default
                # virtual-time budget fires early and ships Georgia.
                "--virtual-time-budget=9000",
                f"--screenshot={out_path}",
                f"{master.as_uri()}?format={fmt}",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Chrome writes the PNG and then routinely fails to exit headless.
        try:
            proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
    if not out_path.exists() or out_path.stat().st_mtime == before:
        sys.exit(f"Chrome produced no screenshot for {out_path.name}")


def main(argv):
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    if not SRC.is_dir():
        sys.exit(f"missing {SRC.relative_to(ROOT)}")
    OUT.mkdir(parents=True, exist_ok=True)

    wanted = set(argv[1:])
    masters = sorted(SRC.glob("*.html"))
    if wanted:
        masters = [m for m in masters if m.stem in wanted]
        if not masters:
            sys.exit(f"no master matches {', '.join(sorted(wanted))}")

    for master in masters:
        for fmt, size in FORMATS.items():
            out_path = OUT / f"{master.stem}-{fmt}.png"
            render(master, fmt, size, out_path)
            print(f"  wrote assets/social/{out_path.name}  {size[0]}x{size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
