"""Behavioral checks for the deterministic stratified split."""

import pandas as pd

from src.config import CONFIRMATION_FRACTION, SEED
from src.data.prepare import make_split_indices


def test_split_is_deterministic_and_covers_every_row() -> None:
    income = pd.Series(["<=50K"] * 10 + [">50K"] * 4)

    first = make_split_indices(income, SEED, CONFIRMATION_FRACTION)
    second = make_split_indices(income, SEED, CONFIRMATION_FRACTION)

    pd.testing.assert_frame_equal(first, second)
    assert first["row_index"].tolist() == list(range(len(income)))
    assert first["partition"].value_counts().to_dict() == {
        "exploration": 11,
        "confirmation": 3,
    }


def test_split_keeps_each_income_class_in_both_partitions() -> None:
    income = pd.Series(["<=50K"] * 10 + [">50K"] * 4)

    split = make_split_indices(income)
    assigned = pd.DataFrame({"income": income, "partition": split["partition"]})
    counts = assigned.groupby(["income", "partition"]).size()

    assert counts["<=50K", "confirmation"] == 2
    assert counts[">50K", "confirmation"] == 1
    assert counts["<=50K", "exploration"] == 8
    assert counts[">50K", "exploration"] == 3
