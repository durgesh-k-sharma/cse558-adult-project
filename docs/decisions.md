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

No final feature encoding or modeling decision has been made yet.

## Exploration and proposal question (seed 558 split)

- **Exploration rows used:** 39,073; confirmation rows were not summarized.
- **Primary proposal question:** Does the association between `education-num`
  and `income >50K` differ by sex after adjustment for age and hours-per-week?
- **Reason:** The question tests an interaction beyond the obvious marginal
  education and sex comparisons and supports explicit analysis of a sensitive
  attribute. It is associational; this observational dataset does not support
  a causal interpretation.
- **Exploratory evidence:** `>50K` rates were 11.1% for females (1,441/12,941)
  and 30.3% for males (7,908/26,132), a 19.1 percentage-point difference.
  Across education-num levels, rates ranged from 1.6% (1/64 at level 1) to
  74.5% (493/662 at level 15). These are exploration descriptions, not
  adjusted effects or confirmation results.
- **Missingness:** After trimming categorical whitespace, `?` counts in
  exploration were 2,258 for workclass, 2,267 for occupation, and 674 for
  native-country (5,199 missing-marker cells total). The proposal recommends
  explicit conversion to missing values followed by an explicit missing
  category so records are retained and missingness remains visible.
- **Duplicates:** There were 38 exact duplicate exploration rows. Retain them
  because the source has no row identifier proving they are erroneous, and
  dropping repeated census profiles would change observed frequencies.
- **Outliers and noisy values:** Retain and flag the 194 exploration rows at
  capital-gain 99,999 because this is a documented top-code; no hours-per-week
  values fell outside the documented 1–99 range (0/39,073).
- **Redundant attributes:** `education` and `education-num` mapped one-to-one
  in exploration (0 conflicting education categories and 0 conflicting
  numeric levels). The proposal recommends keeping `education-num` and
  omitting redundant `education`; omit `fnlwgt` as a personal predictor
  because it is a census sampling weight. These are candidate feature choices,
  not yet applied to an encoded matrix.
- **Candidate size-floor check:** With seven nominal predictors one-hot encoded
  (including explicit `?` categories) and five numeric/ordinal predictors, the
  candidate matrix has 91 columns. On exploration, 39,073 × 91 = 3,555,643
  cells, above the 3,000,000 floor. This calculation does not create or approve
  an encoding scheme.
- **Primary test proposal:** Logistic regression with one education-num-by-sex
  interaction; compare nested models by a one-degree-of-freedom likelihood
  ratio test. Check independent observations, convergence, sparse cells, and
  continuous-term logit linearity; compare with a categorical education-by-sex
  interaction model (15 degrees of freedom) as a less constrained alternative.
  No correction is needed for the single primary test; apply Holm if additional
  confirmatory tests are added.

The exploration figure generator is `src/analysis/explore.py`; run it with
`uv run python -m src.analysis.explore`. It writes two PDF figures under
`reports/figures/` from exploration rows. The completed proposal source is
`docs/proposal.tex`; group name, member details, and TA mentor remain for the
user to fill. The proposed encoding has not been applied to the data pipeline.
