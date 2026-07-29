# Copyright Removals Analysis

[![Stars](https://img.shields.io/github/stars/chirag127/copyright-removals-analysis?style=flat-square)](https://github.com/chirag127/copyright-removals-analysis/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](./LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)

Data analysis of Google's public Web Search copyright-removal (DMCA delisting) transparency dataset.

**Live:** https://copyright-removals-analysis.oriz.in

---

## What it analyzes

Google's [Transparency Report](https://transparencyreport.google.com/copyright/overview) publishes every DMCA-style delisting request received for web search results. This project explores that dataset to answer:

1. Who files the most removal requests (copyright owners)?
2. Which intermediary agencies submit on their behalf?
3. Which domains are most targeted?
4. How has request volume trended year-over-year?
5. What fraction of requested URLs actually get deindexed?

## Key findings

Run the notebook or CLI to generate findings from the latest dataset. Example outputs (2023 snapshot):

- Several hundred million URLs have been requested for removal since records began.
- A small set of music/film industry organisations accounts for the majority of requests.
- File-sharing and streaming aggregator domains dominate the most-targeted list.
- Request volume peaked around 2016–2017 and has declined as platforms improved DMCA tooling.
- Removal rates exceed 90% for most filing organisations.

## Project structure

```
notebooks/copyright-removals-analysis.ipynb   interactive analysis
src/copyright_removals/
  download.py                                 fetch + extract + cache dataset
  analyze.py                                  headless CLI analysis + chart output
data/                                         gitignored — downloaded CSVs
output/                                       gitignored — generated charts
requirements.txt
docs/index.html                               landing page (GitHub Pages)
```

## How to run

### Notebook

```bash
git clone https://github.com/chirag127/copyright-removals-analysis.git
cd copyright-removals-analysis
pip install -r requirements.txt
jupyter notebook notebooks/copyright-removals-analysis.ipynb
```

Run all cells — cell 2 downloads the dataset on first run (~80 MB).

### CLI

```bash
pip install -r requirements.txt
python -m copyright_removals.analyze --download --report
# Charts saved to output/; findings printed to stdout
```

## Data source

Google Transparency Report — Web Search Copyright Removals  
Dataset URL: https://storage.googleapis.com/transparencyreport/google-websearch-copyright-removals.zip  
Data is public and published by Google.

## License

MIT — see [LICENSE](./LICENSE).
