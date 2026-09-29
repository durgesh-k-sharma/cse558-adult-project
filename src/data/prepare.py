"""Download Adult data and create the reproducible holdout split."""

from __future__ import annotations

import hashlib
import io
import math
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import CONFIRMATION_FRACTION, SEED, SOURCE_ARCHIVE_SHA256

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
ARCHIVE_PATH = RAW_DIR / "adult.zip"
SPLIT_PATH = PROCESSED_DIR / "split_indices.parquet"
ARCHIVE_URL = "https://archive.ics.uci.edu/static/public/2/adult.zip"
UCI_COLUMNS = (
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
    "income",
)


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest for a file, reading it in fixed-size blocks."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_archive(destination: Path = ARCHIVE_PATH) -> str:
    """Fetch and validate the UCI ZIP archive if it is not already cached."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        with zipfile.ZipFile(destination) as archive:
            if archive.testzip() is not None:
                raise ValueError(f"Cached archive is corrupt: {destination}")
        digest = sha256_file(destination)
        if digest != SOURCE_ARCHIVE_SHA256:
            raise ValueError(
                f"Cached archive checksum mismatch: expected "
                f"{SOURCE_ARCHIVE_SHA256}, got {digest}"
            )
        return digest

    temporary_path = destination.with_suffix(destination.suffix + ".part")
    try:
        request = urllib.request.Request(
            ARCHIVE_URL, headers={"User-Agent": "CSE558-Adult-Project/0.1"}
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            temporary_path.write_bytes(response.read())
        with zipfile.ZipFile(temporary_path) as archive:
            if archive.testzip() is not None:
                raise ValueError("Downloaded UCI archive failed its ZIP CRC check")
        digest = sha256_file(temporary_path)
        if digest != SOURCE_ARCHIVE_SHA256:
            raise ValueError(
                f"Downloaded archive checksum mismatch: expected "
                f"{SOURCE_ARCHIVE_SHA256}, got {digest}"
            )
        temporary_path.replace(destination)
    finally:
        temporary_path.unlink(missing_ok=True)
    return digest


def load_source_tables(archive_path: Path = ARCHIVE_PATH) -> pd.DataFrame:
    """Load the official training and test source files without cleaning values."""
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        required_files = {"adult.data", "adult.test"}
        if not required_files.issubset(names):
            raise ValueError(f"UCI archive is missing {required_files - names}")

        frames = []
        for filename in ("adult.data", "adult.test"):
            frame = pd.read_csv(
                io.BytesIO(archive.read(filename)),
                names=UCI_COLUMNS,
                skipinitialspace=True,
                comment="|",
                skip_blank_lines=True,
            )
            frames.append(frame)

    data = pd.concat(frames, ignore_index=True)
    # UCI appends a period to labels in adult.test. Remove that source-format
    # difference so both files use the same two strata; no rows are filtered.
    data["income"] = data["income"].astype("string").str.strip().str.rstrip(".")
    return data


def make_split_indices(
    income: pd.Series,
    seed: int = SEED,
    confirmation_fraction: float = CONFIRMATION_FRACTION,
) -> pd.DataFrame:
    """Assign every row to a stratified exploration or confirmation partition."""
    if not 0 < confirmation_fraction < 1:
        raise ValueError("confirmation_fraction must be strictly between 0 and 1")
    if income.isna().any():
        raise ValueError("income contains missing labels; cannot stratify")

    generator = np.random.default_rng(seed)
    confirmation_indices: list[int] = []
    for label in sorted(income.unique().tolist()):
        class_indices = np.flatnonzero(income.to_numpy() == label)
        if len(class_indices) < 2:
            raise ValueError(f"income class {label!r} needs at least two rows")
        count = math.ceil(len(class_indices) * confirmation_fraction)
        confirmation_indices.extend(
            generator.choice(class_indices, size=count, replace=False).tolist()
        )

    confirmation = np.zeros(len(income), dtype=bool)
    confirmation[confirmation_indices] = True
    return pd.DataFrame(
        {
            "row_index": np.arange(len(income), dtype=np.int64),
            "partition": np.where(confirmation, "confirmation", "exploration"),
        }
    )


def prepare_dataset() -> dict[str, object]:
    """Download source data and write split indices, returning reproducibility facts."""
    archive_sha256 = download_archive()
    data = load_source_tables()
    split = make_split_indices(data["income"])

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    split.to_parquet(SPLIT_PATH, index=False)

    partition_counts = split["partition"].value_counts().to_dict()
    income_counts = (
        data.assign(partition=split["partition"])
        .groupby(["partition", "income"], observed=True)
        .size()
        .unstack(fill_value=0)
        .to_dict()
    )
    missing_marker_counts = {
        column: int(data[column].astype("string").eq("?").sum())
        for column in data.columns
        if data[column].astype("string").eq("?").any()
    }
    return {
        "archive": str(ARCHIVE_PATH.relative_to(PROJECT_ROOT)),
        "archive_sha256": archive_sha256,
        "rows": len(data),
        "features": len(data.columns) - 1,
        "income_counts": data["income"].value_counts().sort_index().to_dict(),
        "missing_marker_counts": missing_marker_counts,
        "partition_counts": partition_counts,
        "stratified_counts": income_counts,
        "split_file": str(SPLIT_PATH.relative_to(PROJECT_ROOT)),
    }


def main() -> None:
    """Run the preparation pipeline and print its observed counts."""
    result = prepare_dataset()
    print(f"Source: {result['archive']}")
    print(f"SHA-256: {result['archive_sha256']}")
    print(f"Rows: {result['rows']}, features: {result['features']}")
    print(f"Income counts: {result['income_counts']}")
    print(f"Literal '?' counts: {result['missing_marker_counts']}")
    print(f"Partition counts: {result['partition_counts']}")
    print(f"Partition by income: {result['stratified_counts']}")
    print(f"Wrote: {result['split_file']}")


if __name__ == "__main__":
    main()
