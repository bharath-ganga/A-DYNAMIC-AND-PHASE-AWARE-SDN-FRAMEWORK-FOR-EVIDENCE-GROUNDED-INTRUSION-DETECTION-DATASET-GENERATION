# Beyond Static Traffic — SDN Research

Interactive website for **Beyond Static Traffic: A Dynamic and Phase-Aware SDN Framework for Evidence-Grounded Intrusion Detection Dataset Generation**.

[Open the live website](https://a-dynamic-and-phase-aware-sdn-framework-for-evidence-groun.pages.dev/)

The website is publicly deployed on Cloudflare Pages. This repository contains the website source, research paper, dataset exports, original graphs, and narrated video. It does not contain the Mininet/Ryu experiment execution implementation.

## Run locally

Requires Python 3. No Node packages or build step are required to view the website.

```sh
python serve_preview.py
```

Open **http://127.0.0.1:4173/**. This preview server supports HTTP byte ranges so video chapter seeking works correctly. For static hosting, serve `dist/` directly; the files are already built.

## Features

- Beginner-friendly SDN architecture story: a 60-second, six-scene animation with large moving packet envelopes, separate controller-request and rule messages, a flow-table check, direct switch forwarding, plain-English captions, chapter controls, pause/replay, and optional browser English read-aloud. The technical diagram remains expandable below.
- [SDN Architecture](https://a-dynamic-and-phase-aware-sdn-framework-for-evidence-groun.pages.dev/#architecture): a six-step animated teaching walkthrough of application intent, a reactive OpenFlow exchange, rule installation, direct switch forwarding, and later telemetry/evaluation. Includes layer explanations, presenter wording, playback controls, and a labeled illustrative flow rule.
- [Evidence lab](https://a-dynamic-and-phase-aware-sdn-framework-for-evidence-groun.pages.dev/#evidence): animated stable/constrained/recovery sequence synchronized with reported H28 phase means, clickable comparison bars, a selector for all 24 actual H14 runs, and a claim-to-source explorer with original graphs, CSVs, paper references, and scientific limits. H28 aggregate measurements remain separate from the H14 run records.
- Separate [How it works](https://a-dynamic-and-phase-aware-sdn-framework-for-evidence-groun.pages.dev/#explainer) tab: animated six-stage experiment workflow, problem statement, tools, reproduction requirements, objectives, and limitations.
- Interactive teaching animations for Logistic Regression, Random Forest, RBF-SVM, Gradient Boosting, and Soft Voting, with adjustable illustrative input and the actual H23 metrics displayed separately.
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

## Complete supplied result folders

The original directory exports are also available under [research-artifacts](research-artifacts/README.md):

- [FINAL RESULTS](research-artifacts/FINAL%20RESULTS/), including the guide package and the additional LSTM/GRU/Random Forest result files and model artifacts.
- [D05_FINAL_DATASET_EXPORT_v1](research-artifacts/D05_FINAL_DATASET_EXPORT_v1/), including the H14 splits, supporting datasets, audits, and reports.

All 174 supplied files are preserved byte-for-byte, with a [SHA-256 manifest](research-artifacts/SHA256SUMS.txt). These additional artifacts remain separate from the paper's reported evaluation and do not automatically alter the website's results.
