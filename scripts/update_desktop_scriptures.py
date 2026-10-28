"""Write Casks/desktop-scriptures.rb for Desktop Scriptures' latest release.

Run by .github/workflows/update-casks.yml (daily, or by hand). Reads the
latest GitHub Release of kz6fittycent/Desktop-Scriptures - GitHub's
/releases/latest skips pre-releases - takes the macOS .dmg's checksum from
the .sha256 file published beside it, and rewrites the cask. Prints what it
did; the workflow commits only if the file changed.

    python3 scripts/update_desktop_scriptures.py [--tag TAG]

--tag reads a specific release instead (for trying this out).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = "kz6fittycent/Desktop-Scriptures"
CASK = Path(__file__).resolve().parent.parent / "Casks" / "desktop-scriptures.rb"
DMG_RE = re.compile(r"^Desktop-Scriptures-(?P<version>[0-9][0-9.]*)-macos-arm64\.dmg$")

TEMPLATE = """\
cask "desktop-scriptures" do
  version "{version}"
  sha256 "{sha256}"

  url "https://github.com/kz6fittycent/Desktop-Scriptures/releases/download/{tag}/Desktop-Scriptures-#{{version}}-macos-arm64.dmg"
  name "Desktop Scriptures"
  desc "Offline LDS scripture reader with notes, tags, search and opt-in AI"
  homepage "https://github.com/kz6fittycent/Desktop-Scriptures"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on macos: ">= :ventura"

  app "Desktop Scriptures.app"

  zap trash: "~/Library/Application Support/Desktop Scriptures"

  caveats <<~EOS
    Desktop Scriptures isn't signed by Apple yet, so macOS refuses to open it
    the first time (and after each upgrade). Open it once, then go to
    System Settings > Privacy & Security, scroll down, and click
    "Open Anyway" next to Desktop Scriptures.
  EOS
end
"""


def _get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "homebrew-tap-updater"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def render(release: dict) -> str | None:
    """The cask for this release, or None if it has no macOS build."""
    assets = {a["name"]: a["browser_download_url"] for a in release.get("assets", [])}
    for name in assets:
        match = DMG_RE.match(name)
        if match and f"{name}.sha256" in assets:
            sha = _get(assets[f"{name}.sha256"]).decode().split()[0].lower()
            if not re.fullmatch(r"[0-9a-f]{64}", sha):
                raise SystemExit(f"Unreadable checksum for {name}: {sha!r}")
            return TEMPLATE.format(version=match["version"], sha256=sha, tag=release["tag_name"])
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag")
    args = parser.parse_args()
    api = f"https://api.github.com/repos/{REPO}/releases/" + (f"tags/{args.tag}" if args.tag else "latest")
    try:
        release = json.loads(_get(api))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            print("No release published yet; nothing to do.")
            return 0
        raise
    cask = render(release)
    if cask is None:
        print(f"{release['tag_name']} has no macOS .dmg with a checksum; nothing to do.")
        return 0
    if CASK.exists() and CASK.read_text() == cask:
        print(f"Cask already at {release['tag_name']}.")
        return 0
    CASK.parent.mkdir(exist_ok=True)
    CASK.write_text(cask)
    print(f"Updated the cask to {release['tag_name']}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
