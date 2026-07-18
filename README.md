# AER 2022 — Rebel on the Canal

> Cao & Chen (2022), *American Economic Review* 112(5): 1555–1590.
> **"Rebel on the Canal: Disrupted Trade Access and Social Conflict in China"**

A reading-and-replication workspace for the above paper. This repository contains:

1. **The paper PDF** — `AER2022-Rebel on the Canal- Disrupted Trade Access and Social Conflict in China.pdf` (4.6 MB).
2. **Author-supplied replication scripts** — `master.do` (entry point) and `Program/setup.do` (package installer).
3. **Chinese-language reading notes** — three companion documents at the repo root (see "Reading Notes" below).
4. **Citation metadata** — `source.txt` (credit for the `spatial_HAC` user-written package).

## What is NOT in this repository

`master.do` orchestrates a full empirical reproduction, but the data and auxiliary scripts are **not shipped here**. Researchers who want to actually run the paper's analysis must obtain the official replication package from the AEA **openICPSR** portal (link in the published AER article) and place its contents alongside `master.do`.

Specifically absent:

| Path master.do expects | In this repo? |
|---|---|
| `Program/Clean/clean.do` | No |
| `Program/Analysis/*.do` (~30 figures and tables) | No |
| `Program/Adofile/spatial_HAC/` (Hsiang 2010 ado) | No (cited in `source.txt`) |
| `Data/Raw/` (shape files, GIS layers) | No |
| `Data/Final/rebellion.dta` (analysis panel) | No |
| `Results/` (output figures and tables) | No |

> `master.do` will still **parse and execute** the lines it can reach — `clear`, `set`, `cd`, `run Program/setup.do` — but it will stop at the first missing `Program/Clean/clean.do` once the openICPSR files are dropped in place.

## How to use `master.do`

```bash
# 1. Download the official replication package from AEA openICPSR.
#    (URL is in the published article.)

# 2. Drop its contents so the directory tree matches what master.do expects:
#
#    .
#    ├── master.do                 <- this repo
#    ├── Program/
#    │   ├── setup.do              <- this repo (package installer)
#    │   ├── Adofile/spatial_HAC/  <- from openICPSR
#    │   ├── Clean/clean.do        <- from openICPSR
#    │   └── Analysis/*.do         <- from openICPSR
#    ├── Data/
#    │   ├── Raw/                  <- from openICPSR
#    │   └── Final/                <- from openICPSR
#    └── Results/                  <- created by master.do
#

# 3. Edit master.do line 9 — replace `D:/FullReplication` with your local
#    project root. macOS/Linux users: uncomment one of the example lines
#    just below it.

# 4. From Stata:
do master.do
```

## Reading Notes

| File | Audience | Content |
|---|---|---|
| [论文解释.md](论文解释.md) | Anyone curious about the paper | Plain-language walkthrough of identification, findings, and mechanisms. Each claim tagged to a specific table or figure. |
| [论文模型解读与StatsPAI复现分析.md](论文模型解读与StatsPAI复现分析.md) | Researchers considering reproduction | Equation-by-equation dissection of the paper + assessment of whether StatsPAI can reproduce it. |
| [source.txt](source.txt) | Anyone running `master.do` | Citation for the `spatial_HAC` user-written package (Hsiang 2010). |

## Internal working notes

`docs/superpowers/specs/` contains design specs from collaborative editing sessions (e.g. the spec used to draft [论文解释.md](论文解释.md)). These are working notes, not part of the paper or replication package — keep them under version control, but don't treat them as deliverable artefacts.

## License

- **Replication scripts and reading notes in this repository** are released under the [MIT License](LICENSE).
- **The paper PDF** (`AER2022-Rebel on the Canal- …pdf`) is the property of the American Economic Association; see AER's copyright terms before redistribution.
- **The replication package** (data + auxiliary scripts + spatial_HAC ado) is governed by the AEA openICPSR license; obtain it from the official portal.