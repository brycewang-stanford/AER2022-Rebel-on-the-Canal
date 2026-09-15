# AER 2022 — Rebel on the Canal

> Cao & Chen (2022), *American Economic Review* 112(5): 1555–1590.
> **"Rebel on the Canal: Disrupted Trade Access and Social Conflict in China"**

A reading-and-replication workspace for the above paper.

## Layout

```text
.
├── Data/                  原始数据 — openICPSR 157781-V1 (not tracked by git)
│   ├── Raw/               shape files, GIS layers
│   └── Final/             rebellion.dta (analysis panel)
├── Program/               原始代码 — author's Stata replication code
│   ├── master.do          entry point            <- in repo
│   ├── setup.do           package installer      <- in repo
│   ├── Adofile/           source.txt (in repo) + spatial_HAC/ (from openICPSR)
│   ├── Clean/clean.do     <- from openICPSR
│   └── Analysis/*.do      <- from openICPSR (~30 figures and tables)
├── Materials/             其它材料 — paper, reading notes, DID references
│   ├── AER2022-Rebel on the Canal- ….pdf
│   ├── Rebel on the Canal (AER 2022).md
│   ├── 论文模型解读与StatsPAI复现分析.md
│   ├── attachments/       figures embedded in the Obsidian note
│   └── docs/              staggered-DID command references, StatsPAI notes, working specs
└── Results/               created by master.do (not tracked by git)
```

`Program/` and `Data/` keep the author's folder names on purpose: `master.do` calls `run Program/...` and reads `Data/...` relative to the project root.

## What is NOT in this repository yet

| Path master.do expects | In this repo? |
|---|---|
| `Program/Clean/clean.do` | No |
| `Program/Analysis/*.do` (~30 figures and tables) | No |
| `Program/Adofile/spatial_HAC/` (Hsiang 2010 ado) | No (cited in `Program/Adofile/source.txt`) |
| `Data/Raw/` (shape files, GIS layers) | No |
| `Data/Final/rebellion.dta` (analysis panel) | No |

Obtain them from the official replication package on AEA **openICPSR** (project 157781) and drop them into the matching folders above. `Data/` and `Results/` contents are git-ignored (openICPSR license + file size).

## How to run

1. Download the openICPSR package and place files as in **Layout**.
2. Edit the `cd` line in `Program/master.do` — replace `D:/FullReplication` with your local project root (the folder containing `Program/` and `Data/`).
3. From Stata: `do Program/master.do`

## Reading Notes

| File | Audience | Content |
|---|---|---|
| [Rebel on the Canal (AER 2022).md](<Materials/Rebel on the Canal (AER 2022).md>) | Anyone curious about the paper | The single source of truth on the paper's content: identification, the five core models, findings, mechanisms, and a 2022–2026 modern-DID reassessment. Each claim tagged to a specific table or figure. Written as an Obsidian note (YAML frontmatter, callouts, `attachments/` figures); mirrors the copy in the author's vault. |
| [论文模型解读与StatsPAI复现分析.md](Materials/论文模型解读与StatsPAI复现分析.md) | Researchers considering reproduction | Equation-by-equation dissection of the paper + assessment of whether StatsPAI can reproduce it. |
| [source.txt](Program/Adofile/source.txt) | Anyone running `master.do` | Citation for the `spatial_HAC` user-written package (Hsiang 2010). |

## Internal working notes

`Materials/docs/superpowers/specs/` contains design specs from collaborative editing sessions. These are working notes, not part of the paper or replication package.

## License

- **Replication scripts and reading notes in this repository** are released under the [MIT License](LICENSE).
- **The paper PDF** is the property of the American Economic Association; see AER's copyright terms before redistribution.
- **The replication package** (data + auxiliary scripts + spatial_HAC ado) is governed by the AEA openICPSR license; obtain it from the official portal.
