import ast
from pathlib import Path

from typer.testing import CliRunner

from ingest.cli import app

runner = CliRunner()


def test_scrape_happy_path_with_sample_xml(tmp_path):
    sample_xml = Path("data/sample.xml").resolve()
    assert sample_xml.exists(), "Sample XML fixture is missing"

    result = runner.invoke(
        app,
        [
            "scrape",
            "--input-xml",
            str(sample_xml),
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0, result.output

    stats = ast.literal_eval(result.output.strip())
    assert stats["input_xml"] == str(sample_xml)
    output_path = Path(stats["output_jsonl"])  # should be inside tmp_path
    assert output_path.exists()
    assert output_path.parent == tmp_path
    assert stats["total_apps"] >= stats["matched_apps"] >= 0
