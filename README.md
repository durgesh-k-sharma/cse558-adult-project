# CSE558 Adult dataset project

Reproducible analysis of the UCI Adult (Census Income) dataset for CSE558.
The project focuses on data understanding and inference, with a later scalable
modeling phase.

## Prepare the dataset

Install the pinned environment and create the raw archive and split indices:

```bash
uv sync
uv run python -m src.data.prepare
```

The command downloads the UCI archive only when it is absent from `data/raw/`,
checks its ZIP integrity and recorded SHA-256, reads the source tables, and
writes a deterministic stratified exploration/confirmation split to
`data/processed/split_indices.parquet`. It reports the archive SHA-256 and split
counts. The raw archive is not modified by the pipeline.

The split seed, ratio, and reason are recorded in `docs/decisions.md`. Use only
exploration rows for EDA. Do not inspect confirmation rows until hypotheses
have been fixed.

## Explore and draft the proposal

After preparing the split, regenerate the exploration-only PDF figures used in
the proposal with:

```bash
uv run python -m src.analysis.explore
```

The command writes `reports/figures/income_by_sex.pdf` and
`reports/figures/income_by_education_num.pdf`. Both figures use exploration
rows only.

## Development checks

```bash
uv run ruff check .
uv run pytest -q
```

See `docs/project_guidelines.md` for the course requirements.
