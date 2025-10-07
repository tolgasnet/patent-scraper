from dataclasses import dataclass
import math

import pandas as pd


@dataclass(frozen=True)
class Page:
    """Slice of a dataframe with pagination metadata."""

    records: pd.DataFrame
    current: int
    total_pages: int
    page_size: int
    total_records: int


def paginate(frame: pd.DataFrame, page: int, page_size: int = 10) -> Page:
    """Return the dataframe slice for the requested page."""
    if page_size <= 0:
        raise ValueError("page_size must be positive")

    total_records = len(frame)
    total_pages = max(1, math.ceil(total_records / page_size))
    current = max(1, min(page, total_pages))

    start = (current - 1) * page_size
    end = start + page_size
    records = frame.iloc[start:end]

    return Page(records=records, current=current, total_pages=total_pages, page_size=page_size, total_records=total_records)
