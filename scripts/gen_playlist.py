#!/usr/bin/env python3
"""Writes playlist.m3u from catalog.json.

--base is the URL this repository's files are served from: the guide (url-tvg) and the
channel logos and posters (tvg-logo) point there. Stream and film URLs are absolute and are
taken from catalog.json as they are: the live channels play public test streams, the films and
episodes play this repository's GitHub Release assets (tag media-v1).

Usage: python3 scripts/gen_playlist.py [--base URL] [--out playlist.m3u]
Standard library only.
"""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_BASE = "https://nuancebit.github.io/overchoice-review-media"


def attr(value: str) -> str:
    # M3U attributes are double-quoted and cannot escape a quote.
    assert '"' not in value and "\n" not in value, value
    return value


def build(catalog: dict, base: str) -> str:
    lines = [f'#EXTM3U url-tvg="{attr(base)}/guide.xml"']
    lines.append("#PLAYLIST:Overchoice Review")
    for ch in catalog["channels"]:
        logo = f'{base}/art/logos/{ch["id"].split(".")[0]}.png'
        lines.append(f'#EXTINF:-1 tvg-id="{attr(ch["id"])}" tvg-name="{attr(ch["name"])}" '
                     f'tvg-logo="{attr(logo)}" group-title="Demo Channels",{ch["name"]}')
        lines.append(ch["url"])
    for mv in catalog["movies"]:
        lines.append(f'#EXTINF:-1 tvg-name="{attr(mv["name"])}" tvg-logo="{attr(base)}/art/posters/{attr(mv["poster"])}" '
                     f'group-title="Movies",{mv["name"]}')
        lines.append(mv["url"])
    se = catalog["series"]
    for ep in se["episodes"]:
        lines.append(f'#EXTINF:-1 tvg-name="{attr(ep["name"])}" tvg-logo="{attr(base)}/art/posters/{attr(se["poster"])}" '
                     f'group-title="Series",{ep["name"]}')
        lines.append(ep["url"])
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--out", default=str(ROOT / "playlist.m3u"))
    a = ap.parse_args()
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    text = build(catalog, a.base.rstrip("/"))
    pathlib.Path(a.out).write_text(text, encoding="utf-8")
    print(f"wrote {a.out}: {text.count('#EXTINF')} entries")


if __name__ == "__main__":
    main()
