# Adult data dictionary

The dataset contains 14 predictors and the `income` target. Units and ranges
below follow the UCI documentation. Missingness is the literal string `?` in
`workclass`, `occupation`, and `native-country`; other columns have no documented
missing marker. The pipeline measured these source marker counts without
changing the raw values. A later cleaning step will convert `?` to missing data
before deciding how to handle each column.

| Attribute | Type | Unit | Documented range or values | Missingness |
|---|---|---|---|---|
| age | Discrete | Years | 17–90 in source records | None documented |
| workclass | Nominal | Category | Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked | 2,799 `?` rows |
| fnlwgt | Continuous | Census sampling weight | Positive integer; source-dependent | None documented |
| education | Nominal | Highest education category | 16 source categories | None documented |
| education-num | Discrete | Years of education | 1–16 | None documented |
| marital-status | Nominal | Category | 7 source categories | None documented |
| occupation | Nominal | Category | 14 source categories | 2,809 `?` rows |
| relationship | Nominal | Category | 6 source categories | None documented |
| race | Nominal | Category | 5 source categories | None documented |
| sex | Nominal | Category | Female, Male | None documented |
| capital-gain | Continuous | USD | 0–99,999 in source records | None documented |
| capital-loss | Continuous | USD | 0–4,356 in source records | None documented |
| hours-per-week | Continuous | Hours per week | 1–99 in source records | None documented |
| native-country | Nominal | Country | 41 source categories | 857 `?` rows |
| income | Nominal | Annual income bracket | `<=50K`, `>50K` | None documented |

The ranges above describe observed/documented source values, not validation
bounds. The first pipeline run records row, target, split, and missing-marker
counts. A later preparation step will quantify missing cells after explicitly
converting `?` to missing values.
