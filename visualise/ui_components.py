import pandas as pd
import streamlit as st

from data_access import PatentFile

PAGE_STATE_KEY = "page"
PAGE_SIZE = 10


def select_dataset(files: list[PatentFile]) -> PatentFile:
    """Render dataset selector and return the chosen file."""
    st.sidebar.header("Data")
    if not files:
        st.sidebar.error("No NDJSON files found in data/ (expected pattern: data/patents_*.jsonl)")
        st.stop()
    display_names = [f.display_name for f in files]
    default_index = 0 if files else None
    selection = st.sidebar.selectbox("Choose NDJSON file", display_names, index=default_index)
    selected = next(file for file in files if file.display_name == selection)
    if not selected.path.exists():
        st.error("File not found. Please check the path or generate the output first.")
        st.stop()
    return selected


def render_filters() -> str:
    """Render filter controls and return the free-text search query."""
    st.sidebar.header("Filters")
    return st.sidebar.text_input("🔍 Search titles or CPC codes:", "")


def render_download_button(frame: pd.DataFrame) -> None:
    """Render a CSV download button for the filtered data."""
    csv_bytes = frame.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label="💾 Export CSV",
        data=csv_bytes,
        file_name="filtered_patents.csv",
        mime="text/csv",
    )


def render_metrics(total_all: int, total_filtered: int) -> None:
    """Display overall totals for context."""
    col_total, col_filtered, _ = st.columns([1, 1, 4])
    col_total.metric("Total Patents", f"{total_all:,}")
    col_filtered.metric("After Filters", f"{total_filtered:,}")


def render_paginated_table(frame: pd.DataFrame, page_size: int = PAGE_SIZE) -> tuple[int, int]:
    """Render the paginated dataframe and return (current_page, total_pages)."""
    total_records = len(frame)
    total_pages = (total_records - 1) // page_size + 1 if total_records else 1

    page = st.session_state.get(PAGE_STATE_KEY, 1)
    page = max(1, min(page, total_pages))
    st.session_state[PAGE_STATE_KEY] = page

    start = (page - 1) * page_size
    end = start + page_size
    st.dataframe(frame.iloc[start:end], use_container_width=True)

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⬅️ Prev", use_container_width=True) and st.session_state[PAGE_STATE_KEY] > 1:
            st.session_state[PAGE_STATE_KEY] -= 1
    with col_next:
        if st.button("Next ➡️", use_container_width=True) and st.session_state[PAGE_STATE_KEY] < total_pages:
            st.session_state[PAGE_STATE_KEY] += 1

    st.markdown(f"**Page {st.session_state[PAGE_STATE_KEY]} / {total_pages}**")
    return st.session_state[PAGE_STATE_KEY], total_pages
