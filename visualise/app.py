import streamlit as st

from visualise.cpc_filters import detect_cpc_column, filter_by_search
from visualise.data_access import PatentService
from visualise.pagination import paginate
from visualise.session_state import SessionManager
from visualise import ui_components as ui


def run_app(
    st_module=st,
    service: PatentService | None = None,
    page_size: int = 10,
) -> None:
    """Run the Streamlit application with injectable dependencies."""
    st_module.title("🧬 Patent Scraper Viewer")

    service = service or PatentService()
    session = SessionManager(st_module.session_state)

    patent_files = service.list_files()
    selected_file = ui.select_dataset(st_module, patent_files)
    session.record_dataset(selected_file.path.as_posix())

    full_df = service.load_dataframe(selected_file)
    cpc_column = detect_cpc_column(full_df)

    search_query = ui.render_filters(st_module, default_query=session.search_query)
    session.update_search_query(search_query)

    filtered_df = filter_by_search(full_df, cpc_column, search_query)

    ui.render_download_button(st_module, filtered_df)
    ui.render_metrics(st_module, len(full_df), len(filtered_df))

    page = paginate(filtered_df, session.page, page_size=page_size)
    session.page = ui.render_paginated_table(st_module, page)


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
