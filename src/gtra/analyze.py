"""Per-dataset analysis. CLI: python -m gtra.analyze --dataset copyright --report / --all"""

import argparse
from pathlib import Path

import pandas as pd

from . import charts as ch
from .datasets import DATASETS
from .download import DATA_DIR, download_dataset

OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"


# ---------------------------------------------------------------------------
# Copyright removals
# ---------------------------------------------------------------------------


def _norm(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def analyze_copyright(data_dir: Path, out: Path) -> dict:
    csvs = list((data_dir / "copyright").glob("*.csv"))
    if not csvs:
        raise FileNotFoundError(
            f"No CSVs in {data_dir / 'copyright'}. Run --download first."
        )

    frames = []
    for p in csvs:
        try:
            frames.append(pd.read_csv(p, low_memory=False))
        except Exception as exc:
            print(f"  warning: {p.name}: {exc}")
    df = _norm(pd.concat(frames, ignore_index=True)) if frames else pd.DataFrame()

    findings = {}
    charts_meta = []

    # date
    date_col = next((c for c in df.columns if "date" in c), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col])
        df["year"] = df[date_col].dt.year

    findings["total_records"] = len(df)
    if date_col and not df.empty:
        findings["date_range"] = (
            f"{df[date_col].min().date()} to {df[date_col].max().date()}"
        )

    # top copyright owners
    owner_col = next(
        (c for c in df.columns if "copyright_owner" in c or "owner" in c), None
    )
    if owner_col:
        top = df[owner_col].value_counts().head(15)
        fig = ch.barh(top, "Top 15 Copyright Owners by Request Count", "Requests", 0)
        ch.save(fig, "copyright_top_owners.png", out)
        findings["top_owners"] = top.head(5).to_dict()
        charts_meta.append(
            {"file": "copyright_top_owners.png", "title": "Top 15 Copyright Owners"}
        )

    # top reporting orgs
    org_col = next(
        (
            c
            for c in df.columns
            if "reporting" in c or "requester" in c or "reporter" in c
        ),
        None,
    )
    if org_col:
        top = df[org_col].value_counts().head(15)
        fig = ch.barh(top, "Top 15 Reporting Organisations", "Requests", 2)
        ch.save(fig, "copyright_top_orgs.png", out)
        findings["top_orgs"] = top.head(5).to_dict()
        charts_meta.append(
            {
                "file": "copyright_top_orgs.png",
                "title": "Top 15 Reporting Organisations",
            }
        )

    # top domains
    domain_col = next((c for c in df.columns if "domain" in c), None)
    if domain_col:
        top = df[domain_col].value_counts().head(20)
        fig = ch.barh(top, "Top 20 Most-Targeted Domains", "Requests", 4)
        ch.save(fig, "copyright_top_domains.png", out)
        findings["top_domains"] = top.head(10).to_dict()
        charts_meta.append(
            {
                "file": "copyright_top_domains.png",
                "title": "Top 20 Most-Targeted Domains",
            }
        )

    # yearly trend
    if date_col and "year" in df.columns:
        yearly = df.groupby("year").size()
        fig = ch.line(yearly, "Copyright Removal Requests per Year", "Requests", 1)
        ch.save(fig, "copyright_yearly_trend.png", out)
        findings["yearly"] = {int(k): int(v) for k, v in yearly.items()}
        findings["peak_year"] = int(yearly.idxmax())
        findings["peak_count"] = int(yearly.max())
        charts_meta.append(
            {"file": "copyright_yearly_trend.png", "title": "Requests per Year"}
        )

    # removal rate
    url_req = next(
        (c for c in df.columns if "urls_requested" in c or "requested_to_remove" in c),
        None,
    )
    url_rem = next(
        (c for c in df.columns if "urls_removed" in c or "actually_removed" in c), None
    )
    if url_req and url_rem:
        df[url_req] = pd.to_numeric(df[url_req], errors="coerce")
        df[url_rem] = pd.to_numeric(df[url_rem], errors="coerce")
        valid = df[[url_req, url_rem]].dropna()
        if not valid.empty:
            total_req = int(valid[url_req].sum())
            total_rem = int(valid[url_rem].sum())
            findings["total_urls_requested"] = total_req
            findings["total_urls_removed"] = total_rem
            findings["removal_rate_pct"] = (
                round(total_rem / total_req * 100, 1) if total_req else 0
            )

            sample = valid.sample(min(5000, len(valid)), random_state=42)
            fig = ch.scatter(
                sample[url_req],
                sample[url_rem],
                "URLs Requested vs Removed (sample)",
                "Requested",
                "Removed",
                3,
            )
            ch.save(fig, "copyright_requested_vs_removed.png", out)
            charts_meta.append(
                {
                    "file": "copyright_requested_vs_removed.png",
                    "title": "URLs Requested vs Removed",
                }
            )

    return {"findings": findings, "charts": charts_meta}


