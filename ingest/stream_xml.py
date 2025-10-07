"""
Streaming runner (no CLI; use from your own Typer app):
- Assumes fixed input XML path (no archives).
- Writes NDJSON to a conventional filename using the provided date range.
- Emits only {"title", "cpc": [...] } per match.
"""

from pathlib import Path
from typing import Dict, Iterator, List, Optional
import json
from lxml import etree as ET
from ingest.patent_xml import PatentApplication

# ---- Conventions / constants ----
OUTPUT_DIR: Path = Path("data")  # NDJSON directory

def _iter_multi_xml_docs(path: Path) -> Iterator[bytes]:
    """
    Yield each concatenated XML document by splitting on XML declarations.
    Works with USPTO multi-XML where each application is a full XML doc.
    """
    with open(path, "rb") as f:
        buf = []
        for line in f:
            if line.lstrip().startswith(b"<?xml"):
                if buf:
                    yield b"".join(buf)
                    buf = [line]
                else:
                    buf = [line]
            else:
                buf.append(line)
        if buf:
            yield b"".join(buf)

def _out_path_for(start_date: str, end_date: str, output_dir: Optional[Path] = None) -> Path:
    """
    Conventional output file:
      data/patents_syn_bio_<start>_<end>.jsonl
    """
    target_dir = output_dir or OUTPUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / f"patents_synbio_{start_date}_{end_date}.jsonl"

def stream_and_write(
    *,
    start_date: str,
    end_date: str,
    cpc_prefixes: List[str],
    input_xml: str,
    output_dir: Optional[Path] = None,
) -> Dict:
    """
    Stream the given XML file (input_xml) and write matches to a conventional NDJSON path.
    start_date/end_date are required (YYYYMMDD). No validation here.
    """
    total = 0
    matched = 0
    out_path = _out_path_for(start_date, end_date, output_dir)

    parser = ET.XMLParser(recover=True, resolve_entities=False, no_network=True, huge_tree=True)

    with open(out_path, "w", encoding="utf-8") as out:
        for doc_bytes in _iter_multi_xml_docs(Path(input_xml)):
            total += 1
            try:
                elem = ET.fromstring(doc_bytes, parser=parser)  # one <us-patent-application> per chunk
            except ET.XMLSyntaxError:
                # skip malformed chunk and continue
                continue

            app = PatentApplication(elem)

            pub_date = app.pub_date()
            if pub_date is None or pub_date < start_date or pub_date > end_date:
                continue

            if not app.matches_synbio_cpc(cpc_prefixes):
                continue

            out.write(json.dumps({"title": app.title(), "cpc": app.cpc_codes()}, ensure_ascii=False) + "\n")
            matched += 1

    stats = {
        "input_xml": input_xml,
        "output_jsonl": str(out_path),
        "total_apps": total,
        "matched_apps": matched,
    }
    return stats
