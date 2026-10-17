#!/usr/bin/env python3
"""Writes guide.xml (XMLTV) for the demo channels in catalog.json.

The guide starts at today 00:00 UTC and ends --days + 1 days later, so from any moment of
the day it was made it reaches at least --days (default 7) days ahead. A daily run keeps it
rolling. Programme titles are neutral and describe what the stream actually shows. The output depends
only on the date, so a re-run on the same day produces an identical file (no empty commits).

Usage: python3 scripts/gen_guide.py [--days 7] [--base URL] [--out guide.xml]
Standard library only.
"""
import argparse
import datetime as dt
import json
import pathlib
from xml.sax.saxutils import escape, quoteattr

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_BASE = "https://nuancebit.github.io/overchoice-review-media"

# Per theme: a cycle of (minutes, title, description, category). Each cycle sums to 24 h.
SCHEDULES = {
    "bars": [
        (120, "Test Card", "Colour bars with an on-screen clock. A continuous test signal for checking picture and sound.", "Technical"),
        (60, "Signal Check", "Colour bars and a reference tone with the current time.", "Technical"),
    ],
    "mixed": [
        (60, "Streaming Showcase", "A looping demonstration channel of short clips and presentations.", "Documentary"),
        (30, "Studio Reel", "Short clips from the looping demonstration channel.", "Documentary"),
        (30, "Showcase Replay", "The demonstration loop continues.", "Documentary"),
    ],
    "pattern": [
        (30, "Pattern and Tone", "A counting test pattern with a beep, for checking audio and video sync.", "Technical"),
    ],
    "animation": [
        (60, "Animation Hour", "Big Buck Bunny, an open movie by the Blender Foundation (CC BY 3.0), from the start.", "Animation"),
    ],
}


def xmltv_time(t: dt.datetime) -> str:
    return t.strftime("%Y%m%d%H%M%S +0000")


def programmes(channel_id: str, theme: str, start: dt.datetime, end: dt.datetime):
    cycle = SCHEDULES[theme]
    t, i = start, 0
    while t < end:
        minutes, title, desc, cat = cycle[i % len(cycle)]
        stop = min(t + dt.timedelta(minutes=minutes), end)
        yield t, stop, title, desc, cat
        t, i = stop, i + 1


def build(catalog: dict, today: dt.date, days: int, base: str) -> str:
    start = dt.datetime(today.year, today.month, today.day, tzinfo=dt.timezone.utc)
    # One extra day: generated at 00:00 or 23:59, the guide still reaches `days` days past now.
    end = start + dt.timedelta(days=days + 1)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!DOCTYPE tv SYSTEM "xmltv.dtd">',
           '<tv generator-info-name="overchoice-review-media gen_guide.py">']
    channels = catalog["channels"]
    for ch in channels:
        out.append(f'  <channel id={quoteattr(ch["id"])}>')
        out.append(f'    <display-name lang="en">{escape(ch["name"])}</display-name>')
        out.append(f'    <icon src={quoteattr(base + "/art/logos/" + ch["id"].split(".")[0] + ".png")}/>')
        out.append('  </channel>')
    for ch in channels:
        for s, e, title, desc, cat in programmes(ch["id"], ch["theme"], start, end):
            out.append(f'  <programme start="{xmltv_time(s)}" stop="{xmltv_time(e)}" channel={quoteattr(ch["id"])}>')
            out.append(f'    <title lang="en">{escape(title)}</title>')
            out.append(f'    <desc lang="en">{escape(desc)}</desc>')
            out.append(f'    <category lang="en">{escape(cat)}</category>')
            out.append('  </programme>')
    out.append('</tv>')
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7, help="minimum look-ahead in days")
    ap.add_argument("--base", default=DEFAULT_BASE, help="URL the repo files are served from (channel icons)")
    ap.add_argument("--out", default=str(ROOT / "guide.xml"))
    ap.add_argument("--today", help="YYYY-MM-DD (UTC); default: today")
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today) if a.today else dt.datetime.now(dt.timezone.utc).date()
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    text = build(catalog, today, a.days, a.base.rstrip("/"))
    pathlib.Path(a.out).write_text(text, encoding="utf-8")
    print(f"wrote {a.out}: {len(catalog['channels'])} channels, {text.count('<programme ')} programmes, {len(text.encode())} bytes")


if __name__ == "__main__":
    main()
