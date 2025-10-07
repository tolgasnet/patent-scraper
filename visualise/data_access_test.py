from pathlib import Path

import pandas as pd

from visualise.data_access import PatentFile, list_patent_files, load_patent_dataframe


def test_list_patent_files_returns_sorted(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "patents_synbio_b.jsonl").write_text("{}\n", encoding="utf-8")
    (data_dir / "patents_synbio_a.jsonl").write_text("{}\n", encoding="utf-8")

    files = list_patent_files(data_dir=data_dir)

    assert [pf.display_name for pf in files] == ["a", "b"]
    assert all(isinstance(pf, PatentFile) for pf in files)


def test_list_patent_files_handles_missing_dir(tmp_path):
    data_dir = tmp_path / "missing"

    files = list_patent_files(data_dir=data_dir)

    assert files == []


def test_load_patent_dataframe_reads_jsonl(tmp_path):
    path = tmp_path / "patents_synbio_sample.jsonl"
    path.write_text('{"title": "Sample"}\n', encoding="utf-8")

    patent_file = PatentFile(path=path)
    df = load_patent_dataframe(patent_file)

    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["title"] == "Sample"
