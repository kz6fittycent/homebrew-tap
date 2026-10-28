cask "desktop-scriptures" do
  version "2.3.4"
  sha256 "96072a381993bad83b91d11b17686cd58a862207714d71848033b5112361de4e"

  url "https://github.com/kz6fittycent/Desktop-Scriptures/releases/download/v2.3.4/Desktop-Scriptures-#{version}-macos-arm64.dmg"
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
