from pathlib import Path
import json

from ingest import stream_xml


def test_stream_and_write_filters_and_writes(tmp_path):
    sample_xml = Path("data/sample.xml").resolve()
    assert sample_xml.exists(), "Sample XML fixture is missing"

    output_dir = tmp_path / "out"
    stats = stream_xml.stream_and_write(
        start_date="20251001",
        end_date="20251002",
        cpc_prefixes=["A01B"],
        input_xml=str(sample_xml),
        output_dir=output_dir,
    )

    assert stats["input_xml"] == str(sample_xml)
    assert Path(stats["output_jsonl"]).parent == output_dir
    assert stats["matched_apps"] > 0
    assert stats["matched_apps"] <= stats["total_apps"]

    output_file = Path(stats["output_jsonl"])
    assert output_file.exists()

    lines = output_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == stats["matched_apps"]
    first = json.loads(lines[0])
    assert "title" in first
    assert "cpc" in first
