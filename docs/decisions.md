# Decisions

## Initial source and exploration/confirmation split

- **Dataset:** UCI Adult (Census Income), UCI dataset 2, accessed from the
  official archive at <https://archive.ics.uci.edu/static/public/2/adult.zip>.
- **Split:** 80% exploration and 20% confirmation, stratified by `income`.
- **Seed:** 558, defined once in `src/config.py`.
- **Reason:** Reserving a confirmation sample before EDA reduces the risk of
  choosing hypotheses after seeing their confirmation results. Stratification
  keeps both income classes represented at similar proportions in each part.
- **Assignment rule:** Within each income class, select
  `ceil(class_rows * 0.20)` rows for confirmation using NumPy's
  `default_rng(SEED)`. The resulting total may differ slightly from exactly
  20% because each class is rounded up independently.
- **Source labels:** `adult.test` adds a trailing period to income labels.
  `src/data/prepare.py` removes only that punctuation so the two source files
  share the same target labels. It does not remove rows or clean predictors.
- **Observed source size:** 48,842 rows and 14 predictors, with 37,155 rows in
  `<=50K` and 11,687 in `>50K`.
- **Observed split:** 39,073 exploration rows and 9,769 confirmation rows.
  Confirmation counts are 7,431 in `<=50K` and 2,338 in `>50K`.
- **Archive checksum:** SHA-256
  `7537312dd56c2b98035880805ce99e68183a30ee468aa5329d6df0fbb3cc21bb`.
- **Missing markers, before cleaning:** 2,799 in `workclass`, 2,809 in
  `occupation`, and 857 in `native-country`. The literal `?` values remain
  unchanged in the raw input. These counts are not a decision to drop, impute,
  or retain them as a final modeling category.

The confirmation row indices are stored at
`data/processed/split_indices.parquet`. All EDA must load only rows assigned to
`exploration`; do not inspect confirmation rows until hypotheses are fixed.

No missing-value, duplicate, outlier, feature encoding, or modeling decisions
have been made yet.
