import streamlit as st

from cpc_filters import detect_cpc_column, filter_by_search
from data_access import list_patent_files, load_patent_dataframe
import ui_components as ui

st.title("🧬 Patent Scraper Viewer")

patent_files = list_patent_files()
selected_file = ui.select_dataset(patent_files)

full_df = load_patent_dataframe(selected_file)
cpc_column = detect_cpc_column(full_df)

search_query = ui.render_filters()

previous_dataset = st.session_state.get("_selected_dataset")
previous_query = st.session_state.get("_search_query")
current_dataset = selected_file.path.as_posix()
if previous_dataset != current_dataset:
    st.session_state[ui.PAGE_STATE_KEY] = 1
    st.session_state["_selected_dataset"] = current_dataset
if previous_query != search_query:
    st.session_state[ui.PAGE_STATE_KEY] = 1
    st.session_state["_search_query"] = search_query

filtered_df = filter_by_search(full_df, cpc_column, search_query)

ui.render_download_button(filtered_df)
ui.render_metrics(len(full_df), len(filtered_df))
ui.render_paginated_table(filtered_df)
