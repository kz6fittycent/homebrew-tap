# kz6fittycent's Homebrew tap

```
brew install --cask kz6fittycent/tap/desktop-scriptures
```

| Cask | App |
|---|---|
| `desktop-scriptures` | [Desktop Scriptures](https://github.com/kz6fittycent/Desktop-Scriptures): an offline LDS scripture reader with notes, tags, search, and opt-in AI. macOS 13 or later on Apple Silicon. |

Update with `brew upgrade --cask desktop-scriptures`.

The apps aren't signed by Apple, so macOS refuses to open them the first
time (and after each upgrade): open the app once, then go to **System
Settings → Privacy & Security** and click **Open Anyway**.

Casks update themselves: `.github/workflows/update-casks.yml` checks each
app's latest GitHub Release once a day.
