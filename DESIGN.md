# Design Choices

Companion guide: see [README.md](README.md) for setup, commands, and workflow details.

## Ingestion Pipeline
- **Typer CLI for scraping**: Simple command-line entrypoint that’s easy to run manually or drop into cron/automation later.
- **Text-only USPTO feeds**: Stick to the "no images" archives—they’re about 100× smaller yet carry all the text needed for filtering and reporting.
- **Streaming XML parsing**: `_iter_multi_xml_docs` feeds each application chunk to lxml so we never load the full USPTO file; the parser uses `recover`/`no_network` to ride through messy XML safely.
- **Efficient ingest loop**: Pub-date and CPC checks happen before serialization, and `_norm` standardises codes so prefix matching is cheap and consistent.
- **NDJSON output**: Plain text files that stream to disk, load with `pandas.read_json(lines=True)`, and slot easily into downstream pipelines.

## Data Model
- **JSONL schema**: Each record carries `title` and `cpc` list, leaning on the same structure for both ingestion and UI.
- **Curated CPC list**: Start with the core synthetic-biology prefixes defined in [`ingest/cpc_prefixes.py`](ingest/cpc_prefixes.py) and include both inventive and additional assignments so cross-disciplinary work isn’t missed, while keeping the list easy to grow later.

## Dashboard & UX
- **Single-field search focus**: The sidebar search locks onto one high-signal field (title for now) to keep the UI simple for non-technical teammates.
- **Session-backed pagination**: A tiny state helper slices DataFrames without extra libraries, so big result sets stay responsive.
- **Open internal access**: No login in the MVP; trusted teammates reach the app directly, with authentication ready to add if policy changes.

## Testing & Tooling
- **Client-friendly exports**: CSV download names and formats match what non-technical teammates expect.
- **Manual weekly run**: The `scrape` command documents the cadence; automation can follow once the team wants a scheduler.
- **Unit test coverage**: Pytest suites cover ingestion, XML parsing, and UI helpers to prevent regressions as filters evolve.

## Technical Consumption
- **Batch file convention**: Each scrape writes `data/patents_synbio_<start>_<end>.jsonl`, ready to push to shared storage like Amazon S3 or Google Cloud Storage for engineers and other pipelines.
- **No API in MVP**: Engineers consume the JSONL drops directly; an API can be layered on later if workflows demand it.

## Non-technical Consumption
- **Streamlit dashboard**: Internal users browse the latest file via the built-in UI without needing external BI tools.
- **On-demand CSV download**: The “Export CSV” button streams the current filter as `filtered_patents.csv`, giving investors a quick takeaway without extra tooling.
