# Shortform Kit skills for Claude

Agent skills for people who work with short-form video. They use the free public API of [Shortform Kit](https://shortformkit.com): no API key, no account, Python 3 standard library only.

| Skill | What it does |
|---|---|
| [social-video-transcript](social-video-transcript/) | Transcribe public Instagram Reels, TikToks and YouTube videos or Shorts from a link (Whisper, 90+ languages, SRT/VTT), read captions and hashtags, find YouTube channel IDs and RSS feeds, check 2026 upload specs for 9 platforms |

## Install

**Claude Code** (personal skills):

```bash
git clone https://github.com/diegobruegger-prog/shortformkit-skills.git
cp -r shortformkit-skills/social-video-transcript ~/.claude/skills/
```

**Claude.ai**: Settings, Capabilities, Skills, upload the `social-video-transcript` folder as a ZIP. The skill calls shortformkit.com, so code execution needs network access to that domain.

Then just paste a link: "What's the hook of this Reel?", "Give me German subtitles for this YouTube clip", "How long can a TikTok be?".

## Prefer MCP?

The same tools run as a remote MCP server: `https://shortformkit.com/mcp` ([docs](https://shortformkit.com/mcp-server/), [repo](https://github.com/diegobruegger-prog/shortformkit-mcp)).

## Fair use

About 30 requests per minute per IP, transcriptions run one at a time. Only use transcripts and downloads of content you own or are allowed to use.

MIT License.
