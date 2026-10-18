#!/usr/bin/env python3
"""Checks playlist.m3u and guide.xml against each other.

- the playlist parses to the expected number of entries (default 12), every entry has a URL;
- every tvg-id in the playlist has a <channel> in the guide and the other way round;
- per channel the programmes are contiguous: no gap, no overlap;
- per channel the guide covers now (or --at) to --days days later (default 7).

Usage: python3 scripts/check.py [--playlist playlist.m3u] [--guide guide.xml]
                                [--entries 12] [--days 7] [--at 2026-10-17T12:00:00Z]
Exit code 0 when everything holds, 1 otherwise. Standard library only.
"""
import argparse
import datetime as dt
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent


def parse_time(s: str) -> dt.datetime:
    return dt.datetime.strptime(s, "%Y%m%d%H%M%S %z")


def parse_playlist(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    entries, pending = [], None
    for l in lines:
        if l.startswith("#EXTINF"):
            pending = l
        elif not l.startswith("#") and pending is not None:
            m = re.search(r'tvg-id="([^"]*)"', pending)
            g = re.search(r'group-title="([^"]*)"', pending)
            entries.append({"tvg_id": m.group(1) if m else None,
                            "group": g.group(1) if g else None,
                            "name": pending.rsplit(",", 1)[-1], "url": l})
            pending = None
    header = lines[0] if lines else ""
    return header, lines, entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--playlist", default=str(ROOT / "playlist.m3u"))
    ap.add_argument("--guide", default=str(ROOT / "guide.xml"))
    ap.add_argument("--entries", type=int, default=12)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--at", help="ISO time to check coverage from; default: now")
    a = ap.parse_args()
    errors = []

    header, lines, entries = parse_playlist(pathlib.Path(a.playlist).read_text(encoding="utf-8"))
    if not header.startswith("#EXTM3U"):
        errors.append("playlist: first line is not #EXTM3U")
    if "#PLAYLIST:Overchoice Review" not in lines:
        errors.append("playlist: #PLAYLIST:Overchoice Review missing")
    if len(entries) != a.entries:
        errors.append(f"playlist: {len(entries)} entries, expected {a.entries}")
    ids = {e["tvg_id"] for e in entries if e["tvg_id"]}

    root = ET.parse(a.guide).getroot()
    chans = {c.get("id") for c in root.findall("channel")}
    if ids != chans:
        errors.append(f"tvg-id mismatch: playlist-only {sorted(ids - chans)}, guide-only {sorted(chans - ids)}")

    at = (dt.datetime.fromisoformat(a.at.replace("Z", "+00:00")) if a.at
          else dt.datetime.now(dt.timezone.utc))
    until = at + dt.timedelta(days=a.days)
    per = {}
    for p in root.findall("programme"):
        per.setdefault(p.get("channel"), []).append((parse_time(p.get("start")), parse_time(p.get("stop"))))
    for cid in sorted(chans):
        progs = sorted(per.get(cid, []))
        if not progs:
            errors.append(f"{cid}: no programmes")
            continue
        for (s1, e1), (s2, e2) in zip(progs, progs[1:]):
            if s2 != e1:
                errors.append(f"{cid}: {'gap' if s2 > e1 else 'overlap'} at {e1.isoformat()} -> {s2.isoformat()}")
        if any(e <= s for s, e in progs):
            errors.append(f"{cid}: programme with stop <= start")
        if progs[0][0] > at or progs[-1][1] < until:
            errors.append(f"{cid}: covers {progs[0][0].isoformat()} .. {progs[-1][1].isoformat()}, "
                          f"needs {at.isoformat()} .. {until.isoformat()}")

    first = min(s for v in per.values() for s, _ in v) if per else None
    last = max(e for v in per.values() for _, e in v) if per else None
    print(f"playlist: {len(entries)} entries, {len(ids)} tvg-ids; guide: {len(chans)} channels, "
          f"{sum(len(v) for v in per.values())} programmes, {first} .. {last}")
    for e in errors:
        print("FAIL", e)
    print("OK" if not errors else f"{len(errors)} problem(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
