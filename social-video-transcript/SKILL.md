---
name: social-video-transcript
description: Transcribe and read public Instagram Reels, TikToks and YouTube videos or Shorts from a link (Whisper, 90+ languages, SRT/VTT), look up YouTube channel IDs and RSS feeds, and check 2026 upload specs for 9 platforms. Use when the user pastes a social video link or asks about video sizes, lengths or caption limits.
---

# Social Video Transcript

Turns a link to a public short-form or YouTube video into text you can work with: a timestamped Whisper transcript, the caption and hashtags, and the platform's upload rules. Built on the free public API of [Shortform Kit](https://shortformkit.com). No API key, no account, nothing to install beyond Python 3.

## When to Use This Skill

- The user pastes an Instagram Reel, TikTok, YouTube video or Short and wants the words, a summary, the hook, quotes or subtitles.
- The user wants competitor research: compare what several creators say in their videos.
- The user needs SRT or VTT subtitles for a public video.
- The user asks for a YouTube channel ID (UC...) or a channel's RSS feed.
- The user asks what size, length, file type or caption limit a platform allows (Reels, TikTok, Shorts, Stories, LinkedIn, X, Facebook, Pinterest, Snapchat, Threads).

Do not use it for private accounts, login-only content or for downloading content the user is not allowed to use.

## What This Skill Does

1. **Transcript**: Whisper on the server, about as long as the audio, up to 20 minutes per call (use `--start`/`--end` for longer videos). Optional `--lang` and `--translate` to English. Can save `.srt` and `.vtt`.
2. **Info**: platform, title, creator, duration, caption, hashtags, available qualities, carousel size.
3. **Channel ID**: UC ID, handle, channel URL and RSS feed from a @handle or any video link.
4. **Specs**: 2026 upload specs with sources, filtered by platform and format.

## How to Use

Run the bundled script (Python 3, standard library only):

```bash
python3 scripts/sfk.py transcript "https://www.instagram.com/reel/..."
python3 scripts/sfk.py transcript "https://youtu.be/..." --start 10:00 --end 20:00 --srt part.srt
python3 scripts/sfk.py transcript "https://www.tiktok.com/@user/video/..." --translate
python3 scripts/sfk.py info "https://www.tiktok.com/@user/video/..."
python3 scripts/sfk.py channel @mkbhd
python3 scripts/sfk.py specs instagram reels
```

Then do what the user asked with the output: summarise, pull the hook (first 1 to 3 sentences), write chapters from the timestamps, rewrite as a script, or compare videos.

If the environment has no network access to shortformkit.com, say so and offer the website instead: https://shortformkit.com/video-to-text/ (transcripts) or https://shortformkit.com/social-media-video-specs-2026/ (specs).

## Examples

**User:** "What's the hook of this Reel? https://www.instagram.com/reel/ABC/"
Run `transcript`, quote the first sentence or two, explain why it works, suggest two variations.

**User:** "Give me German subtitles for this YouTube clip."
Run `transcript URL --lang de --srt clip.srt` and hand over the file.

**User:** "How long can a TikTok be and how many hashtags should I use?"
Run `specs tiktok` and answer from the rows, citing the source link in the output.

**User:** "I need the channel ID for @veritasium."
Run `channel @veritasium` and give the ID, channel URL and RSS feed.

## Notes

- Fair use: about 30 requests per minute per IP. Transcriptions run one at a time on the server, so a long video can take a minute or two.
- Prefer an MCP connection? The same tools are available as a remote MCP server at `https://shortformkit.com/mcp`.
- Only use transcripts and downloads of content you own or are allowed to use.
