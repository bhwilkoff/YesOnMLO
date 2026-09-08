#!/usr/bin/env python3
"""Render branding/og-image-master.html -> assets/og-image.png (1200x630).

Headless Chrome, because the master uses the site's real Google Fonts
(Lora + Source Sans Pro) and any other rasterizer substitutes faces.
Never hand-edit the PNG; edit the master and re-run this.

    python3 tools/render_og_image.py
"""
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
MASTER = ROOT / "branding" / "og-image-master.html"
OUT = ROOT / "assets" / "og-image.png"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main() -> int:
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    before = OUT.stat().st_mtime if OUT.exists() else 0
    with tempfile.TemporaryDirectory() as profile:
        proc = subprocess.Popen(
            [
                CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                f"--user-data-dir={profile}",
                "--window-size=1200,630",
                # Webfonts must finish loading before the shot; the default
                # virtual-time budget fires too early and ships Georgia.
                "--virtual-time-budget=8000",
                f"--screenshot={OUT}",
                MASTER.as_uri(),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Chrome writes the PNG and then routinely fails to exit in
        # headless mode. Wait, then kill it — the screenshot is done.
        try:
            proc.wait(timeout=45)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
    if not OUT.exists() or OUT.stat().st_mtime == before:
        sys.exit("Chrome produced no screenshot")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
