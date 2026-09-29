# Course Project — Guidelines

<!-- CSE558 Data Science | Monsoon 2026 | Project Guidelines 1 / 2 -->

## About Project

Every project starts with data collection, followed by data preparation. It then has two required parts — your group must do both.

- **Statistical inference.** Draw inferences from your data using statistical analysis such as hypothesis testing. Know which tests you are using and why they fit your problem, and compare them comprehensively against other tests.
- **Scalable training.** Train and validate ML models (regression, classification, clustering, decision trees), then make training tractable at your data's scale by summarising the data, the model, or both. Know which model you are using and why, and compare it comprehensively against others.

Detailed instructions for these two parts will follow. Right now, do Steps 1 and start working on step 2.

## Step 1 — Form your group

1. Form a group of five members or fewer.
2. Choose a group name.
3. Exactly one member fills the form for the whole group. Enter the group name and every member's name, roll number and institute email.
4. Once, your group has been decided then fill the Google form by 1 September 2026.

Each group is given a TA mentor to ask for advice.

## Step 2 — Project proposal

Use the proposal template provided alongside these guidelines, and submit it as a PDF. The template shows a fully worked example throughout; replace it with your own.

### Get your data

- Already have a dataset? Skip to Understand and prepare. Otherwise take one from kaggle.com/datasets.
- Search for raw or uncleaned data. A pre-cleaned, competition-ready dataset defeats the purpose of the preparation phase.
- Prefer a mix of attribute types — nominal, discrete and continuous.
- Size requirement: after encoding or embedding, #samples × #features ≥ 3,000,000. Encoding/embedding is usually what gets you there. Check this before you commit — a dataset that cannot reach the floor will have to be replaced, and replacing it late is going to be costly for your grades.
- Cite where the data came from.

### Understand and prepare

- Build a data dictionary: for every attribute, its type (nominal, discrete or continuous), its unit, its range and its missingness.
- Handle missing values, outliers, noisy records, duplicates, and choose an encoding or embedding. Every step needs a stated reason; "we tried it and it worked" is not a reason.

<!-- CSE558 Data Science | Monsoon 2026 | Project Guidelines 2 / 2 -->

- Report the effect in numbers — rows, features, missingness, duplicates, before and after. Say what you lost as well as what you gained.

### Explore, then commit

- Split before you explore. Hold out a confirmation set, do all your EDA on the exploration portion, and record the split and its seed.
- Do as much EDA as you need to understand the data — not a fixed number of plots, but enough that you can defend what you ask next. Every figure gets a caption stating its takeaway, not its contents.
- List the obvious questions anyone would ask of this dataset after knowing it at high level.
- State your problem statement(s): one or two sentences each, specific to your feature set, and phrased so each could come out either way. More than one is fine — mark which is primary, and keep the list short, because every extra statement is another test in Step 3 and another comparison to correct for. Then say why yours are not already on the obvious list.
- Correlation is not causation. If your framing has a causal flavour, say so, and say what would be needed to justify it.

### What the proposal must contain

1. Where you collected the dataset, how many rows and columns, and a few features named with their real-world meaning.
2. How you prepared the data, and why you chose those steps over the alternatives.
3. What changed after preparation, in before-and-after numbers.
4. Your exploration/confirmation split, with the seed.
5. Some captioned figures, the obvious questions, your problem statement(s) with one marked primary, and why they are not on the obvious list

### How you are graded

On how far you dug into the data and what you could infer from it — not on model accuracy. Three standards apply to everything you submit:

- **Justified** — every choice has a stated reason.
- **Quantified** — every claim comes with a number, not an adjective.
- **Reproducible** — a TA can re-run your work and get the same result.

All the best!