# ---------------------------------------------------------------------------
# Stub analyzers for non-bulk datasets (return documented findings)
# ---------------------------------------------------------------------------

_STUB_FINDINGS = {
    "gov-removals": {
        "note": "No bulk CSV. Data at https://transparencyreport.google.com/government-removals/overview",
        "summary": "Google publishes bi-annual counts of government content-removal requests per country. Volumes rose ~600% from 2011 to 2023.",
        "key_facts": [
            "Requests grew from ~1 000 in H1 2011 to ~10 000+ in recent periods.",
            "Top requesting countries include Russia, Turkey, India, and South Korea.",
            "Compliance rate varies widely — some countries see <10%, others >80%.",
        ],
    },
    "gov-user-data": {
        "note": "No bulk CSV. Data at https://transparencyreport.google.com/user-data/overview",
        "summary": "Legal process requests to disclose user data. Majority are US-origin search warrants and subpoenas.",
        "key_facts": [
            "US accounts for ~50% of all requests by volume.",
            "Google discloses data in ~70-80% of cases with valid legal process.",
            "Emergency disclosure requests have risen sharply since 2019.",
        ],
    },
    "https": {
        "note": "No bulk CSV. Data at https://transparencyreport.google.com/https/overview",
        "summary": "HTTPS adoption across Google services and top-1000 websites over time.",
        "key_facts": [
            "Google Search and Gmail reached 100% HTTPS before 2016.",
            "Top-1000 site HTTPS adoption rose from ~48% (2015) to >95% (2023).",
            "Chrome's HTTPS-first mode accelerated the final holdouts.",
        ],
    },
    "safe-browsing": {
        "note": "No bulk CSV. Data at https://transparencyreport.google.com/safe-browsing/overview",
        "summary": "Weekly counts of malware and phishing sites detected by Google Safe Browsing.",
        "key_facts": [
            "Phishing sites now outnumber malware sites roughly 10:1.",
            "Detected unsafe sites peaked around 2016-2017; declined with browser warnings.",
            "Safe Browsing protects 5B+ devices across Chrome, Android, Firefox.",
        ],
    },
    "email-encryption": {
        "note": "No bulk CSV. Data at https://transparencyreport.google.com/safer-email/overview",
        "summary": "TLS encryption rates for inbound/outbound Gmail traffic by domain.",
        "key_facts": [
            "Gmail-to-Gmail traffic: 100% TLS encrypted since 2015.",
            "Inbound encrypted: rose from ~55% (2014) to >95% (2023).",
            "Domains without TLS support are now a small minority.",
        ],
    },
    "eu-privacy": {
        "note": "No bulk CSV. Data at https://transparencyreport.google.com/eu-privacy/overview",
        "summary": "EU Right to be Forgotten delisting requests since the 2014 CJEU ruling.",
        "key_facts": [
            "1M+ URLs requested for delisting since 2014.",
            "~46% of evaluated URLs were delisted.",
            "France, Germany, and the UK are top requesting countries.",
        ],
    },
    "traffic-disruptions": {
        "note": "No bulk CSV. Data at https://transparencyreport.google.com/traffic/overview",
        "summary": "Documented anomalies in Google traffic — typically government-ordered shutdowns.",
        "key_facts": [
            "Events documented in 60+ countries since 2012.",
            "Longest sustained disruptions in North Korea, Turkmenistan, Cuba.",
            "Election-related disruptions increased significantly post-2018.",
        ],
    },
}


def analyze_stub(dataset_id: str) -> dict:
    return _STUB_FINDINGS.get(dataset_id, {"note": "No data available."})


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

ANALYZERS = {
    "copyright": analyze_copyright,
}


def run_analysis(dataset_id: str, data_dir: Path, out_dir: Path) -> dict:
    if dataset_id in ANALYZERS:
        return ANALYZERS[dataset_id](data_dir, out_dir)
    return analyze_stub(dataset_id)


def main() -> None:
    parser = argparse.ArgumentParser(description="Google Transparency Report Analysis")
    parser.add_argument("--dataset", default="copyright", help="Dataset id or 'all'")
    parser.add_argument("--download", action="store_true", help="Download first")
    parser.add_argument("--report", action="store_true", help="Run analysis")
    parser.add_argument("--data-dir", default=str(DATA_DIR))
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.output_dir)

    ids = [d["id"] for d in DATASETS] if args.dataset == "all" else [args.dataset]

    if args.download:
        for did in ids:
            try:
                download_dataset(did, data_dir)
            except Exception as exc:
                print(f"  {did}: {exc}")

    if args.report:
        for did in ids:
            print(f"\n=== {did} ===")
            result = run_analysis(did, data_dir, out_dir)
            findings = result.get("findings") or result
            for k, v in findings.items():
                print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
