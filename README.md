# Beyond Static Traffic — SDN Research

Interactive website for **Beyond Static Traffic: A Dynamic and Phase-Aware SDN Framework for Evidence-Grounded Intrusion Detection Dataset Generation**.

[Open the hosted website](https://beyond-static-traffic-sdn.bharathganga7.chatgpt.site/)

The hosted Site currently has private access. This repository contains the website source, research paper, dataset exports, original graphs, and narrated video. It does not contain the Mininet/Ryu experiment execution implementation.

## Run locally

Requires Python 3. No Node packages or build step are required to view the website.

```sh
python serve_preview.py
```

Open **http://127.0.0.1:4173/**. This preview server supports HTTP byte ranges so video chapter seeking works correctly. For static hosting, serve `dist/` directly; the files are already built.

## Features

- Interactive network illustration with six workload controls, node inspection, star/line topology switching, guided walkthrough, and snapshot export.
- Large stable/constrained/recovery controls synchronized with the paper's H28 phase means.
- Separate views for results, dataset exploration, graph library, downloads, methodology, workload evidence, and paper access.
- Filterable H14 dataset: 216 observations, 20 columns, pagination, run search, and filtered CSV export.
- 29 original graphs with category filters, enlargement, and PNG downloads.
- Nearly six-minute English narrated film with 14 chapters, burned-in captions, transcript, and video/caption downloads. Narration uses a synthesized voice.
- Responsive layouts, keyboard controls, reduced-motion support, and animation pause controls.

## Files

| Path | Contents |
| --- | --- |
| `dist/index.html` | Website entry point |
| `dist/*.css`, `dist/*.js` | Styles, navigation, network animation, dataset/gallery behavior, and video chapters |
| `dist/paper.pdf` | Supplied research paper |
| `dist/evidence/` | H14 CSV splits, source tables, original ZIP exports, and 29 graph PNGs |
| `dist/research-explainer-english.mp4` | Detailed English narrated video |
| `dist/film-chapters.json` | Chapter timestamps and narration text |
| `dist/narration-transcript.txt`, `dist/narration-en.vtt` | Transcript and captions |
| `narration-story.json` | Narration and scene definitions |
| `synthesize_narration.ps1`, `make_narrated_film.py` | Narration/video generation scripts |
| `serve_preview.py` | Static preview server with video range support |
| `.openai/hosting.json` | Existing Sites project identity and static output configuration; contains no credentials |

Other root-level Python and HTML files preserve the authoring and asset-preparation scripts used during development. Some reference the original Windows workspace and ZIP locations; adjust those paths before rerunning them. Restyling/setup scripts are authoring history, not a required build pipeline, and should not be rerun over the final site indiscriminately.

## Regenerate the narrated film

The supplied MP4 is ready to use. Regeneration requires Windows PowerShell with `System.Speech`, Microsoft Zira Desktop, Python with Pillow, and FFmpeg on `PATH`.

```powershell
python -m pip install Pillow
./synthesize_narration.ps1
python make_narrated_film.py
```

Intermediate WAV and render files stay in `.narration-work/`, which is ignored by Git. Google Fonts are optional; system-font fallbacks are provided.

## Research scope

- **H14:** 216 observations; run-disjoint 72-row training, validation, and test partitions. The export contains four scenario values, while the broader framework describes six workloads.
- **H23:** 144 prospective intervals from 16 additional runs, evaluated with five frozen models.
- **H28:** 12 runs and 36 phase conditions measuring RTT and TCP bulk goodput.
- Newly trained H14 analysis is supplementary and remains separate from the paper's H23 frozen-model results.

Animations illustrate concepts; they do not represent a live SDN connection or execute attacks. Synthetic probing labels are not independently verified malicious ground truth. The paper's limitations remain visible throughout the website.

## Authors

Dr. S. Bharath Bhushan, Ganga Bharath, Pathepur Dikshith, Badveli Guru Pala Nivesh Reddy, and Chitteti Durga Sai.
