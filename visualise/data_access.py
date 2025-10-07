from dataclasses import dataclass
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
PATENT_GLOB = "patents_*.jsonl"


@dataclass(frozen=True)
class PatentFile:
    """Metadata about a candidate NDJSON file for display."""

    path: Path

    @property
    def display_name(self) -> str:
        stem = self.path.name.replace("patents_synbio_", "")
        return stem.replace(".jsonl", "")


def list_patent_files(data_dir: Path = DATA_DIR, pattern: str = PATENT_GLOB) -> list[PatentFile]:
    """Return available NDJSON files sorted by name."""
    data_dir = Path(data_dir)
    if not data_dir.exists():
        return []
    candidates = sorted(data_dir.glob(pattern))
    return [PatentFile(path=c) for c in candidates]


def load_patent_dataframe(patent_file: PatentFile) -> pd.DataFrame:
    """Load the dataframe for the given patent file."""
    return pd.read_json(patent_file.path, lines=True)
