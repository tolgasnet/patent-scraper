# Design Choices

Companion guide: see [README.md](README.md) for setup, commands, and workflow details.

## Ingestion Pipeline
- **Typer CLI for scraping** – Quick command you can run by hand or pop into cron when automation makes sense.
- **Text-only USPTO feeds** – Grab the “no images” bundles: they’re roughly 100× smaller and still carry the text we care about.
- **Streaming XML parsing** – `_iter_multi_xml_docs` hands one application at a time to lxml, so we never pull the whole USPTO file into memory. `recover`/`no_network` keeps the parser steady even when the XML is quirky.
- **Efficient ingest loop** – We check pub dates and CPC prefixes before writing anything, and `_norm` keeps codes tidy so prefix matches stay quick.
- **NDJSON output** – One patent per line, easy to stream to disk and just as easy to load back with `pandas.read_json(lines=True)`.

## Data Model
- **JSONL schema** – Each record keeps the title plus its CPC list, so ingestion and UI work off the same simple shape.
- **CPC list** – We start with the core synthetic-biology prefixes in [ingest/cpc_prefixes.py](ingest/cpc_prefixes.py) and include both inventive and additional assignments so cross-disciplinary work still shows up. The list stays small and easy to tweak later.

## Dashboard & UX
- **Single-field search** – The sidebar sticks to one high-signal field (title for now), keeping things uncluttered for non-technical teammates.
- **Pagination** – A tiny state helper slices the table so big result sets stay responsive without extra libraries.
- **No Login** – No login in the MVP; trusted teammates visit the app directly, and we can bolt on auth later if policy changes.

## Testing & Tooling
- **Client-friendly exports** – CSV downloads keep familiar filenames and columns, so investors know what they’re looking at right away.
- **Manual weekly run** – The `scrape` command documents the cadence; we can automate it later when the team wants a scheduler.

## Technical Consumption
- **Batch file convention** – Each run emits `data/patents_synbio_<start>_<end>.jsonl`, ready to stash in S3 or Google Cloud Storage so other pipelines can pick it up.
- **No API in MVP** – Engineers just grab the JSONL drops for now. If we see the need, an API can sit on top later.

## Non-technical Consumption
- **Streamlit dashboard** – Internal teammates browse the latest batch through the built-in UI—no extra BI tools required.
- **On-demand CSV download** – The “Export CSV” button streams the current slice as `filtered_patents.csv`, giving investors a quick takeaway with one click.
