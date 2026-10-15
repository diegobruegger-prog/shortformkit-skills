#!/usr/bin/env python3
"""Shortform Kit helper for the social-video-transcript skill. Standard library only.

  sfk.py transcript URL [--lang de] [--translate] [--start 1:00] [--end 2:30] [--srt out.srt] [--vtt out.vtt]
  sfk.py info URL
  sfk.py channel @handle|channel-url|video-url
  sfk.py specs [platform] [format]

Uses the free public API of https://shortformkit.com (no key, fair-use limit of about 30 requests per minute per IP).
Works with public Instagram, TikTok, YouTube, X, Facebook, Pinterest and Threads posts.
"""
import argparse, io, json, sys, time, urllib.error, urllib.request, zipfile

API = "https://shortformkit.com"
UA = "shortformkit-skill/1.0 (+https://github.com/diegobruegger-prog/shortformkit-skills)"


def _req(method, path, body=None, raw=False, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API + path, data=data, method=method, headers={"Content-Type": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            b = resp.read()
            return b if raw else json.loads(b)
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read()).get("detail")
        except Exception:  # noqa: BLE001
            msg = None
        sys.exit(f"Error {e.code}: {msg or e.reason}")


def transcript(a):
    body = {"url": a.url, "kind": "transcript", "translate": a.translate}
    for k in ("start", "end"):
        if getattr(a, k):
            body[k] = getattr(a, k)
    if a.lang:
        body["language"] = a.lang
    job = _req("POST", "/api/download", body)["job"]
    t0 = time.time()
    while True:
        j = _req("GET", f"/api/job/{job}")
        if j.get("status") == "done":
            break
        if j.get("status") == "error":
            sys.exit("Error: " + str(j.get("error") or "transcription failed"))
        if time.time() - t0 > 600:
            sys.exit(f"Still running after 10 minutes, check {API}/api/job/{job}")
        print(f"[{j.get('phase') or j.get('status')}]", file=sys.stderr)
        time.sleep(3)
    if a.srt or a.vtt:
        z = zipfile.ZipFile(io.BytesIO(_req("GET", f"/api/file/{job}", raw=True, timeout=120)))
        for ext, out in (("srt", a.srt), ("vtt", a.vtt)):
            if out:
                name = next(n for n in z.namelist() if n.endswith("." + ext))
                open(out, "wb").write(z.read(name))
                print(f"saved {out}", file=sys.stderr)
    print(f"# language: {j.get('language')}  platform: {j.get('platform')}  source: {a.url}")
    print(j.get("text", ""))


def info(a):
    d = _req("POST", "/api/info", {"url": a.url})
    keep = ("platform", "title", "uploader", "duration", "caption", "hashtags", "qualities", "is_gallery", "gallery_count", "thumbnail")
    print(json.dumps({k: d.get(k) for k in keep if d.get(k) not in (None, "", [])}, ensure_ascii=False, indent=1))


def channel(a):
    d = _req("POST", "/api/channel", {"q": a.query})
    d["channel_url"] = f"https://www.youtube.com/channel/{d['id']}"
    d["rss_feed"] = f"https://www.youtube.com/feeds/videos.xml?channel_id={d['id']}"
    print(json.dumps(d, ensure_ascii=False, indent=1))


def specs(a):
    d = _req("GET", "/data/social-media-video-specs-2026.json")
    rows = [r for r in d["rows"] if a.platform.lower() in r["platform"].lower() and a.format.lower() in r["format"].lower()]
    if not rows:
        sys.exit("No match. Platforms: " + ", ".join(sorted({r["platform"] for r in d["rows"]})))
    for r in rows:
        r.pop("by_source", None)
    print(json.dumps({"updated": d.get("updated"), "rows": rows, "source": f"{API}/social-media-video-specs-2026/"}, ensure_ascii=False, indent=1))


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
s = p.add_subparsers(dest="cmd", required=True)
t = s.add_parser("transcript"); t.add_argument("url"); t.add_argument("--lang"); t.add_argument("--translate", action="store_true")
t.add_argument("--start"); t.add_argument("--end"); t.add_argument("--srt"); t.add_argument("--vtt"); t.set_defaults(f=transcript)
i = s.add_parser("info"); i.add_argument("url"); i.set_defaults(f=info)
c = s.add_parser("channel"); c.add_argument("query"); c.set_defaults(f=channel)
sp = s.add_parser("specs"); sp.add_argument("platform", nargs="?", default=""); sp.add_argument("format", nargs="?", default=""); sp.set_defaults(f=specs)
args = p.parse_args()
args.f(args)
