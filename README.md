# 07-reproducibility

Assignment 07 for [DSC 190: Tools of the Trade](https://github.com/dsc-courses/dsc190-tools-2026-sp/tree/main/assignments/07-reproducibility).

This repository builds a reproducible event-data pipeline with Python, pandas,
uv, DVC, and Marimo. The pipeline starts from a raw event log, removes invalid
records, adds derived date fields, creates analysis-ready features, and then
uses the final feature table in a Marimo report.

The DVC pipeline has three stages:

- `clean`: reads `data/raw/events.csv`, drops rows with missing required fields,
  invalid event types, invalid timestamps, or non-positive durations, and writes
  `data/clean/events.csv`.
- `transform`: reads the clean events, adds a `date` column from `timestamp`,
  and writes `data/transformed/events.csv`.
- `features`: reads the transformed events, adds `duration_minutes` and
  `weekday`, and writes `data/features/events.csv`.

Run the full pipeline with:

```bash
uv run dvc repro
```

## Repository Tree

```text
.
├── README.md                         # Project overview and usage notes
├── pyproject.toml                    # Python project metadata and dependencies
├── uv.lock                           # Locked dependency versions for uv
├── dvc.yaml                          # DVC pipeline stage definitions
├── dvc.lock                          # DVC-tracked dependency and output hashes
├── data
│   ├── raw
│   │   └── events.csv                # Original input event log
│   ├── clean
│   │   └── events.csv                # Cleaned events produced by clean.py
│   ├── transformed
│   │   └── events.csv                # Events with derived date column
│   └── features
│       └── events.csv                # Final feature table used by the report
├── notebooks
│   └── report.py                     # Marimo report with duration histogram
└── src
    └── eventflow
        ├── clean.py                  # Cleans raw event records
        ├── transform.py              # Adds date-level transformed fields
        ├── features.py               # Builds final analysis features
        └── __init__.py               # Package entry point placeholder
```

## Contents

The `src/eventflow` package contains the Python scripts used by the DVC
pipeline. Each script reads the output of the previous stage, performs one
focused transformation, and writes a CSV output under `data/`.

The `data/raw` directory contains the source dataset. The `data/clean`,
`data/transformed`, and `data/features` directories contain generated pipeline
outputs. DVC records these outputs in `dvc.lock` and ignores the generated CSVs
from normal git tracking.

The `notebooks/report.py` file is a Marimo notebook that loads
`data/features/events.csv` and displays a histogram of event durations in
minutes.
