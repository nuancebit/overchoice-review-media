# Overchoice review media

This repository exists so that app reviewers and testers can try the Overchoice app with
legal sample content. It holds one M3U playlist, a programme guide (XMLTV), artwork and,
as release assets, eight Creative Commons films by the Blender Foundation / Blender Studio.

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
| Movies | Big Buck Bunny, Elephants Dream, Sintel, Tears of Steel, Sprite Fright | Release [`media-v1`](https://github.com/nuancebit/overchoice-review-media/releases/tag/media-v1) of this repository |
| Series | Caminandes S01E01-E03 | Release `media-v1` of this repository |

### Films

The films are unchanged copies of the Internet Archive files listed under Attribution.
Each was only re-muxed for streaming
(`ffmpeg -i in.mp4 -map 0 -c copy -video_track_timescale <source timescale> -movflags +faststart out.mp4`):
the index (`moov` atom) moves to the start of the file so a player can start without reading
the end of the file first. Audio and video are not re-encoded: every audio and video packet,
with its timestamps, is identical to the source, and so is the duration. The release notes list each file with its source.

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
python3 scripts/check.py          # 14 entries, channel ids match, no gaps or overlaps, now -> +7 days
```

The scripts use the Python standard library only, and the guide depends only on the date, so
two runs on the same day produce the same file. `catalog.json` is the single list of channels,
films and episodes; for each film it keeps the release URL (`url`) and the original Internet
Archive file (`source`). Both generators take `--base URL` to serve the site from elsewhere.

## Attribution

All films are by the Blender Foundation / Blender Studio and are licensed under Creative
Commons Attribution licences. The files in release `media-v1` are copies of the Internet
Archive files below, re-muxed for streaming as described above (no other change).

| Title | Year | Author | Licence | Source |
|---|---|---|---|---|
| Big Buck Bunny | 2008 | Blender Foundation (Peach open movie project), www.bigbuckbunny.org | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) | [peach.blender.org/about](https://peach.blender.org/about/), file: [archive.org/details/BigBuckBunny_124](https://archive.org/details/BigBuckBunny_124) |
| Elephants Dream | 2006 | Blender Foundation / Netherlands Media Art Institute (Orange open movie project), orange.blender.org | [CC BY 2.5](https://creativecommons.org/licenses/by/2.5/) | [orange.blender.org](https://orange.blender.org/), file: [archive.org/details/ElephantsDream](https://archive.org/details/ElephantsDream) |
| Sintel | 2010 | Blender Foundation (Durian open movie project), www.sintel.org | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) | [durian.blender.org/sharing](https://durian.blender.org/sharing/), file: [archive.org/details/Sintel](https://archive.org/details/Sintel) |
| Tears of Steel | 2012 | Blender Foundation (Mango open movie project), mango.blender.org | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) | [mango.blender.org/sharing](https://mango.blender.org/sharing/), file: [archive.org/details/Tears-of-Steel](https://archive.org/details/Tears-of-Steel) |
| Sprite Fright | 2021 | Blender Studio | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [studio.blender.org/projects/sprite-fright](https://studio.blender.org/projects/sprite-fright/), [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Sprite_Fright_-_Blender_Open_Movie-full_movie.webm), file: [archive.org/details/sprite-fright](https://archive.org/details/sprite-fright) |
| Caminandes 1: Llama Drama | 2013 | Pablo Vazquez, Beorn Leonard, Francesco Siddi; music Jan Morgenstern; Blender Foundation | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Caminandes-_Llama_Drama_-_Short_Movie.ogv), file: [archive.org/details/Caminandes1LlamaDrama](https://archive.org/details/Caminandes1LlamaDrama) |
| Caminandes 2: Gran Dillama | 2013 | Pablo Vazquez, Beorn Leonard, Francesco Siddi; music Jan Morgenstern; Blender Foundation | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) | [caminandes.com/sharing (archived)](https://web.archive.org/web/2017/http://www.caminandes.com/sharing/), file: [archive.org/details/Caminandes2GranDillama](https://archive.org/details/Caminandes2GranDillama) |
| Caminandes 3: Llamigos | 2016 | Pablo Vazquez and the Blender Institute team; Blender Foundation | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Caminandes_3_-_Llamigos_-_Blender_Animated_Short.webm), file: [archive.org/details/CaminandesLlamigos](https://archive.org/details/CaminandesLlamigos) |

All files are H.264 video with AAC stereo audio, in the versions the Internet Archive offers:
Big Buck Bunny and Elephants Dream 640x360, Tears of Steel 862x360, Sintel 564x240,
Sprite Fright 1920x804, Caminandes 1-3 1920x1080. Together about 694 MB.

The posters in `art/posters/` are single frames from these films, cropped to 2:3 and scaled.
They are adaptations of the films above and are shared under the same licence as the film
they come from, with the same attribution.

The test streams on the live channels belong to their operators (Unified Streaming,
Apple, Mux) and are linked, not copied. They are published by those operators for testing
streaming players. The Big Buck Bunny footage in the Mux stream is the CC BY 3.0 film credited
above.

## Licence of this repository

See [LICENSE](LICENSE). In short: the scripts, the playlist, the guide and the channel
logos are released under CC0 1.0; the posters and the films follow the licence of their film.

## Contact

This repository is maintained by nuancebit for testing the Overchoice app. It contains no
personal data and the app sends nothing to it beyond the normal HTTP requests for these
files.
