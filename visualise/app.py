from typing import Callable, NamedTuple

import pandas as pd
import streamlit as st

from visualise import ui_components as ui
from visualise.cpc_filters import filter_by_title
from visualise.data_access import PatentFile, list_patent_files, load_patent_dataframe

_PAGE_KEY = "page"
_DATASET_KEY = "_selected_dataset"
_SEARCH_KEY = "_search_query"


class Page(NamedTuple):
    records: pd.DataFrame
    current: int
    total_pages: int
    page_size: int
    total_records: int


def _get_page(state) -> int:
    return max(1, int(state.get(_PAGE_KEY, 1) or 1))


def _set_page(state, value: int) -> None:
    state[_PAGE_KEY] = max(1, int(value))


def _get_search(state) -> str:
    return str(state.get(_SEARCH_KEY, ""))


def _update_search(state, query: str) -> None:
    if _get_search(state) != query:
        state[_SEARCH_KEY] = query
        _set_page(state, 1)


def _update_dataset(state, dataset_identifier: str) -> None:
    if state.get(_DATASET_KEY) != dataset_identifier:
        state[_DATASET_KEY] = dataset_identifier
        _set_page(state, 1)


def paginate(frame: pd.DataFrame, page: int, page_size: int = 10) -> Page:
    if page_size <= 0:
        raise ValueError("page_size must be positive")

    total_records = len(frame)
    total_pages = max(1, -(-total_records // page_size))  # ceiling division
    current = max(1, min(page, total_pages))

    start = (current - 1) * page_size
    end = start + page_size
    records = frame.iloc[start:end]

    return Page(
        records=records,
        current=current,
        total_pages=total_pages,
        page_size=page_size,
        total_records=total_records,
    )


def run_app(
    st_module=st,
    list_files: Callable[[], list[PatentFile]] = list_patent_files,
    load_frame: Callable[[PatentFile], pd.DataFrame] = load_patent_dataframe,
    page_size: int = 10,
) -> None:
    """Run the Streamlit application with injectable dependencies."""
    st_module.title("🧬 Patent Scraper Viewer")

    state = st_module.session_state

    patent_files = list_files()
    selected_file = ui.select_dataset(st_module, patent_files)
    dataset_id = selected_file.path.as_posix()
    _update_dataset(state, dataset_id)

    full_df = load_frame(selected_file)

    search_query = ui.render_filters(st_module, default_query=_get_search(state))
    _update_search(state, search_query)

    filtered_df = filter_by_title(full_df, search_query)

    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    ui.render_download_button(st_module, csv_bytes)
    ui.render_metrics(st_module, len(full_df), len(filtered_df))

    page = paginate(filtered_df, _get_page(state), page_size=page_size)
    new_page = ui.render_paginated_table(st_module, page)
    _set_page(state, new_page)


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
