import typer
from stream_xml import stream_and_write
from cpc_prefixes import CPC_PREFIXES

INPUT_XML_SAMPLE = "data/sample.xml"
INPUT_XML_LARGE = "data/ipa251002.xml"

app = typer.Typer()

@app.command()
def version():
    typer.echo("0.1.0")

@app.command()
def scrape():
    """Example command: scrape patent data."""
    stats = stream_and_write(start_date="20251001", end_date="20251002", cpc_prefixes=CPC_PREFIXES, input_xml=INPUT_XML_LARGE)
    typer.echo(stats)

if __name__ == "__main__":
    app()