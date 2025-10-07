# 🧬 Patent Scraper MVP

Minimal Streamlit + Typer project for scraping synthetic-biology patents, storing them as NDJSON, and reviewing them via a lightweight UI.

Companion guide: see [DESIGN.md](DESIGN.md) for context on core architecture and trade-offs.

## Project Layout
- `ingest/` – Typer CLI (`ingest/cli.py`) and helpers for streaming USPTO XML into `data/patents_synbio_*.jsonl`
- `visualise/` – Streamlit app (`visualise/app.py`) and supporting modules for filtering and browsing
- `data/` – Sample USPTO XML (`sample.xml`) plus generated/expected JSONL outputs
- `Makefile` – Convenience commands for scraping, running the UI, and executing tests

## Prerequisites
- Python 3.11+ (managed via Poetry)
- Poetry 1.8+

Install Poetry (macOS example):
```bash
brew install poetry
```

## Setup
Install dependencies:
```bash
poetry install
```

Optional: open a shell within the virtualenv
```bash
poetry env activate
```

## Running the Scraper (weekly job)
Generate a fresh NDJSON dataset (defaults to `data/ipa251002.xml`):
```bash
make run-cli
```
By default this uses the included `data/sample.xml` (small example dataset). If you want to test with a larger file, download the latest “Patent Application Full-text Data (No Images)” (~200 MB ZIP) from https://data.uspto.gov/bulkdata/datasets, extract the XML into the `data/` folder, and update `INPUT_XML_LARGE` in `ingest/cli.py` to point to the new filename.

Version-controlled JSONL outputs (`data/patents_synbio_*.jsonl`) ship with the repo, so you only need the large download if you want to rerun the ingest yourself.

For the MVP, treat this as the weekly cron/automation entrypoint. You can override the input/output paths:
```bash
poetry run python ingest/cli.py scrape \
    --start-date 20251001 \
    --end-date 20251002 \
    --input-xml data/sample.xml \
    --output-dir data/
```
Schedule the command (e.g. cron, GitHub Actions) to run once a week.

## Running the UI
Launch the Streamlit dashboard:
```bash
make run-ui
```
This sets `PYTHONPATH=.`, so Streamlit can import `visualise.*`. Open the URL shown in the terminal to explore patents. Use the sidebar to search titles and download filtered CSVs (named `filtered_patents.csv`).

## Tests
Execute the full test suite:
```bash
make test
```
This runs pytest across CLI, ingestion, and Streamlit helper modules. All tests pass against the sample data.

## Data Schema & Assumptions
Each JSONL record emitted by `stream_and_write` looks like:
```json
{"title": "Some Patent", "cpc": ["A01B1/02", "B25G1/01"]}
```
- `title`: string, invention title pulled from the patent application
- `cpc`: list of normalized CPC classification codes
- Filtered to pub dates within `[start_date, end_date]` and CPC prefixes in `ingest/cpc_prefixes.py`

The visualiser consumes the JSONL files as-is; engineers can reuse them downstream (CRM, analytics).

## CSV Exports
The UI offers a “Export CSV” button. Click to download the current filtered subset as `filtered_patents.csv`. The file is streamed directly to the browser (no server-side persistence). Large datasets may take a moment to generate; if performance becomes an issue, consider batching or limiting the page size.

## Next Steps
- Automate the weekly scrape via cron/GitHub Actions
- Extend the dataset schema (inventors, assignees, etc.)
- Optionally expose an API once internal workflows stabilize
