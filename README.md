# Overchoice review media

This repository exists so that app reviewers and testers can try the Overchoice app with
legal sample content. It holds one M3U playlist, a programme guide (XMLTV) and six channel
logos. **It hosts no film files**: the playlist links to Creative Commons films by the Blender
Foundation / Blender Studio where their makers and the Internet Archive publish them.

**Playlist URL (enter this in the app as an M3U source):**

```
https://nuancebit.github.io/overchoice-review-media/playlist.m3u
```

The playlist's header points the app at `guide.xml` on the same site, so the guide loads
with no extra setup.

## What is in the playlist

| Section | Entries | Played from |
|---|---|---|
| Live | Overchoice Demo 1-6 | Public test streams (see below) |
| Movies | Elephants Dream, Tears of Steel, Sintel | Blender's download server (`download.blender.org`), linked |
| Series | Caminandes S01E01-E03 | The Internet Archive (`archive.org`), linked |

### Films

The playlist only links to the films; nothing is copied into this repository. The movies play
from the files Blender publishes on `download.blender.org`, the Caminandes episodes from the
Internet Archive. Films and episodes carry no artwork in the playlist: the app finds their
posters itself.

| Entry | File |
|---|---|
| Elephants Dream (2006) | [elephantsdream-720-h264-st-aac.mov](https://download.blender.org/ED/elephantsdream-720-h264-st-aac.mov) |
| Tears of Steel (2012) | [tears_of_steel_720p.mov](https://download.blender.org/demo/movies/ToS/tears_of_steel_720p.mov) |
| Sintel (2010) | [Sintel.2010.1080p.mkv](https://download.blender.org/durian/movies/Sintel.2010.1080p.mkv) |
| Caminandes S01E01 Llama Drama | [archive.org/details/Caminandes1LlamaDrama](https://archive.org/details/Caminandes1LlamaDrama) |
| Caminandes S01E02 Gran Dillama | [archive.org/details/Caminandes2GranDillama](https://archive.org/details/Caminandes2GranDillama) |
| Caminandes S01E03 Llamigos | [archive.org/details/CaminandesLlamigos](https://archive.org/details/CaminandesLlamigos) |

### Live demo channels

The channel names are invented. Each one plays a public test stream that its operator
publishes for testing players:

| Channel | Stream | Runs |
|---|---|---|
| Overchoice Demo 1 | Unified Streaming demo, live test card (`demo.unified-streaming.com`) | 24/7 live |
| Overchoice Demo 2 | Unified Streaming virtual channel demo (`virtual-channel.unified-streaming.com`) | 24/7 live loop |
| Overchoice Demo 3 | Unified Streaming demo, live test card with SCTE-35 markers | 24/7 live |
| Overchoice Demo 4 | Unified Streaming demo, live test card, fMP4 packaging | 24/7 live |
| Overchoice Demo 5 | Apple HLS example "bipbop 16x9" (`devstreaming-cdn.apple.com`) | 30 min, then ends |
| Overchoice Demo 6 | Mux HLS test stream, Big Buck Bunny (`test-streams.mux.dev`) | 10.5 min, then ends |

Demo 5 and 6 are on-demand test streams: they start from the beginning each time the
channel is opened and stop at their end. The guide for these channels is generic.

### Programme guide

`guide.xml` is a rolling 7-day guide: it starts at 00:00 UTC on the day it is generated and
always reaches at least seven days past the current time, with neutral programme titles that
describe what each stream shows. The workflow `.github/workflows/pages.yml` runs every day
(and on every push to `main`): it regenerates the guide, commits it when it changed, and
deploys the site to GitHub Pages.

To regenerate by hand:

```
python3 scripts/gen_guide.py      # guide.xml, 7 days (--days N to change)
python3 scripts/gen_playlist.py   # playlist.m3u from catalog.json
python3 scripts/check.py          # 12 entries, channel ids match, no gaps or overlaps, now -> +7 days
```

The scripts use the Python standard library only, and the guide depends only on the date, so
two runs on the same day produce the same file. `catalog.json` is the single list of channels,
films and episodes, each with the URL the playlist links to. Both generators take `--base URL`
to serve the site from elsewhere.

## Credits

The films are by the Blender Foundation / Blender Studio and are published under Creative
Commons Attribution licences ([Blender Studio terms](https://studio.blender.org/terms-and-conditions/)).
This repository hosts none of them; it only links to the files listed above.

| Film | Year | By | Licence |
|---|---|---|---|
| [Elephants Dream](https://orange.blender.org/) | 2006 | Blender Foundation / Netherlands Media Art Institute | [CC BY 2.5](https://creativecommons.org/licenses/by/2.5/) |
| [Tears of Steel](https://mango.blender.org/) | 2012 | Blender Foundation | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) |
| [Sintel](https://durian.blender.org/) | 2010 | Blender Foundation | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) |
| [Caminandes 1: Llama Drama](https://archive.org/details/Caminandes1LlamaDrama) | 2013 | Blender Foundation | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) |
| [Caminandes 2: Gran Dillama](https://studio.blender.org/projects/caminandes-2/) | 2013 | Blender Foundation | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) |
| [Caminandes 3: Llamigos](https://studio.blender.org/projects/caminandes-3/) | 2016 | Blender Studio | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

The test streams on the live channels belong to their operators (Unified Streaming,
Apple, Mux) and are linked, not copied. They are published by those operators for testing
streaming players. The Mux stream shows Big Buck Bunny (2008, Blender Foundation,
[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)).

## Licence of this repository

See [LICENSE](LICENSE). In short: the scripts, the data, the playlist, the guide and the
channel logos are released under CC0 1.0. The linked films and streams are not part of this
repository.

## Contact

This repository is maintained by nuancebit for testing the Overchoice app. It contains no
personal data and the app sends nothing to it beyond the normal HTTP requests for these
files.
