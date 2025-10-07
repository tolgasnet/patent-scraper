from pathlib import Path

import typer

from ingest.cpc_prefixes import CPC_PREFIXES
from ingest.stream_xml import stream_and_write

INPUT_XML_SAMPLE = "data/sample.xml"
INPUT_XML_LARGE = "data/ipa251002.xml"

app = typer.Typer()

@app.command()
def version():
    typer.echo("0.1.0")

@app.command()
def scrape(
    start_date: str = typer.Option("20251001", "--start-date", help="Lower bound publication date (YYYYMMDD)."),
    end_date: str = typer.Option("20251002", "--end-date", help="Upper bound publication date (YYYYMMDD)."),
    input_xml: Path = typer.Option(Path(INPUT_XML_LARGE), "--input-xml", exists=True, file_okay=True, dir_okay=False, readable=True),
    output_dir: Path | None = typer.Option(None, "--output-dir", help="Directory for NDJSON output; defaults to data/"),
):
    """Scrape patent data from an XML source into NDJSON."""
    stats = stream_and_write(
        start_date=start_date,
        end_date=end_date,
        cpc_prefixes=CPC_PREFIXES,
        input_xml=str(input_xml),
        output_dir=output_dir,
    )
    typer.echo(stats)

if __name__ == "__main__":
    app()
