"""Google Copyright Removals — headless analysis CLI.

Usage:
    python -m copyright_removals.analyze --download --report
"""

import argparse
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")

from .download import DATA_DIR, download_dataset

OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"
SNS_THEME = {"style": "darkgrid", "palette": "muted"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_data(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Load all CSVs from data_dir into a dict keyed by stem."""
    csvs = list(data_dir.glob("*.csv"))
    if not csvs:
        raise FileNotFoundError(f"No CSVs in {data_dir}. Run with --download first.")
    frames = {}
    for p in csvs:
        try:
            frames[p.stem] = pd.read_csv(p, low_memory=False)
        except Exception as exc:
            print(f"  Warning: could not load {p.name}: {exc}")
    return frames


def _save(fig: plt.Figure, name: str, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    path = out / name
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Analysis functions (each returns a list of finding strings)
# ---------------------------------------------------------------------------


def analyse_requests(df: pd.DataFrame, out: Path) -> list[str]:
    findings = []
    print("\nColumns:", df.columns.tolist())
    print(df.shape)

    # Normalise column names: lowercase, strip, replace spaces
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # --- date parsing ---
    date_col = next((c for c in df.columns if "date" in c), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col])
        df["year"] = df[date_col].dt.year
        df["month"] = df[date_col].dt.to_period("M")

    # --- top copyright owners ---
    owner_col = next(
        (c for c in df.columns if "copyright_owner" in c or "owner" in c), None
    )
    if owner_col:
        top_owners = df[owner_col].value_counts().head(15)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.set_theme(**SNS_THEME)
        top_owners.sort_values().plot.barh(ax=ax, color=sns.color_palette("muted")[0])
        ax.set_title("Top 15 Copyright Owners by Request Count")
        ax.set_xlabel("Requests")
        _save(fig, "top_copyright_owners.png", out)
        top3 = top_owners.head(3).index.tolist()
        findings.append(f"Top 3 copyright owners: {', '.join(str(x) for x in top3)}")

    # --- top reporting organisations ---
    org_col = next(
        (
            c
            for c in df.columns
            if "reporting" in c or "requester" in c or "reporter" in c
        ),
        None,
    )
    if org_col:
        top_orgs = df[org_col].value_counts().head(15)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.set_theme(**SNS_THEME)
        top_orgs.sort_values().plot.barh(ax=ax, color=sns.color_palette("muted")[1])
        ax.set_title("Top 15 Reporting Organizations")
        ax.set_xlabel("Requests")
        _save(fig, "top_reporting_orgs.png", out)
        top3 = top_orgs.head(3).index.tolist()
        findings.append(f"Top 3 reporting orgs: {', '.join(str(x) for x in top3)}")

    # --- most targeted domains ---
    domain_col = next((c for c in df.columns if "domain" in c), None)
    if domain_col:
        top_domains = df[domain_col].value_counts().head(20)
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.set_theme(**SNS_THEME)
        top_domains.sort_values().plot.barh(ax=ax, color=sns.color_palette("muted")[2])
        ax.set_title("Top 20 Most-Targeted Domains")
        ax.set_xlabel("Requests")
        _save(fig, "top_targeted_domains.png", out)
        top3 = top_domains.head(3).index.tolist()
        findings.append(f"Most targeted domains: {', '.join(str(x) for x in top3)}")

    # --- trends over time ---
    if date_col and "year" in df.columns:
        yearly = df.groupby("year").size()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.set_theme(**SNS_THEME)
        yearly.plot(ax=ax, marker="o", color=sns.color_palette("muted")[3])
        ax.set_title("Copyright Removal Requests per Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Requests")
        _save(fig, "requests_per_year.png", out)
        peak_year = int(yearly.idxmax())
        findings.append(
            f"Peak year for removal requests: {peak_year} ({int(yearly.max()):,} requests)"
        )

    # --- URLs removed vs requested ---
    url_req_col = next(
        (c for c in df.columns if "urls_requested" in c or "requested_to_remove" in c),
        None,
    )
    url_rem_col = next(
        (c for c in df.columns if "urls_removed" in c or "actually_removed" in c), None
    )
    if url_req_col and url_rem_col:
        df[url_req_col] = pd.to_numeric(df[url_req_col], errors="coerce")
        df[url_rem_col] = pd.to_numeric(df[url_rem_col], errors="coerce")
        valid = df[[url_req_col, url_rem_col]].dropna()
        if not valid.empty:
            total_req = int(valid[url_req_col].sum())
            total_rem = int(valid[url_rem_col].sum())
            rate = total_rem / total_req * 100 if total_req else 0
            findings.append(
                f"Overall removal rate: {rate:.1f}% "
                f"({total_rem:,} removed of {total_req:,} requested)"
            )

            # scatter sample
            sample = valid.sample(min(5000, len(valid)), random_state=42)
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.set_theme(**SNS_THEME)
            ax.scatter(
                sample[url_req_col],
                sample[url_rem_col],
                alpha=0.3,
                s=10,
                color=sns.color_palette("muted")[4],
            )
            ax.set_title("URLs Requested vs Removed (sample)")
            ax.set_xlabel("Requested")
            ax.set_ylabel("Removed")
            _save(fig, "requested_vs_removed.png", out)

    total = len(df)
    findings.insert(0, f"Total records: {total:,}")
    if date_col:
        date_range = f"{df[date_col].min().date()} to {df[date_col].max().date()}"
        findings.insert(1, f"Date range: {date_range}")

    return findings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Copyright Removals Analysis")
    parser.add_argument(
        "--download", action="store_true", help="Download dataset first"
    )
    parser.add_argument(
        "--report", action="store_true", help="Run analysis + save charts"
    )
    parser.add_argument(
        "--data-dir", default=str(DATA_DIR), help="Path to data directory"
    )
    parser.add_argument(
        "--output-dir", default=str(OUTPUT_DIR), help="Path to output directory"
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.output_dir)

    if args.download:
        download_dataset(data_dir)

    if args.report:
        frames = _load_data(data_dir)
        all_findings: list[str] = []

        for stem, df in frames.items():
            print(f"\n=== {stem} ===")
            findings = analyse_requests(df, out_dir)
            all_findings.extend(findings)

        print("\n=== KEY FINDINGS ===")
        for i, f in enumerate(all_findings, 1):
            print(f"  {i}. {f}")


if __name__ == "__main__":
    main()
