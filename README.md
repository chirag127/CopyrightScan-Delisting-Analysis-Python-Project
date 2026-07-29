# CopyrightScan-Delisting-Analysis-Python-Project

Analyzes content delisting trends from copyright infringement using Google's public web-search copyright-removals dataset.

**Live:** https://CopyrightScan-Delisting-Analysis-Python-Project.oriz.in

[![Stars](https://img.shields.io/github/stars/chirag127/CopyrightScan-Delisting-Analysis-Python-Project?style=flat-square)](https://github.com/chirag127/CopyrightScan-Delisting-Analysis-Python-Project/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](./LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)

## What it does

Downloads Google's [Transparency Report web-search copyright removals](https://storage.googleapis.com/transparencyreport/google-websearch-copyright-removals.zip) dataset and explores delisting patterns — removal-request volume, reporting organizations, and specified domains — with pandas.

## Files

| File | Purpose |
|------|---------|
| `main.py` | Downloads the dataset, unzips it, loads the CSV into a DataFrame |
| `a.ipynb` | Jupyter notebook for interactive exploration and trend analysis |

## Setup

```bash
git clone https://github.com/chirag127/CopyrightScan-Delisting-Analysis-Python-Project.git
cd CopyrightScan-Delisting-Analysis-Python-Project
pip install pandas requests
```

## Usage

Run the downloader/loader:

```bash
python main.py
```

Or open the notebook for interactive analysis:

```bash
jupyter notebook a.ipynb
```

The dataset ships as CSV files (records, requests, domains) extracted from the downloaded zip.

## License

MIT — see [LICENSE](./LICENSE).
