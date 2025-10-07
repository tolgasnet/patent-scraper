import streamlit as st
import pandas as pd
import os
from glob import glob


st.title("🧬 Patent Scraper Viewer")

# Sidebar: pick an NDJSON file starting with 'patents_' from data/
st.sidebar.header("Data")
candidates = sorted(glob("data/patents_*.jsonl"))  # include only NDJSON
if not candidates:
    st.sidebar.error("No NDJSON files found in data/ (expected pattern: data/patents_*.jsonl)")
    st.stop()
display_names = [os.path.basename(f).replace("patents_synbio_", "").replace(".jsonl", "") for f in candidates]
selected_display = st.sidebar.selectbox("Choose NDJSON file", display_names, index=0)
selected_file = candidates[display_names.index(selected_display)]

exists = os.path.exists(selected_file)
if not exists:
    st.error("File not found. Please check the path or generate the output first.")
    st.stop()

@st.cache_data(show_spinner=False)
def load_ndjson(path: str) -> pd.DataFrame:
    return pd.read_json(path, lines=True)

df = load_ndjson(selected_file)

# --- Helpers for CPC handling ---
def _ensure_cpc_column(frame: pd.DataFrame) -> str | None:
    if "CPC" in frame.columns:
        return "CPC"
    if "cpc" in frame.columns:
        return "cpc"
    return None

cpc_col = _ensure_cpc_column(df)

st.sidebar.header("Filters")

# Search box for titles or CPC codes
search_query = st.sidebar.text_input("🔍 Search titles or CPC codes:", "")

# Apply filters
if search_query:
    q = search_query.lower()
    def _row_matches(row) -> bool:
        title = str(row.get("title", "")).lower()
        cpc_val = row.get(cpc_col, "")
        cpc_text = " ".join(map(str, cpc_val)) if isinstance(cpc_val, (list, tuple)) else str(cpc_val)
        return (q in title) or (q in cpc_text.lower())
    df = df[df.apply(_row_matches, axis=1)]

# Insert download button in sidebar after filters
csv = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="💾 Export CSV",
    data=csv,
    file_name="filtered_patents.csv",
    mime="text/csv",
)

# Update total_patents after filtering
total_patents = len(df)

total_all = load_ndjson(selected_file)
total_all_count = len(total_all)

col_total, col_filtered, _ = st.columns([1, 1, 4])
col_total.metric("Total Patents", f"{total_all_count:,}")
col_filtered.metric("After Filters", f"{total_patents:,}")

# Pagination logic
page_size = 10
total_pages = (total_patents - 1) // page_size + 1
if "page" not in st.session_state:
    st.session_state.page = 1

# Compute slice
start = (st.session_state.page - 1) * page_size
end = start + page_size

# Table first
st.dataframe(df.iloc[start:end], use_container_width=True)

# Pager below the table
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("⬅️ Prev", use_container_width=True) and st.session_state.page > 1:
        st.session_state.page -= 1
with col_next:
    if st.button("Next ➡️", use_container_width=True) and st.session_state.page < total_pages:
        st.session_state.page += 1
st.markdown(f"**Page {st.session_state.page} / {total_pages}**")
