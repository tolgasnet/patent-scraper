from pathlib import Path

import pytest
from lxml import etree as ET

from ingest.patent_xml import PatentApplication
from ingest.stream_xml import _iter_multi_xml_docs


@pytest.fixture(scope="module")
def sample_apps() -> list[PatentApplication]:
    sample_xml = Path("data/sample.xml").resolve()
    assert sample_xml.exists(), "Sample XML fixture is missing"

    apps: list[PatentApplication] = []
    for chunk in _iter_multi_xml_docs(sample_xml):
        elem = ET.fromstring(chunk)
        apps.append(PatentApplication(elem))
    return apps


def test_cpc_and_metadata_extraction(sample_apps):
    first = sample_apps[0]
    assert first.pub_date() == "20251002"
    assert first.title() == "SPRING ACTION SHOVEL"
    assert first.cpc_codes() == ["A01B1/02", "B25G1/01"]


def test_matches_synbio_cpc_normalises_prefixes(sample_apps):
    app = sample_apps[0]
    assert app.matches_synbio_cpc(["a01 b"]) is True
    assert app.matches_synbio_cpc(["C12N"]) is False
    assert app.matches_synbio_cpc([]) is False


def test_handles_multiple_applications(sample_apps):
    assert len(sample_apps) == 2
    titles = [app.title() for app in sample_apps]
    assert "SPRING ACTION SHOVEL" in titles
    assert "AGRICULTURAL IMPLEMENT WITH VISION SENSORS" in titles
