# Google Transparency Report Analysis

**Live:** https://google-transparency-report-analysis.oriz.in

[![Stars](https://img.shields.io/github/stars/chirag127/google-transparency-report-analysis?style=flat-square)](https://github.com/chirag127/google-transparency-report-analysis/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](./LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/chirag127/google-transparency-report-analysis/ci.yml?style=flat-square&label=CI)](https://github.com/chirag127/google-transparency-report-analysis/actions)
[![Pages](https://img.shields.io/badge/GH%20Pages-live-44bba4?style=flat-square)](https://google-transparency-report-analysis.oriz.in)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)

Independent data analysis and visualization of Google's complete Transparency Report.

---

## What it analyzes

8 Google Transparency Report datasets:

| Dataset | Data type |
|---|---|
| Copyright Removals (Web Search) | Bulk CSV — full programmatic analysis |
| Government Requests to Remove Content | Interactive report |
| Government Requests for User Information | Interactive report |
| HTTPS Encryption in Transit | Interactive report |
| Safe Browsing — Unsafe Sites | Interactive report |
| Email Encryption in Transit | Interactive report |
| EU Right to be Forgotten | Interactive report |
| Traffic Disruptions | Interactive report |

## Key findings

- 500M+ URLs requested for copyright removal since 2011; removal rate ~90%
- Government content-removal requests grew 10x from 2011 to 2023
- Top-1000 website HTTPS adoption: 48% (2015) to 96% (2023)
- 1M+ EU Right to be Forgotten URLs evaluated; ~46% delisted
- Phishing sites now outnumber malware sites ~10:1 in Safe Browsing data

## Project structure

```
src/gtra/
  datasets.py          registry of all 8 datasets
  download.py          fetch + cache bulk datasets
  analyze.py           per-dataset analysis, CLI
  charts.py            reusable matplotlib/seaborn helpers
  build_site_data.py   export findings as JSON to docs/data/
notebooks/
  google-transparency-report-analysis.ipynb   master notebook
docs/                  static data-viz site (GH Pages)
  assets/style.css     editorial design -- deep blue/teal palette
  assets/app.js        Chart.js + shared logic
  index.html, copyright.html, government-removals.html, ...
tests/
  test_datasets.py     registry integrity
  test_download.py     caching logic (mocked HTTP)
  test_analyze.py      chart smoke tests + JSON schema
  e2e/test_site.py     Playwright -- every page loads, charts render
.github/workflows/
  ci.yml               pytest on push
  e2e.yml              Playwright e2e
  deploy.yml           build + deploy to GH Pages
  megalinter.yml       MegaLinter auto-fix
```

## How to run

### Notebook

```bash
git clone https://github.com/chirag127/google-transparency-report-analysis.git
cd google-transparency-report-analysis
pip install -r requirements.txt
pip install -e .
jupyter notebook notebooks/google-transparency-report-analysis.ipynb
```

### CLI

```bash
pip install -r requirements.txt && pip install -e .

# Download + analyze copyright dataset
python -m gtra.analyze --dataset copyright --download --report

# All datasets (stubs for non-bulk)
python -m gtra.analyze --dataset all --report

# Export JSON for the site
python -m gtra.build_site_data
```

### Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ --ignore=tests/e2e -v

# E2E (serve docs/ first)
cd docs && python -m http.server 8080 &
pytest tests/e2e/ -v
```

## Data sources

All data from Google's official [Transparency Report](https://transparencyreport.google.com). Google transparency data is public. No license restrictions stated; subject to Google ToS. This project is independent and not affiliated with Google.

| Dataset | URL |
|---|---|
| Copyright Removals | https://storage.googleapis.com/transparencyreport/google-websearch-copyright-removals.zip |
| Government Removals | https://transparencyreport.google.com/government-removals/overview |
| User Data | https://transparencyreport.google.com/user-data/overview |
| HTTPS | https://transparencyreport.google.com/https/overview |
| Safe Browsing | https://transparencyreport.google.com/safe-browsing/overview |
| Email Encryption | https://transparencyreport.google.com/safer-email/overview |
| EU Privacy | https://transparencyreport.google.com/eu-privacy/overview |
| Traffic Disruptions | https://transparencyreport.google.com/traffic/overview |

## License

MIT -- see [LICENSE](./LICENSE).
