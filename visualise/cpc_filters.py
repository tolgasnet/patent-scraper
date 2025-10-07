from collections.abc import Iterable
from typing import Any

import pandas as pd

def detect_cpc_column(frame: pd.DataFrame) -> str | None:
    """Return the CPC column name if present (case-insensitive)."""
    if "CPC" in frame.columns:
        return "CPC"
    if "cpc" in frame.columns:
        return "cpc"
    return None

def extract_prefixes(value: Any) -> list[str]:
    """Extract four-character CPC prefixes from a value or iterable of values."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []

    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        values = value
    else:
        values = [value]

    prefixes: list[str] = []
    for code in values:
        s = str(code).strip().upper()
        if not s:
            continue
        prefix = ""
        for ch in s:
            if ch.isalnum():
                prefix += ch
                if len(prefix) >= 4:
                    break
            else:
                break
        if prefix:
            prefixes.append(prefix)
    return prefixes


def filter_by_search(frame: pd.DataFrame, cpc_column: str | None, query: str) -> pd.DataFrame:
    """Return rows where the query matches the title or CPC codes."""
    if not query:
        return frame
    lowered = query.lower()

    def _row_matches(row: pd.Series) -> bool:
        title = str(row.get("title", "")).lower()
        if lowered in title:
            return True
        if not cpc_column:
            return False
        cpc_value = row.get(cpc_column, "")
        if isinstance(cpc_value, Iterable) and not isinstance(cpc_value, (str, bytes)):
            cpc_text = " ".join(map(str, cpc_value))
        else:
            cpc_text = str(cpc_value)
        return lowered in cpc_text.lower()

    return frame[frame.apply(_row_matches, axis=1)]
