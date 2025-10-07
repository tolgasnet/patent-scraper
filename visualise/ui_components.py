import pandas as pd

from .data_access import PatentFile


def select_dataset(st_module, files: list[PatentFile]) -> PatentFile:
    """Render dataset selector and return the chosen file."""
    st_module.sidebar.header("Data")
    if not files:
        st_module.sidebar.error("No NDJSON files found in data/ (expected pattern: data/patents_*.jsonl)")
        st_module.stop()
    display_names = [f.display_name for f in files]
    selection = st_module.sidebar.selectbox("Choose NDJSON file", display_names, index=0)
    selected = next(file for file in files if file.display_name == selection)
    if not selected.path.exists():
        st_module.error("File not found. Please check the path or generate the output first.")
        st_module.stop()
    return selected


def render_filters(st_module, default_query: str = "") -> str:
    """Render filter controls and return the search query."""
    st_module.sidebar.header("Filters")
    return st_module.sidebar.text_input("🔍 Search titles:", value=default_query)


def render_download_button(st_module, frame: pd.DataFrame) -> None:
    """Render a CSV download button for the filtered data."""
    csv_bytes = frame.to_csv(index=False).encode("utf-8")
    st_module.sidebar.download_button(
        label="💾 Export CSV",
        data=csv_bytes,
        file_name="filtered_patents.csv",
        mime="text/csv",
    )


def render_metrics(st_module, total_all: int, total_filtered: int) -> None:
    """Display overall totals for context."""
    col_total, col_filtered, _ = st_module.columns([1, 1, 4])
    col_total.metric("Total Patents", f"{total_all:,}")
    col_filtered.metric("After Filters", f"{total_filtered:,}")


def render_paginated_table(st_module, page) -> int:
    """Render the paginated dataframe and return the new page number."""
    st_module.dataframe(page.records, use_container_width=True)

    col_prev, col_next = st_module.columns(2)
    new_page = page.current

    with col_prev:
        if st_module.button("⬅️ Prev", use_container_width=True, disabled=page.current <= 1):
            new_page = max(1, page.current - 1)
    with col_next:
        if st_module.button("Next ➡️", use_container_width=True, disabled=page.current >= page.total_pages):
            new_page = min(page.total_pages, page.current + 1)

    st_module.markdown(f"**Page {page.current} / {page.total_pages}**")
    return new_page
