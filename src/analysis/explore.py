"""Generate proposal figures from the Adult exploration partition."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data.prepare import PROJECT_ROOT, SPLIT_PATH, load_source_tables

FIGURE_DIR = PROJECT_ROOT / "reports" / "figures"


def load_exploration_data() -> pd.DataFrame:
    """Load the rows assigned to exploration and normalize source strings."""
    split = pd.read_parquet(SPLIT_PATH)
    exploration_indices = split.loc[
        split["partition"].eq("exploration"), "row_index"
    ].to_numpy()
    source = load_source_tables()
    exploration = source.iloc[exploration_indices].copy()
    for column in exploration.select_dtypes(include=["object", "string"]):
        exploration[column] = exploration[column].astype("string").str.strip()
    exploration["income"] = exploration["income"].str.rstrip(".")
    return exploration


def _pdf_escape(value: str) -> str:
    """Escape a string for a PDF text operator."""
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _write_pdf_bar_chart(
    path: Path,
    title: str,
    labels: list[str],
    values: list[float],
    x_label: str,
) -> None:
    """Write a compact vector PDF bar chart without external dependencies."""
    width, height = 720, 420
    left, right, top, bottom = 72, 24, 54, 78
    chart_width = width - left - right
    chart_height = height - top - bottom
    bar_gap = chart_width / len(labels)
    bar_width = min(38.0, bar_gap * 0.62)
    commands = ["1 1 1 rg", f"0 0 {width} {height} re f"]

    def text(x: float, y: float, size: float, value: str) -> str:
        return f"BT /F1 {size:g} Tf {x:.2f} {y:.2f} Td ({_pdf_escape(value)}) Tj ET"

    commands.append(text(width / 2 - len(title) * 4.2, height - 30, 15, title))
    for tick in range(0, 101, 20):
        y = bottom + chart_height * tick / 100
        commands.extend(
            [
                "0.84 0.87 0.91 RG 0.5 w",
                f"{left} {y:.2f} m {width - right} {y:.2f} l S",
                "0.20 0.25 0.31 rg",
                text(left - 38, y - 3, 9, f"{tick}%"),
            ]
        )
    for index, (label, value) in enumerate(zip(labels, values, strict=True)):
        center = left + bar_gap * (index + 0.5)
        bar_height = chart_height * value
        y = bottom + chart_height - bar_height
        commands.extend(
            [
                "0.20 0.48 0.72 rg",
                (
                    f"{center - bar_width / 2:.2f} {bottom:.2f} {bar_width:.2f} "
                    f"{bar_height:.2f} re f"
                ),
                "0.12 0.16 0.22 rg",
                text(center - 12, y + 6, 9, f"{value:.1%}"),
                text(center - len(label) * 2.5, bottom - 18, 9, label),
            ]
        )
    commands.extend(
        [
            "0.12 0.16 0.22 rg",
            text(width / 2 - len(x_label) * 3, 24, 10, x_label),
            "BT /F1 10 Tf 0 1 -1 0 18 155 Tm (Share earning above $50K) Tj ET",
        ]
    )
    stream = ("\n".join(commands) + "\n").encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
            "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
        + stream
        + b"endstream",
    ]
    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for object_number, body in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{object_number} 0 obj\n".encode("ascii"))
        output.extend(body)
        output.extend(b"\nendobj\n")
    xref_offset = len(output)
    output.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(output)


def generate_figures() -> dict[str, object]:
    """Create both captioned proposal figures using exploration rows only."""
    data = load_exploration_data()
    income_by_sex = pd.crosstab(data["sex"], data["income"], normalize="index")
    education_counts = pd.crosstab(data["education-num"], data["income"])
    education_rates = education_counts.div(education_counts.sum(axis=1), axis=0)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    _write_pdf_bar_chart(
        FIGURE_DIR / "income_by_sex.pdf",
        "Exploration: income above $50K by sex",
        [str(value) for value in income_by_sex.index],
        [float(income_by_sex.loc[key].get(">50K", 0.0)) for key in income_by_sex.index],
        "Sex",
    )
    _write_pdf_bar_chart(
        FIGURE_DIR / "income_by_education_num.pdf",
        "Exploration: income above $50K by education-num",
        [str(value) for value in education_rates.index],
        [
            float(education_rates.loc[key].get(">50K", 0.0))
            for key in education_rates.index
        ],
        "Education-num",
    )
    return {
        "exploration_rows": len(data),
        "income_by_sex": {
            str(key): {
                "n": int(pd.crosstab(data["sex"], data["income"]).loc[key].sum()),
                "rate_gt_50k": float(income_by_sex.loc[key].get(">50K", 0.0)),
            }
            for key in income_by_sex.index
        },
        "income_by_education_num": {
            str(key): float(education_rates.loc[key].get(">50K", 0.0))
            for key in education_rates.index
        },
    }


def main() -> None:
    """Generate the proposal PDFs and print their exploration sample size."""
    summary = generate_figures()
    print(f"Exploration rows: {summary['exploration_rows']}")
    print(f"Figures: {FIGURE_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
