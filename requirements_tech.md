## Technical Requirements

1. **Language**
   Use **Python 3.11+** as the primary language.

2. **Data ingestion**

   * Load USPTO bulk XML files from a local path: assume file is in project root
   * Parse using **lxml** or **xmltodict**.
   * Extract and structure data into dictionaries or DataFrames.

3. **Filtering**

   * Apply keyword-based matching (simple regex or substring).
   * Match CPC codes against a small predefined list of synthetic biology codes stored in a JSON file.

4. **Storage**

   * Use an **in-memory SQLite database** (`sqlite3.connect(":memory:")`).
   * Create one main table and an **FTS5** virtual table for text search on title and abstract.

5. **Data output**

   * Export a **weekly JSON file** (e.g. `patents_YYYY-MM-DD.json`).
   * Include metadata fields and filter results for consumption by other engineers.
   * Use a consistent file naming pattern to support weekly data integration.

6. **Search and UI**

   * Build a **Streamlit app** that provides:

     * A text search box for title and abstract.
     * Filters for CPC code and week/date.
     * A paginated results table (`st.dataframe`).
     * Summary metrics or charts (e.g. counts by CPC or assignee).
     * Download buttons for CSV or JSON.

7. **Integration for engineers**

   * Provide a helper function returning a pandas DataFrame of the current week’s data.
   * Ensure JSON output is easy to load by other Python or ETL scripts.

8. **Error handling and logging**

   * Log summary stats (total parsed, in-scope count, errors).
   * Write logs to a local file (`run_YYYY-MM-DD.log`).

9. **Configuration**

   * Use a `.env` file for paths and mode configuration.
   * Provide sensible defaults to allow running without configuration.

10. **Developer experience**

    * Include a `requirements.txt` listing dependencies.
    * Add a `Makefile` or `run.sh` with `install`, `run`, and `clean` commands.
    * Use a simple folder structure:

      ```
      src/
      data/
      output/
      ui/
      ```
    * Provide a concise **README** with setup steps, run instructions, and sample output.

11. **Dependencies**

    * `streamlit`, `pandas`, `lxml` (or `xmltodict`), `sqlite3`, `python-dotenv`, `tqdm`
    * Optional: `altair` for lightweight charts.

12. **Performance**

    * Handle a single week of patent data fully in memory.
    * Complete each run within a few minutes on a standard laptop.

13. **Security**

    * No external APIs or credentials required.
    * Run locally only.

14. **Delivery**

    * Deliver as a **GitHub repository** containing:

      * Source code
      * Example JSON output
      * Screenshot(s) of the Streamlit UI
      * README with assumptions, setup, and usage details

---
