import pandas as pd


def filter_by_title(frame: pd.DataFrame, query: str, title_column: str = "title") -> pd.DataFrame:
    """Return rows whose title contains the case-insensitive query."""
    if not query or title_column not in frame.columns:
        return frame

    lowered = query.lower()
    titles = frame[title_column].astype(str).str.lower()
    mask = titles.str.contains(lowered, na=False)
    return frame[mask]
